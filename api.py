import os
import re
from flask import Flask, request, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# DB_PASS = os.environ["F_API_DB_PASS"]
DATABASE_URL = os.environ["DATABASE_URL"]
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "au_prop REST API"
    }
)    

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:"+DB_PASS+"@localhost:5432/au_prop_api"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["DEBUG"] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/")
def hello():
    message = "Homepage: au_prop API"
    return render_template("index.html", message=message)


@app.route("/houses", methods=["GET"])
def handle_houses():
    args = request.args
    houses = HouseModel.query.filter_by(**args)
    results = [
        {"full_address": house.full_address,
         "suburb": house.suburb,
         "state": house.state,
         "postcode": house.postcode,
         "price": house.price,
         "bedrooms": house.bedrooms,
         "bathrooms": house.bathrooms,
         "parking_spaces": house.parking_spaces,
         "building_size": house.building_size,
         "building_size_unit": house.building_size_unit,
         "land_size": house.land_size,
         "land_size_unit": house.land_size_unit,
         "listing_company_name": house.listing_company_name,
         "sold_date": house.sold_date,
         "description": house.description,
         "listing_download_date": house.listing_download_date,
        } for house in houses]

    return {"House count": len(results), "House(s)": results}


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)
    

class HouseModel(db.Model):
    __tablename__ = "houses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_address = db.Column(db.String())
    suburb = db.Column(db.String())
    state = db.Column(db.String())
    postcode = db.Column(db.String())
    price = db.Column(db.String())
    bedrooms = db.Column(db.String())
    bathrooms = db.Column(db.String())
    parking_spaces = db.Column(db.String())
    building_size = db.Column(db.String())
    building_size_unit = db.Column(db.String())
    land_size = db.Column(db.String())
    land_size_unit = db.Column(db.String())
    listing_company_name = db.Column(db.String())
    sold_date = db.Column(db.String())
    description = db.Column(db.String())
    listing_download_date = db.Column(db.String())
    
    def __init__(self, 
                 full_address, 
                 suburb,
                 state,
                 postcode,
                 price,
                 bedrooms,
                 bathrooms,
                 parking_spaces,
                 building_size,
                 building_size_unit,
                 land_size,
                 land_size_unit,
                 listing_company_name,
                 sold_date,
                 description,
                 listing_download_date):
        self.full_address = full_address
        self.suburb = suburb
        self.state = state
        self.postcode = postcode
        self.price = price
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.parking_spaces = parking_spaces
        self.building_size = building_size
        self.building_size_unit = building_size_unit
        self.land_size = land_size
        self.land_size_unit = land_size_unit
        self.listing_company_name = listing_company_name
        self.sold_date = sold_date
        self.description = description
        self.listing_download_date = listing_download_date


    def __repr__(self):
        return f"<House {self.address}>"


if __name__ == "__main__":
    app.run()
