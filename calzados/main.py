import numpy as np
import time

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


def read_db():
    Session = sessionmaker(bind=engine)
    session = Session()
    data = session.query(Ventas).all()

    paises = []
    generos = []
    talles = []
    precios = []

    for venta in data:        
        paises.append(venta.pais)
        generos.append(venta.genero)
        talles.append(venta.talle)
        precios.append(float(venta.precio.replace("$", "")))

    paises = np.array(paises)
    generos = np.array(generos)
    talles = np.array(talles)
    precios = np.array(precios)
    
    session.close()

    return paises, generos, talles, precios


def obtener_paises_unicos(paises):
    paises_unicos = np.unique(paises)
    return paises_unicos


def obtener_ventas_por_pais(paises_objetivo, paises, precios):
    # Opcion utilizando numpy mask
    total_ventas= {}
    for pais in paises_objetivo:
        mask = paises == pais
        total_ventas[pais] = sum(precios[mask])
    
    return total_ventas
    

def obtener_calzado_mas_vendido_por_pais(paises_objetivo, paises, talles):
    # Opcion utilizando numpy mask + unique con return_counts
    resultado = {}
    for pais in paises_objetivo:
        mask = paises == pais

        # Cantidad de ventas de cada tamaño de cada calzado
        # en ese pais (mask)
        talles_pais, count = np.unique(talles[mask], return_counts=True)

        # Indice de calzado más vendido
        imax = np.argmax(count)

        # Tamaño de calzado más vendido en ese pais
        resultado[pais] = talles_pais[imax]

    # Opcion utilizando python sin numpy
    resultado = {}
    for pais in paises_objetivo:
        
        # Primero armar una lista de todos los tamaños de calzados
        # y cantidad de ventas de cada uno
        talles_pais = {}
        for c, s in zip(paises, talles):
            if c == pais:
                if s not in talles_pais:
                    talles_pais[s] = 0
                talles_pais[s] += 1

        # Tamaño de calzado más vendido en ese pais
        talles_max = max(talles_pais, key=talles_pais.get)
        resultado[pais] = talles_max

    return resultado


def obtener_ventas_por_genero_pais(paises_objetivo, genero_objetivo, paises, generos):
    # Opcion utilizando numpy mask
    total_ventas_genero = {}
    for i, pais in enumerate(paises):
        if pais not in paises_objetivo:
            continue

        if pais not in total_ventas_genero:
            total_ventas_genero[pais] = 0
        if generos[i] == genero_objetivo:
            total_ventas_genero[pais] += 1
    
    # Opcion utilizando python sin numpy
    total_ventas_genero = {}
    for pais in paises_objetivo:
        mask = paises == pais
        total_ventas_genero[pais] = sum(generos[mask] == genero_objetivo)
   
    return total_ventas_genero


if __name__ == "__main__":
    paises, generos, talles, precios = read_db()

    paises_objetivo = obtener_paises_unicos(paises)
    print(paises_objetivo)

    ventas = obtener_ventas_por_pais(paises_objetivo, paises, precios)
    print(ventas)

    calzados_mas_vendidos = obtener_calzado_mas_vendido_por_pais(paises_objetivo, paises, talles)
    print(calzados_mas_vendidos)

    ventas_genero = obtener_ventas_por_genero_pais(paises_objetivo, "Female", paises, generos)
    print(ventas_genero)
