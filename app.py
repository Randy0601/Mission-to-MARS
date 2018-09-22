from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import mars_scrape

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# conn = "mongodb://localhost:27017"

# client = pymongo.MongoClient(conn)
# db = client.mars_db
# collection = db.mars_scrape

mars_data = {}

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars 
    mars_data = mars_scrape.scrape()
    print(mars_data)
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)
   

if __name__ == "__main__":
    app.run(debug=True)
