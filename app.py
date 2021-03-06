# -*- coding: utf-8 -*-
from flask_restful import reqparse
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import time, sqlite3, json, requests
from flask_cors import CORS
from flask import request
import pytest
from pkg_resources import parse_version

CEND = '\33[0m'
CBOLD = '\33[1m'
CITALIC = '\33[3m'
CURL = '\33[4m'
CBLINK = '\33[5m'
CBLINK2 = '\33[6m'
CSELECTED = '\33[7m'
CBLACK = '\33[30m'
CRED = '\33[31m'
CGREEN = '\33[32m'
CYELLOW = '\33[33m'
CBLUE = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE = '\33[36m'
CWHITE = '\33[37m'

app = Flask(__name__)
CORS(app)
METEO_API_KEY = "7070e352228b6beb3dd6e4e30da0baaa"


@app.route('/status', methods=['GET'])
def status():
    return "OK"


@app.route('/help', methods=['GET'])
def help():
    helper = []
    helper.append({"/api/nbCapteur": "Nombre de capteur"})
    helper.append({"/api/addStation": "Ajoute automatiquement une station"})
    helper.append({"/api/addType": "Ajoute automatiquement un type"})
    helper.append({"/api/deleteStation": "Supprime une station où son Id est passe en parametre"})
    helper.append({"/api/deleteType": "Supprime un type ou son Id est passé en parametre"})
    helper.append({"/api/listeTable": "Affiche la liste des tables"})
    helper.append({"/api/change/": "Modifie les valeurs d'une table ou les parametres sont passes en parametres"})
    helper.append({"/api/capteur": "Recuperes les contenus de tables par rapport aux parametres passes"})
    helper.append({"/api/meteo/": "Retourne la meteo local"})
    return jsonify(helper)


@app.route('/api/nbCapteur', methods=['GET'])
def nbCapteur():
    print(CGREEN + "Demande du nombre de capteur" + CEND)
    conn = sqlite3.connect('capteur.db')
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM Sensor;")
    listeTables = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(listeTables)


@app.route('/api/addStation', methods=['GET'])
def addStation():
    print(CGREEN + "Création d'une nouvelle station" + CEND)
    conn = sqlite3.connect('capteur.db')
    cur = conn.cursor()
    cur.execute("insert into Station (Name) values (\"Nouvelles station\");")
    conn.commit()
    cur.close()
    conn.close()
    return "ok"


@app.route('/api/addType', methods=['GET'])
def addType():
    print(CGREEN + "Création d'un nouveau type de capteur" + CEND)
    conn = sqlite3.connect('capteur.db')
    cur = conn.cursor()
    cur.execute("insert into SensorTypes (Unit) values (\"Nouvelle unite\");")
    conn.commit()
    cur.close()
    conn.close()
    return "ok"


@app.route('/api/deleteStation', methods=['GET'])
def deleteStation():
    num = int(request.args.get('num'))
    print(CGREEN + "Suppression de la station numéro " + str(num) + CEND)
    conn = sqlite3.connect('capteur.db')
    cur = conn.cursor()
    cur.execute("delete from Station where Id=" + str(num) + ";")
    conn.commit()
    cur.close()
    conn.close()
    return "ok"


@app.route('/api/deleteType', methods=['GET'])
def deleteType():
    num = int(request.args.get('num'))
    print(CGREEN + "Suppression du type numéro " + str(num) + CEND)
    conn = sqlite3.connect('capteur.db')
    cur = conn.cursor()
    cur.execute("delete from SensorTypes where Id=" + str(num) + ";")
    conn.commit()
    cur.close()
    conn.close()
    return "ok"


@app.route('/api/listeTable', methods=['GET'])
def listeTable():
    print(CGREEN + "Demande de la liste des tables disponibles" + CEND)
    conn = sqlite3.connect('capteur.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    listeTables = cur.fetchall()
    print(listeTables)
    del listeTables[1]
    cur.close()
    conn.close()
    return jsonify(listeTables)


@app.route('/api/change/', methods=['GET'])
def change():
    print(CGREEN + "Modification d'une table" + CEND)
    try:
        sensorid = int(request.args.get('sensorid'))
        sensorname = request.args.get('sensorname')
        column = request.args.get('column')
        table = request.args.get('table')
        print("sensorid " + str(sensorid) + " sensorname= " + sensorname + " column= " + column)
        conn = sqlite3.connect('capteur.db')  # Connexion à la DB
        cur = conn.cursor()
        requete = "update " + table + " set " + column + "=\"" + sensorname + "\" where Id=" + str(sensorid) + ";"
        print(requete)
        cur.execute(requete)
        conn.commit()
        return jsonify("ok")
    except sqlite3.Error as error:
        print("Erreur lors de la connexion à SQLite :", error)
    except TypeError as tp:
        print("Type error :", tp)
    return jsonify(None)


@app.route('/api/capteur', methods=['GET'])
def capteur():
    try:
        numTable = int(request.args.get('numTable'))
        if (numTable == 3):
            sensorid = int(request.args.get('sensorid'))
            print(CGREEN + "Demande des relevés du capteur numéro " + str(sensorid) + CEND)
            amount = int(request.args.get('amount'))
            startdate = request.args.get('startdate')
            enddate = request.args.get('enddate')
            print("{} {} {} {}".format(sensorid, amount, startdate, enddate))
        currentTimestamp = datetime.now()  # On récupère la date d'aujourd'hui
        date_dt = currentTimestamp.strftime(
            "%Y-%m-%d %H:%M:%S")  # strftime permet de forcer le format de la date et donc de supprimer les décimales des secondes
        conn = sqlite3.connect('capteur.db')  # Connexion à la DB
        cur = conn.cursor()  # initialisation d'un curseur pour la DB

        parser = reqparse.RequestParser()  # initialisation du parser
        parser.add_argument('time', required=False)  # ajout d'argument
        keys, values = zip(*parser.parse_args().items())  # On sépare la clé et la valeur

        if values[0] is None:  # s'il y a aucun parametre, on prend 4 comme valeur par default
            args = 4
        elif not (float(values[0]).is_integer()):
            raise TypeError('Arguments must be integers')
        else:
            args = int(values[0])

        timeLine = str((currentTimestamp - timedelta(weeks=args)).strftime(
            "%Y-%m-%d %H:%M:%S"))  # date d'aujourd'hui - nb semaines

        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        listeTables = cur.fetchall()  # On recupere toute les infos des tables

        del listeTables[1]
        key = []  # On initialise une liste vide
        dic = []  # On initialise une liste vide
        tables = [t[0] for t in listeTables]  # On garde que le nom de chaque table
        t = tables[numTable]
        condition = " "
        if t == "SensorReading":
            if (not (startdate is None)):
                print(datetime.fromtimestamp(int(startdate)))
                condition += " and DateAdded  >= \"" + str(datetime.fromtimestamp(int(startdate))) + "\" "
            if (not (enddate is None)):
                #         print(datetime.fromtimestamp(int(enddate)))
                condition += " and DateAdded  <= \"" + str(datetime.fromtimestamp(int(enddate))) + "\" "
            print("SELECT * FROM SensorReading WHERE SensorId  = " + str(sensorid) + condition + "order by DateAdded;");
            cur.execute(
                "SELECT * FROM SensorReading WHERE SensorId  = " + str(sensorid) + condition + "order by DateAdded;")
        elif t == "Sensor":
            cur.execute("SELECT * FROM Sensor WHERE DateAdded ;")
        else:
            cur.execute("SELECT * FROM " + t)  # On recupere toutes les donnees d'un table

        names = ([description[0] for description in cur.description])  # On recupere le nom des colonnes de la table
        res = cur.fetchall()  # On lance la requete SQL a la base de donnee
        for r in res:
            dic.append(dict(zip(names, r)))  # On passe sous forme de dictionnaire les donnees avec leurs clefs
        key.append({t: dic})  # On incremente la liste des donnees avec le nom de leur table
        dic = []  # On reset la liste des donnees

        #  del key[1]                                      #On supprime la deuxieme case du tableau qui contient des informations sur la bdd que nous n'avons pas besoin
        # ser = json.dumps(dic) #On serialise la liste en json
        data = {'status': 'ok', 'data': key}
        cur.close()
        conn.close()
        return jsonify(data)
    except sqlite3.Error as error:
        print("Erreur lors de la connexion à SQLite :", error)
    except TypeError as tp:
        print("Type error :", tp)
    return jsonify(None)


@app.route('/api/meteo/', methods=['GET'])
def meteo():
    print(CGREEN + "Demande du nombre de capteur" + CEND)
    parser = reqparse.RequestParser()  # initialisation du parser
    parser.add_argument('place', required=False)  # ajout d'argument
    keys, values = zip(*parser.parse_args().items())  # On sépare la clé et la valeur

    if values[0] is None:
        place = "Paris"  # lieu par default
    else:
        place = values[0]  # on garde la première valeur, qui correspond à la ville donnée en paramètre

    if METEO_API_KEY is None:
        # URL de test :
        METEO_API_URL = "https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx"
    else:
        # URL avec clé :
        METEO_API_URL = "https://api.openweathermap.org/data/2.5/forecast?q=" + place + "&appid=" + METEO_API_KEY

    response = requests.get(METEO_API_URL)
    content = json.loads(response.content.decode('utf-8'))

    if response.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'La requête à l\'API météo n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(
                content['message'])
        }), 500

    data = []  # On initialise une liste vide
    for prev in content["list"]:
        date = prev['dt_txt']
        temperature = prev['main']['temp'] - 273.15  # Conversion de Kelvin en °c
        temperature = round(temperature, 2)  # On arrondi la valeur à 2 chiffres après la virgule
        weather = prev['weather'][0]['main']  # On récupère le temps dans weather
        data.append([place, date, temperature, weather])

    return jsonify({
        'status': 'ok',
        'data': data
    })


def start():
    app.run(host='0.0.0.0', port=5001, debug=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)


@pytest.fixture(scope='session')
def test_request_example():
    assert 1 == 1
