
import numpy as np
import time

import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


base = declarative_base()
class Venta(base):
    __tablename__ = "venta"
    id = Column(Integer, primary_key=True)
    date = Column(String)
    product_id = Column(Integer)
    country = Column(String)
    gender = Column(String)
    size = Column(String)
    price = Column(String)

    def __repr__(self):
        return f"Venta: {self.id}"


def read_db(path):
    engine = sqlalchemy.create_engine(path)
    Session = sessionmaker(bind=engine)
    session = Session()
    data = session.query(Venta).all()

    country = []
    gender = []
    size = []
    price = []

    for venta in data:
        if (not venta.country or
            not venta.gender or
            not venta.size or
            not venta.price):
            continue
        
        country.append(venta.country)
        gender.append(venta.gender)
        size.append(venta.size)
        price.append(float(venta.price.replace("$", "")))

    country = np.array(country)
    gender = np.array(gender)
    size = np.array(size)
    price = np.array(price)

    return country, gender, size, price


def paises_unicos(country):
    countries = np.unique(country)
    return countries


def ventas_pais(countries, country, price):
    # Opcion utilizando numpy mask
    total_sales = {}
    for country_name in countries:
        mask = country == country_name
        total_sales[country_name] = sum(price[mask])
    
    return total_sales
    

def calzado_pais(countries, contry, size):
    # Opcion utilizando numpy mask + unique con return_counts
    resultado = {}
    for country_name in countries:
        mask = country == country_name

        # Cantidad de ventas de cada tamaño de cada calzado
        # en ese pais (mask)
        sizes, count = np.unique(size[mask], return_counts=True)

        # Indice de calzado más vendido
        imax = np.argmax(count)

        # Tamaño de calzado más vendido en ese pais
        resultado[country_name] = sizes[imax]

    # Opcion utilizando python sin numpy
    resultado = {}
    for country_name in countries:
        
        # Primero armar una lista de todos los tamaños de calzados
        # y cantidad de ventas de cada uno
        sizes = {}
        for c, s in zip(country, size):
            if c == country_name:
                if s not in sizes:
                    sizes[s] = 0
                sizes[s] += 1

        # Tamaño de calzado más vendido en ese pais
        size_max = max(sizes, key=sizes.get)
        resultado[country_name] = size_max

    return resultado


def ventas_genero_pais(countries, gender_target, country, gender):
    t1 = time.time()
    total_geneder = {}
    for i, country_name in enumerate(country):
        if country_name not in countries:
            continue

        if country_name not in total_geneder:
            total_geneder[country_name] = 0
        if gender[i] == gender_target:
            total_geneder[country_name] += 1
    
    t2 = time.time()
    #print("Tiempo algoritmo:", t2-t1)

    # Cantidad de ventas a mujeres por pais
    t1 = time.time()
    total_geneder = {}
    for country_name in countries:
        mask = country == country_name
        total_geneder[country_name] = sum(gender[mask] == gender_target)
    
    t2 = time.time()
    #print("Tiempo algoritmo:", t2-t1)
    
    return total_geneder


if __name__ == "__main__":
    country, gender, size, price = read_db("sqlite:///ventas_calzados.db")

    countries = paises_unicos(country)
    print(countries)

    ventas = ventas_pais(countries, country, price)
    print(ventas)

    calzados_mas_vendidos = calzado_pais(countries, country, size)
    print(calzados_mas_vendidos)

    ventas_genero = ventas_genero_pais(countries, "Female", country, gender)
    print(ventas_genero)
