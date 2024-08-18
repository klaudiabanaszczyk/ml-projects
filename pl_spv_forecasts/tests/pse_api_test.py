# status code
from pl_spv_forecasts.src.services.pse_data.api.fetch_data import PseApi
from datetime import date

response = PseApi().call_pse_api(date(2024, 6, 14))


def test_status_code():
    assert response.status_code == 200


def test_structure():
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'


def test_data_integrity():
    data = response.json()
    assert isinstance(data, dict)
    assert "value" in data
    assert "pv" in data['value'][0].keys()
    assert "wi" in data['value'][0].keys()
