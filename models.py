from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Patient(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable = False)
    age = db.Column(db.Integer,nullable = False)
    gender = db.Column(db.String(10),nullable = False)
    phone = db.Column(db.String(20),nullable = False)
    email = db.Column(db.String(20),nullable = True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    #Relationships
    appointments = db.relationship('Appointment', backref ='patient',lazy = True)
    bills = db.relationship('Billing', backref ='patient',lazy = True)
class Doctor(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    specialty = db.Column(db.String(100),nullable = False)
    phone = db.Column(db.String(20),nullable = False)
    availability = db.Column(db.String(50),default = "Available")
    #Relationships
    appointments = db.relationship('Appointment', backref = 'doctor',lazy = True)
class Appointment(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'),nullable = False)
    doctor_id = db.Column(db.Integer,db.ForeignKey('doctor.id'),nullable = False)
    date = db.Column(db.String(20),nullable = False)
    time = db.Column(db.String(20),nullable = False)
    status = db.Column(db.String(20),default ="Scheduled")
class Billing(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    patient_id = db.Column(db.Integer,db.ForeignKey('patient.id'),nullable = False)
    amount = db.Column(db.Float,nullable = False)
    status = db.Column(db.String(20),default = "Pending")
    date = db.Column(db.DateTime,default=datetime.utcnow)


    
