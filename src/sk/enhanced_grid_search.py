from dataclasses import dataclass, field
from functools import reduce
import itertools
import pprint
from typing import Any, Callable, Dict, List
from joblib import Parallel, delayed
import numpy as np
from itertools import product
from sklearn import clone
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold, StratifiedKFold
from tqdm import tqdm
from sklearn.base import BaseEstimator
import pandas as pd

@dataclass
class ExecutionInfo:
    scoring: str  # main score or refit
    current_best_score: float  # best global based on refit
    current_execution: int  # the current execution of the total (splits * total combinations)

@dataclass
class BestResult:
    metric: str
    scores: list
    recalculated_scores: dict
    avg_score: float
    params: dict
    estimator: BaseEstimator
    confusion_matrix: np.ndarray
    predicted_probabilities: list[dict] = field(default=None, repr=False)

@dataclass
class TrainingData:
    X: pd.DataFrame = field(default=None, repr=False)
    y: pd.Series = field(default=None, repr=False)

@dataclass
class Result:
    fitted_with: TrainingData
    best: BestResult
    scores: list[dict]

class EnhancedGridSearchCV:
    def __init__(
        self, 
        estimator: BaseEstimator, 
        param_grid: Dict[str, List[Any]], 
        cross_validation=StratifiedKFold(n_splits=10), 
        positive_class=None,
        scoring:list=[], 
        n_jobs: int = 7,
        tqdm = tqdm
    ):
        self.estimator = estimator
        self.param_grid = param_grid
        self.cross_validation = cross_validation if type(cross_validation) != int else KFold(cross_validation)
        self.scoring = scoring
        self.n_jobs = n_jobs
        self.result_ = None
        self.classes_ = []
        self._tqdm = tqdm
        self.positive_class = positive_class
        keys, values = zip(*self.param_grid.items())
        self.param_combinations_ = [dict(zip(keys, v)) for v in product(*values)]

    def total_executions(self):
        return self.cross_validation.n_splits * len(self.param_combinations_)

    def fit(self, X: pd.DataFrame, y: pd.Series) -> Result:
        self.classes_ = y.unique()

        pb = self._tqdm(
            total=self.total_executions(), 
            colour='green',
            desc='Initializing...',
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]"
        )

        def update_progress(info: ExecutionInfo):
            pb.set_description(f"Current best {info.scoring}: {"{:.3f}".format(info.current_best_score)}")
            pb.update(1)

        try:
            result = self._eval_pipeline(X, y, callback=update_progress)
            self.result_ = result
        finally:
            pb.close()

        return result

    def predict(self, X: pd.DataFrame) -> np.array:
        if self.result_ is None:
            raise ValueError("The model has not been fitted yet. Please call 'fit' with appropriate arguments before using 'predict'.")
        
        return self.result_.best.estimator.predict(X)

    def predict_proba(self, X: pd.DataFrame):
        if self.result_ is None:
            raise ValueError("The model has not been fitted yet. Please call 'fit' with appropriate arguments before using 'predict_proba'.")
        
        return self.result_.best.estimator.predict_proba(X)

    def _eval_pipeline(
        self,
        X,
        y,
        callback: Callable[[int, int], None] = None
    ) -> Result:
        X = X.reset_index(drop=True)
        y = y.reset_index(drop=True)

        scoring_keys = list(self.scoring.keys())
        refit_score = scoring_keys[0]

        best_score = -np.inf
        best_fold_score = None
        best_params = None
        results = []

        execution = 0

        parallel = Parallel(n_jobs=self.n_jobs, return_as='generator', verbose=0)

        def process_fold(params, train_index, test_index):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]

            e = clone(self.estimator)
            e.set_params(**params)
            e.fit(X_train, y_train)

            validation_scores = {
                score_name: scorer(e, X_test, y_test) for score_name, scorer in self.scoring.items()
            }

            # train_scores = {
            #     score_name: scorer(e, X_train, y_train) for score_name, scorer in scoring.items()
            # }

            return {
                'validation': validation_scores,
                'train': validation_scores
            }
        
        def parse_scores(score_values):
            scores = {
                key: {
                    'validation': [],
                    'train': []
                } for key in scoring_keys
            }

            for score in score_values:
                for key in scoring_keys:
                   scores[key]['validation'].append(score['validation'][key])
                   scores[key]['train'].append(score['train'][key])

            return scores

        task_list = []

        for params in self.param_combinations_:
            for train_index, test_index in self.cross_validation.split(X, y):
                task_list.append((params, train_index, test_index))

        task_results = parallel(
            delayed(process_fold)(params, train_index, test_index)
            for params, train_index, test_index in task_list
        )

        params_result_dict = {str(params): [] for params in self.param_combinations_}

        for (params, _, _), scores in zip(task_list, task_results):
            combination_results = params_result_dict[str(params)]
            combination_results.append(scores)

            if len(combination_results) == self.cross_validation.n_splits:
                current_fold_scores = [score['validation'][refit_score] for score in combination_results]
                current_score = np.mean(current_fold_scores)

                if current_score > best_score:
                    best_fold_score = combination_results
                    best_score = current_score
                    best_params = params

            execution += 1

            if callback:
                info = ExecutionInfo(
                    scoring=refit_score,
                    current_best_score=best_score,
                    current_execution=execution
                )

                callback(info)

        for params, score_values in params_result_dict.items():
            scores = parse_scores(score_values)

            results.append({
                "params": eval(params),
                'scores': scores
            })

        best_estimator: BaseEstimator = clone(self.estimator)
        best_estimator.set_params(**best_params)
        best_estimator.fit(X, y)
        y_pred = best_estimator.predict(X)
        predicted_probabilities = best_estimator.predict_proba(X)

        return Result(
            best=BestResult(
                metric=refit_score,
                scores=parse_scores(best_fold_score),
                recalculated_scores={
                    score_name: scorer(best_estimator, X, y) for score_name, scorer in self.scoring.items()
                },
                avg_score=best_score,
                params=best_params,
                estimator=best_estimator,
                confusion_matrix=confusion_matrix(y, y_pred),
                predicted_probabilities=[
                    dict(zip(self.classes_, probs)) for probs in predicted_probabilities
                ]
            ),
            scores=results,
            fitted_with=TrainingData(X, y)
        )
