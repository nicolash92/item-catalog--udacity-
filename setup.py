from flask import (
    Flask,
    abort,
    g,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Markup,
    jsonify,
    session as login_session,
    make_response)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json

from models import User, Item, Category, Base

engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/gencat')
def gencat():
    newCat = Category(name='Soccer')
    session.add(newCat)
    newCat = Category(name='Basketball')
    session.add(newCat)
    newCat = Category(name='Baseball')
    session.add(newCat)
    newCat = Category(name='Snowboarding')
    session.add(newCat)
    newCat = Category(name='Rock Climbing')
    session.add(newCat)
    newCat = Category(name='Foosball')
    session.add(newCat)
    newCat = Category(name='Skating')
    session.add(newCat)
    newCat = Category(name='Hockey')
    session.add(newCat)
    session.commit()
    return redirect(url_for('index'))


@app.route('/deler')
def deleteUsers():
    users = session.query(User).all()
    for user in users:
        session.delete(user)
        session.commit()
    return "done"


@app.route('/list-users')
def showUsers():
    users = session.query(User).all()
    for user in users:
        print(user.email)
    return render_template('users.html', users=users)


@app.route('/addDefItem')
def addDefItem():
    category = session.query(Category).first()
    user = session.query(User).first()
    newItem = Item(
        name="Stick",
        picture="https://image.shutterstock.com/z/" +
                "stock-photo-magic-staff-on-a-white" +
                "-background-1224280675.jpg",
        price="$50.49",
        description="a long slender piece of wood",
        category_id=category.name,
        owner=user.id
        )
    session.add(newItem)
    session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    app.secret_key = str(json.loads(open('client_secrets.json',
                                         'r').read())['flask_secret'])
    app.run(host='0.0.0.0', port=5000)
