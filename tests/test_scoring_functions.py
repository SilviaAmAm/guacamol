import pytest

from guacamol.common_scoring_functions import IsomerScoringFunction
from guacamol.score_modifier import GaussianModifier


def test_isomer_scoring_function_returns_one_for_correct_molecule():
    c11h24 = IsomerScoringFunction({'C': 11, 'H': 24})

    # all those smiles fit the formula C11H24
    smiles1 = 'CCCCCCCCCCC'
    smiles2 = 'CC(CCC)CCCCCC'
    smiles3 = 'CCCCC(CC(C)CC)C'

    assert c11h24.score(smiles1) == 1.0
    assert c11h24.score(smiles2) == 1.0
    assert c11h24.score(smiles3) == 1.0


def test_isomer_scoring_function_penalizes_additional_atoms():
    c11h24 = IsomerScoringFunction({'C': 11, 'H': 24})

    # all those smiles are C11H24O
    smiles1 = 'CCCCCCCCCCCO'
    smiles2 = 'CC(CCC)COCCCCC'
    smiles3 = 'CCCCOC(CC(C)CC)C'

    # the penalty corresponds to a deviation of 1.0 from the gaussian modifier in the total number of atoms
    penalty_tot_num_atoms = 1.0 - GaussianModifier(mu=0, sigma=2)(1.0)
    expected_score = 1.0 - penalty_tot_num_atoms / 3.0

    assert c11h24.score(smiles1) == pytest.approx(expected_score)
    assert c11h24.score(smiles2) == pytest.approx(expected_score)
    assert c11h24.score(smiles3) == pytest.approx(expected_score)


def test_isomer_scoring_function_penalizes_incorrect_number_atoms():
    c11h24 = IsomerScoringFunction({'C': 12, 'H': 24})

    # all those smiles fit the formula C11H24O
    smiles1 = 'CCCCCCCCOCCC'
    smiles2 = 'CC(CCOC)CCCCCC'
    smiles3 = 'COCCCC(CC(C)CC)C'

    # the penalty corresponds to a deviation of 1.0 from the gaussian modifier in the number of C atoms
    penalty_tot_num_atoms = 1.0 - GaussianModifier(mu=0, sigma=1)(1.0)
    expected_score = 1.0 - penalty_tot_num_atoms / 3.0

    assert c11h24.score(smiles1) == pytest.approx(expected_score)
    assert c11h24.score(smiles2) == pytest.approx(expected_score)
    assert c11h24.score(smiles3) == pytest.approx(expected_score)
