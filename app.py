#Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_table = mongo.db.mars_information.find_one()

    return render_template("index.html", mars_information=mars_table)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape functions
    mars_table = mongo.db.mars_information
    news_title, news_paragraph = scrape_mars.scrape_mars_news()
    featured_img_url = scrape_mars.scrape_mars_image()
    mars_facts = scrape_mars.scrape_mars_facts()
    mars_hemispheres = scrape_mars.mars_hemispheres()

    mars_information={
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image_url":featured_img_url,
        "mars_table":mars_facts,
        "hemisphere_image_urls":mars_hemispheres
    }

    print(mars_information)
    mars_table.update({}, mars_information, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)