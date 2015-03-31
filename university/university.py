#!/usr/bin/python3

import os
import random
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DB name
DB_NAME = 'university.sqlite'

# drop old DB if exists
if os.path.exists(DB_NAME):
	print("... Drop old DB ...")
	os.remove(DB_NAME)

# DB "connection"
Base = declarative_base()
engine = create_engine('sqlite:///' + DB_NAME)


#########################################################################
# DB definition
#########################################################################

class Student(Base):
	__tablename__ = "student"

	snum = Column(Integer, primary_key = True)
	sname = Column(String(80), nullable = False)
	major = Column(String(80))
	level = Column(String(2))
	age = Column(Integer)

class Faculty(Base):
	__tablename__ = "faculty"

	fid = Column(Integer, primary_key = True)
	fname = Column(String(80), nullable = False)
	deptid = Column(Integer)

class Class(Base):
	__tablename__ = "class"

	cname = Column(String(80), primary_key = True)
	meets_at = Column(String(8))
	room = Column(String(10))
	fid = Column(Integer, ForeignKey('faculty.fid'))

	faculty = relationship(Faculty)

class Enrolled(Base):
	__tablename__ = "enrolled"

	snum = Column(Integer, ForeignKey('student.snum'), primary_key = True)
	cname = Column(String(80), ForeignKey('class.cname'), primary_key = True)

	student = relationship(Student)
	class_obj = relationship(Class)

Base.metadata.create_all(engine)

#########################################################################


#########################################################################
# fill DB
#########################################################################

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# names
first_names = ['Ale', 'Pietro', 'Pippo', 'Gino', 'Alice', 'Francesca', 'Geltrude', 'Mario', 'Fede', 'Alex', 'Titti']
second_names = ['Rossi', 'Bianchi', 'Blu', 'Cognome', 'Random', 'Robot', 'Chess', 'Sacchi', 'Spider', 'Monello']

# courses
courses = ['History', 'DB', 'OS', 'English', 'Programming languages', 'HCI', 'Biology', 'Math', 'Physics', 'Chemistry']

# levels
levels = ['JR', 'SR']

def random_name():
	return random.choice(first_names) + " " + random.choice(second_names)

def random_age():
	return random.randint(10, 40)

def random_int():
	return random.randint(200, 300)

def random_room():
	return random.choice(['A', 'B', 'C']) + str(random.randint(1, 100))

def random_time():
	return str(random.randint(8, 18)) + ":" + str(random.randint(0, 59))

# parameters
STUDENTS = 50
FACULTIES = 10
CLASSES = 15
ENROLLED = 40

students_list = []
faculties_list = []
classes_list = []

# random students
for i in range(STUDENTS):
	s = Student(sname=random_name(), major=random.choice(courses), level=random.choice(levels), age=random_age())
	students_list.append(s)
	session.add(s)

# random faculties
for i in range(FACULTIES):
	f = Faculty(fname=random_name(), deptid=random_int())
	faculties_list.append(f)
	session.add(f)

# random classes
for i in range(CLASSES):
	c = Class(cname="Lesson_"+str(i), meets_at=random_time(), room=random_room(), faculty=random.choice(faculties_list))
	classes_list.append(c)
	session.add(c)

# possible enrolled tuples
cross = [(s, c) for s in students_list for c in classes_list]

# random enrolled
for i in range(ENROLLED):
	o = random.choice(cross)
	cross.remove(o)
	e = Enrolled(student=o[0], class_obj=o[1])
	session.add(e)

# write to db
session.commit()

#########################################################################

print("Random DB generated! =D")
