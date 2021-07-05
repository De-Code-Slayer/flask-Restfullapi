from collections import namedtuple
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import column_property


#########initialistion of the flask frame work####

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#########database ########


class usermodels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return "user(name = {name}, id =  {id}, age = {age}, gender = {gender} "

# db.create_all()



####### request form arguments ###########
user_args = reqparse.RequestParser()
user_args.add_argument(
    "age", type=int, help="please enter age", required=True)
user_args.add_argument(
    "gender", type=str, help="please enter a gender", required=True)
user_args.add_argument(
    "name", type=str, help="please enter a name", required=True)
user_args.add_argument(
    "id", type=int, help="please enter an id", required=True)

###########################################################################
user_patch = reqparse.RequestParser()
user_patch.add_argument(
    "age", type=int, help="please enter age")
user_patch.add_argument(
    "gender", type=str, help="please enter a gender")
user_patch.add_argument(
    "name", type=str, help="please enter a name", required=True)





######## classes of routes and request methods for the api #########
################# response formatting #####################

resource_fiels = {
    "id": fields.Integer,
    "name": fields.String,
    "age": fields.Integer,
    "gender": fields.String
}




class Users(Resource):
    @marshal_with(resource_fiels)
    def get(self, username):
        response = usermodels.query.filter_by(name=username).first()
        if not response:
            abort(404, message="user does not exist")
        return response

    """ def delete(self, username):
        abort_if_no_user(username)
        del user[username]

        return "deleted successfully", 201 """


class Add_users(Resource):
    @marshal_with(resource_fiels)
    def put(self):
        args = user_args.parse_args()
        result = usermodels.query.filter_by(name=args["name"]).first()
        if result:
            abort(409, message="id is taken by nother user")
        user = usermodels(id=args["id"], name=args["name"], age=args["age"], gender=args["gender"])
       
        db.session.add(user)
        db.session.commit()

        return user, 201
    @marshal_with(resource_fiels)
    def patch(self, username):   
        args = user_patch.parse_args()
        result = usermodels.query.filter_by(name=args["name"]).first()
        if not result:
            abort(404, message="User does not exist")
         
        return

###### adding the classe to a route and argument#####
api.add_resource(Users, "/user/<string:username>")
api.add_resource(Add_users, "/adduser")

if __name__ == "__main__":
    app.run(debug=True)
