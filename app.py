import csv
import random
import sqlite3

import requests
from faker import Faker
from flask import Flask, render_template
from webargs import fields
from webargs.flaskparser import use_args

from constants import PASSWORD_CHARACTERS
from settings import ROOT_PATH, DB_PATH

app = Flask(__name__)
fake = Faker(['en_UK', 'uk_UA', 'ru_RU'])


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/path/sub-path/etc')
def path_example():
    return 'Hi again!'


@app.route('/hello')
@use_args({"name": fields.Str(required=True), "age": fields.Int(required=True)}, location="query")
def hi(args):
    return f'Hello {args["name"]}, I am {args["age"]} old.'


@app.route('/generate-password/<int:password_length>')
def generate_password(password_length: int):
    """Generate password.
    """
    password_as_list = [random.choice(PASSWORD_CHARACTERS) for _ in range(password_length)]
    random.shuffle(password_as_list)
    password = ''.join(password_as_list)
    return f"""<p>Length: {len(password)};</p>
<p>{password}</p>
"""


@app.route('/example-request')
def example_request():
    response = requests.get(url='https://example.com')
    return str(response.status_code)


@app.route('/requirements')
def read_requirements():
    return ROOT_PATH.joinpath('requirements.txt').read_text()


@app.route('/generate-users/')
@app.route('/generate-users/<int:users>')
def generate_users(users=100):
    """Generate users.
    Example: Vasya example@mail.com
    """
    list_of_users = [(fake.first_name(), fake.unique.ascii_email()) for _ in range(users)]
    return render_template('users.html', number=users, users_list=list_of_users)


@app.route('/space/')
def count_astronauts():
    response = requests.get("http://api.open-notify.org/astros.json")
    list_of_astronauts_data = response.json()["people"]
    number_of_astronauts = len(list_of_astronauts_data)
    names_of_astronauts = [astronaut["name"] for astronaut in list_of_astronauts_data]
    return f"{number_of_astronauts} astronauts: {names_of_astronauts}"


@app.route('/mean/')
def count_mean():
    with open('people_data.csv') as csvfile:
        rows = list(csv.reader(csvfile))
        general_height = 0
        general_weight = 0
        number = len(rows) - 1
        for index in range(1, number):
            general_height += float(rows[index][1])
            general_weight += float(rows[index][2])
        average_height = (general_height / number) * 2.54
        average_weight = (general_weight / number) * 0.453592
    return f"Average height: {average_height}cm<br>Average weight: {average_weight}kg"


if __name__ == '__main__':
    app.run()
