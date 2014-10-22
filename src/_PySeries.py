#!/usr/bin/env python
# -*- encoding: utf8 -*-
"""
_PySeries.py

Created by Ramon Maria Gallart Escolà on 2012-05-24.
Copyright (c) 2012 ramagaes.com. All rights reserved.
"""
from .settings.constants import PROGRAM, VERSION, INFO, DEBUG, WARNING, ERROR
from utils import print_message
from .settings.conf import DO_DEBUG
from sys import exit
from .plugins import todohdtv
from .plugins import divxatope

# Vigilem si hi ha hagut errors en el procés
errors = False
# Aquí guardem les series
series = []
# Comprovem si existeix el fitxer de darreres actualitzacions
# Indica si existeix el fitxer d'actualitzacions
eacts = True
# Aquí guardem les actualitzacions
acts = []
# Aquí guardarem la llista de les sèries que s'han actualitzat
# Aquesta llista la guardarem en el fitxer html de sortida
series_actualitzades = []
# Aquí guardarem les noves actualitzacions que anem trobant
# de les sèries que tenim
acts2 = []
# Aquí posem les diferents cookies
cookies = {}


def llegir_series():
    """
    Llegeix el fitxer de sèries per ser processat.
    """
    print_message(DEBUG, 'Estem a llegir series', DO_DEBUG)
    # Llegim el fitxer series.txt
    try:
        fseries = open("series.txt")

        # Afegim les series del fitxer com a tuples en una llista
        for line in fseries.readlines():
            line = line.strip()
            if len(line) == 0 or line.startswith('#'):
                continue
            parts = line.split("#")
            # Convertim cada línia en una tupla on:
            # 0: identificador de la serie
            # 1: web on està la informació de la sèrie
            # 2: nom de la serie
            # 3: url de la serie
            t = (parts[0].strip(), parts[1].strip(),
                    parts[2].strip(), parts[3].strip())
            series.append(t)

            # Per debugar. Assegurem que tenim totes les series
            for s in series:
                print_message(DEBUG, s[1] + " - " + s[2], DO_DEBUG)

            # Tanquem fseries
            fseries.close()
    except Exception as e:
        raise Exception(e.message)


def llegir_actualitzacions():
    print_message(DEBUG, 'Estem a llegir actualitzacions', DO_DEBUG)
    try:
        facts = open("acts.txt")
        # Afegim les actualitzacions del fitxer com a tuples en una llista
        for line in facts.readlines():
            parts = line.split("#")
            # Convertim cada linia en una tupla on:
            # 0: és el codi identificador de la serie
            # 1: és el hash del darrer cop que es va llegir la pàgina
            t = (parts[0].strip(), parts[1].strip())
            acts.append(t)

        # Per debugar. Mirem si tenim les actualitzacions
        for a in acts:
            print_message(DEBUG, a[1], DO_DEBUG)

        # Tanquem facts
        facts.close()
    except Exception as e:
        eacts = False
        print_message(INFO,
                "No existeix fitxer d'actualitzacions. El crearem després: "
                + e.message)
        errors = True


def escriure_actualitzacions():
    """
    Escriu en el fitxer acts.txt les actualitzacions de les sèries
    """
    print_message(DEBUG, 'Estem a escriure actualitzacions', DO_DEBUG)
    print_message(INFO, "Escribint actualitzacions" + ("." * 30))
    try:
        facts = open("acts.txt", "w")
        print_message(DEBUG, acts2, DO_DEBUG)

        if acts2:
            for a in acts2:
                facts.write(a + "\r\n")

        facts.close()
    except Exception as e:
        print_message(ERROR,
                "No he pogut crear el fitxer d'actualitzacions: "
                + e.message)
        errors = True


def escriure_html():
    """
    Escriu en el fitxer output.html els enllaços a les sèries que han
    estat actualitzades.
    """
    print_message(DEBUG, 'Estem a escriure html', DO_DEBUG)
    print_message(INFO, "Escribint la sortida en html" + ("." * 30))
    try:
        output = open("output.html", "w")
        output.write("<!DOCTYPE html>\r\n")
        output.write("""<html>\r\n<head>\r\n\t<title>Llista de
           s&egrave;ries</title>\r\n</head>""")
        output.write("<body>")
        if series_actualitzades:
            output.write("""\r\n\t<h1>Llista de s&egrave;ries per
                actualitzar</h1>\r\n\t<ul>""")
            for serie in series_actualitzades:
                output.write("\r\n\t\t" + serie)

            output.write("\r\n\t</ul>")
        else:
            output.write("""\r\n\t<h1>Totes les s&egrave;ries estan
                actualitzades</h1>\r\n\t""")
            output.write("\r\n</body>\r\n</html>\r\n")
    except Exception as e:
        print_message(ERROR, "No he pogut crear el fitxer de sortida: "
                + e.message)
        errors = True


def get_cookies():
    """
    Obté les cookies emmagatzemades al fitxer cookies.data
    """
    print_message(DEBUG, 'Estem a get cookies', DO_DEBUG)
    try:
        f = open('cookies.data', 'r')
        for line in f.readlines():
            parts = line.split('#')
            # Cada línia representa una cookie del lloc.
            # El nom de les cookies han de coincidir amb el valor
            # assignat a la constant COOKIE_NAME de cada lloc.
            # 0: nom de la cookie
            # 1: valor de la cookie
            cookies[parts[0].strip()] = parts[1].strip()
            print_message(DEBUG, parts[0].strip() + ' = ' + parts[1].strip(),
                    DO_DEBUG)

        f.close()
    except Exception as e:
        print_message(ERROR, "Error llegint fitxer de cookies: " + e.message)
        errors = True


def processar_series():
    print_message(DEBUG, 'Estem a processar series', DO_DEBUG)
    get_cookies()
    try:
        llegir_series()
    except Exception as e:
        print_message(ERROR, "Error llegint fitxer de sèries: " + e.message)
        exit()

    llegir_actualitzacions()
    # ......
    # Iterem per totes les sèries, baixem la seva pàgina i comparem
    # amb la llista d'actualitzacions
    hash_actual = ""
    for serie in series:
        id_serie, web_serie, nom_serie, url_serie = serie
        print_message(INFO, "Comprovant darrera actualització de la sèrie: " +
                nom_serie)
        try:
            if web_serie == 'todohdtv':
                hash_actual = todohdtv.get_digest(url_serie,
                        None, DO_DEBUG)
            elif web_serie == 'divxatope':
                hash_actual = divxatope.get_digest(url_serie,
                        None, DO_DEBUG)

        except Exception as e:
            print_message(ERROR, "Error tractant [" + nom_serie + "]: " +
                    e.message)

        print_message(DEBUG, "--> " + hash_actual, DO_DEBUG)

        if eacts:
            # Si existeix el fitxer, compararem cada entrada de la llista de
            # sèries amb les que hi ha d'actualitzacions
            trobat = False
            for act in acts:
                id_serie_act, hash_anterior = act
                # si la sèrie no és la que estem tractant, saltem el bucle
                if id_serie_act != id_serie:
                    continue
                # hem trobat la sèrie!
                # comprovem si el hash actual és el mateix que ja teníem.
                # Si no ho és, afegim el hash actual a acts2 i a la sortida de
                # sèries actualitzades. Si ho és, només reescribim el registre
                # al fitxer d'actualitzacions
                # Sortim del bucle
                trobat = True
                # debug dates
                print_message(DEBUG, "hash_anterior: " + hash_anterior)
                print_message(DEBUG, "hash_actual: " + hash_actual)
                if hash_anterior != hash_actual:
                    acts2.append(id_serie + "#" + hash_actual)
                    series_actualitzades.append("<li><a href=\"" + url_serie
                        + "\" target=\"_blank\">" + nom_serie + "</a></li>")
                    print_message(INFO, "'" + nom_serie + "' actualitzada!!")
                else:
                    acts2.append(id_serie + "#" + hash_actual)

                break

            # aquí entrem en el cas que la sèrie no estigui en el fitxer
            # d'actualitzacions
            if not trobat:
                acts2.append(id_serie + "#" + hash_actual)
                series_actualitzades.append("<li><a href=\"" + url_serie +
                    "\" target=\"_blank\">" + nom_serie + "</a></li>")

        else:
            # Si no existeix el fitxer d'actualitzacions, igualment visitarem
            # les pàgines de les sèries i les marcarem per visitar a la
            # sortida.
            acts2.append(id_serie + "#" + hash_actual)
            series_actualitzades.append("<li><a href=\"" + url_serie +
                "\" target=\"_blank\">" + nom_serie + "</a></li>")
            print_message(INFO, "'" + nom_serie + "' actualitzada!!")

        hash_actual = ""
        hash_anterior = ""
  # ......
    escriure_actualitzacions()
    escriure_html()


def main():
    processar_series()
    if errors:
        print_message(INFO, 'Programa acabat amb errors')
