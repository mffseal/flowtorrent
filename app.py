from flask import Flask
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)

users = [
    {'username': 'Tom', 'password': '111111'},
    {'username': 'Michael', 'password': '123456'}
]

@auth.get_password
def get_password(username):
    for user in users:
        if user['username'] == username:
            return user['password']
    return None

@app.route('/')
@auth.login_required
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
