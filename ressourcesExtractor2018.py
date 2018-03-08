#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
"""
On renseigne le path d'un dossier où on trouvera uniquement des 
fichiers .properties ainsi que le path et le nom du fichier d'un fichier csv
a créer. Enfin on indique le délimiteur de ce csv eg ';' ou '§'.
On lance le script et celui ci va créer le fichier csv avec 3 colonnes :
la clé + valeur, la clé, la valeur. Il ne va pas créer deux fois une meme ligne 
(avec la meme clé et la meme valeur) mais le signaler dans la console.

todo : refaire ce script en NodeJS voir https://www.npmjs.com/package/properties-file
"""
import csv, os
#### VARIABLES A RENSEIGNER AVANT DE LANCER LE SCRIPT
langTab = ['fr_FR', 'de_DE', 'en_GB', 'fr_BE', 'nl_BE', 'nl_NL', 'it_IT', 'en', 'en_US']
langCheck = ['fr_FR', 'nl_NL','de_DE', 'en_HK', 'en_US', 'es_ES', 'en_GB'] # on veut ces langues


user = os.environ['USERPROFILE']
ressourceFolder = os.path.join(user, 'workspace\\ba-sh-salesforce-site-ecomm\\cartridges\\app_bash\\cartridge\\templates\\resources')
csvFolder = os.path.join(user,'Desktop')
csvName = 'properties'
theDelimiter = 'œ'
####
keyValTab = []
def loadProperties(filePath):
    """
    Read the file passed as parameter as a properties file.
    """
    sep='='
    comment_char='#'
    props = {}
    try:
        with open(filePath, "rt") as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(comment_char):
                    key_value = l.split(sep)
                    key = key_value[0].strip()
                    value = sep.join(key_value[1:]).strip().strip('"').strip()
                    props[key] = value 
    except Exception:
        pass
    return props


def getAllProperties():
    """
    Gets properties objects for all languages
    """
    allProperties = {}
    for lang in langCheck:
        allProperties[lang] = {}
        for element in os.listdir(ressourceFolder):
            if lang not in element: # exemple if 'nl_NL' not in file name we pass
                continue
            properties = loadProperties(os.path.join(ressourceFolder, element))
            allProperties[lang].update(properties)
    return allProperties


def getAllKeys(allProperties):
    """
    returns properties list from the properties object passed as parameter
    """
    assert type(allProperties) == dict
    allKeys = []
    for key in allProperties:
        allKeys.extend(list(allProperties[key].keys()))
    return sorted(list(set(allKeys)))


if __name__ == '__main__':
    allProperties = getAllProperties()
    keys = getAllKeys(allProperties)
    with open(csvFolder + '/' + csvName + '.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=theDelimiter, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['PROPERTIES'] + langCheck)
        for key in keys:
            row = []
            row.append(key)
            for lang in langCheck:
                if (key in allProperties[lang]):
                    row.append(allProperties[lang][key])
                else:
                    row.append(" ")
            spamwriter.writerow(row)


 




    
