from flask import Flask, request, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo
import json
from bson import json_util
import os
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "471125e7d4a5442adfe176401d43e5adb6fa1cbf"
app.config["MONGO_URI"] = "mongodb+srv://tharanbala33:4119911narahT$@cluster01.p1sa2ws.mongodb.net/sample_mflix?retryWrites=true&w=majority"
CORS(app)

mongodb_client = PyMongo(app)
db = mongodb_client.db

# def format_server_time():
#   server_time = time.localtime()
#   return time.strftime("%I:%M:%S %p", server_time)

@app.route('/')
def index():
    return render_template('hello.html')

@app.route("/get", methods=["GET"])
def get():
    firstname = request.args.get('FirstName')
    lastname = request.args.get('LastName')
    dob = request.args.get('dob')
    epanther = request.args.get('epanther')
    campusid = request.args.get('campusid')
    # documents = db.hd_users.find()
    result = []
    # for document in documents:
    #     if first_name and last_name and dob:
    #         if document['first_name'] == first_name and document['last_name'] == last_name and document['dob']:
    #             response.append(document)
    #     if epanther:
    #         if document['epanther'] == epanther:
    #             response.append(document)
    #     if campusid:
    #         if document['campusid'] == campusid:
    #             response.append(document)
    # # user = db.users.find_one({"name": "Ned Stark"})
    # return json_util.dumps(response)
    if firstname and lastname and dob:
        response = db.hd_users.find_one({"$and": [{'first_name': firstname}, {'last_name': lastname}, {'dob': dob}]})
        result.append(response)
    
    if epanther:
       response = db.hd_users.find_one({'epanther': epanther})
       result.append(response)
    
    if campusid:
        response = db.hd_users.find_one({'campusid': int(campusid)})
        result.append(response)
                                        
    return json_util.dumps(result), 200

@app.route("/update", methods=["POST"])
def update():
    epanther = request.args.get('epanther')
    phone_number = request.args.get('mobile')
    email = request.args.get('email')
    if phone_number:
        db.hd_users.update_one({'epanther': epanther}, {"$set": {"phone_number": int(phone_number)}})
        result = {"status": "Updated"}, 200
    if email:
        db.hd_users.update_one({'epanther': epanther}, {"$set": {"email_address": email}})
        result = {"status": "Updated"}, 200
    return result

@app.route("/verify", methods=["GET"])
def verify():
    epanther = request.args.get('epanther')
    ssn = request.args.get('ssn')
    dob = request.args.get('dob')
    address = request.args.get('address')
    if epanther:
        response = db.hd_users.find_one({'epanther': epanther})
        if ssn and dob and address:
            if response['SSN'] == int(ssn) and response['dob'] == dob and response['address'] == address:
                result = {"status": "Healthy"}, 200
            elif response['SSN'] == int(ssn) or response['dob'] == dob or response['address'] == address:
                result = {"status": "Unhealthy, recheck entered data"}, 200
            else:
                result = {"status": "Wrong Information"}, 200
    return result

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))