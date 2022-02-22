from flask import Flask, render_template
from flask_migrate import Migrate, upgrade
from model import db, seedData,user_manager,User
from areas.site.sitePages import siteBlueprint
from areas.customer.customerPages import customerBlueprint
from searchmotor import addDocuments,createIndex


 
app = Flask(__name__)
app.config.from_object('config.ConfigDebug')


db.app = app
db.init_app(app)
migrate = Migrate(app,db)
user_manager.app = app
user_manager.init_app(app,db,User)

app.register_blueprint(siteBlueprint)
app.register_blueprint(customerBlueprint)


if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData()
        # createIndex()
        # addDocuments()
       
        
    app.run(host="127.0.0.1", port=5000, debug=True)














@app.route("/loggain", methods=['GET', 'POST'])
def loggain():
    return render_template("loggain.html")






@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("register.html")






