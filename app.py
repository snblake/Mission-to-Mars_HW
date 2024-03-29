from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scraper

app= Flask(__name__)
app.config["MONGO_URI"]= "mongodb://localhost:27017/mars_app"

mongo= PyMongo(app)

@app.route("/")
def home():
    mars=mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars=mongo.db.mars.update({}, scraper(), upsert=True)
    return redirect("/")

if __name__=="__main__":
    app.run()
