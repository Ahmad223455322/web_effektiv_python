from model import db, Customer,Account,Transaction
from areas.customer.LRU_cach import LRUCache
import time

Lru_klass = LRUCache(3)
def sortering_transaktionerbild(sortColumn,sortOrder,id):
    
    allaPersoner = Transaction.query.filter_by(AccountId=id)


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

def sortering_kontobild(sortColumn,sortOrder,id):
   
    allaPersoner = Account.query.filter_by(CustomerId=id)


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
    

    if sortColumn == "Yrke":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.Yrke.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.Yrke.asc())
    
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
           
    paginationObject = allaPersoner.paginate(page,20,False)

    return paginationObject
 
 
def customer_decorator(functionaliasset):
    def wrapper(id):
        hittad = Lru_klass.get_cash(id)
        if hittad == -1 :
            valtkund = functionaliasset(id)
            Lru_klass.put(id,valtkund)
            return valtkund    
        return hittad
    return wrapper         


@customer_decorator
def sleep_fun(id):
    time.sleep(5)
    valtkund= Customer.query.get(id)
    return valtkund

# def timing_decerator(functionaliasset):
#     def wrapper(*args,**kwargs):
#         start= default_timer
#         res=functionaliasset(*args,**kwargs)
#         end= default_timer
#         print(f'det tog {end-start}såhär mycket tid')
#         return res
#     return wrapper

