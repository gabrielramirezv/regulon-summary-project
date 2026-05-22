from src.filters import filter_by_min_genes, filter_by_type


def test_filter_by_min_genes():
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
    }

    result = filter_by_min_genes(regulon, 2)

    assert "CRP" in result
    assert "FNR" not in result


def test_filter_by_type_dual():
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
    }

    result = filter_by_type(regulon, "dual")

    assert "CRP" in result
    assert "FNR" not in result

def test_filter_by_min_genes_and_type():
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
        "ArcA": {"genes": ["someGene"], "activados": 0, "reprimidos": 1},
    }

    result = filter_by_min_genes(regulon, 2)
    result = filter_by_type(result, "dual")

    assert "CRP" in result
    assert "FNR" not in result
    assert "ArcA" not in result

def test_filter_by_min_genes_zero():
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
    }

    result = filter_by_min_genes(regulon, 0)

    assert "CRP" in result
    assert "FNR" in result

def test_filter_by_min_genes_negative():
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
    }

    result = filter_by_min_genes(regulon, -1)

    assert "CRP" in result
    assert "FNR" in result

def test_filter_by_min_genes_no_regulons():
    regulon = {}

    result = filter_by_min_genes(regulon, 2)

    assert result == {}

def test_filter_by_type_no_regulons():
    regulon = {}

    result = filter_by_type(regulon, "dual")

    assert result == {}

def test_filter_by_type_no_matches():
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
    }

    result = filter_by_type(regulon, "activator")

    assert result == {}

def test_filter_by_type_invalid_type():
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
    }

    result = filter_by_type(regulon, "invalid_type")

    assert result == {}

def test_filter_by_min_genes_and_type_no_matches():
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
    }

    result = filter_by_min_genes(regulon, 3)
    result = filter_by_type(result, "dual")

    assert result == {}

def test_filter_by_min_genes_and_type_all_matches():
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
    }

    result = filter_by_min_genes(regulon, 1)
    result = filter_by_type(result, "dual")

    assert "CRP" in result
    assert "FNR" not in result

def test_filter_by_min_genes_keeps_only_regulators_with_enough_genes():
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
        "ArcA": {"genes": ["someGene"], "activados": 0, "reprimidos": 1},
    }

    result = filter_by_min_genes(regulon, 2)

    assert "CRP" in result
    assert "FNR" not in result
    assert "ArcA" not in result

def test_filter_by_type_keeps_only_regulators_of_specified_type():
    regulon = {
        "CRP": {"genes": ["lacZ", "cyaA"], "activados": 1, "reprimidos": 1},
        "FNR": {"genes": ["narG"], "activados": 0, "reprimidos": 1},
        "ArcA": {"genes": ["someGene"], "activados": 0, "reprimidos": 1},
    }

    result = filter_by_type(regulon, "dual")

    assert "CRP" in result
    assert "FNR" not in result
    assert "ArcA" not in result