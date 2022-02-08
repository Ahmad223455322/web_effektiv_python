from flask import Blueprint,render_template,flash,redirect,url_for
from flask_user import current_user
from model import db, Customer,Account
from sqlalchemy.sql import func
siteBlueprint = Blueprint('site', __name__)








@siteBlueprint.route("/", methods=['GET', 'POST'])
def startpage():
    return render_template("site/index.html")




@siteBlueprint.route("/Statistik.html",methods=['GET', 'POST'])
def Statistik():
    antalPersoner = Customer.query.count()
    antalkonto = Account.query.count()
    Summary = db.session.query(func.sum(Account.Balance)).all()
    return render_template("site/Statistik.html",antalPersoner=antalPersoner,antalkonto=antalkonto,Summary=Summary[0][0])
