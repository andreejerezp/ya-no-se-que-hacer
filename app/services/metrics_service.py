from db.dao import count_visitors, count_excursions



def get_home_metrics() -> dict[str, int]:
    """Business-layer wrapper for the initial home page metrics."""
    return {
        "visitantes": count_visitors(),
        "excursiones": count_excursions(),
    }
