#!/bin/bash
#  \t = ################
# echo -e "\n${Cyan}${Color_Off}"

# Reset
Color_Off='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

writeText(){
	t="########"
	t2="################"
	taille=`echo $1 | wc -c`
	rep1=""
	rep2=""
	rep3=""
	for (( i = 0; i < $taille; i++ )); do
		rep1="${rep1}#"
	done
	for (( i = 0; i < 8; i++ )); do
		rep2="${rep2} "
	done
	for (( i = 0; i < 8*2+$taille-2; i++ )); do
		rep3="${rep3} "
	done
	echo -e "${2}"
	echo -e "\n${t}${rep1}${t}"
	echo -e "#${rep3}#"
	echo -e "${2}#${rep2}$1${rep2}#"
	echo -e "#${rep3}#"
	echo -e "${2}${t}${rep1}${t}"
	echo -e ${Color_Off}
}

pathadd() {
    if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
        PATH="${PATH:+"$PATH:"}$1"
    fi
}

pathadd "/usr/bin/python3"

writeText "Début de l'installation" $Cyan

writeText "Installation des pré-requis" $Cyan

sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt install php7.3
sudo apt-get install php-curl
sudo pip3 install -r requirements.txt

mkdir log

writeText "Création du service \"listen\"" $Cyan

SOURCEPATH=$(dirname "$0")            # relative
SOURCEPATH=$(cd "$SOURCEPATH"/.. && pwd)    # absolutized and normalized
JARDIN_BRUYERE_DIRECTORY=${SOURCEPATH}/Serveur
Directory_Listen=${JARDIN_BRUYERE_DIRECTORY}/listen
Directory_Api=${JARDIN_BRUYERE_DIRECTORY}/api
#==================================================================================================================
#             Creation du LISTEN
#==================================================================================================================
ChaineCaracteres="
[Unit]
# After=network.service
Description=Partie listen

[Service]
Type=simple
Environment=PYTHONUNBUFFERED=1
WorkingDirectory=${JARDIN_BRUYERE_DIRECTORY}
ExecStart=${JARDIN_BRUYERE_DIRECTORY}/listen.sh
User=root
StandardOutput=append:${JARDIN_BRUYERE_DIRECTORY}/log/listen_jardin.log
StandardError=append:${JARDIN_BRUYERE_DIRECTORY}/log/listen_jardin_err.log


[Install]
WantedBy=multi-user.target
# WantedBy=default.target
"
sudo echo -e "${ChaineCaracteres}"  > /etc/systemd/system/listen.service 
#==================================================================================================================
#             Creation d'API
#==================================================================================================================
writeText "Création du service \"api\"" $Cyan

ChaineCaracteres="
[Unit]
# After=network.service
Description=Partie API

[Service]
Type=simple
Environment=PYTHONUNBUFFERED=1
WorkingDirectory=${JARDIN_BRUYERE_DIRECTORY}
ExecStart=${JARDIN_BRUYERE_DIRECTORY}/app.sh
User=root
StandardOutput=append:${JARDIN_BRUYERE_DIRECTORY}/log/api_jardin.log
StandardError=append:${JARDIN_BRUYERE_DIRECTORY}/log/api_jardin_err.log

# User=do-user

[Install]
WantedBy=multi-user.target
# WantedBy=default.target
"
sudo echo -e "${ChaineCaracteres}" > /etc/systemd/system/api.service 
#==================================================================================================================
#             Creation du SITE
#==================================================================================================================
ChaineCaracteres="
[Unit]
# After=network.service
Description=Partie SITE

[Service]
Type=simple
WorkingDirectory=${JARDIN_BRUYERE_DIRECTORY}
ExecStart=${JARDIN_BRUYERE_DIRECTORY}/administration.sh
User=root
StandardOutput=append:${JARDIN_BRUYERE_DIRECTORY}/log/administration_jardin.log
StandardError=append:${JARDIN_BRUYERE_DIRECTORY}/log/administration_jardin_err.log


[Install]
WantedBy=multi-user.target
# WantedBy=default.target
"
sudo echo -e "${ChaineCaracteres}"  > /etc/systemd/system/administration.service 

sudo systemctl daemon-reload
sudo systemctl restart api.service
sudo systemctl restart listen.service
sudo systemctl restart administration.service

writeText "Création réalisée" $Cyan
writeText "Vérification de l'installation" $Cyan

writeText "Verification de \"api.service\"" $Cyan
sudo systemctl status api.service

writeText "Verification de \"listen.service\"" $Cyan
sudo systemctl status listen.service

writeText "Verification de \"administration.service\"" $Cyan
sudo systemctl status administration.service
