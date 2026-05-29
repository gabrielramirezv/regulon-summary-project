import pandas as pd


def filter_by_min_genes(regulon: pd.DataFrame, min_genes: int) -> pd.DataFrame:
    return regulon[regulon["total_genes"] >= min_genes]


def filter_by_type(regulon: pd.DataFrame, regulator_type: str) -> pd.DataFrame:
    if regulator_type == "all":
        return regulon

    return regulon[regulon["type"] == regulator_type]


def filter_interactions_by_regulon(
    interactions: pd.DataFrame,
    regulon: pd.DataFrame,
) -> pd.DataFrame:
    valid_tfs = set(regulon["TF"])

    return interactions[interactions["TF"].isin(valid_tfs)]
