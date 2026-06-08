from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "faculty" or "hod"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    risk_probability = Column(Float, nullable=False)
    prediction = Column(String, nullable=False)  # "AT-RISK" or "SAFE"
    risk_factors = Column(JSON)  # Stores list of risk factors
    uploaded_by = Column(String)  # Faculty email
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StudentData(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"))
    school = Column(String)
    sex = Column(String)
    age = Column(Integer)
    address = Column(String)
    famsize = Column(String)
    Pstatus = Column(String)
    Medu = Column(Integer)
    Fedu = Column(Integer)
    Mjob = Column(String)
    Fjob = Column(String)
    reason = Column(String)
    guardian = Column(String)
    traveltime = Column(Integer)
    studytime = Column(Integer)
    failures = Column(Integer)
    schoolsup = Column(String)
    famsup = Column(String)
    paid = Column(String)
    activities = Column(String)
    nursery = Column(String)
    higher = Column(String)
    internet = Column(String)
    romantic = Column(String)
    famrel = Column(Integer)
    freetime = Column(Integer)
    goout = Column(Integer)
    Dalc = Column(Integer)
    Walc = Column(Integer)
    health = Column(Integer)
    absences = Column(Integer)
    G1 = Column(Integer)
    G2 = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())