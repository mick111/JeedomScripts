#!/usr/bin/python
import os
import sys


def lireFichier (emplacement) :
    # Ouverture du fichier contenant la temperature
    fichTemp = open(emplacement)
    # Lecture du fichier
    contenu = fichTemp.read()
    # Fermeture du fichier apres qu'il ai ete lu
    fichTemp.close()
    return contenu

def recupTemp (contenuFich) :
    # Supprimer la premiere ligne qui est inutile
    secondeLigne = contenuFich.split("\n")[1]
    temperatureData = secondeLigne.split(" ")[9]
    # Supprimer le "t="
    temperature = float(temperatureData[2:])
    # Mettre un chiffre apres la virgule
    temperature = temperature / 1000
    return temperature

contenuFich = lireFichier("/sys/bus/w1/devices/28-{}/w1_slave".format(sys.argv[1]))
temperature = recupTemp (contenuFich)

print temperature