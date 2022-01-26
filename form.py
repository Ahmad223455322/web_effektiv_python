from email import message
from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators,SelectField
from wtforms.fields import IntegerField
from model import Account



class Instätning(FlaskForm):
    från = IntegerField("Från",[validators.NumberRange(min=1,max=6000,message="Skriv rätt kontonummer!!")])
    val = SelectField("Välj", choices=[('', 'Välj'),('i', 'insättning'), ('u', 'uttag')] ,validators=validators.DataRequired()) 
    belopp = IntegerField("Belopp",[validators.NumberRange(min=1,max=15000,message="Max belopp är 15000 Kr!!")])

    def validate_från(self,från):
        kund = Account.query.filter(Account.Id==från.data).first()
        if kund == None:
            raise validators.ValidationError("Kontot finns inte i databas")
        # if form.belopp.data== "" and från.data > cgossenaccoundt.balcac
        



class Överförnig(FlaskForm):
    från = IntegerField("Från",[validators.NumberRange(min=1,max=4,message="Skriv rätt kontonummer!!")])
    till = IntegerField("Till",[validators.NumberRange(min=1,max=4,message="Skriv rätt kontonummer!!")])
    belopp = IntegerField("Belopp",[validators.NumberRange(min=1,max=15000,message="Max belopp är 15000 Kr!!")])

    def validate_från(self,från):
        kund = Account.query.filter(Account.Id==från.data).first()
        if kund == None:
            raise validators.ValidationError("Kontot finns inte i databas")
        # if form.belopp.data== "" and från.data > cgossenaccoundt.balcac
        
