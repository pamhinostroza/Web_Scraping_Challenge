from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os


#Create flask app
app = Flask(__name__)   

#Use flask_pymongo to set up mongo connection
app.config["Mongo_URL"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Create route that renders index.html template & find documents 
@app.route("/")
def home():
        #obtain data
        mars_information = mongo.db.mars_information.find_one()
        return render_template("index.html", mars_information = mars_information)

#Create route for scrape function
@app.route("/scrape")
def scrape():
        #scrape functions
        mars_news = scrape_mars.scrape_mars_news()
        mars_image = scrape_mars.scrape_mars_mars_image()
        mars_facts = scrape_mars.scrape_mars_facts()
        mars_hemispheres = scrape_mars.scrape_mars_hemispheres()
        mongo.db.collection.update({}, mars_news, upsert = True)
        return redirect("/")

    if __name__ =="__main__":
        app.run(debug=True)