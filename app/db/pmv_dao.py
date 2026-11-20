"""DAO adicional para Video 7. No modifica el DAO original del Video 6."""
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from db.connection import engine

# --- Inscripción transaccional ---
def get_visitors():
    with engine.connect() as c:
        return c.execute(text("SELECT idVisitante, nombre, contacto FROM VISITANTE ORDER BY nombre")).mappings().all()

def get_excursions():
    sql = text("""SELECT ex.numCorrelativo, ex.numInterno, ex.codigoExcursion, ex.modalidad,
                       ex.horario, ex.fecha, ex.capacidad, pn.nombre AS parque, a.nombre AS area
                FROM EXCURSION ex
                JOIN AREA a ON a.numCorrelativo=ex.numCorrelativo AND a.numInterno=ex.numInterno
                JOIN PARQUE_NATURAL pn ON pn.numCorrelativo=a.numCorrelativo
                ORDER BY ex.fecha, pn.nombre, a.nombre, ex.codigoExcursion""")
    with engine.connect() as c:
        return c.execute(sql).mappings().all()

def create_inscription(visitor_id, excursion_key, observations=None):
    park_id, area_id, excursion_code = excursion_key
    # El bloqueo de la excursión reduce el riesgo de sobrepasar la capacidad en altas simultáneas.
    with engine.begin() as c:
        row = c.execute(text("""SELECT capacidad FROM EXCURSION
                             WHERE numCorrelativo=:park AND numInterno=:area AND codigoExcursion=:code
                             FOR UPDATE"""),
                        {"park": park_id, "area": area_id, "code": excursion_code}).mappings().first()
        if not row:
            raise ValueError("La excursión seleccionada ya no existe.")
        exists = c.execute(text("""SELECT 1 FROM INSCRIPCION
                               WHERE numCorrelativo=:park AND numInterno=:area
                                 AND codigoExcursion=:code AND idVisitante=:visitor"""),
                          {"park": park_id, "area": area_id, "code": excursion_code,
                           "visitor": visitor_id}).first()
        if exists:
            raise ValueError("Este visitante ya está inscrito en esa excursión.")
        occupied = c.execute(text("""SELECT COUNT(*) FROM INSCRIPCION
                                 WHERE numCorrelativo=:park AND numInterno=:area
                                   AND codigoExcursion=:code
                                   AND asistencia <> 'Cancelada'"""),
                           {"park": park_id, "area": area_id, "code": excursion_code}).scalar_one()
        if occupied >= row["capacidad"]:
            raise ValueError("La excursión alcanzó su capacidad máxima.")
        c.execute(text("""INSERT INTO INSCRIPCION
                     (numCorrelativo, numInterno, codigoExcursion, idVisitante, asistencia, observaciones)
                     VALUES (:park, :area, :code, :visitor, 'Pendiente', :obs)"""),
                 {"park": park_id, "area": area_id, "code": excursion_code,
                  "visitor": visitor_id, "obs": observations or None})

# --- Especies ---
def list_species(search=""):
    sql = text("""SELECT e.idEspecie, e.nombreVulgar, e.denominacionCientifica,
                       e.estadoConservacion, e.fechaIncorporacion,
                       CASE WHEN v.idEspecie IS NOT NULL THEN 'Vegetal'
                            WHEN an.idEspecie IS NOT NULL THEN 'Animal'
                            WHEN m.idEspecie IS NOT NULL THEN 'Mineral'
                            ELSE 'Sin subtipo' END AS tipo
                FROM ESPECIE e LEFT JOIN VEGETAL v ON v.idEspecie=e.idEspecie
                LEFT JOIN ANIMAL an ON an.idEspecie=e.idEspecie
                LEFT JOIN MINERAL m ON m.idEspecie=e.idEspecie
                WHERE e.nombreVulgar LIKE :q OR e.denominacionCientifica LIKE :q
                ORDER BY e.denominacionCientifica""")
    with engine.connect() as c:
        return c.execute(sql, {"q": f"%{search}%"}).mappings().all()

def create_species(common, scientific, conservation, date_added, subtype, detail1=None, detail2=None, detail3=None):
    with engine.begin() as c:
        result = c.execute(text("""INSERT INTO ESPECIE
            (nombreVulgar, denominacionCientifica, estadoConservacion, fechaIncorporacion)
            VALUES (:common, :scientific, :conservation, :date_added)"""),
            {"common": common or None, "scientific": scientific, "conservation": conservation or None,
             "date_added": date_added})
        species_id = result.lastrowid
        if subtype == "Vegetal":
            c.execute(text("INSERT INTO VEGETAL (idEspecie, floracion) VALUES (:id, :d1)"), {"id": species_id, "d1": detail1 or None})
        elif subtype == "Animal":
            c.execute(text("INSERT INTO ANIMAL (idEspecie, alimentacion, periodoCelo) VALUES (:id, :d1, :d2)"),
                      {"id": species_id, "d1": detail1 or None, "d2": detail2 or None})
        elif subtype == "Mineral":
            c.execute(text("INSERT INTO MINERAL (idEspecie, caracteristicasMineral, rocas, cristales) VALUES (:id, :d1, :d2, :d3)"),
                      {"id": species_id, "d1": detail1 or None, "d2": detail2 or None, "d3": detail3 or None})
        return species_id

def update_species(species_id, common, scientific, conservation, date_added):
    with engine.begin() as c:
        result = c.execute(text("""UPDATE ESPECIE SET nombreVulgar=:common,
            denominacionCientifica=:scientific, estadoConservacion=:conservation,
            fechaIncorporacion=:date_added WHERE idEspecie=:id"""),
            {"common": common or None, "scientific": scientific, "conservation": conservation or None,
             "date_added": date_added, "id": species_id})
        if result.rowcount == 0:
            raise ValueError("No se encontró la especie seleccionada.")

def delete_species(species_id):
    with engine.begin() as c:
        c.execute(text("DELETE FROM ESPECIE WHERE idEspecie=:id"), {"id": species_id})

# --- Parques naturales ---
def list_parks(search=""):
    sql = text("""SELECT numCorrelativo, nombre, superficie, fechaDeclaracion,
                       anioDeclaracion, estadoConservacion, presupuesto,
                       idTrabajadorAdministrador
                FROM PARQUE_NATURAL WHERE nombre LIKE :q ORDER BY nombre""")
    with engine.connect() as c:
        return c.execute(sql, {"q": f"%{search}%"}).mappings().all()

def create_park(name, area, declaration_date, declaration_year, conservation, budget, admin_worker):
    with engine.begin() as c:
        result = c.execute(text("""INSERT INTO PARQUE_NATURAL
            (nombre, superficie, fechaDeclaracion, anioDeclaracion, estadoConservacion, presupuesto, idTrabajadorAdministrador)
            VALUES (:name, :area, :date, :year, :conservation, :budget, :admin)"""),
            {"name": name, "area": area, "date": declaration_date, "year": declaration_year or None,
             "conservation": conservation or None, "budget": budget, "admin": admin_worker or None})
        return result.lastrowid

def update_park(park_id, name, area, declaration_date, declaration_year, conservation, budget, admin_worker):
    with engine.begin() as c:
        result = c.execute(text("""UPDATE PARQUE_NATURAL SET nombre=:name, superficie=:area,
            fechaDeclaracion=:date, anioDeclaracion=:year, estadoConservacion=:conservation,
            presupuesto=:budget, idTrabajadorAdministrador=:admin WHERE numCorrelativo=:id"""),
            {"name": name, "area": area, "date": declaration_date, "year": declaration_year or None,
             "conservation": conservation or None, "budget": budget, "admin": admin_worker or None, "id": park_id})
        if result.rowcount == 0:
            raise ValueError("No se encontró el parque seleccionado.")

def delete_park(park_id):
    with engine.begin() as c:
        c.execute(text("DELETE FROM PARQUE_NATURAL WHERE numCorrelativo=:id"), {"id": park_id})
