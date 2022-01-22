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

def sortering_transaktionerbild(sortColumn,sortOrder):
   
    allaPersoner = Transaction.query


    if sortColumn == "ID":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Transaction.Id.desc())
        else:
            allaPersoner = allaPersoner.order_by(Transaction.Id.asc())

    if sortColumn == "Typ":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Transaction.Type.desc())
        else:
            allaPersoner = allaPersoner.order_by(Transaction.Type.asc())

    
    if sortColumn == "Operation":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Transaction.Operation.desc())
        else:
            allaPersoner = allaPersoner.order_by(Transaction.Operation.asc())
         
    
    if sortColumn == "Datum":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Transaction.Date.desc())
        else:
            allaPersoner = allaPersoner.order_by(Transaction.Date.asc())
    
    if sortColumn == "Amount":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Transaction.Amount.desc())
        else:
            allaPersoner = allaPersoner.order_by(Transaction.Amount.asc())
    
    if sortColumn == "NewBalance":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Transaction.NewBalance.desc())
        else:
            allaPersoner = allaPersoner.order_by(Transaction.NewBalance.asc())
    
    if sortColumn == "AccountId":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Transaction.AccountId.desc())
        else:
            allaPersoner = allaPersoner.order_by(Transaction.AccountId.asc())                

    return allaPersoner   

def sortering_kontobild(sortColumn,sortOrder):
   
    allaPersoner = Account.query


    if sortColumn == "ID":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Account.Id.desc())
        else:
            allaPersoner = allaPersoner.order_by(Account.Id.asc())

    if sortColumn == "Kontotyp":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Account.AccountType.desc())
        else:
            allaPersoner = allaPersoner.order_by(Account.AccountType.asc())

    
    if sortColumn == "Skapad":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Account.Created.desc())
        else:
            allaPersoner = allaPersoner.order_by(Account.Created.asc())
         
    
    if sortColumn == "Balans":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Account.Balance.desc())
        else:
            allaPersoner = allaPersoner.order_by(Account.Balance.asc())
    
    if sortColumn == "KundID":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Account.CustomerId.desc())
        else:
            allaPersoner = allaPersoner.order_by(Account.CustomerId.asc())
    return allaPersoner    

def sortering_kundbild(sortColumn,sortOrder, page, sök):
    
    allaPersoner = Customer.query.filter(Customer.Id.like(sök) |
                   Customer.GivenName.like('%'+sök+'%')|
                   Customer.City.like('%'+sök+'%'))
  


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
           
    paginationObject = allaPersoner.paginate(page,50,False)

    return paginationObject
 
 

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
    
    page=int(request.args.get('page','1'))   
    sök=request.args.get('sök','')
    sortColumn = request.args.get('sortColumn','ID')
    sortOrder = request.args.get('sortOrder','asc')
    
    paginationObject=sortering_kundbild(sortColumn,sortOrder, page, sök)
    databas = Customer.query.all()
    return render_template("Kundbild.html",
                    databas=databas,
                    listOfCustomers=paginationObject.items, 
                    page=page,sortColumn=sortColumn,
                    sortOrder=sortOrder,
                    sök=sök,
                    has_next=paginationObject.has_next,
                    has_prev=paginationObject.has_prev, 
                    pages=paginationObject.pages)





@app.route("/kontobild", methods=['GET', 'POST'])
def kontobild():
    sortColumn = request.args.get('sortColumn','ID')
    sortOrder = request.args.get('sortOrder','asc')
    sort= sortering_kontobild(sortColumn,sortOrder)
    id = request.args.get('id')
    valtkund= Customer.query.get(id)
    kontolist= db.session.query(Customer, Account).join(Account).where(Account.CustomerId == id).all()
    summan = db.session.query(func.sum(Account.Balance)).filter(Account.CustomerId == id).all()
    return render_template("kontobild.html",kontolist=kontolist,sort=sort, valtkund = valtkund, summan = summan[0][0])







@app.route("/transaktionerbild", methods=['GET', 'POST'])
def transaktionerbild():
    sortColumn = request.args.get('sortColumn','ID')
    sortOrder = request.args.get('sortOrder','asc')
    sort= sortering_transaktionerbild(sortColumn,sortOrder)
    
    id = request.args.get('id')
    valtkonto= Account.query.get(id)
    transaktioner= db.session.query(Account,Transaction).join(Transaction).where(Transaction.AccountId == id).all()
    return render_template("transaktionerbild.html",transaktioner=transaktioner,sort=sort,valtkonto=valtkonto)









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