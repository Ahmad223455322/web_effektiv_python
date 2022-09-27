from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_user import roles_required,roles_accepted
from model import db, Customer,Account,Transaction
from sqlalchemy.sql import func
from datetime import datetime
from form import Instätning,Överförnig
from searchmotor import client
from .services import sortering_kontobild,sortering_kundbild,sortering_transaktionerbild,sleep_fun
from areas.customer.LRU_cach import LRUCache
import time

customerBlueprint = Blueprint('customer', __name__)
Lru_klass = LRUCache(3)







@customerBlueprint.route("/överföring", methods=['GET', 'POST'])
@roles_required("Admin")
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
            flash("Tack operationen är genomfört", "success")
            return redirect(url_for('customer.överföring',form=form))    
    return render_template('customer/överföring.html',form=form)
    

 


@customerBlueprint.route("/insätning", methods=['GET', 'POST'])
@roles_required("Admin")
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
@roles_accepted("Admin","Cashier")
def kundbild():


    page=int(request.args.get('page','1'))

    sök=request.args.get('sök','')

    sortColumn = request.args.get('sortColumn','ID')

    sortOrder = request.args.get('sortOrder','asc')





    Lru_klass = LRUCache(50)
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
@roles_accepted("Admin","Cashier")
def kontobild():
    sortColumn = request.args.get('sortColumn','ID')
    sortOrder = request.args.get('sortOrder','asc')
    id = int(request.args.get('id'))
    

    valtkund= sleep_fun(id)
    sort= sortering_kontobild(sortColumn,sortOrder,id)
    summan = db.session.query(func.sum(Account.Balance)).filter(Account.CustomerId == id).all()
    FÖRNAMN = db.session.query(Customer.GivenName).filter(Customer.Id==id).all()
    return render_template("customer/Kontobild.html",sort=sort,
    valtkund = valtkund, summan=summan[0][0],FÖRNAMN=FÖRNAMN,id=id)





@customerBlueprint.route("/transaktionerbild", methods=['GET', 'POST'])
@roles_accepted("Admin","Cashier")
def transaktionerbild():
    sortColumn = request.args.get('sortColumn','Datum')
    sortOrder = request.args.get('sortOrder','desc')
    id = int(request.args.get('id'))
    sort= sortering_transaktionerbild(sortColumn,sortOrder,id)
    valtkonto= Account.query.get(id)
    Saldo = db.session.query(Account.Balance).filter(Account.Id==id).all()
    return render_template("customer/transaktionerbild.html",sort=sort,valtkonto=valtkonto,Saldo=Saldo[0][0],id=id)




@customerBlueprint.route("/customer")
def indexPage():
    
    sortColumn = request.args.get('sortColumn', 'Id')
    sortOrder = request.args.get('sortOrder', 'asc')
    page = int(request.args.get('page', 1,))
    sök = request.args.get('sök','*')

    skip = (page-1) * 50
    result = client.search(search_text=sök,
        include_total_count=True,skip=skip,
        top=50,
        order_by=sortColumn + ' '  + sortOrder )
    summa= result.get_count()/50
    antal_utan_procent= round(summa)   
    top=50    

    alla = result
    return render_template('customer/customer.html', 
    listOfCustomers=alla,
    page=page,
    sortColumn=sortColumn,
    sortOrder=sortOrder,
    search_text=sök,
    skip=skip,
    top=top,
    antal_utan_procent=antal_utan_procent,
    )
