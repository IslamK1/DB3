from sqlalchemy import (
    Column, Integer, String, Text, Date, Time, Numeric,
    ForeignKey, CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "USER"
    __table_args__ = {"quote": True}  

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    given_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    city = Column(String(100))
    phone_number = Column(String(30))
    profile_description = Column(Text)
    password = Column(String(255), nullable=False)

    caregiver = relationship("Caregiver", back_populates="user", uselist=False, cascade="all, delete")
    member = relationship("Member", back_populates="user", uselist=False, cascade="all, delete")

class Caregiver(Base):
    __tablename__ = "caregiver"

    caregiver_user_id = Column(Integer, ForeignKey("USER.user_id", ondelete="CASCADE"), primary_key=True)
    photo = Column(String(255))
    gender = Column(String(10))
    caregiving_type = Column(String(30), nullable=False)
    hourly_rate = Column(Numeric(8,2), nullable=False)

    user = relationship("User", back_populates="caregiver")
    applications = relationship("JobApplication", back_populates="caregiver", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="caregiver", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("caregiving_type IN ('babysitter','elderly','playmate')"),
    )

class Member(Base):
    __tablename__ = "member"

    member_user_id = Column(Integer, ForeignKey("USER.user_id", ondelete="CASCADE"), primary_key=True)
    house_rules = Column(Text)
    dependent_description = Column(Text)

    user = relationship("User", back_populates="member")
    address = relationship("Address", uselist=False, back_populates="member", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="member", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="member", cascade="all, delete-orphan")

class Address(Base):
    __tablename__ = "address"

    member_user_id = Column(Integer, ForeignKey("member.member_user_id", ondelete="CASCADE"), primary_key=True)
    house_number = Column(String(50))
    street = Column(String(200))
    town = Column(String(100))

    member = relationship("Member", back_populates="address")

class Job(Base):
    __tablename__ = "job"

    job_id = Column(Integer, primary_key=True, autoincrement=True)
    member_user_id = Column(Integer, ForeignKey("member.member_user_id", ondelete="CASCADE"))
    required_caregiving_type = Column(String(30), nullable=False)
    other_requirements = Column(Text)
    date_posted = Column(Date, nullable=False)

    member = relationship("Member", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("required_caregiving_type IN ('babysitter','elderly','playmate')"),
    )

class JobApplication(Base):
    __tablename__ = "job_application"

    caregiver_user_id = Column(Integer, ForeignKey("caregiver.caregiver_user_id", ondelete="CASCADE"), primary_key=True)
    job_id = Column(Integer, ForeignKey("job.job_id", ondelete="CASCADE"), primary_key=True)
    date_applied = Column(Date, nullable=False)

    caregiver = relationship("Caregiver", back_populates="applications")
    job = relationship("Job", back_populates="applications")

class Appointment(Base):
    __tablename__ = "appointment"

    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    caregiver_user_id = Column(Integer, ForeignKey("caregiver.caregiver_user_id", ondelete="CASCADE"))
    member_user_id = Column(Integer, ForeignKey("member.member_user_id", ondelete="CASCADE"))
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    work_hours = Column(Numeric(5,2), nullable=False)
    status = Column(String(20), nullable=False)

    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")

    __table_args__ = (
        CheckConstraint("status IN ('pending','accepted','declined')"),
    )
