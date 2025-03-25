import pytest
from hh_api import HeadHunterAPI

@pytest.fixture
def hh_api():
    return HeadHunterAPI()

def test_get_vacancies(hh_api, monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {"items": [{"id": "0", "name": "Test", "alternate_url": "url",
                                   "employer": {"name": "Company"},
                                   "area": {"name": "Moscow"},
                                   "salary": {"from": 100000, "to": 150000, "currency": "RUB"}}]}
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    vacancies = hh_api.get_vacancies("Python")
    first_vacancy = vacancies[0]
    assert first_vacancy[0] == "0"
    assert first_vacancy[1] == "Test"
    assert first_vacancy[2] == "url"
    assert first_vacancy[3] == "Company"
    assert first_vacancy[4] == "Moscow"
    assert first_vacancy[5] == 100000
    assert first_vacancy[6] == 150000
    assert first_vacancy[7] == "RUB"
