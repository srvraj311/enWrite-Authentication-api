from flask import Flask, jsonify, request
from flask_restful import Api , Resource
from pymongo import MongoClient
import bcrypt
import os

# Default Salt
salt = bcrypt.gensalt()


app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb://db:27017")
db = client["primaryDatabase"]
users = db["users"]


@app.route("/")
def home():
    return "Working" 

def passToHash(password):
    """Hash a password for storing."""
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed


# Function to generate a key:
def generate_key(username, password):
    salt = b'$2b$12$1wnt3vXHtkYjOs1LV.pD4O'
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), salt)
    hashed_us = bcrypt.hashpw(username.encode("utf-8"), salt)
    key = hashed_pw + hashed_us
    return key


# Function to mach password - used in Stored Class
def verifyPw(username, password):
	try:
		hashed_pw = users.find({
			"username":username
		})[0]["password"]
		if bcrypt.hashpw(password.encode("utf-8"),hashed_pw) == hashed_pw:
			return True
		else:
			return False
	except:
		return False


def alreadyInDataBase(uname):
    try:
        existing = users.find({"username":uname})[0]["username"]
        if uname == existing:
            return True
    except: return False


class Create_Account(Resource):
    def post(self):
        data = request.get_json()
        username_recieved = data["username"]
        password_recieved = data["password"]
        email = data["email"]

        if alreadyInDataBase(username_recieved) == True:
            toReturn = {
                "status":"301",
                "message":"Account already exists"
            }
            return jsonify(toReturn)

        password = passToHash(password_recieved)
        key = generate_key(username_recieved, password_recieved)
        
        try:
            users.insert_one({
                "username":username_recieved,
                "password":password,
                "email":email,
                "login":"not-active",
                "notes_count":"0",
                "notes":[],
                "reminders":[],
                "key":str(key)
            })
            toReturn = {
                "status":"200",
                "message":"Account Created Successfully",
                "key":str(key)
            }
            return jsonify(toReturn)

        except:
            toReturn = {
                "status":"300",
                "message":"Unable to save to Database : SIGNUP",
                "key":str(key)
            }
            return jsonify(toReturn)


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]        

        # username check in DB
        if alreadyInDataBase(username):

            if verifyPw(username, password):
                key = generate_key(username, password)
                toReturn = {
                    "status":200,
                    "message":"Logged In",
                    "key": str(key),
                    "DATA":{
                        "username":users.find({"username":username})[0]["username"],
                        "email":users.find({"username":username})[0]["email"],
                        "notes_count":users.find({"username":username})[0]["notes_count"],
                        "notes":users.find({"username":username})[0]["notes"],
                        "reminders":users.find({"username":username})[0]["reminders"]
                    }
                }
                users.update_one({"username":username},{"$set":{
                    "login":"active"
                }})
                return jsonify(toReturn)
            else:
                toReturn = {
                    "status":"302",
                    "message":"Wrong Credentials",
                }
                return jsonify(toReturn)
        else:
            toReturn = {
                "status":"303",
                "message":"User Not found"
            }
            return jsonify(toReturn)
    

class Reset(Resource):
    def post(self):
        data = request.get_json()

        username = data["username"]
        password = data["password"]
        new_password = data["new_password"]

        if alreadyInDataBase(username):

            if verifyPw(username, password):
                users.update_one({
                    "username":username
                },{"$set":
                {
                    "password":passToHash(new_password)
                }})

                toReturn = {
                    "status":"200",
                    "message":"Password Updated"
                }
                return jsonify(toReturn)
            else:
                toReturn = {
                    "status":"302",
                    "message":"Wrong Credentials",
                }
                return jsonify(toReturn)
        else:
            toReturn = {
                "status":"303",
                "message":"User Not found"
            }
            return jsonify(toReturn)


class UpdateNotes(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        key = data["key"]
        notes = data["notes"]
        reminders = data["reminders"]
        if alreadyInDataBase(username):
            if key == users.find({"username":username})[0]["key"]:
                users.update_one({
                    "username":username
                },{"$set":{
                    "notes":notes,
                    "reminders":reminders,
                    "notes_count":str(len(notes))
                }})

                toReturn = {
                    "status":"200",
                    "message":"updated to server"
                }

                return jsonify(toReturn)
            else:
                toReturn = {
                    "status":"305",
                    "message":"key mismatch"
                }
                return jsonify(toReturn)
        else:
            toReturn = {
                "status":"304",
                "message":"dataBase Error ,  Login:Active"
            }
            return jsonify(toReturn)


class RetrieveNotes(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        key = data["key"]

        if alreadyInDataBase(username):
            if key == users.find({"username":username})[0]["key"]:
                toReturn = {
                    "status":"200",
                    "email":users.find({"username":username})[0]["email"],
                    "username":users.find({"username":username})[0]["username"],
                    "notes":users.find({"username":username})[0]["notes"],
                    "reminders":users.find({"username":username})[0]["reminders"]
                }
                return jsonify(toReturn)
            else:
                toReturn = {
                    "status":"305",
                    "message":"key mismatch"
                }
                return jsonify(toReturn)
        else:
            toReturn = {
                "status":"304",
                "message":"Database Error : RETRIEVE FAILED"
            }
            
            return jsonify(toReturn)


api.add_resource(Create_Account,"/signup")
api.add_resource(Login, "/login")
api.add_resource(Reset, "/reset")
api.add_resource(UpdateNotes, "/update")
api.add_resource(RetrieveNotes, "/get")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)