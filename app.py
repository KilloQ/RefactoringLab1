from flask import Flask, render_template, request
from database import Database
from hh_api import HeadHunterAPI

app = Flask(__name__)
db = Database("hh_bd.db")
hh_api = HeadHunterAPI()

db.create_table()


@app.route('/', methods=['GET', 'POST'])
def index():
    keyword = request.form.get('keyword', '')
    city = request.form.get('city', '')
    salary_from = request.form.get('salary_from', None)

    if request.method == 'POST' and keyword:
        db.clear_vacancies()
        vacancies = hh_api.get_vacancies(keyword)
        db.insert_vacancies(vacancies)

        vacancies = db.get_filtered_vacancies(city, salary_from)
        return render_template('index.html', vacancies=vacancies, keyword=keyword, city=city, salary_from=salary_from)

    return render_template('index.html', keyword=keyword, city=city, salary_from=salary_from)


if __name__ == '__main__':
    app.run(debug=True)