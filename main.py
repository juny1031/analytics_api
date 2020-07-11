from flask import Flask, request, jsonify, make_response
import uuid
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Text

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.sqlite'
db = SQLAlchemy(app)

class FLASKDB(db.Model):
    __tablename__ = 'cookie_table'
    KEY = db.Column(Integer, primary_key=True)
    UID = db.Column(Text)
    DATE = db.Column(Text)
    URL = db.Column(Text)

db.create_all()

@app.route("/", methods = ['GET'])
def post():
    response = make_response(jsonify())
    maxage = 60 * 60 * 24 * 120
    dt = datetime.datetime.now()
    
    if 'uid' in request.cookies:
        key = None
        cookie = request.cookies.get('uid')
        date = dt.strftime('%Y年%m月%d日 %H:%M:%S')
        url = request.referrer
        cookie_log = FLASKDB(KEY = key, UID = cookie, DATE = date, URL = url)
        db.session.add(cookie_log)
        db.session.commit()        
        return''
    else:
        response.set_cookie('uid', value = str(uuid.uuid4()), max_age = maxage)
        return response
    
    
@app.route("/count")
def count():
    user_cookie = request.cookies.get('uid')
    count_cookie = FLASKDB.query.filter_by(UID = user_cookie).count()
    add_first_count = count_cookie + 1
    return str(add_first_count) + '回目のアクセスです'

app.run(host="127.0.0.1", port=5000)
