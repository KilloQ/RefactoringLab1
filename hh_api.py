import requests
class HeadHunterAPI:
    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, keyword):
        vacancies = []
        for page in range(20):
            params = {
                "text": keyword,
                "area": 113,
                "per_page": 100,
                "page": page,
                "only_with_salary": True,
                "order_by": "publication_time"
            }
            response = requests.get(self.BASE_URL, params=params)
            if response.status_code == 200:
                for vacancy in response.json().get("items", []):
                    vacancies.append((
                        str(vacancy.get("id")),
                        str(vacancy.get("name")),
                        str(vacancy.get("alternate_url")),
                        str(vacancy.get("employer", {}).get("name")),
                        str(vacancy.get("area", {}).get("name")),
                        vacancy.get("salary", {}).get("from"),
                        vacancy.get("salary", {}).get("to"),
                        str(vacancy.get("salary", {}).get("currency"))
                    ))
        return vacancies
