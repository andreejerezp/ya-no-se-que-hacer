"""Basic integration tests; run while MySQL and the populated schema are available."""
from db.dao import count_visitors, count_excursions



def test_counts_are_non_negative_integers():
    assert isinstance(count_visitors(), int) and count_visitors() >= 0
    assert isinstance(count_excursions(), int) and count_excursions() >= 0



def test_expected_population_exists():
    # The synthetic population used in this project should have at least some rows.
    assert count_visitors() > 0
    assert count_excursions() > 0
