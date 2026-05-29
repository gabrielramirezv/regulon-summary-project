import pandas as pd

VALID_EFFECTS = {"+", "-", "-+"}


def load_interactions(filename: str) -> pd.DataFrame:

    # Leer el archivo, ignorando las líneas que comienzan con '#'
    df = pd.read_csv(filename, sep = "\t", comment="#")

    # Usar nombres TF, gene y effect para las columnas relevantes
    # 2)regulatorName, 5)geneName, 6)function
    df = df.rename(columns={"2)regulatorName": "TF",
                            "5)geneName": "gene",
                            "6)function": "effect"})

    # Conservar solo las columnas relevantes
    required_columns = ["TF", "gene", "effect"]
    df = df[required_columns]

    # Eliminar filas con valores faltantes en las columnas requeridas
    df = df.dropna(subset=required_columns)

    # Filtrar filas donde el valor de "effect" no es válido
    df = df[df["effect"].isin(VALID_EFFECTS)]

    return df
