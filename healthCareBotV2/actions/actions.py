from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, ValidationAction
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.interfaces import Action
import sqlite3
import hashlib
import json


class ActionVerifyRut(Action):

    def name(self) -> Text:
        return "action_verify_rut"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> Dict[Text, Any]:
       
       
        rut = tracker.get_slot("rut")
        nombre = tracker.get_slot("nombre")
        
        if rut == None: 
            print('Sin información')
        else: 
            # mensaje = nombre
            print(rut, nombre)

        return [SlotSet("mensaje", nombre)]  
    
class ActionBuscaDataBase(Action):
    def name(self) -> Text:
        return "action_busca_database"
    
    @staticmethod
    def keylist(dicc):
        keylist = []
        for k in dicc:
            keylist.append(k)

        return keylist   
    
    @staticmethod
    def generar_hash(cadena):
        # Crear un objeto de hash utilizando el algoritmo SHA256
        hasher = hashlib.sha256()

        # Convertir la cadena en bytes y actualizar el objeto de hash
        hasher.update(cadena.encode('utf-8'))

        # Obtener el hash resultante en formato hexadecimal
        hash_resultado = hasher.hexdigest()

        return hash_resultado
    
    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict):
        
        rut = tracker.get_slot('rut')
        rutHashed = self.generar_hash(rut)
        print('caquita loca', rutHashed)

        return []

        

        
