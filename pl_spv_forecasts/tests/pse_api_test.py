# status code
from pl_spv_forecasts.src.services.pse_data.api.fetch_data import PseApi
from datetime import date


def test_status_code():
    response = PseApi().call_pse_api(date(2024, 6, 14))
    assert response.status_code == 200


# structure
def test_structure():
    response = PseApi().call_pse_api(date(2024, 6, 14))
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'


# data integrity
def test_data_integrity():
    response = PseApi().call_pse_api(date(2024, 6, 14))
    data = response.json()
    assert isinstance(data, dict)
    assert "value" in data
    assert "pv" in data['value'][0].keys()
    assert "wi" in data['value'][0].keys()
