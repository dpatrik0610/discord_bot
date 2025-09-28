import pytest
from domain.dice_roller import DiceRoller
from domain.die import Die

roller = DiceRoller()


def test_invalid_notation():
    with pytest.raises(ValueError):
        roller.roll("invalid")

def test_single_die():
    result = roller.roll("1d6", debug=True)
    dice = result["details"][0]
    assert isinstance(dice, Die)
    assert dice.count == 1
    assert dice.sides == 6
    assert dice.modifier == 0

def test_die_with_modifier():
    result = roller.roll("1d6+3", debug=True)
    dice = result["details"][0]
    assert isinstance(dice, Die)
    assert dice.count == 1
    assert dice.sides == 6
    assert dice.modifier == 3

def test_die_without_count():
    result = roller.roll("d8", debug=True)
    dice = result["details"][0]
    assert dice.count == 1
    assert dice.sides == 8
    assert dice.modifier == 0

def test_multiple_dice_with_modifiers():
    result = roller.roll("2d6-2+1d4+3+1d6", debug=True)
    dice_list = result["details"]
    assert len(dice_list) == 3
    assert dice_list[0].count == 2 and dice_list[0].sides == 6 and dice_list[0].modifier == -2
    assert dice_list[1].count == 1 and dice_list[1].sides == 4 and dice_list[1].modifier == 3
    assert dice_list[2].count == 1 and dice_list[2].sides == 6 and dice_list[2].modifier == 0

def test_negative_modifier():
    result = roller.roll("3d6-2", debug=True)
    dice = result["details"][0]
    assert dice.count == 3
    assert dice.sides == 6
    assert dice.modifier == -2

def test_multiple_dice_without_modifiers():
    result = roller.roll("2d6+1d4+3", debug=True)
    dice_list = result["details"]
    assert len(dice_list) == 2
    assert dice_list[0].count == 2 and dice_list[0].sides == 6 and dice_list[0].modifier == 0
    assert dice_list[1].count == 1 and dice_list[1].sides == 4 and dice_list[1].modifier == 3

def test_zero_count_die():
    with pytest.raises(ValueError, match="Dice count must be positive"):
        roller.roll("0d6", debug=True)

def test_negative_die_count():
    with pytest.raises(ValueError, match="Dice count must be positive"):
        roller.roll("-2d6", debug=True)

def test_too_many_dice():
    with pytest.raises(ValueError, match="Too many dice"):
        roller.roll("101d6", debug=True)

def test_too_many_sides():
    with pytest.raises(ValueError, match="Too many sides"):
        roller.roll("2d1001", debug=True)

def test_multiple_consecutive_modifiers():
    with pytest.raises(ValueError, match="Expected dice at"):
        roller.roll("+2+4-5", debug=True)

def test_spaces_in_notation():
    result = roller.roll("2d6 + 1d4 +3", debug=True)
    dice_list = result["details"]
    assert len(dice_list) == 2
    assert dice_list[0].count == 2 and dice_list[0].sides == 6 and dice_list[0].modifier == 0
    assert dice_list[1].count == 1 and dice_list[1].sides == 4 and dice_list[1].modifier == 3
