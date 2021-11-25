from datetime import time
from re import I
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oprksofuzybgca:f0de8365b4ec44c860ffbcc5062c8ef293a98e7301ae77f51cabc2d87d5e24fe@ec2-52-86-193-24.compute-1.amazonaws.com:5432/dcu9mllmc34tni'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Notas(db.Model):
    __tablename__ ="notas"
    idNota = db.Column(db.Integer, primary_key = True)
    tituloNota = db.Column(db.String(80))
    cuerpoNota = db.Column(db.String(150))

    def __init__(self, tituloNota, cuerpoNota):
        self.tituloNota = tituloNota
        self.cuerpoNota = cuerpoNota

@app.route('/')
def index():
    nombre = "DIEGO"
    lista = ["DIEGO","JAIR ","IRVING"]
    return render_template("index.html", var = lista)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/crearnota", methods=['POST'])
def crearnota():
    campotitulo = request.form["campotitulo"]
    camponota = request.form["camponota"]
    print(campotitulo)
    print(camponota)
    notaNueva = Notas(tituloNota=campotitulo, cuerpoNota=camponota)
    db.session.add(notaNueva)
    db.session.commit()

    return render_template("index.html",titulo = campotitulo, nota = camponota)

@app.route("/leernotas")
def leernotas():
    consulta_notas = Notas.query.all()
    print(consulta_notas)
    for nota in consulta_notas:
        titulo = nota.tituloNota
        cuerpo = nota.cuerpoNota
        print(nota.tituloNota)
        print(nota.cuerpoNota)
    
    return render_template("list.html",consulta = consulta_notas)

@app.route("/eliminarnota/<id>")
def eliminar(id):
    nota = Notas.query.filter_by(idNota = int(id)).delete()
    db.session.commit()
    return leernotas()

@app.route("/modificar", methods=['POST'])
def modificarnota():
    idnota = request.form["idnota"]
    nuevoTitulo = request.form["campotitulo"]
    nuevocampo = request.form["camponota"]
    nota = Notas.query.filter_by(idNota=int(idnota)).first()
    nota.tituloNota = nuevoTitulo
    nota.cuerpoNota = nuevocampo
    db.session.commit()
    return leernotas()


@app.route("/editarnota/<ID>")
def editar(ID):
    nota = Notas.query.filter_by(idNota = int(ID)).first()
    print(nota)
    print(nota.tituloNota)
    print(nota.cuerpoNota)
    
    return render_template("modify.html", nota = nota)





if __name__ == "__main__":
    db.create_all()
    app.run()