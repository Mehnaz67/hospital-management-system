import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Patient, Doctor, Appointment, Billing

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hosipital-key-secret-123'
if os.environ.get('VERCEL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/hospital.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'

#Intialize Database
db.init_app(app)

with app.app_context():
    db.create_all()

#Dashboard view
@app.route('/')

def dashboard():
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()
    total_revenue = db.session.query(db.func.sum(Billing.amount)).filter(Billing.status == 'Paid').scalar() or 0.0

    return render_template('index.html', patients_count = total_patients,doctors_count = total_doctors,appointments_count = total_appointments,revenue = total_revenue)
#Patient management system
@app.route('/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email')

        new_patient = Patient(name = name, age = int(age), gender = gender, phone = phone, email = email)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('patients'))
    all_patients = Patient.query.order_by(Patient.id.desc()).all()
    return render_template('patients.html', patients = all_patients)
#doctor management system
@app.route('/doctors', methods=['GET','POST'])
def doctors():
    if request.method == 'POST':
        name = request.form.get('name')
        specialty = request.form.get('specialty')
        phone = request.form.get('phone')
        availability = request.form.get('availability','Available')
        new_doctor = Doctor(name = name, specialty = specialty, phone = phone, availability = availability)
        db.session.add(new_doctor)
        db.session.commit()
        return redirect(url_for('doctors'))
    all_doctors = Doctor.query.all()
    return render_template('doctors.html', doctors = all_doctors)
#appointments booking outes
@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        doctor_id = request.form.get('doctor_id')
        date = request.form.get('date')
        time = request.form.get('time')

        new_app = Appointment(patient_id = int(patient_id),doctor_id = int(doctor_id),date = date, time= time)
        db.session.add(new_app)
        db.session.commit()
        return redirect(url_for('appointments'))
    all_appointments = Appointment.query.all()
    all_patients = Patient.query.all()
    all_doctors = Doctor.query.all()
    return render_template('appointments.html', appointments=all_appointments, patients=all_patients, doctors=all_doctors)
#Billing routes
@app.route('/billing', methods=['GET','POST'])
def billing():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        amount = request.form.get('amount')
        status = request.form.get('status','pending')

        new_bill = Billing(patient_id = int(patient_id), amount = float(amount),status = status)
        db.session.add(new_bill)
        db.session.commit()
        return redirect(url_for('billing'))
    all_bills = Billing.query.all()
    all_patients = Patient.query.all()
    return render_template('billing.html',bills=all_bills, patients=all_patients)
#Search route
@app.route('/search')
def search():
    query = request.args.get('q', '')
    patient_results = Patient.query.filter(
        Patient.name.ilike(f'%{query}%') | Patient.phone.ilike(f'%{query}%')
    ).all()
    return render_template('search_results.html', query=query, patients=patient_results)

if __name__ == '__main__':
    app.run(debug=True)





