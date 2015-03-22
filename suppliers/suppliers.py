#!/usr/bin/python3

import os
import random
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DB name
DB_NAME = 'suppliers.sqlite'

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

class Suppliers(Base):
	__tablename__ = "suppliers"

	sid = Column(Integer, primary_key = True)
	sname = Column(String(80), nullable = False)
	address = Column(String(80))

class Parts(Base):
	__tablename__ = "parts"

	pid = Column(Integer, primary_key = True)
	pname = Column(String(80), nullable = False)
	color = Column(String(80))

class Catalog(Base):
	__tablename__ = "catalog"

	sid = Column(Integer, ForeignKey('suppliers.sid'), primary_key = True)
	pid = Column(Integer, ForeignKey('parts.pid'), primary_key = True)
	cost = Column(Float, nullable = False)

	supplier = relationship(Suppliers)
	part = relationship(Parts)

Base.metadata.create_all(engine)

#########################################################################


#########################################################################
# fill DB
#########################################################################

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# parameters
SUPPLIERS_NUMBER = 30
PARTS_NUMBER = 50
CATALOG_NUMBER = 60

# random fields
s_names = ['Ale', 'Pietro', 'Pippo', 'Gino', 'Alice', 'Francesca', 'Geltrude', 'Mario', 'Fede', 'Alex', 'Titti']
s_second_names = ['Rossi', 'Bianchi', 'Blu', 'Cognome', 'Random', 'Robot', 'Chess', 'Sacchi', 'Spider', 'Monello']
s_addresses = ['Via Rossi', 'Viale Verona', 'Sulla montagna', 'Somewhere', 'Ocean', 'Everest', 'On the way']
p_names = ['books', 'chips', 'objects', 'videos', 'things', 'cose', 'cars', 'universities', 'computers', 'phones']
p_colors = ['white', 'black', 'green', 'red', 'yellow', 'blue', 'violet', 'orange', 'purple', 'grey']
c_costs = [12, 34, 56, 101, 1, 23, 99, 22, 111, 77, 34, 17, 34]

# store elements -> to easily add catalog
suppliers_list = []
parts_list = []

# insert suppliers
for i in range(SUPPLIERS_NUMBER):
	# NB: sid added automatically
	name = random.choice(s_names) + ' ' + random.choice(s_second_names)
	address = random.choice(s_addresses) + ' ' + str(random.randint(1, 10))
	s = Suppliers(sname=name, address=address)
	session.add(s)
	suppliers_list.append(s)

# insert parts
for i in range(PARTS_NUMBER):
	# NB: pid added automatically
	p = Parts(pname=random.choice(p_names), color=random.choice(p_colors))
	session.add(p)
	parts_list.append(p)

# calculate tuples suppliers-parts
cross = [(s, p) for s in suppliers_list for p in parts_list]

# insert catalog
for i in range(CATALOG_NUMBER):
	# extract & remove couple (s, p) from cross
	couple = random.choice(cross)
	cross.remove(couple)

	c = Catalog(cost=random.choice(c_costs), supplier=couple[0], part=couple[1])
	session.add(c)

# write to db
session.commit()

#########################################################################

print("Random DB generated! =D")
