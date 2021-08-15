from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 

counter = 2
budgetAmount = 0
totalExpense = 0
allExpenses ={}
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:monogram@localhost/budget'
db=SQLAlchemy(app)


# Renders index html on startup 
@app.route("/") 
def index():
    return render_template("budget.html", budgetAmount=0, totalExpense=0, remaining=0, allExpenses={"Expense Name": "Expense Amt"})

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
        # counter = 1
        global budgetAmount
        global totalExpense
        global counter
        global allExpenses
        if request.form["budget"] == "budget":
            budgetAmount=request.form["budget_amount"] 
            counter+=1
            totalExpense = 0
            allExpenses = {}
            print(request.form)
            budget=Budget(budgetAmount)
            db.session.add(budget)
            db.session.commit()
            return render_template("budget.html",budgetAmount=budgetAmount, allExpenses=allExpenses, totalExpense= totalExpense, remaining=(int(budgetAmount)-int(totalExpense)))


        #Expense button
        elif request.form["budget"]=="expense":    
            eName=request.form["expense_name"]
            eCost=request.form["expense_amount"]
            expense=Expense(eName,eCost,counter)
            allExpenses[eName] = eCost
            totalExpense += int(eCost)
            db.session.add(expense)
            db.session.commit()
            return render_template("budget.html",eName=eName,eCost=eCost,totalExpense=totalExpense, allExpenses=allExpenses, budgetAmount=budgetAmount, remaining=(int(budgetAmount)-int(totalExpense)))    
    

if __name__ =='__main__':
    app.debug=True
    app.run()
