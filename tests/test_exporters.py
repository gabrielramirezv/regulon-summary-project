from src.exporters import write_summary, write_sif

def test_write_summary(tmp_path):
    # Esta prueba verifica que la función write_summary genere un archivo TSV con el formato correcto
    # y que contenga los datos esperados.
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
    }
    output_file = tmp_path / "summary.tsv"
    write_summary(regulon, output_file)

    with open(output_file) as f:
        lines = f.read().strip().split("\n")
        assert lines[0] == "TF\tTotal genes\tActivados\tReprimidos\tTipo\tLista de genes"
        assert lines[1] == "CRP\t2\t1\t1\tdual\tcyaA, lacZ"
        assert lines[2] == "FNR\t1\t0\t1\trepresor\tnarG"

def test_write_sif(tmp_path):
    # Esta prueba verifica que la función write_sif genere un archivo SIF con el formato correcto
    # y que contenga las interacciones esperadas.
    regulon = [
        ("CRP", "lacZ", "+"),
        ("CRP", "cyaA", "-"),
        ("FNR", "narG", "-"),
    ]
    output_file = tmp_path / "network.sif"
    write_sif(regulon, output_file)

    with open(output_file) as f:
        lines = f.read().strip().split("\n")
        assert lines[0] == "CRP\tactivates\tlacZ"
        assert lines[1] == "CRP\trepresses\tcyaA"
        assert lines[2] == "FNR\trepresses\tnarG"

def test_write_summary_empty_regulon(tmp_path):
    # Esta prueba verifica que la función write_summary maneje correctamente un regulon vacío
    # y genere un archivo con solo el encabezado.
    regulon = {}
    output_file = tmp_path / "empty_summary.tsv"
    write_summary(regulon, output_file)

    with open(output_file) as f:
        lines = f.read().strip().split("\n")
        assert len(lines) == 1
        assert lines[0] == "TF\tTotal genes\tActivados\tReprimidos\tTipo\tLista de genes"

def test_write_sif_empty_regulon(tmp_path):
    # Esta prueba verifica que la función write_sif maneje correctamente un regulon vacío
    # y genere un archivo vacío.
    regulon = []
    output_file = tmp_path / "empty_network.sif"
    write_sif(regulon, output_file)

    with open(output_file) as f:
        content = f.read().strip()
        assert content == ""

def test_write_summary_single_interaction(tmp_path):
    # Esta prueba verifica que la función write_summary maneje correctamente un regulon con una sola interacción
    # y genere un archivo con la información correcta.
    regulon = {
        "CRP": {"genes": ["lacZ"], "activados": 1, "reprimidos": 0},
    }
    output_file = tmp_path / "single_summary.tsv"
    write_summary(regulon, output_file)

    with open(output_file) as f:
        lines = f.read().strip().split("\n")
        assert len(lines) == 2
        assert lines[0] == "TF\tTotal genes\tActivados\tReprimidos\tTipo\tLista de genes"
        assert lines[1] == "CRP\t1\t1\t0\tactivador\tlacZ"

def test_write_sif_single_interaction(tmp_path):
    # Esta prueba verifica que la función write_sif maneje correctamente un regulon con una sola interacción
    # y genere un archivo con la información correcta.
    regulon = [
        ("CRP", "lacZ", "+"),
    ]
    output_file = tmp_path / "single_network.sif"
    write_sif(regulon, output_file)

    with open(output_file) as f:
        lines = f.read().strip().split("\n")
        assert len(lines) == 1
        assert lines[0] == "CRP\tactivates\tlacZ"

def test_write_sif_writes_expected_interactions(tmp_path):
    # Esta prueba verifica que la función write_sif escriba las interacciones esperadas en el archivo SIF.
    regulon = [
        ("CRP", "lacZ", "+"),
        ("CRP", "cyaA", "-"),
        ("FNR", "narG", "-"),
    ]
    output_file = tmp_path / "expected_network.sif"
    write_sif(regulon, output_file)

    with open(output_file) as f:
        lines = f.read().strip().split("\n")
        assert len(lines) == 3
        assert lines[0] == "CRP\tactivates\tlacZ"
        assert lines[1] == "CRP\trepresses\tcyaA"
        assert lines[2] == "FNR\trepresses\tnarG"