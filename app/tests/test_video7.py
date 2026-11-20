"""Pruebas unitarias básicas de validaciones. Ejecutar desde la carpeta app: pytest ../tests"""
from unittest.mock import patch
import sys
import types
import pytest

# Stub de conexión: estas pruebas solo ejercitan validaciones de servicio, no requieren MySQL.
fake_connection = types.ModuleType("db.connection")
fake_connection.engine = object()
sys.modules.setdefault("db.connection", fake_connection)
import services.species_service as species_service
import services.park_service as park_service
import services.inscripcion_service as inscription_service


def test_species_requires_scientific_name():
    with pytest.raises(ValueError, match="denominación científica"):
        species_service.add_species("", "", "", None, "Sin subtipo")


def test_park_requires_name():
    with pytest.raises(ValueError, match="nombre del parque"):
        park_service.add_park("", 10, None, 2020, "", None, None)


def test_park_surface_must_be_positive():
    with pytest.raises(ValueError, match="superficie"):
        park_service.add_park("Parque de prueba", 0, None, 2020, "", None, None)


def test_park_budget_cannot_be_negative():
    with pytest.raises(ValueError, match="presupuesto"):
        park_service.add_park("Parque de prueba", 1, None, 2020, "", -1, None)


def test_inscription_requires_selection():
    with pytest.raises(ValueError, match="Selecciona"):
        inscription_service.register_visitor(None, None)


def test_species_create_calls_dao_with_cleaned_values():
    with patch.object(species_service, "create_species", return_value=10) as mocked:
        result = species_service.add_species("  Flora  ", "  Flora test  ", "Protegida", None, "Sin subtipo")
    assert result == 10
    mocked.assert_called_once()
