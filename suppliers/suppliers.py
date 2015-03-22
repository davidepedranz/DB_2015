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
SUPPLIERS_NUMBER = 46
PARTS_NUMBER = 498
CATALOG_NUMBER = 1000 

# random fields
s_names = ['Ale', 'Pietro', 'Pippo', 'Gino', 'Alice', 'Francesca', 'Geltrude', 'Mario', 'Fede', 'Alex', 'Titti']
s_second_names = ['Rossi', 'Bianchi', 'Blu', 'Cognome', 'Random', 'Robot', 'Chess', 'Sacchi', 'Spider', 'Monello']
s_addresses = ['Via Rossi', 'Viale Verona', 'Sulla montagna', 'Somewhere', 'Ocean', 'Everest', 'On the way']
p_names = ['books', 'chips', 'objects', 'videos', 'things', 'cose', 'cars', 'universities', 'computers', 'phones']
p_colors = ['white', 'black', 'green', 'red', 'yellow', 'blue', 'violet', 'orange', 'purple', 'grey', 'light blue', 'pink']
c_costs_small = [12, 34, 56, 77, 89, 95]
c_costs_big = [102, 152, 166, 177, 189, 200]
c_costs = c_costs_small + c_costs_big

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

## insert a supplier who supply every part
supplier_all_parts = Suppliers(sname='All part', address='Address X')
session.add(supplier_all_parts)
suppliers_list.append(supplier_all_parts)

## insert a supplier who supply every red part
supplier_all_red = Suppliers(sname='All red', address='Address X')
session.add(supplier_all_red)
suppliers_list.append(supplier_all_red)

## insert a supplier who supply every green part
supplier_all_green = Suppliers(sname='All green', address='Address X')
session.add(supplier_all_green)
suppliers_list.append(supplier_all_green)

## insert a supplier who supply every green and red part
supplier_all_red_and_green = Suppliers(sname='All red and green', address='Address X')
session.add(supplier_all_red_and_green)
suppliers_list.append(supplier_all_red_and_green)

## insert a part supplied by every supplier
part_all_suppliers = Parts(pname='Every supplier', color='special')
session.add(part_all_suppliers)
parts_list.append(part_all_suppliers)

## insert a part supplied by every supplier at less than 100
part_all_suppliers_less_100 = Parts(pname='Every supplier less 100', color='special')
session.add(part_all_suppliers_less_100)
parts_list.append(part_all_suppliers_less_100)

# supply every part
for pp in parts_list:
	if pp != part_all_suppliers and pp != part_all_suppliers_less_100:

		c = Catalog(cost=random.choice(c_costs), supplier=supplier_all_parts, part=pp)
		session.add(c)

		if pp.color == 'red':
			c = Catalog(cost=random.choice(c_costs), supplier=supplier_all_red, part=pp)
			session.add(c)
			c1 = Catalog(cost=random.choice(c_costs), supplier=supplier_all_red_and_green, part=pp)
			session.add(c1)

		if pp.color == 'green':
			c = Catalog(cost=random.choice(c_costs), supplier=supplier_all_green, part=pp)
			session.add(c)
			c1 = Catalog(cost=random.choice(c_costs), supplier=supplier_all_red_and_green, part=pp)
			session.add(c1)

# supplied by every supplier
for ss in suppliers_list:
	c = Catalog(cost=random.choice(c_costs), supplier=ss, part=part_all_suppliers)
	session.add(c)

	c1 = Catalog(cost=random.choice(c_costs_small), supplier=ss, part=part_all_suppliers_less_100)
	session.add(c1)

# write to db
session.commit()

#########################################################################

print("Random DB generated! =D")
