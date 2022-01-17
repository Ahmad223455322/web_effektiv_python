from re import A, T
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData, Customer,Account,Transaction
from sqlalchemy.sql import func

 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Ahmad123.@localhost/Bank'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)
 
 

@app.route("/", methods=['GET', 'POST'])
def startpage():
    return render_template("index.html")




@app.route("/Statistik.html",methods=['GET', 'POST'])
def Statistik():
    antalPersoner = Customer.query.count()
    antalkonto = Account.query.count()
    Summary = db.session.query(func.sum(Account.Balance)).all()
    return render_template("Statistik.html",antalPersoner=antalPersoner,antalkonto=antalkonto,Summary=Summary[0][0])





@app.route("/loggain", methods=['GET', 'POST'])
def loggain():
    return render_template("loggain.html")







@app.route("/Kundbild", methods=['GET', 'POST'])
def kundbild():
    databas = Customer.query.all()
    return render_template("Kundbild.html",databas=databas)





@app.route("/kontobild", methods=['GET', 'POST'])
def kontobild():
    konto = Account.query.all()
    return render_template("Kontobild.html",konto=konto)














@app.route("/category/<id>")
def category(id):
    products = Product.query.all()
    return render_template("category.html", products=products)


if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
    app.run()
    seedData(db)














#trendingCategories = Category.query.all() trendingCategories=trendingCategories
#trendingCategories = Category.query.all() trendingCategories=trendingCategories
#trendingCategories = Category.query.all() trendingCategories=trendingCategories