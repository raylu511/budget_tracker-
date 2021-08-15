from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 

counter = 0
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
    budgetAmount_=db.Column(db.Integer)
    expense=db.relationship('Expense')

    def __init__(self,budgetAmount_):
        self.budgetAmount_=budgetAmount_
     

#Expense Class
class Expense(db.Model):
    __tablename__="expense"
    id=db.Column(db.Integer,primary_key=True)
    eName_=db.Column(db.String(120))
    eCost_=db.Column(db.Integer)
    budgetId_=db.Column(db.Integer,db.ForeignKey("budget.id"))

    def __init__(self,eName_,eCost_,budgetId_):
        self.eName_=eName_
        self.eCost_=eCost_
        self.budgetId_=budgetId_


#POST REQUEST
@app.route("/submit",methods=["POST"])
def submit():


    
    if request.method=="POST":     
        #Budget button
        if request.form["budget"] == "budget":
            global budgetAmount
            budgetAmount=request.form["budget_amount"] 
            global counter
            counter+=1
            print(request.form)
            budget=Budget(budgetAmount)
            db.session.add(budget)
            db.session.commit()
            return render_template("budget.html",budgetAmount=budgetAmount)


        #Expense button
        elif request.form["budget"]=="expense":    
            eName=request.form["expense_name"]
            eCost=request.form["expense_amount"]
            expense=Expense(eName,eCost,counter)
            db.session.add(expense)
            db.session.commit()
            return render_template("budget.html",eName=eName,eCost=eCost,budgetAmount=budgetAmount)    
    

if __name__ =='__main__':
    app.debug=True
    app.run()
