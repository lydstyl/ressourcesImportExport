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
langTab = ['fr_FR', 'de_DE', 'en', 'fr_BE', 'nl_BE', 'nl_NL', 'it_IT', 'en', 'en_AE']
lang1 = langTab[0] # on veut ça
lang2 = langTab[7] # par rapport à ça ?

###
user = os.environ['USERPROFILE']
ressourceFolder = os.path.join(user, 'workspace\\ba-sh-salesforce-site-ecomm\\cartridges\\app_bash\\cartridge\\templates\\resources')
csvFolder = os.path.join(user,'Desktop')
csvName = lang1 + '_' + lang2 + '_properties'
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
print(lang1 + '-->' + lang2)
with open(csvFolder + '/' + csvName + '.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=theDelimiter,
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['FILE'] + ['KEY'] + ['VAL ' + lang1] + ['VAL2 ici ' + lang2]) #on ajoute lang ici fr_FR be_FR be_NL nl_NL it_IT en_AE
    for element in os.listdir(ressourceFolder):
        if lang1 not in element: # exemple if 'nl_NL' not in file name we pass
            continue
        properties = loadProperties(ressourceFolder + '/' + element)

        fileNameOtherLang = element.replace(lang1, lang2)
        properties2 = loadProperties(ressourceFolder + '/' + fileNameOtherLang)
        for key in properties:
            keyVal = key + properties[key]
            doublon = 'False'
            if keyVal in keyValTab: # double found
                doublon = 'True'
            keyValTab.append(keyVal)
            
            val2 = ''
            for key2 in properties2:
                if key2 == key:
                    val2 = properties2[key2]

            spamwriter.writerow([element] + [key] + [properties[key]] + [val2])
