# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 11:54:46 2015

@author: leo_cdo_inter

##############################################################################
Contient : _sexe, _code_csp_insee, _csp_insee, _url


"""

from os.path import join
from process_text import _process_text
import re
path = '/fichiers_de_reference/autres'

#### AUTRES INFOS
def _sexe(val):
    '''Repère le sexe'''
    val =_process_text(val)
    return val in ['homme', 'femme', 'h', 'f', 'm', 'masculin', 'feminine']

def _code_csp_insee(val):
    '''Repère les code csp telles que définies par l'INSEE'''
    val = _process_text(val)
    if not len(val) == 4:
        return False
    a = bool(re.match(r'^[123456][1-9]{2}[abcdefghijkl]$', val))
    b = val in ['7100', '7200', '7400', '7500', '7700', '7800', '8100', '8300', '8400', '8500', '8600']
    return a or b

def _csp_insee(val):
    '''Repère les csp telles que définies par l'INSEE'''
    val = _process_text(val)
    f = open(join(path, 'csp_insee.txt'), 'r')
    liste = f.read().split('\n')
    f.close()
    return val in liste

def _url(val):
    '''Repère les url'''
    a = 'http://' in val
    b = 'www.' in val
    c = any([x in val for x in ['.fr', '.com', '.org', '.gouv', '.net']])
    d = not ('@' in val)
    return (a or b or c) and d

def _courriel(val):
    '''Repère les courriel'''
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'
    return re.match(regex, val)

def _tel_fr(val):
    '''Repère les numeros de telephone francais'''
    # TODO: Cette regex ne marche pas
    regex = r'^(0|(00|\+)33)[67][0-9]{8}$'
    return re.match(regex, val)

def _siren(val):
    '''Repere les codes SIREN'''
    val = val.replace(' ', '')
    regex = r'[0-9]{9}'
    if not bool(re.match(regex, val)):
        return False
    # Vérification par clé propre aux codes siren
    cle = 0
    pair = False
    for x in val:
        y = int(x) * (1 + pair)
        cle += y // 10 + y % 10
        pair = not pair

    return cle % 10 == 0
