from pathlib import Path
import pandas as pd


def ensure_output_dir(output_file: str) -> None:
    output_path = Path(output_file)

    if output_path.parent != Path("."):
        output_path.parent.mkdir(parents=True, exist_ok=True)


def write_summary(
    regulon: pd.DataFrame,
    output_file: str,
    top_n: int | None = None,
) -> None:
    ensure_output_dir(output_file)

    summary = regulon.sort_values("total_genes", ascending=False)

    if top_n is not None:
        summary = summary.head(top_n)

    summary.to_csv(output_file, sep="\t", index=False)


def write_sif(interactions: pd.DataFrame, output_file: str) -> None:
    ensure_output_dir(output_file)

    # Crear un DataFrame con TF, effect y gene
    sif = interactions[["TF", "effect", "gene"]]

    # Guardar el DataFrame en formato SIF (tab-separado, sin encabezado)
    sif.to_csv(output_file, sep="\t", index=False, header=False)
