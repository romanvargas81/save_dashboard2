from flask import Flask
from quickbooks.views import QUIKBOOKS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
SQLAlchemy(app)

app.register_blueprint(QUIKBOOKS)

if __name__ == '__main__':
    app.run(debug=True)