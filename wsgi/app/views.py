from app import app
from flask import render_template, request
import unirest
from forms import MessageForm
import database
import simple
from flask_navigation import Navigation

nav = Navigation(app)
nav.Bar('top', [nav.Item('Home','index'),nav.Item('Emotion Applic','emotion'),nav.Item('Visualise','polynomial'),nav.Item('Database Coll','get_all_collections')])

@app.route('/')
#@app.route('/index/')

def index():
    return render_template("index.html")

@app.route('/emotion/')
def emotion():
	return render_template("my_form.html",mood='happy',form=MessageForm())

@app.route('/emotion/', methods=['POST'])
def emotion_post():
	msg = request.form['message']
	response = unirest.post("https://community-sentiment.p.mashape.com/text/",
	  headers={
	    "X-Mashape-Key": "6VWQcE5umumsh9oLsHfFlOseFGbDp1caaUKjsnj6PJRqxZKslv",
	    "Content-Type": "application/x-www-form-urlencoded",
    	"Accept": "application/json"
    	},
  		params={
    	"txt": msg
  		}
	)
	return render_template("my_form.html",mood=response.body['result']['sentiment'],form=MessageForm())

