import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, User, Caregiver, Member, Address, Job, JobApplication, Appointment

app = Flask(__name__)
app.secret_key = "devsecret"

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:12345678@localhost:5432/caregiver_platform")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=False)


if os.environ.get("FLASK_ENV") == "development":
    Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users")
def users_list():
    session = Session()
    users = session.query(User).all()
    return render_template("users/list.html", users=users)


@app.route("/users/new", methods=["GET","POST"])
def users_new():
    session = Session()
    try:
        if request.method == "POST":
            email = request.form["email"]
            given_name = request.form["given_name"]
            surname = request.form["surname"]
            city = request.form.get("city")
            phone_number = request.form.get("phone_number")
            profile_description = request.form.get("profile_description")
            password = request.form["password"] or "password"
            u = User(email=email, given_name=given_name, surname=surname, city=city, phone_number=phone_number, profile_description=profile_description, password=password)
            session.add(u)
            session.commit()
            flash("User created")
            return redirect(url_for("users_list"))
        return render_template("users/form.html")
    except Exception as e:
        session.rollback()
        flash(f"Error: {str(e)}")
        return render_template("users/form.html")
    finally:
        session.close()

# --- Caregivers list & create ---
@app.route("/caregivers")
def caregivers_list():
    session = Session()
    rows = session.query(Caregiver).join(User, Caregiver.caregiver_user_id==User.user_id).all()
    return render_template("caregivers/list.html", caregivers=rows)

@app.route("/caregivers/new", methods=["GET","POST"])
def caregivers_new():
    session = Session()
    if request.method == "POST":
        email = request.form["email"]
        given_name = request.form["given_name"]
        surname = request.form["surname"]
        city = request.form.get("city")
        phone_number = request.form.get("phone_number")
        profile_description = request.form.get("profile_description")
        password = request.form.get("password") or "password"
        caregiving_type = request.form["caregiving_type"]
        hourly_rate = request.form["hourly_rate"]
        gender = request.form.get("gender")
        photo = request.form.get("photo")

        u = User(email=email, given_name=given_name, surname=surname, city=city, phone_number=phone_number, profile_description=profile_description, password=password)
        session.add(u)
        session.commit()  
        c = Caregiver(caregiver_user_id=u.user_id, photo=photo, gender=gender, caregiving_type=caregiving_type, hourly_rate=hourly_rate)
        session.add(c)
        session.commit()
        flash("Caregiver created")
        return redirect(url_for("caregivers_list"))
    return render_template("caregivers/form.html")

# --- Members list & create ---
@app.route("/members")
def members_list():
    session = Session()
    rows = session.query(Member).join(User, Member.member_user_id==User.user_id).all()
    return render_template("members/list.html", members=rows)

@app.route("/members/new", methods=["GET","POST"])
def members_new():
    session = Session()
    if request.method == "POST":
        email = request.form["email"]
        given_name = request.form["given_name"]
        surname = request.form["surname"]
        city = request.form.get("city")
        phone_number = request.form.get("phone_number")
        profile_description = request.form.get("profile_description")
        password = request.form["password"] or "password"
        house_rules = request.form.get("house_rules")
        dependent_description = request.form.get("dependent_description")
        street = request.form.get("street")
        house_number = request.form.get("house_number")
        town = request.form.get("town")

        u = User(email=email, given_name=given_name, surname=surname, city=city, phone_number=phone_number, profile_description=profile_description, password=password)
        session.add(u)
        session.commit()
        m = Member(member_user_id=u.user_id, house_rules=house_rules, dependent_description=dependent_description)
        session.add(m)
        session.commit()
        if street:
            addr = Address(member_user_id=m.member_user_id, house_number=house_number, street=street, town=town)
            session.add(addr)
            session.commit()
        flash("Member created")
        return redirect(url_for("members_list"))
    return render_template("members/form.html")

# --- Jobs list & create ---
@app.route("/jobs")
def jobs_list():
    session = Session()
    rows = session.query(Job).order_by(Job.date_posted.desc()).all()
    return render_template("jobs/list.html", jobs=rows)

@app.route("/jobs/new", methods=["GET","POST"])
def jobs_new():
    session = Session()
    if request.method == "POST":
        member_user_id = int(request.form["member_user_id"])
        required_caregiving_type = request.form["required_caregiving_type"]
        other_requirements = request.form.get("other_requirements")
        date_posted = request.form.get("date_posted") 
        j = Job(member_user_id=member_user_id, required_caregiving_type=required_caregiving_type, other_requirements=other_requirements, date_posted=date_posted)
        session.add(j)
        session.commit()
        flash("Job created")
        return redirect(url_for("jobs_list"))
    members = session.query(Member).all()
    return render_template("jobs/form.html", members=members)

# --- Job applications (create) ---
@app.route("/job_applications/new", methods=["GET","POST"])
def job_applications_new():
    session = Session()
    if request.method == "POST":
        caregiver_user_id = int(request.form["caregiver_user_id"])
        job_id = int(request.form["job_id"])
        from datetime import date
        ja = JobApplication(caregiver_user_id=caregiver_user_id, job_id=job_id, date_applied=date.today())
        session.add(ja)
        session.commit()
        flash("Application created")
        return redirect(url_for("jobs_list"))
    caregivers = session.query(Caregiver).all()
    jobs = session.query(Job).all()
    return render_template("job_applications/form.html", caregivers=caregivers, jobs=jobs)

# --- Appointments (list + create) ---
@app.route("/appointments")
def appointments_list():
    session = Session()
    rows = session.query(Appointment).order_by(Appointment.appointment_date.desc()).all()
    return render_template("appointments/list.html", appointments=rows)

@app.route("/appointments/new", methods=["GET","POST"])
def appointments_new():
    session = Session()
    if request.method == "POST":
        caregiver_user_id = int(request.form["caregiver_user_id"])
        member_user_id = int(request.form["member_user_id"])
        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]
        work_hours = request.form["work_hours"]
        status = request.form["status"]
        a = Appointment(caregiver_user_id=caregiver_user_id, member_user_id=member_user_id, appointment_date=appointment_date, appointment_time=appointment_time, work_hours=work_hours, status=status)
        session.add(a)
        session.commit()
        flash("Appointment created")
        return redirect(url_for("appointments_list"))
    caregivers = session.query(Caregiver).all()
    members = session.query(Member).all()
    return render_template("appointments/form.html", caregivers=caregivers, members=members)

if __name__ == "__main__":
    print("Starting Flask app...")
    print("Database URL:", DATABASE_URL)
    app.run(debug=True, port=5000)