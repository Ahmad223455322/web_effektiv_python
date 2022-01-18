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



def sortering(sortColumn,sortOrder):

    if sortColumn == "" or sortColumn == None:
        sortColumn = "namn"

    if sortOrder == "" or sortOrder == None:
        sortOrder = "asc"

    activePage = "personerPage"
    allaPersoner = Customer.query


    if sortColumn == "ID":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.Id.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.Id.asc())

    if sortColumn == "Förnamn":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.GivenName.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.GivenName.asc())

    
    if sortColumn == "Efternamn":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.Surname.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.Surname.asc())
         
    
    if sortColumn == "Adress":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.Streetaddress.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.Streetaddress.asc())
    
    if sortColumn == "Stad":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.City.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.City.asc())
        
    
    if sortColumn == "Land":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.Country.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.Country.asc())
    
    if sortColumn == "Email":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.EmailAddress.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.EmailAddress.asc())
    
    if sortColumn == "Telefon":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.Telephone.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.Telephone.asc())


    if sortColumn == "Personnummer":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.Birthday.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.Birthday.asc())
    return allaPersoner
 
 

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
    # listOfCustomers = Customer.query.limit(50).all()
    sortColumn = request.args.get('sortColumn')
    sortOrder = request.args.get('sortOrder')
    listOfCustomers=sortering(sortColumn,sortOrder)
    databas = Customer.query.all()
    return render_template("Kundbild.html",databas=databas,listOfCustomers=listOfCustomers)





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