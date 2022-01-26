#créer un répertoire de travail
mkdir API
cd API

#installer sqlite3
sudo apt-get install sqlite3

#créer la db avec sqlite3
sqlite3 capteur.db < database.sql

#tester si la db est bien créé
sqlite3 capteur.db
SELECT name FROM sqlite_master WHERE type='table';

#Exemple de requetes possible 
#SELECT * FROM RelevesCapteurs;
#INSERT INTO RelevesCapteurs (`DateAjout`,`IdCapteur`,`Valeur`) VALUES('2021-10-01 00:00:00',1,12);

#quitter l'invite de commande sqlite3
.quit


#Installer Flask :
sudo apt install python3-pip
pip3 install flask flask-restful requests

#Sur un premier terminal, lancer l'application de l'API
export FLASK_APP=app.py
flask run --port 5000

#Sur un deuxième terminal, lancer l'application du listener
export FLASK_APP=listen.py
flask run --port 5050