from db.pmv_dao import get_visitors, get_excursions, create_inscription


def visitor_options():
    return get_visitors()


def excursion_options():
    return get_excursions()


def register_visitor(excursion_key, visitor_id, observations=""):
    if not visitor_id or not excursion_key:
        raise ValueError("Selecciona un visitante y una excursión.")
    create_inscription(visitor_id, excursion_key, observations)
