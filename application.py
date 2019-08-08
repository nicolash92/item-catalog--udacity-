from flask import (
    Flask,
    g,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Markup,
    jsonify,
    session as login_session)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from google.oauth2 import id_token
from google.auth.transport import requests

import json

from flask_httpauth import HTTPTokenAuth

from models import User, Item, Category, Base

engine = create_engine('postgresql://catalog:password@localhost/catalog',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Token')

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
CLIENT_SECRET = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_secret']

# setup categories
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


@auth.verify_token
def verify_token(token):
    print('___________VERIFY TOKEN__________')
    print(token)
    print('___________VERIFY TOKEN__________')
    user_id = User.verify_auth_token(token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
        g.current_user = user
        return True
    flash(Markup('''
    <div class="ui negative message">
    <div class="header"> Unauthorized Access: LogIn!</div>
    </div>'''))
    return False


@app.route('/oauthcallback', methods=['POST'])
def googleSignIn():
    try:
        if request.form.get('idtoken'):
            token = request.form['idtoken']
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token,
                                                  requests.Request(),
                                                  CLIENT_ID)

            if idinfo['iss'] not in ['accounts.google.com',
                                     'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # ID token is valid.
            # Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            useremail = idinfo['email']
            userpicture = idinfo['picture']

            # check if user is registered otherwise register a new user
            user = session.query(User).filter_by(id=userid).first()
            if not user:
                user = User(id=userid, picture=userpicture, email=useremail)
                session.add(user)
                session.commit()
                flash(Markup('''
                <div class="ui success message">
                <div class="header"> Registered New User: {}!</div>
                </div>'''.format(useremail)))
            if not login_session.get('token'):
                print('--------------Flashed Logged In----------------------')
                flash(Markup('''
                    <div class="ui success message">
                    <div class="header"> LoggedIn User: {}!</div>
                    </div>'''.format(useremail)))
            login_session['token'] = user.generate_auth_token()
            print('tkn:::')
            print(login_session['token'])
            return login_session.get('token')

        elif 'token' in login_session:
            g.current_user = None
            if login_session.get('token'):
                flash(Markup('''
                    <div class="ui success message">
                    <div class="header">LoggedOut Successfully!</div>
                    </div>'''))
            login_session.pop('token', None)
            return "Logged Out"

    except ValueError:
        # Invalid token
        pass

    return redirect(url_for('index'))


@app.route('/token')
@auth.login_required
def updateToken():
    token = g.current_user.generate_auth_token()
    return token


@app.route('/')
def index():
    categories = session.query(Category).all()
    items = session.query(Item).limit(10)
    return render_template(
        "index.html",
        categories=categories,
        items=items,
        items_category="Sample Items",
        client_id=CLIENT_ID
        )


@app.route('/catalog/<string:items_category>/items')
def showCategory(items_category):
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=items_category).all()
    return render_template(
        "index.html",
        categories=categories,
        items=items,
        items_category=items_category,
        client_id=CLIENT_ID)


@app.route('/catalog/<string:items_category>/<string:item_name>')
def showItem(items_category, item_name):
    token = request.headers.get('Authorization')
    user_id = None
    if token:
        user_id = User.verify_auth_token(token.split()[1])
    category = session.query(Category).filter_by(name=items_category).one()
    item = session.query(Item).filter_by(category_id=category.name,
                                         name=item_name).one()
    return render_template("item.html", item=item, user=user_id)


@app.route('/catalog/add', methods=['GET', 'POST'])
@auth.login_required
def addItem():
    if request.method == 'POST':
        try:
            # get form data and check if category or
            # name is empty, and current user is set
            # otherwise flash an error and exit
            jsondata = request.get_json(force=True)
            name = jsondata.get('name')
            picture = jsondata.get('picture')
            description = jsondata.get('description')
            price = jsondata.get('price')
            category = jsondata.get('category')
            if(not category or not name and g.current_user):
                flash(Markup('''
                <div class="ui negative message">
                <div class="header"> Somrthing went Wrong</div>
                </div>'''))
                return "RedirectToIndex"
            # if we cant find the category then this throws an exception
            session.query(Category).filter_by(name=category).one()
            if session.query(Item).filter_by(name=name).first():
                flash(Markup('''
                <div class="ui negative message">
                <div class="header"> There's already an/a: {}</div>
                </div>'''.format(name)))
                return "RedirectToIndex"

            newItem = Item(name=name,
                           picture=picture,
                           description=description,
                           price=price,
                           category_id=category,
                           owner=g.current_user.id
                           )
            session.add(newItem)
            session.commit()
            flash(Markup('''
                <div class="ui success message">
                <div class="header"> Item Added</div>
                </div>'''))
            return "Success"
        except BaseException:
            flash(Markup('''
                <div class="ui negative message">
                <div class="header"> Somrthing went Wrong</div>
                </div>'''))
            return "RedirectToIndex"
    categories = session.query(Category).all()
    return render_template("add-item.html",
                           categories=categories)


@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'PUT'])
@auth.login_required
def editItem(item_name):
    try:
        if request.method == 'PUT':
            try:
                # get form data and check if category or
                # name is empty, and current user is set
                # otherwise flash an error and exit
                jsondata = request.get_json(force=True)
                name = jsondata.get('name')
                picture = jsondata.get('picture')
                description = jsondata.get('description')
                price = jsondata.get('price')
                category = jsondata.get('category')
                if(not category or not name and g.current_user):
                    flash(Markup('''
                    <div class="ui negative message">
                    <div class="header"> Somrthing went Wrong</div>
                    </div>'''))
                    return "RedirectToIndex"
                # if we cant find the category then this throws an exception
                session.query(Category).filter_by(name=category).one()

                # if the name is changed to somthing that
                # already exists the edit fails
                if (name != item_name and
                        session.query(Item).filter_by(name=name).first()):
                    flash(Markup('''
                    <div class="ui negative message">
                    <div class="header"> There's already an/a: {}</div>
                    </div>'''.format(name)))
                    return "RedirectToIndex"
                # if we cant find or update the item, an exception is thrown
                item = session.query(Item).filter_by(name=item_name).one()
                item.name = name
                item.picture = picture
                item.description = description
                item.price = price
                item.category_id = category
                session.add(item)
                session.commit()
                flash(Markup('''
                    <div class="ui success message">
                    <div class="header"> Item Edited</div>
                    </div>'''))
                return "Success"
            except BaseException:
                flash(Markup('''
                    <div class="ui negative message">
                    <div class="header"> Somrthing went Wrong</div>
                    </div>'''))
                return "RedirectToIndex"
        item = session.query(Item).filter_by(name=item_name).one()
        categories = session.query(Category).all()
        return render_template("edit-item.html",
                               categories=categories,
                               item=item)
    except BaseException:
        flash(Markup('''
            <div class="ui negative message">
            <div class="header"> Somrthing went Wrong</div>
            </div>'''))
        return "RedirectToIndex"


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'DELETE'])
@auth.login_required
def deleteItem(item_name):
    if request.method == 'DELETE':
        # try to find item and delete otherwise
        # flash error message and redirect to Index
        try:
            item = session.query(Item).filter_by(name=item_name).one()
            session.delete(item)
            session.commit()
        except BaseException:
            flash(Markup('''
                <div class="ui negative message">
                <div class="header"> Somrthing went Wrong</div>
                </div>'''))
            return "RedirectToIndex"
        # Successfully Deleted
        flash(Markup('''
            <div class="ui success message">
            <div class="header">{} Deleted!</div>
            </div>'''.format(item_name)))
        return "RedirectToIndex"
    # try to find item and render page
    # otherwise go back to index and flash error
    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except BaseException:
        flash(Markup('''
            <div class="ui negative message">
            <div class="header"> Somrthing went Wrong</div>
            </div>'''))
        return "RedirectToIndex"
    return render_template("delete-item.html", item=item)


# API ENDPOINTS
@app.route('/api/catalog')
def apiGetCatalog():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    catalog = [category.serialize for category in categories]
    for category in catalog:
        category['item'] = [i.serialize for i in items
                            if i.category_id == category['name']]
    return jsonify({'Category': catalog})


@app.route('/api/catalog/<string:item_name>')
def apiGetItem(item_name):
    item = session.query(Item).filter_by(name=item_name).first()
    if item:
        return jsonify({'Item': item.serialize,
                       'Category': item.category_id})
    return jsonify({'Error': "Item Not Found"})


if __name__ == '__main__':
    app.debug = True
    app.secret_key = str(json.loads(open('client_secrets.json',
                                         'r').read())['flask_secret'])
    app.run(host='0.0.0.0', port=5000)
