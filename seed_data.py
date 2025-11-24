import os
from datetime import date, timedelta, time
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Caregiver, Member, Address, Job, JobApplication, Appointment

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:12345678@localhost:5432/caregiver_platform")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def seed():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    # USERS 
    users = [
        User(email='alex.care@example.com', given_name='Alex', surname='Care', city='Astana', phone_number='+77001110001', profile_description='Experienced babysitter', password='pass1'),
        User(email='bella.care@example.com', given_name='Bella', surname='Khan', city='Almaty', phone_number='+77001110002', profile_description='Loves kids and arts', password='pass2'),
        User(email='charlie.care@example.com', given_name='Charlie', surname='Smith', city='Astana', phone_number='+77001110003', profile_description='Elderly care specialist', password='pass3'),
        User(email='diana.care@example.com', given_name='Diana', surname='Lee', city='Shymkent', phone_number='+77001110004', profile_description='Playmate with sports background', password='pass4'),
        User(email='evan.care@example.com', given_name='Evan', surname='Brown', city='Astana', phone_number='+77001110005', profile_description='Part-time sitter', password='pass5'),
        User(email='fatima.care@example.com', given_name='Fatima', surname='Ali', city='Almaty', phone_number='+77001110006', profile_description='Senior caregiver', password='pass6'),
        User(email='george.care@example.com', given_name='George', surname='Ibrahim', city='Astana', phone_number='+77001110007', profile_description='Soft-spoken babysitter', password='pass7'),
        User(email='hannah.care@example.com', given_name='Hannah', surname='Ng', city='Aktobe', phone_number='+77001110008', profile_description='Creative playmate', password='pass8'),
        User(email='ivan.care@example.com', given_name='Ivan', surname='Petrov', city='Astana', phone_number='+77001110009', profile_description='Experienced with elderly dementia', password='pass9'),
        User(email='julia.care@example.com', given_name='Julia', surname='Moroz', city='Almaty', phone_number='+77001110010', profile_description='Weekend babysitter', password='pass10'),
        # members
        User(email='arman.armanov@example.com', given_name='Arman', surname='Armanov', city='Astana', phone_number='+77001234567', profile_description='Member needing care support', password='mypass1'),
        User(email='amina.aminova@example.com', given_name='Amina', surname='Aminova', city='Astana', phone_number='+77002223333', profile_description='Family with elderly parent', password='mypass2'),
        User(email='bekzat.member@example.com', given_name='Bekzat', surname='Zholdas', city='Almaty', phone_number='+77003334444', profile_description='Looking for babysitter', password='mypass3'),
        User(email='gulnar.member@example.com', given_name='Gulnar', surname='Sadykova', city='Astana', phone_number='+77004445555', profile_description='Need playmate for child', password='mypass4'),
        User(email='nursultan.member@example.com', given_name='Nursultan', surname='Mukhtar', city='Karaganda', phone_number='+77005556666', profile_description='Elderly care needed', password='mypass5'),
        User(email='olga.member@example.com', given_name='Olga', surname='Kareva', city='Astana', phone_number='+77006667777', profile_description='Need weekend sitter', password='mypass6'),
        User(email='paul.member@example.com', given_name='Paul', surname='Sokolov', city='Almaty', phone_number='+77007778888', profile_description='Looking for flexible hours', password='mypass7'),
        User(email='rina.member@example.com', given_name='Rina', surname='Tokayeva', city='Astana', phone_number='+77008889999', profile_description='Has allergies', password='mypass8'),
        User(email='sami.member@example.com', given_name='Sami', surname='Kassym', city='Shymkent', phone_number='+77009990011', profile_description='Requires experienced caregiver', password='mypass9'),
        User(email='tara.member@example.com', given_name='Tara', surname='Orlova', city='Astana', phone_number='+77001001010', profile_description='Prefers soft-spoken caregivers', password='mypass10'),
        User(email='umar.member@example.com', given_name='Umar', surname='Aitbay', city='Astana', phone_number='+77002002020', profile_description='Lives on Kabanbay Batyr street', password='mypass11'),
        User(email='vina.member@example.com', given_name='Vina', surname='Sabitova', city='Astana', phone_number='+77003003030', profile_description='Lives on Kabanbay Batyr street', password='mypass12'),
    ]

    session.add_all(users)
    session.commit()

    users_db = session.query(User).order_by(User.user_id).all()

    caregivers = [
        Caregiver(caregiver_user_id=users_db[i].user_id,
                  photo='/photos/x.jpg', gender='M',
                  caregiving_type=['babysitter','babysitter','elderly','playmate','babysitter','elderly','babysitter','playmate','elderly','babysitter'][i],
                  hourly_rate=[8.5,12,15,9,7.5,11,10.5,9.5,8,14][i])
        for i in range(10)
    ]

    session.add_all(caregivers)
    session.commit()

    members = [
        Member(member_user_id=users_db[i].user_id,
               house_rules="No pets.",
               dependent_description="Sample")
        for i in range(10, 22)
    ]

   
    members[0].house_rules = "No pets. No smoking."
    members[0].dependent_description = "Elderly father needs care"
    members[1].house_rules = "No pets. Quiet environment."
    members[1].dependent_description = "Elderly mother with mobility issues"

    session.add_all(members)
    session.commit()

    #ADDRESSES
    addrs = [
        Address(member_user_id=users_db[10].user_id, house_number='12A', street='Kabanbay Batyr', town='Astana'),
        Address(member_user_id=users_db[11].user_id, house_number='45', street='Abylay Khan', town='Astana'),
        Address(member_user_id=users_db[12].user_id, house_number='7', street='Bogenbay Batyr', town='Almaty'),
        Address(member_user_id=users_db[13].user_id, house_number='88', street='Kabanbay Batyr', town='Astana'),
    ]
    
    
    more_addresses = [
        Address(member_user_id=users_db[14].user_id, house_number='25', street='Kabanbay Batyr', town='Astana'),
        Address(member_user_id=users_db[15].user_id, house_number='30', street='Kabanbay Batyr', town='Astana')
    ]
    addrs.extend(more_addresses)
    
    session.add_all(addrs)
    session.commit()

    #JOBS
    today = date.today()
    jobs = [
        Job(member_user_id=users_db[10].user_id, required_caregiving_type='babysitter', other_requirements='soft-spoken', date_posted=today),
        Job(member_user_id=users_db[11].user_id, required_caregiving_type='elderly', other_requirements='night shifts', date_posted=today),
        Job(member_user_id=users_db[12].user_id, required_caregiving_type='playmate', other_requirements='energetic', date_posted=today),
    ]
    
    more_jobs = [
        Job(member_user_id=users_db[13].user_id, required_caregiving_type='babysitter', 
            other_requirements='Looking for soft-spoken caregiver', date_posted=today),
        Job(member_user_id=users_db[14].user_id, required_caregiving_type='elderly', 
            other_requirements='Must be soft-spoken and patient', date_posted=today)
    ]
    jobs.extend(more_jobs)
    
    session.add_all(jobs)
    session.commit()

    
    job_applications = [
        JobApplication(caregiver_user_id=caregivers[0].caregiver_user_id, job_id=jobs[0].job_id, date_applied=today),
        JobApplication(caregiver_user_id=caregivers[1].caregiver_user_id, job_id=jobs[0].job_id, date_applied=today),
        JobApplication(caregiver_user_id=caregivers[2].caregiver_user_id, job_id=jobs[1].job_id, date_applied=today),
    ]
    session.add_all(job_applications)
    session.commit()

    
    appointments = [
        Appointment(caregiver_user_id=caregivers[0].caregiver_user_id, member_user_id=members[0].member_user_id,
                    appointment_date=date.today(), appointment_time=time(10,0), work_hours=4, status='accepted'),
        Appointment(caregiver_user_id=caregivers[1].caregiver_user_id, member_user_id=members[1].member_user_id,
                    appointment_date=date.today(), appointment_time=time(14,0), work_hours=3, status='accepted'),
        Appointment(caregiver_user_id=caregivers[2].caregiver_user_id, member_user_id=members[2].member_user_id,
                    appointment_date=date.today(), appointment_time=time(9,0), work_hours=5, status='accepted'),
    ]
    session.add_all(appointments)
    session.commit()

    session.close()
    print("Database seeded successfully with test data!")

if __name__ == "__main__":
    seed()