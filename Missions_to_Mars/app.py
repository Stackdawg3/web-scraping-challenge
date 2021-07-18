from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an Instance of Flask
app = Flask(__name__)

# Use flask_pymongo to Setup Mongo Connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    # Find a Record of Data from the Mongo Database
    mars_data = mongo.db.collection.find_one()
    # Return Template and Data
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scraper():
    # Run Scrape Function
    mars_data = scrape_mars.scrape()
    # Update the Mongo Database
    mongo.db.collection.update({}, mars_data, upsert=True)
    # Redirect Back to Homepage
    return redirect("/") 

if __name__ == "__main__":
    app.run(debug=True)