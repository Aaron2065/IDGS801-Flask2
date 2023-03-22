#se quiere que la pagina sea invocada
from flask import Flask, render_template
from flask import request
from flask import make_response
from flask import flash
from flask_wtf import CSRFProtect

import forms
app=Flask(__name__)

app.config['SECRET_KEY'] = 'esta es tu clave encriptada'
csrf = CSRFProtect()

@app.route("/calcular", methods=['GET'])
def calcular():
    return render_template("calcular.html")

@app.route("/cookie", methods = ['GET', 'POST'])
def cookie():
    reg_user = forms.LoginForm(request.form)
    response = make_response(render_template('cookie.html', form = reg_user))
    if request.method == 'POST' and reg_user.validate():
        user = reg_user.username.data
        pasw = reg_user.password.data
        datos = user + "@" + pasw
        succes_message = 'Bienvenido {}'.format(user)
        response.set_cookie('datos_user', datos)
        flash(succes_message)
    return response


@app.route('/Alumnos', methods=['GET', 'POST'])
def alumnos():
    reg_alum = forms.UserForm(request.form)
    mat = ''
    nom = ''
    if request.method == 'POST' and reg_alum.validate():
        mat = reg_alum.matricula.data
        nom = reg_alum.nombre.data
    return render_template('Alumnos.html', form = reg_alum, mat = mat, nom = nom)


@app.route('/Traductor', methods=['GET', 'POST'])
def diccionario():
    reg_language = forms.IdiomasForm(request.form)
    esp = ""
    eng = ""
    opc = ""
    bus = ""
    palabra = ""
    if request.method == 'POST':
        esp = reg_language.esp.data
        eng = reg_language.eng.data
        opc = reg_language.opc.data
        bus = reg_language.bus.data
        if esp != None and eng != None:
            add_dictionary(eng, esp)
        if opc != None and bus != None:
            palabra = search_dictionary(opc, bus)
    return render_template('traductor.html',form = reg_language, palabra = palabra)

def add_dictionary(eng, esp):
    file = open('palabras.txt','a')
    file.write(eng.lower())
    file.write("\n")
    file.write(esp.lower())
    file.write("\n")
    file.close()
    
def search_dictionary(opc, bus):
    file = open('palabras.txt','r')
    resultado = file.read()
    datos = resultado.split()
    i = 0
    palabra = ""
    if opc == "eng":
        for x in datos:
            if x == bus.lower():
                palabra = datos[i-1]
            if palabra == "":
                palabra = "La palabra aun no se ha agregado"
            i += 1
    else:
        for x in datos:
            if x == bus.lower():
                palabra = datos[i+1]
            if palabra == "":
                palabra = "La palabra aun no se ha agregado"
            i += 1
    return palabra

@app.route('/')
def formulario():
    return render_template('CajasDinamicas.html')
           
@app.route("/Caja", methods = ['GET', 'POST'])
def caja():
    if request.method == 'POST':
        campoN = int(request.form.get('txtCampoN'))
        return render_template('AnalisisDeCajas.html', campoN = campoN)

@app.route("/cajasDinamicas",methods=["POST"])
def cajas():
    numeroString = request.form.getlist('txtNumber')
    numeroInt = list(map(int, numeroString))
    maximo = int(numeroInt[0])
    for a in numeroInt:
        if int(maximo) > int(a):
            maximo = maximo
        else:
            maximo=a
    menor = int(numeroInt[0])
    for m in numeroInt:
        if int(menor) < int(m):
            menor = menor
        else:
            menor=m
    calculo = sum(numeroInt) / len(numeroInt)
    results = []
    results2 = []
    for number in numeroInt:
        resultado = numeroInt.count(number)
        num = resultado;
        results.append("{}".format(number))
        results2.append("aparece {} veces".format(resultado))
    return render_template('resultado.html', maximo = maximo, menor = menor, calculo = calculo, results = results, results2 = results2)

if __name__ == "__main__":
    app.run(debug=True,port=3000)
