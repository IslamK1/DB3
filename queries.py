import os
from decimal import Decimal
from sqlalchemy import create_engine, text, func, case, update, delete
from sqlalchemy.orm import sessionmaker

from models import Base, User, Caregiver, Member, Address, Job, JobApplication, Appointment

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:12345678@localhost:5432/caregiver_platform")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def update_arman_phone():
    session = Session()
    u = session.query(User).filter(User.given_name=="Arman", User.surname=="Armanov").one_or_none()
    if u:
        u.phone_number = "+77773414141"
        session.commit()
    session.close()

def add_commission_to_caregivers():
    session = Session()
    stmt = update(Caregiver).values(
        hourly_rate = case(
            (Caregiver.hourly_rate < 10, Caregiver.hourly_rate + Decimal("0.30")),
            else_ = func.round(Caregiver.hourly_rate * Decimal("1.10"), 2)
        )
    )
    session.execute(stmt)
    session.commit()
    session.close()
    

def delete_jobs_by_amina():
    session = Session()
    u = session.query(User).filter(User.given_name=="Amina", User.surname=="Aminova").one_or_none()
    if u:
        session.query(Job).filter(Job.member_user_id==u.user_id).delete()
        session.commit()
    session.close()

def delete_members_on_kabanbay_batyr():
    session = Session()
    sub = session.query(Address.member_user_id).filter(Address.street.ilike("Kabanbay Batyr"))
    session.query(Member).filter(Member.member_user_id.in_(sub)).delete(synchronize_session=False)
    session.commit()
    session.close()

def accepted_appointments_names():
    session = Session()
    sql = text("""
        SELECT uc.given_name, uc.surname,
               um.given_name, um.surname,
               a.appointment_date, a.appointment_time, a.work_hours
        FROM appointment a
        JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
        JOIN "USER" uc ON uc.user_id = c.caregiver_user_id
        JOIN member m ON a.member_user_id = m.member_user_id
        JOIN "USER" um ON um.user_id = m.member_user_id
        WHERE a.status='accepted'
    """)
    rows = session.execute(sql).fetchall()
    session.close()
    return rows

def jobs_with_soft_spoken():
    session = Session()
    rows = session.query(Job.job_id).filter(
        Job.other_requirements.ilike("%soft-spoken%")
    ).all()
    session.close()
    return rows


def babysitter_work_hours():
    """
    Correct interpretation:
    List work hours for appointments where the caregiver's caregiving_type='babysitter'
    """
    session = Session()
    rows = session.query(Appointment.work_hours).\
        join(Caregiver, Appointment.caregiver_user_id == Caregiver.caregiver_user_id).\
        filter(Caregiver.caregiving_type == 'babysitter').all()
    session.close()
    return rows


def members_looking_elderly_astana_no_pets():
    """
    According to assignment:
    Members who:
      - live in Astana
      - have 'No pets' in house_rules
      - are looking for elderly care (in dependent_description)
    Job table is NOT involved.
    """
    session = Session()
    rows = session.query(
        User.given_name,
        User.surname,
        Member.house_rules
    ).join(Member, User.user_id == Member.member_user_id).\
        filter(
            User.city.ilike("Astana"),
            Member.house_rules.ilike("%No pets%"),
            Member.dependent_description.ilike("%elderly%")
        ).all()
    session.close()
    return rows


# Complex queries

def count_applicants_per_job():
    session = Session()
    rows = session.query(
        Job.job_id,
        func.count(JobApplication.caregiver_user_id).label("applicant_count")
    ).outerjoin(JobApplication, Job.job_id == JobApplication.job_id).\
        group_by(Job.job_id).\
        order_by(func.count(JobApplication.caregiver_user_id).desc()).all()

    session.close()
    return rows


def total_hours_by_caregiver_for_accepted():
    session = Session()
    rows = session.query(
        Caregiver.caregiver_user_id,
        User.given_name,
        User.surname,
        func.sum(Appointment.work_hours).label("total_hours")
    ).join(User, Caregiver.caregiver_user_id == User.user_id).\
        join(Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id).\
        filter(Appointment.status == "accepted").\
        group_by(Caregiver.caregiver_user_id, User.given_name, User.surname).\
        order_by(func.sum(Appointment.work_hours).desc()).all()

    session.close()
    return rows


def average_pay_of_caregivers():
    session = Session()
    rows = session.query(
        Caregiver.caregiver_user_id,
        User.given_name,
        User.surname,
        func.avg(Caregiver.hourly_rate * Appointment.work_hours).label("avg_pay")
    ).join(User, Caregiver.caregiver_user_id == User.user_id).\
        join(Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id).\
        filter(Appointment.status == 'accepted').\
        group_by(Caregiver.caregiver_user_id, User.given_name, User.surname).\
        order_by(func.avg(Caregiver.hourly_rate * Appointment.work_hours).desc()).all()

    session.close()
    return rows


def caregivers_earning_above_average():
    session = Session()

    subq = session.query(
        Caregiver.caregiver_user_id,
        func.avg(Caregiver.hourly_rate * Appointment.work_hours).label("avg_income")
    ).join(Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id).\
        filter(Appointment.status == "accepted").\
        group_by(Caregiver.caregiver_user_id).subquery()

    overall_avg = session.query(func.avg(subq.c.avg_income)).scalar()

    rows = session.query(
        subq.c.caregiver_user_id,
        subq.c.avg_income
    ).filter(subq.c.avg_income > overall_avg).\
        order_by(subq.c.avg_income.desc()).all()

    session.close()
    return rows, overall_avg


def total_cost_all_accepted():
    session = Session()

    rows = session.query(
        Caregiver.caregiver_user_id,
        User.given_name,
        User.surname,
        func.sum(Caregiver.hourly_rate * Appointment.work_hours).label("total_cost")
    ).join(User, Caregiver.caregiver_user_id == User.user_id).\
        join(Appointment, Appointment.caregiver_user_id == Caregiver.caregiver_user_id).\
        filter(Appointment.status == 'accepted').\
        group_by(Caregiver.caregiver_user_id, User.given_name, User.surname).\
        order_by(func.sum(Caregiver.hourly_rate * Appointment.work_hours).desc()).all()

    session.close()
    return rows



# View operations

def create_job_applicants_view():
    session = Session()

    session.execute(text("DROP VIEW IF EXISTS job_applicants_view CASCADE;"))

    session.execute(text("""
        CREATE VIEW job_applicants_view AS
        SELECT
          j.job_id,
          j.required_caregiving_type,
          j.other_requirements,
          j.date_posted,
          c.caregiver_user_id,
          u.given_name AS caregiver_first,
          u.surname AS caregiver_last,
          ja.date_applied
        FROM job j
        LEFT JOIN job_application ja ON j.job_id = ja.job_id
        LEFT JOIN caregiver c ON ja.caregiver_user_id = c.caregiver_user_id
        LEFT JOIN "USER" u ON c.caregiver_user_id = u.user_id;
    """))

    session.commit()
    session.close()


def fetch_job_applicants_view():
    session = Session()
    rows = session.execute(
        text("SELECT * FROM job_applicants_view ORDER BY job_id;")
    ).fetchall()
    session.close()
    return rows


#Testing

if __name__ == "__main__":
    print("PART 2 TESTING")

    print("\nUPDATE")
    update_arman_phone()
    add_commission_to_caregivers()

    print("\nDELETE")
    delete_jobs_by_amina()
    delete_members_on_kabanbay_batyr()

    print("\nSIMPLE QUERIES")
    print(accepted_appointments_names())
    print(jobs_with_soft_spoken())
    print(babysitter_work_hours())
    print(members_looking_elderly_astana_no_pets())

    print("\nCOMPLEX QUERIES")
    print(count_applicants_per_job())
    print(total_hours_by_caregiver_for_accepted())
    print(average_pay_of_caregivers())
    print(caregivers_earning_above_average())

    print("\nDERIVED ATTRIBUTE")
    print(total_cost_all_accepted())

    print("\nVIEW")
    create_job_applicants_view()
    print(fetch_job_applicants_view())
