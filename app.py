from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String,DateTime
import calendar
from datetime import datetime
import re

app = Flask(__name__)
engine = create_engine('sqlite:///project.db',echo=False)
db = sessionmaker(autoflush=False, bind=engine)()
Base= declarative_base()

class Submit(Base):
    __tablename__="submit"

    ID = Column(Integer,primary_key=True)
    Name = Column(String(100),nullable=False)
    Email = Column(String(50),nullable=False) 
    Age = Column(Integer,nullable=False)
    Date_of_Birth = Column(DateTime,nullable=False)
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/submit",methods=['POST'])
def submit():
    if request.method =='POST':
        Name = request.form.get('Name')
        Email = request.form.get("Email")
        Age = request.form.get("Age")
        # Date_of_Birth = datetime.datetime.now()

        selected_date = request.form['Date_of_Birth']

        Date_of_Birth = datetime.strptime(selected_date, '%Y-%m-%d')



        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            return "Invalid email address. Please try again."
        
        if not Age.isdigit() or int(Age) <=0:
            return"Invalid Age.Please try again"

        entry = Submit(Name=Name,Email=Email,Age=Age,Date_of_Birth=Date_of_Birth)
        db.add(entry)
        db.commit()
        return redirect(url_for('success'))
    return render_template("index.html")


@app.route("/view_data")
def display_data():
    submissions = db.query(Submit).all()    
    return render_template("a.html", submissions=submissions)

if __name__=='__main__':
    with app.app_context():
        Base.metadata.create_all(engine)
        app.run(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True)
