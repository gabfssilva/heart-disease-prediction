
import numpy as np
import pandas as pd


def set_types(context: dict) -> bool:
    df = context['raw_dataset']

    for col in numerical_keys:
        if col in df:
            df[col] = df[col].astype(float)

    for col in categorical_keys:
        if col in df:
            df[col] = np.floor(pd.to_numeric(df[col], errors='coerce')).astype('Int64').astype(str)

    context['raw_dataset'] = df

    return True

numerical_keys = [
    "NUMADULT",
    "NUMMEN",
    "NUMWOMEN",
    "HHADULT",
    "PHYSHLTH",
    "MENTHLTH",
    "POORHLTH",
    "SLEPTIM1",
    "CHILDREN",
    "WEIGHT2",
    "HEIGHT3",
    "LCSFIRST",
    "LCSLAST",
    "LCSNUMCG",
    "AVEDRNK3",
    "DRNK3GE5",
    "MAXDRNKS",
    "FLSHTMY3",
    "HIVTSTD3",
    "CHKHEMO3",
    "HPVADSHT",
    "COVIDFS1",
    "COVIDSE1",
    "COPDSMOK",
    "CNCRAGE",
    "MARIJAN1",
    "_AGE80",
    "HTIN4",
    "HTM4",
    "WTKG3",
    "_BMI5",
    "_YRSSMOK",
    "_PACKYRS",
    "_YRSQUIT",
    "DROCDY4_",
    "_DRNKWK2"
]

temporal_keys = [
    "FMONTH",
    "IDATE",
    "IMONTH",
    "IDAY",
    "IYEAR",
    "SMOKDAY2",
    "ALCDAY4",
    "_PACKDAY"
]

categorical_keys = [
    "_STATE",
    "DISPCODE",
    "SEQNO",
    "_PSU",
    "CTELENM1",
    "PVTRESD1",
    "COLGHOUS",
    "STATERE1",
    "CELPHON1",
    "LADULT1",
    "COLGSEX1",
    "LANDSEX1",
    "RESPSLCT",
    "SAFETIME",
    "CTELNUM1",
    "CELLFON5",
    "CADULT1",
    "CELLSEX1",
    "PVTRESD3",
    "CCLGHOUS",
    "CSTATE1",
    "LANDLINE",
    "SEXVAR",
    "GENHLTH",
    "PRIMINSR",
    "PERSDOC3",
    "MEDCOST1",
    "CHECKUP1",
    "EXERANY2",
    "LASTDEN4",
    "RMVTETH4",
    "CVDINFR4",
    "CVDCRHD4",
    "CVDSTRK3",
    "ASTHMA3",
    "ASTHNOW",
    "CHCSCNC1",
    "CHCOCNC1",
    "CHCCOPD3",
    "ADDEPEV3",
    "CHCKDNY2",
    "HAVARTH4",
    "DIABETE4",
    "MARITAL",
    "EDUCA",
    "RENTHOM1",
    "NUMHHOL4",
    "VETERAN3",
    "EMPLOY1",
    "INCOME3",
    "PREGNANT",
    "DEAF",
    "BLIND",
    "DECIDE",
    "DIFFWALK",
    "DIFFDRES",
    "DIFFALON",
    "HADMAM",
    "HOWLONG",
    "CERVSCRN",
    "CRVCLCNC",
    "CRVCLPAP",
    "CRVCLHPV",
    "HADHYST2",
    "HADSIGM4",
    "COLNSIGM",
    "COLNTES1",
    "SIGMTES1",
    "LASTSIG4",
    "COLNCNCR",
    "VIRCOLO1",
    "VCLNTES2",
    "SMALSTOL",
    "STOLTEST",
    "STOOLDN2",
    "BLDSTFIT",
    "SDNATES1",
    "SMOKE100",
    "USENOW3",
    "ECIGNOW2",
    "LCSCTSC1",
    "LCSSCNCR",
    "LCSCTWHN",
    "FLUSHOT7",
    "PNEUVAC4",
    "TETANUS1",
    "HIVTST7",
    "HIVRISK5",
    "COVIDPOS",
    "COVIDSMP",
    "COVIDPRM",
    "PDIABTS1",
    "PREDIAB2",
    "DIABTYPE",
    "INSULIN1",
    "EYEEXAM1",
    "DIABEYE1",
    "DIABEDU1",
    "FEETSORE",
    "TOLDCFS",
    "HAVECFS",
    "WORKCFS",
    "IMFVPLA3",
    "HPVADVC4",
    "SHINGLE2",
    "COVIDVA1",
    "COVIDNU1",
    "CDASSIST",
    "CDHELP",
    "CDSOCIAL",
    "CDDISCUS",
    "CAREGIV1",
    "CRGVREL4",
    "CRGVLNG1",
    "CRGVHRS1",
    "CRGVPRB3",
    "CRGVALZD",
    "CRGVPER1",
    "CRGVHOU1",
    "CRGVEXPT",
    "ACEDEPRS",
    "ACEDRINK",
    "ACEDRUGS",
    "ACEPRISN",
    "ACEDIVRC",
    "ACEPUNCH",
    "ACEHURT1",
    "ACESWEAR",
    "ACETOUCH",
    "ACETTHEM",
    "ACEHVSEX",
    "ACEADSAF",
    "ACEADNED",
    "LSATISFY",
    "EMTSUPRT",
    "SDHISOLT",
    "SDHEMPLY",
    "FOODSTMP",
    "SDHFOOD1",
    "SDHBILLS",
    "SDHUTILS",
    "SDHTRNSP",
    "SDHSTRE1",
    "MARJSMOK",
    "MARJEAT",
    "MARJVAPE",
    "MARJDAB",
    "MARJOTHR",
    "LASTSMK2",
    "STOPSMK2",
    "MENTCIGS",
    "MENTECIG",
    "HEATTBCO",
    "ASBIALCH",
    "ASBIDRNK",
    "ASBIBING",
    "ASBIADVC",
    "ASBIRDUC",
    "FIREARM5",
    "GUNLOAD",
    "LOADULK2",
    "RCSGEND1",
    "RCSXBRTH",
    "RCSRLTN2",
    "CASTHDX2",
    "CASTHNO2",
    "BIRTHSEX",
    "SOMALE",
    "SOFEMALE",
    "TRNSGNDR",
    "HADSEX",
    "PFPPRVN4",
    "TYPCNTR9",
    "BRTHCNT4",
    "WHEREGET",
    "NOBCUSE8",
    "BCPREFER",
    "RRCLASS3",
    "RRCOGNT2",
    "RRTREAT",
    "RRATWRK2",
    "RRHCARE4",
    "RRPHYSM2",
    "QSTVER",
    "QSTLANG",
    "_METSTAT",
    "_URBSTAT",
    "MSCODE",
    "_STSTR",
    "_STRWT",
    "_RAWRAKE",
    "_WT2RAKE",
    "_IMPRACE",
    "_CHISPNC",
    "_CRACE2",
    "_CPRACE2",
    "CAGEG",
    "_CLLCPWT",
    "_DUALUSE",
    "_DUALCOR",
    "_LLCPWT2",
    "_LLCPWT",
    "_RFHLTH",
    "_PHYS14D",
    "_MENT14D",
    "_HLTHPLN",
    "_HCVU652",
    "_TOTINDA",
    "_EXTETH3",
    "_ALTETH3",
    "_DENVST3",
    "_MICHD",
    "_LTASTH1",
    "_CASTHM1",
    "_ASTHMS1",
    "_DRDXAR2",
    "_PRACE2",
    "_MRACE2",
    "_HISPANC",
    "_RACE1",
    "_RACEG22",
    "_RACEGR4",
    "_RACEPR1",
    "_SEX",
    "_AGEG5YR",
    "_AGE65YR",
    "_AGE_G",
    "_BMI5CAT",
    "_RFBMI5",
    "_CHLDCNT",
    "_EDUCAG",
    "_INCOMG1",
    "_RFMAM22",
    "_MAM5023",
    "_HADCOLN",
    "_CLNSCP1",
    "_HADSIGM",
    "_SGMSCP1",
    "_SGMS101",
    "_RFBLDS5",
    "_STOLDN1",
    "_VIRCOL1",
    "_SBONTI1",
    "_CRCREC2",
    "_SMOKER3",
    "_RFSMOK3",
    "_CURECI2",
    "_SMOKGRP",
    "_LCSREC",
    "DRNKANY6",
    "_RFBING6",
    "_RFDRHV8",
    "_FLSHOT7",
    "_PNEUMO3",
    "_AIDTST4"
]