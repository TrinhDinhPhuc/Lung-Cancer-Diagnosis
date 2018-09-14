from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,ForeignKey,BIGINT
from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/CBD-Life'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__='User'
    id = Column(Integer,primary_key=True,autoincrement=True)
    speciality = Column(String(20),nullable=True)
    input_type   = Column(String(20),nullable=True)
    age = Column(Integer,nullable=True)
    gender = Column(String(4),nullable=True)
    name   = Column(String(20),nullable=True)
    phone =  Column(BIGINT,nullable=True)
    email =  Column(String(30),nullable=True)
    input_file = Column(String(50),nullable=False)
    def __init__(self,id,speciality,input_type,age,gender,name,phone,email,input_file):
        self.id=id
        self.speciality=speciality
        self.input_type=input_type
        self.age = age
        self.gender = gender
        self.name = name
        self.phone = phone
        self.email = email
        self.input_file = input_file
    def __repr__(self):
        return ("User(id=%d,speciality='%s',input_type='%s',age='%d',gender='%s',name='%s',phone='%d',email='%s',input_file='%s'" % (self.id,self.speciality,self.input_type,self.age,self.gender,self.name,self.phone,self.email,self.input_file))

# if __name__ == "__main__":
#     db.create_all()

from test import User
from test import db
new_ex =  User(1,'soi than','hiv diagnosis',35,'male','alexander patto',101325,'alex@alex.sander','1.3.5.6.7545.mhd')
db.session.add(new_ex)
db.session.commit()
