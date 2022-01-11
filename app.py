from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

from model import db, seedData

 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Ahmad123.@localhost/Bank'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)
 
 

@app.route("/")
def startpage():
    trendingCategories = Category.query.all()
    return render_template("index.html", trendingCategories=trendingCategories)

@app.route("/category/<id>")
def category(id):
    products = Product.query.all()
    return render_template("category.html", products=products)

@app.route("/ahmad")
def ommig():
    return "<html><body><h1>Hej Jag Heter Ahmad</h1></body></html>"

if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
    seedData(db)
    app.run()

