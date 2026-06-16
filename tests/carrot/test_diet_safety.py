import importlib
import sys
from pathlib import Path

import pytest


@pytest.fixture
def csv_file(tmp_path):
    content = (
        "animal,can_eat_me,i_can_eat_it\n"
        "Lion,True,False\n"
        "Grizzly Bear,True,True\n"
        "Chicken,False,True\n"
    )
    p = tmp_path / "animals.csv"
    p.write_text(content)
    return str(p)


@pytest.fixture
def manager_factory():
    # Insert src into sys.path at runtime, then import the module
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / "src"))

    mod = importlib.import_module("carrot.diet_safety")

    def _make(path):
        return mod.DietSafetyManager(path)

    return _make


def test_get_relationships(csv_file, manager_factory):
    m = manager_factory(csv_file)
    assert m.get_relationship("Lion") == "The animal eats you. Avoid."
    assert m.get_relationship("Grizzly Bear") == "Both: Mutual danger dinner."
    assert m.get_relationship("Chicken") == "You eat the animal. Safe to hunt."
    assert m.get_relationship("Dragon") == "Unknown animal: Dragon"


def test_list_by_category(csv_file, manager_factory):
    m = manager_factory(csv_file)
    assert m.list_by_category("animal") == ["Lion"]
    assert m.list_by_category("me") == ["Chicken"]
    assert m.list_by_category("both") == ["Grizzly Bear"]
    assert (
        m.list_by_category("invalid")
        == "Invalid category. Choose 'me', 'animal', or 'both'."
    )


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Lion", "The animal eats you. Avoid."),
        ("Grizzly Bear", "Both: Mutual danger dinner."),
        ("Chicken", "You eat the animal. Safe to hunt."),
        ("Dragon", "Unknown animal: Dragon"),
    ],
)
def test_get_relationship_parametrized(csv_file, name, expected, manager_factory):
    m = manager_factory(csv_file)
    assert m.get_relationship(name) == expected
