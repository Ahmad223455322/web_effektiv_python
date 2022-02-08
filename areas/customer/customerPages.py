from flask import Blueprint,render_template,request,redirect, session,url_for,flash
from flask_user import roles_required,roles_accepted
from model import db, Customer,Account,Transaction
from sqlalchemy.sql import func
from datetime import datetime
from form import Instätning,Överförnig
from .services import sortering_kontobild,sortering_kundbild,sortering_transaktionerbild

customerBlueprint = Blueprint('customer', __name__)







@customerBlueprint.route("/överföring", methods=['GET', 'POST'])
# @roles_required("Admin")
def överföring():
    
    form= Överförnig(request.form)
    if form.validate_on_submit():
        överföring_1=Account.query.get(form.från.data)
        överföring_2=Account.query.get(form.till.data)
        if överföring_1 and överföring_2:
            nyöverföring_1= Transaction()
            nyöverföring_2= Transaction()
            belopp=form.belopp.data
            nyvärde_1=överföring_1.Balance-belopp
            nyvärde_2=överföring_2.Balance+belopp
            nyöverföring_1.Type ="Debit"
            nyöverföring_1.Operation="Transfer"
            nyöverföring_1.Date=datetime.now()
            nyöverföring_1.Amount=belopp
            nyöverföring_1.NewBalance=nyvärde_1
            nyöverföring_1.AccountId=överföring_1.Id
            överföring_1.Balance= nyvärde_1

            nyöverföring_2.Type ="Debit"
            nyöverföring_2.Operation="Transfer"
            nyöverföring_2.Date=datetime.now()
            nyöverföring_2.Amount=belopp
            nyöverföring_2.NewBalance=nyvärde_2
            nyöverföring_2.AccountId=överföring_2.Id
            överföring_2.Balance= nyvärde_2
            
           
          
            db.session.add(nyöverföring_1)
            db.session.add(nyöverföring_2)
            db.session.commit()
            return redirect(url_for('customer.överföring',form=form))    
    return render_template('customer/överföring.html',form=form)
    

 


@customerBlueprint.route("/insätning", methods=['GET', 'POST'])
# @roles_required("Admin")
def insätning():
  
    
    form= Instätning(request.form)    
    if form.validate_on_submit():
        konto=Account.query.get( form.från.data)
        if konto:
            nytransktion= Transaction()
            val=form.val.data
            belopp=form.belopp.data
            if val== "deposit":
                nyvärde=konto.Balance+belopp
                nytransktion.Type ="Debit"
                nytransktion.Operation=val
                nytransktion.Date=datetime.now()
                nytransktion.Amount= int(belopp)
                nytransktion.NewBalance=nyvärde
                nytransktion.AccountId=konto.Id
                konto.Balance= nyvärde
                db.session.add(nytransktion)
                db.session.commit()
           
          
            elif val== "withdraw":
                nyvärde=konto.Balance-belopp
                nytransktion.Type ="Debit"
                nytransktion.Operation=val
                nytransktion.Date=datetime.now()
                nytransktion.Amount=belopp
                nytransktion.NewBalance=nyvärde
                nytransktion.AccountId=konto.Id
                konto.Balance= nyvärde
                db.session.add(nytransktion)
                db.session.commit()
            flash("Tack operationen är genomfört", "success") # eller "danger" för röd error
            return redirect(url_for('customer.insätning',form=form))    
    return render_template('customer/insättning.html',form=form)
    



@customerBlueprint.route("/Kundbild", methods=['GET', 'POST'])
# @roles_accepted("Admin","Cashier")
def kundbild():
    
    page=int(request.args.get('page','1'))   
    sök=request.args.get('sök','')
    sortColumn = request.args.get('sortColumn','ID')
    sortOrder = request.args.get('sortOrder','asc')
    
    paginationObject=sortering_kundbild(sortColumn,sortOrder, page, sök)
    databas = Customer.query.all()
    return render_template("customer/Kundbild.html",
                    databas=databas,
                    listOfCustomers=paginationObject.items, 
                    page=page,
                    sortColumn=sortColumn,
                    sortOrder=sortOrder,
                    sök=sök,
                    has_next=paginationObject.has_next,
                    has_prev=paginationObject.has_prev, 
                    pages=paginationObject.pages)





@customerBlueprint.route("/kontobild", methods=['GET', 'POST'])
# @roles_accepted("Admin","Cashier")
def kontobild():
    sortColumn = request.args.get('sortColumn','ID')
    sortOrder = request.args.get('sortOrder','asc')
    sort= sortering_kontobild(sortColumn,sortOrder)
    id = request.args.get('id')
    valtkund= Customer.query.get(id)
    kontolist= db.session.query(Customer, Account).join(Account).where(Account.CustomerId == id).all()
    summan = db.session.query(func.sum(Account.Balance)).filter(Account.CustomerId == id).all()
    FÖRNAMN = db.session.query(Customer.GivenName).filter(Customer.Id==id).all()
    return render_template("customer/kontobild.html",kontolist=kontolist,sort=sort, 
    valtkund = valtkund, summan=summan[0][0],FÖRNAMN=FÖRNAMN[0][0])



@customerBlueprint.route("/transaktionerbild", methods=['GET', 'POST'])
# @roles_accepted("Admin","Cashier")
def transaktionerbild():
    sortColumn = request.args.get('sortColumn','ID')
    sortOrder = request.args.get('sortOrder','asc')
    sort= sortering_transaktionerbild(sortColumn,sortOrder)
    id = request.args.get('id')
    valtkonto= Account.query.get(id)
    transaktioner= db.session.query(Account,Transaction).join(Transaction).where(Transaction.AccountId == id).all()
    Saldo = db.session.query(Account.Balance).filter(Account.Id==id).all()
    print(id)
    return render_template("customer/transaktionerbild.html",transaktioner=transaktioner,sort=sort,valtkonto=valtkonto,Saldo=Saldo[0][0])



