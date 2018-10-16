#!/usr/bin/python
import os
import sys

def recupTemp (contenuFich) :
    # Supprimer la premiere ligne qui est inutile
    secondeLigne = contenuFich.split("\n")[1]
    temperatureData = secondeLigne.split(" ")[9]
    # Supprimer le "t="
    temperature = float(temperatureData[2:])
    # Mettre un chiffre apres la virgule
    temperature = temperature / 1000
    return temperature

nom_fichier = "/sys/bus/w1/devices/28-{}/w1_slave".format(sys.argv[1])
try:
 with open(nom_fichier) as fichier:
    contenuFich = fichier.read()
    temperature = recupTemp(contenuFich)
    print temperature
except:
    print 0
