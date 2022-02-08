from email import message
from flask_wtf import FlaskForm
from wtforms import Form, validators,SelectField,FloatField
from wtforms.fields import IntegerField
from model import Account



class Instätning(FlaskForm):
    från = IntegerField("Konto-nummer",[validators.DataRequired(message="Detta fält måste vara fyllt"),validators.NumberRange(min=1,max=5776,message="Skriv kontonummer mellan *.. & ****.. siffra.")])
    val = SelectField("Välj-Operation", choices=[('', 'Välj'),('deposit', 'insättning'), ('withdraw', 'uttag')]) 
    belopp = IntegerField("Belopp",[validators.NumberRange(min=1,max=15000,message="Max belopp är 15000 Kr!!")])

    def validate_belopp(form,från):
        från=Account.query.get(form.från.data)
        belopp=form.belopp.data
        if int(belopp) > int(från.Balance):
            raise validators.ValidationError("Beloppet är större än saldo")
        
    
    def validate_belopp(form,belopp):
        belopp=form.belopp.data    
        if belopp == None:
                raise validators.ValidationError("Detta fält måste fyllas")    
       
        



class Överförnig(FlaskForm):
    från = IntegerField("Från-Konto",[validators.NumberRange(min=1,max=5776,message="Skriv kontonummer mellan *.. & ****.. siffra.")])
    till = IntegerField("Till-Konto",[validators.NumberRange(min=1,max=5776,message="Skriv kontonummer mellan *.. & ****.. siffra.")])
    belopp = IntegerField("Belopp",[validators.NumberRange(min=1,max=15000,message="Max belopp är 15000 Kr!!")])

    def validate_belopp(form,från):
        från=Account.query.get(form.från.data)
        belopp=form.belopp.data
        if int(belopp) > int(från.Balance):
            raise validators.ValidationError("Beloppet är större än saldo")
    
    def validate_belopp(form,belopp):
        belopp=form.belopp.data    
        if belopp == None:
                raise validators.ValidationError("Detta fält måste fyllas")    
       
           