from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8333@localhost/budget_database'
db=SQLAlchemy(app)


# Renders index html on startup 
@app.route("/") 
def index():
    return render_template("budget.html")

#Budget Class
class Budget(db.Model):
    __tablename__="budget"
    id=db.Column(db.Integer,primary_key=True)
    budget_=db.Column(db.Integer)

    def __init__(self,budget_):
        self.budget_=budget_
     

#Expense Class
class Expense(db.Model):
    __tablename__="expense"
    id=db.Column(db.Integer,primary_key=True)
    eName_=db.Column(db.String(120))
    eCost_=db.Column(db.Integer)

    def __init__(self,eName_,eCost_):
        self.eName_=eName_
        self.eCost_=eCost_


#POST REQUEST
@app.route("/submit",methods=["POST"])
def submit():
    if request.method=="POST":
        #Budget button
        if request.form["budget"] == "budget":
            budget=request.form["budget_amount"] 
            print(request.form)
            budget=Budget(budget)
            db.session.add(budget)
            db.session.commit()
        
        #Expense button
        elif request.form["budget"]=="expense":    
            eName=request.form["expense_name"]
            eCost=request.form["expense_amount"]
            expense=Expense(eName,eCost)
            db.session.add(expense)
            db.session.commit()

        return render_template("submit.html")
    

if __name__ =='__main__':
    app.debug=True
    app.run()