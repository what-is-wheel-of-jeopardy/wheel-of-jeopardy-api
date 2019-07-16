from flask import Flask, request, jsonify
import json 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object('config')
CORS(app, resources={r'/*': {'origin': '*'}})
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Model #1  == category table in PostgreSql
class Category(db.Model):
    __tablename__ = 'category_new'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))

# Model #2  == qa table in PostgreSql
class QA(db.Model):
    __tablename__ = 'qa_new'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000))
    answer = db.Column(db.String(500))
    score = db.Column(db.String(100))
    category_id = db.Column(db.Integer)

# Model #3 == v_get_qas view in PostgreSql
class V_get_qas(db.Model):
    __tablename__ = 'v_get_qas'
    id = db.Column(db.String(500), primary_key=True)
    question = db.Column(db.String(1000))
    answer = db.Column(db.String(500))


# ViewModel #1 == v_get_qas view in PostgreSql
class QA_Schema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "question", "answer", "score", "category_id")
qa_schema = QA_Schema()
qas_schema = QA_Schema(many=True)



# ViewModel #2 == category table in PostgreSql
class Category_Schema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name")
category_schema = Category_Schema()
categories_schema = Category_Schema(many=True)


# hello world test call
@app.route('/', methods=['GET'])
def helloWorld():
    return jsonify("Welcome to WoJ!")




# QA CRUD starts ----------------------------------------------------------------------

# get all Q and A once game "Start" button clicked
@app.route("/get_qas", methods=["GET"])
def get_QAs():
    QAs = V_get_qas.query.all()
    json_str = ''
    for qa in QAs:
        tmp = '"' + qa.id + '":{"question": "' + qa.question + '","answer":"' + qa.answer + '"},'
        json_str = json_str + tmp
    json_str = json_str[:-1]
    json_str = '{"display":[{' + json_str + '}]}'
    return json.loads(json_str)


# get all Q and A for admin portal
@app.route("/admin/show_qas", methods=["GET"])
def show_QAs():
    qa = QA.query.all()
    return qas_schema.jsonify(qa)



# get all Q and A by category_id for admin portal
@app.route("/admin/show_qas/<int:category_id>", methods=["GET"])
def show_QA_by_cat_id(category_id):
    qa = QA.query.filter_by(category_id=category_id)
    return qas_schema.jsonify(qa)


# update existing Q and A by qa id
@app.route("/admin/update_qa/<int:qa_id>", methods=["GET", "POST"])
def update_QA(qa_id):
    qa = QA.query.filter_by(id=qa_id).first()
    if request.method == "POST":
        data = json.loads(request.get_data())
        new_question = data['question']
        new_answer = data['answer']
        qa.question = new_question
        qa.answer = new_answer
        db.session.commit()
        return jsonify('Updated for qa id: ' + str(qa_id))

    elif request.method == "GET":
        return qa_schema.jsonify(qa)




# delete existing Q and A by qa id
# @app.route("/admin/delete_qa/<string:qa_id>", methods=["POST"])
# def delete_QA(qa_id):
#     qa = QA.query.filter_by(id=qa_id).first()
#     db.session.delete(qa)
#     db.session.commit()
#     return 'Deleted Successfully!'

# QA CRUD ends ----------------------------------------------------------------------



# Category CRUD starts ----------------------------------------------------------------------

# get all categories for admin portal
@app.route("/admin/show_cats", methods=["GET"])
def show_categories():
    cat = Category.query.all()
    return categories_schema.jsonify(cat)


# update existing category name
@app.route("/admin/update_cat/<int:category_id>", methods=["POST"])
def update_category(category_id):
    data = json.loads(request.get_data())
    new_name = data['name']
    cat = Category.query.filter_by(id=category_id).first()
    cat.name = new_name
    db.session.commit()
    return jsonify("Category updated: " + data['name'])

# Category CRUD ends ----------------------------------------------------------------------
