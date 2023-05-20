import csv
import numpy as np
import time

with open("dataset.csv") as fi:
    data = list(csv.DictReader(fi))

country = []
gender = []
size = []
price = []

empty_col = ["gender", "size", "country"]

for i, row in enumerate(data):
    country.append(row["Country"])
    gender.append(row["Gender"])
    size.append(row["Size (US)"])
    price.append(float(row["SalePrice"].replace("$", "")))

print(i)

country = np.array(country)
gender = np.array(gender)
size = np.array(size)
price = np.array(price)

# Paises distintos
countries = np.unique(country, return_counts=True)[0]
print(countries)

# Calzado por pais
for country_name in countries:
    mask = country == country_name
    sizes, count = np.unique(size[mask], return_counts=True)
    imax = np.argmax(count)
    print(sizes[imax], count[imax])


t1 = time.time()
total_geneder = {}
for i, country_name in enumerate(country):
    if country_name not in countries:
        continue

    if country_name not in total_geneder:
        total_geneder[country_name] = 0
    if gender[i] == "Female":
        total_geneder[country_name] += 1
t2 = time.time()
print(total_geneder, t2-t1)

# Cantidad de ventas a mujeres por pais
t1 = time.time()
total_geneder = {}
for country_name in countries:
    mask = country == country_name
    total_geneder[country_name] = sum(gender[mask] == "Female")
t2 = time.time()
print(total_geneder, t2-t1)


# Total de ventas
total_sales = {}
for country_name in countries:
    mask = country == country_name
    total_sales[country_name] = sum(price[mask])
print(total_sales)


import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine("sqlite:///ventas_calzados.db")
base = declarative_base()

class Ventas(base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True)
    fecha = Column(String)
    producto_id = Column(Integer)
    pais = Column(String)
    genero = Column(String)
    talle = Column(String)
    precio = Column(String)

    def __repr__(self):
        return f"Venta: {self.id}"
    
base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

empty_idx = 0

for i, row in enumerate(data):
    date=row["Date"]
    product_id=row["ProductID"]
    country = row["Country"]
    gender = row["Gender"]
    size = row["Size (US)"]
    price = row["SalePrice"]

    if (i % 50) == 0:
        gender = "Unix"

    # if (i % 100) == 0:
    #     empty_idx += 1

    #     if empty_idx == 1:
    #         gender = ""    
    #     elif empty_idx == 2:
    #         size = ""    
    #     elif empty_idx == 3:
    #         country = ""    
    #     elif empty_idx == 4:
    #         date = ""
    #     else:
    #         empty_idx = 0

    venta = Ventas(
        fecha=date,
        producto_id=product_id,
        pais=country,
        genero=gender,
        talle=size,
        precio=price,
    )

    session.add(venta)

session.commit()