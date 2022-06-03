from flask import Flask, render_template
from webargs import fields
from webargs.flaskparser import use_args
import random
import requests
from faker import Faker
import csv
from constants import PASSWORD_CHARACTERS
from settings import ROOT_PATH

app = Flask(__name__)
fake = Faker(['en_UK', 'uk_UA', 'ru_RU'])


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/path/sub-path/etc')
def path_example():
    return 'Hi again!'


@app.route('/hello')
@use_args({"name": fields.Str(required=True), }, location="query")
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
    names = [fake.first_name() for _ in range(users)]
    emails = [fake.unique.ascii_email() for _ in range(users)]
    list_of_users = [' '.join((names[i], emails[i])) for i in range(users)]
    return render_template('users.html', number=users, users_list=list_of_users)


@app.route('/space/')
def count_astronauts():
    response = requests.get("http://api.open-notify.org/astros.json")
    dict_ = response.json()
    count = sum(1 for _ in dict_["people"])
    peoples = [astronaut["name"] for astronaut in dict_["people"]]
    return f"{count} astronauts: {peoples}"


@app.route('/mean/')
def count_mean():
    with open('people_data.csv') as csvfile:
        rows = list(csv.reader(csvfile))
        dict_1 = {}
        for ind in range(1, len(rows)-1):
            dict_1[rows[ind][0]] = [rows[ind][1], rows[ind][2]]
        suma_h = 0
        suma_w = 0
        number = 0
        for k in dict_1:
            suma_h += float(dict_1[k][0])
            suma_w += float(dict_1[k][1])
            number += 1
        aver_h = (suma_h / number) * 2.54
        aver_w = (suma_w / number) * 0.453592
    return f"Aver height: {aver_h}cm;\tAver weight: {aver_w}kg"


if __name__ == '__main__':
    app.run()
