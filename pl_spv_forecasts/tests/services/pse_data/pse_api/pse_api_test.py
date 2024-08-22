from datetime import date
from json import JSONDecodeError
from unittest import TestCase, main
from unittest.mock import patch

import requests
from pytest import raises

from pl_spv_forecasts.src.services.pse_data.api.fetch_data import PseApi


class TestPseApi(TestCase):
    def setUp(self):
        self.testing_date = date(2024, 6, 14)

    @patch("pl_spv_forecasts.src.services.pse_data.api.fetch_data.requests.get")
    def test_call_pse_api_returns_200(self, mock_requests):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_requests.return_value = mock_response

        result = PseApi().call_pse_api(self.testing_date)
        self.assertTrue(result)

    @patch("pl_spv_forecasts.src.services.pse_data.api.fetch_data.requests.get")
    def test_call_pse_api_returns_400(self, mock_requests):
        mock_response = requests.Response()
        mock_response.status_code = 400
        mock_requests.return_value = mock_response

        result = PseApi().call_pse_api(self.testing_date)
        self.assertFalse(result)

    @patch("pl_spv_forecasts.src.services.pse_data.api.fetch_data.requests.get")
    def test_call_pse_api_returns_invalid_json(self, mock_requests):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b''
        mock_requests.return_value = mock_response

        with raises(JSONDecodeError):
            PseApi().call_pse_api(self.testing_date).json()

    @patch("pl_spv_forecasts.src.services.pse_data.api.fetch_data.requests.get")
    def test_call_pse_api_timeout_handling(self, mock_requests):
        mock_requests.side_effect = requests.exceptions.Timeout

        with raises(requests.exceptions.Timeout):
            PseApi().call_pse_api(self.testing_date)


if __name__ == "__main__":
    main()


def test_api_response_status_and_data_structure():
    # Arrange
    testing_date = date(2024, 6, 14)

    # Act
    pse_api = PseApi()
    response = pse_api.call_pse_api(testing_date)
    data = response.json()

    # Asserts
    assert response.status_code == 200
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'
    assert isinstance(data, dict)
    assert "value" in data
    assert isinstance(data["value"], list)
    assert "pv" in data['value'][0].keys()
    assert "wi" in data['value'][0].keys()
