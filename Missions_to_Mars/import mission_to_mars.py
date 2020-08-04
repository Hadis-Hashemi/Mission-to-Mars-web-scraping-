import mission_to_mars
import mission_to_mars
from flask_pymongo import PyMongo

mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

marsdata = mongo.db.collection

    # Run the scrape function
data = mission_to_mars.scrape()
    

    # Update the Mongo database using update and upsert=True
marsdata.update({}, data, upsert=True)
