from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Here we make our connection to the mongo databases and add our collection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")
collection = mongo.db.mars
# Then we drop anything that was in the collection so we have a fresh start
collection.drop()

@app.route("/")
def index():
    # Here we grab the first entry from the database and render it in the html
    mars_data = collection.find_one()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape_m():
    # Here we call the scrape function from scrape_mars and store the returned dictionary into a variable
    mars_data = scrape_mars.scrape()

    # Then we upsert it to the mongo collection
    collection.update(
        {},
        mars_data,
        upsert=True
    )

    # And return to the index route
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)