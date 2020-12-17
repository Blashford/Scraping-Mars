from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")
collection = mongo.db.mars
collection.drop()

@app.route("/")
def index():
    mars_data = collection.find_one()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape_m():
    mars_data = scrape_mars.scrape()

    collection.update(
        {},
        mars_data,
        upsert=True
    )

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)