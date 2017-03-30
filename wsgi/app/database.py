from app import app
from flask_pymongo import PyMongo
from flask import jsonify 
import os

app.config['MONGO_DBNAME'] = os.environ['OPENSHIFT_APP_NAME']
app.config['MONGO_URI'] = os.environ['OPENSHIFT_MONGODB_DB_URL']+os.environ['OPENSHIFT_APP_NAME']
mongo = PyMongo(app)

@app.route('/database/collections', methods=['GET'])
def get_all_databases():
	return jsonify({'result' : mongo.db.collection_names()})

@app.route('/database/personnel', methods=['GET'])
def get_all_personnel():
	collection = mongo.db.test
	output = []
	for doc in collection.find():
		output.append({'Who' : doc['Name'], 'Job Role' : doc['Profession']})
	return jsonify({'result' : output})

