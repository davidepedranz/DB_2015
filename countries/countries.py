#!/usr/bin/python3

import os
import random
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DB name
DB_NAME = 'countries.sqlite'

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

class Country(Base):
	__tablename__ = "countries"

	code = Column(String(2), primary_key = True)
	name = Column(String(80), nullable = False)
	capital = Column(Integer)
	area = Column(Integer)

class Population(Base):
	__tablename__ = "populations"

	country = Column(String(2), ForeignKey('countries.code'), primary_key = True)
	population = Column(Integer)
	children = Column(Float)
	adult = Column(Float)
	birth_rate = Column(Float)
	death_rate = Column(Float)
	sex_ratio = Column(Float)

	country_obj = relationship(Country)

class Economy(Base):
	__tablename__ = "economies"

	country = Column(String(2), ForeignKey('countries.code'), primary_key = True)
	gdp = Column(Float)
	inflation = Column(Float)
	military = Column(Float)
	poverty_rate = Column(Float)

	country_obj = relationship(Country)

class Language(Base):
	__tablename__ = "languages"

	code = Column(String(2), ForeignKey('countries.code'), primary_key = True)
	language = Column(String(30), primary_key = True)
	percentage = Column(Float)

	country_obj = relationship(Country)

Base.metadata.create_all(engine)

#########################################################################


#########################################################################
# fill DB
#########################################################################

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# parameters
MAX_LANGUAGES = 3

# countries
countries = [('Belgique', 'BE'), ('Bulgaria', 'BG'), ('Czech Republic', 'CZ'), ('Denmark', 'DK'), \
			 ('Germany', 'DE'), ('Estonia', 'EE'), ('Ireland', 'IE'), ('Greece', 'EL'), ('Spain', 'ES'), \
			 ('France', 'FR'), ('Croatia', 'HR'), ('Italy', 'IT'), ('Cyprus', 'CY'), ('Latvia', 'LV'), \
			 ('Lithuania', 'LT'), ('Luxembourg', 'LU'), ('Hungary	Hungary', 'HU'), ('Malta', 'MT'), \
			 ('Netherlands', 'NL'), ('Austria', 'AT'), ('Poland', 'PL'), ('Portugal', 'PT'), ('Romania', 'RO'), \
			 ('Slovenia', 'SI'), ('Slovakia', 'SK'), ('Finland', 'FI'), ('Sweden', 'SE'), ('United Kingdom', 'UK')]
languages = ['Italian', 'German', 'English', 'Danish', 'Polish', 'French', 'Spanish']

numbers = range(2000)
percentages = []
for p in range(1000):
	percentages.append(p / 10)

# insert data
for cc in countries:
	
	# country
	c = Country(code=cc[0], name=cc[1], capital=random.choice(numbers), area=random.choice(numbers))
	session.add(c)

	# population
	children = random.choice(percentages)
	adult = 100 - children
	p = Population(country_obj=c, population=random.choice(numbers), children=children, adult=adult, \
		birth_rate=random.choice(percentages), death_rate=random.choice(percentages), sex_ratio=random.choice(percentages))
	session.add(p)

	# economy
	e = Economy(country_obj=c, gdp=random.choice(numbers), inflation=random.choice(percentages), \
		military=random.choice(percentages), poverty_rate=random.choice(percentages))
	session.add(e)

	# languages
	lang = list(languages)
	for i in range(random.randint(0, MAX_LANGUAGES)):
		current_lang = random.choice(lang)
		lang.remove(current_lang)
		l = Language(country_obj=c, language=current_lang, percentage=random.choice(percentages))
		session.add(l)

# write to db
session.commit()

#########################################################################

print("Random DB generated! =D")
