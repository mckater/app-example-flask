from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
db = SQLAlchemy(app)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(50), unique=True, nullable=False)
    data = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)


@app.route('/')
def index():
    # Получаем все записи из таблицы Items
    items = Items.query.all()
    if not items:
        create_db()
    return render_template('index.html', items=items)


@app.route("/hello")
def hello():
    return "Змейка! Я тебя ❤️"


def create_db():
    with open('items.txt') as items:  # для Linux
    # with open('items.csv') as items:  # для Windows
        for item in items.readlines():
            item_id, data, description = item.split(None, maxsplit=2)
            item_data = Items(item_id=item_id, data=data, description=description)
            db.session.add(item_data)
        db.session.commit()
        return


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = 8080
    app.run(debug=False, host='0.0.0.0', port=port)
