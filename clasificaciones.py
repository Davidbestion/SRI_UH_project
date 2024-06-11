# Metodos para, dada una lista de clasificaciones, obtener palabras relacionadas con cada clasificacion 
# Palabras que, si aparecen en un texto, indican que el texto pertenece a una clasificacion
#
# Ejemplo:
# clasificaciones = ['clima', 'deportes', 'tecnologia']
# palabras_clasificacion = {
#     'clima': ['clima', 'tiempo', 'temperatura', 'lluvia', 'sol'],
#     'deportes': ['deportes', 'futbol', 'baloncesto', 'tenis', 'ciclismo'],
#     'tecnologia': ['tecnologia', 'movil', 'ordenador', 'internet', 'redes']
# }
#

import nltk
from nltk.corpus import wordnet
# from spacy.lang.es import Spanish

clasificaciones = ['clima', 'deportes', 'tecnologia']

#Obtener sinonimos de cada una (todo en espanol)
def obtener_sinonimos(palabra):
    sinonimos = []
    for syn in wordnet.synsets(palabra, lang='spa'):
        for lemma in syn.lemmas('spa'):
            sinonimos.append(lemma.name())
    return sinonimos

def obtener_familias(palabra):
    familias = []
    for syn in wordnet.synsets(palabra, lang='spa'):
        for hypernym in syn.hypernyms():
            for lemma in hypernym.lemmas('spa'):
                familias.append(lemma.name())
    return familias

def obtener_palabras_relacionadas(clasificaciones):
    palabras_clasificacion = {}
    for clasificacion in clasificaciones:
        sinonimos = obtener_sinonimos(clasificacion)
        familias = obtener_familias(clasificacion)
        palabras_clasificacion[clasificacion] = sinonimos + familias
    return palabras_clasificacion

palabras_clasificacion = obtener_palabras_relacionadas(clasificaciones)