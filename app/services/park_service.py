from db.pmv_dao import list_parks, create_park, update_park, delete_park



def search_parks(term=""):
    return list_parks(term.strip())


def add_park(name, surface, declaration_date, declaration_year, conservation, budget, admin_worker=None):
    if not name or not name.strip():
        raise ValueError("El nombre del parque es obligatorio.")
    if surface is None or surface <= 0:
        raise ValueError("La superficie debe ser mayor a cero.")
    if budget is not None and budget < 0:
        raise ValueError("El presupuesto no puede ser negativo.")
    return create_park(name.strip(), surface, declaration_date, declaration_year, conservation, budget, admin_worker)



def edit_park(park_id, name, surface, declaration_date, declaration_year, conservation, budget, admin_worker=None):
    if not name or not name.strip():
        raise ValueError("El nombre del parque es obligatorio.")
    if surface is None or surface <= 0:
        raise ValueError("La superficie debe ser mayor a cero.")
    if budget is not None and budget < 0:
        raise ValueError("El presupuesto no puede ser negativo.")
    update_park(park_id, name.strip(), surface, declaration_date, declaration_year, conservation, budget, admin_worker)


def remove_park(park_id):
    delete_park(park_id)
