from src.core import get_regulator_type, build_regulon


def test_get_regulator_type_returns_activador():
    # Esta prueba verifica que un regulador con genes activados
    # y sin genes reprimidos sea clasificado como "activador".

    data = {
        "genes": ["lacZ", "araB"],
        "activados": 2,
        "reprimidos": 0,
    }

    result = get_regulator_type(data)

    assert result == "activador"

def test_get_regulator_type_returns_represor():
    # Esta prueba verifica que un regulador con genes reprimidos
    # y sin genes activados sea clasificado como "represor".

    data = {
        "genes": ["lacZ", "araB"],
        "activados": 0,
        "reprimidos": 2,
    }

    result = get_regulator_type(data)

    assert result == "represor"

def test_get_regulator_type_returns_dual():
    # Esta prueba verifica que un regulador con genes activados
    # y reprimidos sea clasificado como "dual".

    data = {
        "genes": ["lacZ", "araB"],
        "activados": 1,
        "reprimidos": 1,
    }

    result = get_regulator_type(data)

    assert result == "dual"

def test_build_regulon():
    # Esta prueba verifica que la función build_regulon construya correctamente el regulon
    # a partir de una lista de interacciones.

    interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "cyaA", "-"),
        ("FNR", "narG", "-"),
    ]

    regulon = build_regulon(interactions)

    assert "CRP" in regulon
    assert "FNR" in regulon
    assert regulon["CRP"]["genes"] == ["lacZ", "cyaA"]
    assert regulon["CRP"]["activados"] == 1
    assert regulon["CRP"]["reprimidos"] == 1
    assert regulon["FNR"]["genes"] == ["narG"]
    assert regulon["FNR"]["activados"] == 0
    assert regulon["FNR"]["reprimidos"] == 1

def test_build_regulon_with_duplicates():
    # Esta prueba verifica que la función build_regulon maneje correctamente las interacciones duplicadas
    # y no cuente genes repetidos.

    interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "cyaA", "-"),
    ]

    regulon = build_regulon(interactions)

    assert "CRP" in regulon
    assert regulon["CRP"]["genes"] == ["lacZ", "cyaA"]
    assert regulon["CRP"]["activados"] == 1
    assert regulon["CRP"]["reprimidos"] == 1

def test_build_regulon_with_dual_effect():
    # Esta prueba verifica que la función build_regulon maneje correctamente las interacciones con efecto dual "+-"
    # y cuente tanto activaciones como represiones.

    interactions = [
        ("AraC", "araB", "+-"),
    ]

    regulon = build_regulon(interactions)

    assert "AraC" in regulon
    assert regulon["AraC"]["genes"] == ["araB"]
    assert regulon["AraC"]["activados"] == 1
    assert regulon["AraC"]["reprimidos"] == 1