import pytest

from src.io_utils import load_interactions


def test_load_interactions_happy_path(tmp_path):
    # Verifica que dos lineas validas se carguen como tuplas (TF, gen, efecto).
    # Formato esperado del TSV: id, TF, x, x, gene, effect, x
    test_file = tmp_path / "interactions.tsv"
    test_file.write_text(
        "id1\tCRP\tx\tx\tlacZ\t+\tx\n"
        "id2\tFNR\tx\tx\tnarG\t-\tx\n"
    )

    interactions = load_interactions(test_file)

    assert interactions == [("CRP", "lacZ", "+"), ("FNR", "narG", "-")]


def test_load_interactions_keeps_dual_effect(tmp_path):
    # Verifica que el efecto "+-" (regulacion dual) se conserve.
    test_file = tmp_path / "interactions.tsv"
    test_file.write_text("id1\tAraC\tx\tx\taraB\t+-\tx\n")

    interactions = load_interactions(test_file)

    assert ("AraC", "araB", "+-") in interactions


def test_load_interactions_ignores_invalid_effect(tmp_path):
    # Verifica que las lineas con efecto fuera de {+, -, +-} se descarten.
    test_file = tmp_path / "interactions.tsv"
    test_file.write_text(
        "id1\tCRP\tx\tx\tlacZ\t+\tx\n"
        "id2\tBAD\tx\tx\tgeneX\t?\tx\n"
    )

    interactions = load_interactions(test_file)

    assert interactions == [("CRP", "lacZ", "+")]


def test_load_interactions_ignores_empty_lines(tmp_path):
    # Verifica que las lineas vacias no produzcan interacciones.
    test_file = tmp_path / "interactions.tsv"
    test_file.write_text(
        "\n"
        "id1\tCRP\tx\tx\tlacZ\t+\tx\n"
        "\n"
    )

    interactions = load_interactions(test_file)

    assert interactions == [("CRP", "lacZ", "+")]


def test_load_interactions_ignores_comments(tmp_path):
    # Verifica que las lineas que empiezan con "#" se ignoren.
    test_file = tmp_path / "interactions.tsv"
    test_file.write_text(
        "# este es un comentario\n"
        "id1\tCRP\tx\tx\tlacZ\t+\tx\n"
    )

    interactions = load_interactions(test_file)

    assert interactions == [("CRP", "lacZ", "+")]


def test_load_interactions_ignores_header(tmp_path):
    # Verifica que la linea de encabezado de RegulonDB se descarte.
    test_file = tmp_path / "interactions.tsv"
    test_file.write_text(
        "1)regulatorId\tregulatorName\tX\tX\tgeneName\teffect\tX\n"
        "id1\tCRP\tx\tx\tlacZ\t+\tx\n"
    )

    interactions = load_interactions(test_file)

    assert interactions == [("CRP", "lacZ", "+")]


def test_load_interactions_ignores_short_lines(tmp_path):
    # Verifica que las lineas con menos de 7 columnas se descarten.
    test_file = tmp_path / "interactions.tsv"
    test_file.write_text(
        "id1\tCRP\tx\tlacZ\t+\n"        # solo 5 columnas: se descarta
        "id2\tFNR\tx\tx\tnarG\t-\tx\n"  # 7 columnas: valida
    )

    interactions = load_interactions(test_file)

    assert interactions == [("FNR", "narG", "-")]


def test_load_interactions_empty_filename_raises_value_error():
    # Verifica que pasar "" como filename produzca ValueError.
    with pytest.raises(ValueError):
        load_interactions("")


def test_load_interactions_does_not_validate_empty_tf_or_gene(tmp_path):
    # HALLAZGO: la funcion actual NO descarta lineas con TF o gene vacios;
    # solo valida la columna effect. Este test documenta ese comportamiento.
    # Si se considera un bug, habria que agregar validacion en io_utils.load_interactions.
    test_file = tmp_path / "interactions.tsv"
    test_file.write_text(
        "id1\t\tx\tx\tsomeGene\t+\tx\n"   # TF vacio
        "id2\tCRP\tx\tx\t\t+\tx\n"        # gene vacio
    )

    interactions = load_interactions(test_file)

    assert ("", "someGene", "+") in interactions
    assert ("CRP", "", "+") in interactions
