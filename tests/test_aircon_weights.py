from exceptions import APICallFailure
from unittest.mock import Mock

import pytest
import requests

from aircon_weights import (calculate_average_cubic_weight,
                            calculate_cubic_weight, get_product_dimensions,
                            main)


@pytest.fixture
def mock_single_response():
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "objects": [
            {
                "category": "Air Conditioners",
                "title": "Kogan 10,000 BTU Portable Air Conditioner (2.9KW)",
                "weight": 26200.0,
                "size": {
                    "width": 49.6,
                    "length": 38.7,
                    "height": 89.0
                }
            }
        ],
        "next": None
    }
    return response


@pytest.fixture
def mock_fail_response():
    response = Mock()
    response.status_code = 500
    return response


def test_get_product_dimensions_retrieves_and_formats_data(monkeypatch, mock_single_response):
    monkeypatch.setattr(requests, "get", lambda x: mock_single_response)
    assert get_product_dimensions() == [[49.6, 38.7, 89.0]]


def test_get_product_dimensions_encounters_error(monkeypatch, mock_fail_response):
    monkeypatch.setattr(requests, "get", lambda x: mock_fail_response)
    with pytest.raises(APICallFailure):
        get_product_dimensions()


@pytest.mark.parametrize(
    "width, length, height, expected", [
        (0, 1, 1, 0),  # include zero value
        (100, 100, 100, 250),  # integers (even after divison cm -> m)
        (33.3, 44.4, 55.5, 20.51)  # floats
    ]
)
def test_calculate_cubic_weight(width, length, height, expected):
    assert round(calculate_cubic_weight(width, length, height), 2) == expected


def test_calculate_average_cubic_weight():
    assert calculate_average_cubic_weight([[100, 100, 100], [200, 200, 200]]) == 1125


def test_calculate_average_cubic_weight_when_no_products_found():
    assert calculate_average_cubic_weight([]) == 0


def test_end_to_end_success_output(monkeypatch, mock_single_response, capsys):
    monkeypatch.setattr(requests, "get", lambda x: mock_single_response)
    main()
    captured = capsys.readouterr()
    assert captured.out == "Average cubic weight of products in Air Conditioners is: 42.71kg\n"


def test_end_to_end_user_feedback_for_failed_api_call(monkeypatch, mock_fail_response, capsys):
    monkeypatch.setattr(requests, "get", lambda x: mock_fail_response)
    main()
    captured = capsys.readouterr()
    assert captured.out == "Failed to retrieve product data from the API, exiting...\n"
