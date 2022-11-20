import os
import json
import random
import string
import requests
import time
from datetime import datetime

import traceback
from flask import Flask, request, jsonify, render_template, Response


# Crear el server Flask
app = Flask(__name__)


# Base de datos
from flask_sqlalchemy import SQLAlchemy

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

# Asociamos nuestro controlador de la base de datos con la aplicacion
db = SQLAlchemy()
db.init_app(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    titulo = db.Column(db.String(100))
    texto = db.Column(db.String(300))


# ------------ Views ----------------- #
@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/")
def blog():
    return render_template('blog.html')

# ---------------- API ------------------------
@app.route('/post', methods=['GET', 'POST'])
def post():
    try:
        if request.method == 'GET':
            username = request.args.get('username')
  
            posts = []
            for post in Post.query.filter_by(username=username).order_by(Post.id.desc()).limit(3):
                posts.append({"titulo": post.titulo, "texto": post.texto})
            return jsonify({"posts": posts})

        if request.method == 'POST':
            username = request.form['username']
            titulo = request.form['titulo']
            texto = request.form['texto']

            post = Post(username=username, titulo=titulo, texto=texto)
            # agregar post a la base de datos
            db.session.add(post)
            db.session.commit()

            return jsonify({"id": post.id, "titulo": post.titulo, "texto": post.texto})

    except Exception as e:
        print(e)
        print(jsonify({'trace': traceback.format_exc()}))
        return Response(status=401)


# Este método se ejecutará solo una vez
# la primera vez que ingresemos a un endpoint
@app.before_first_request
def before_first_request_func():
    # Crear aquí todas las bases de datos
    db.create_all()
    print("Base de datos generada")


if __name__ == '__main__':
    print('Inove@Server start!')

    # Lanzar server
    app.run(host="127.0.0.1", port=5000)