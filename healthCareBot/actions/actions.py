from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import hashlib
import json


class ValidateRut(FormValidationAction):
    def name(self) -> Text:
       return "validate_rut_form"
    
    # función para hashear datos
    @staticmethod
    def generar_hash(cadena):
        # Crear un objeto de hash utilizando el algoritmo SHA256
        hasher = hashlib.sha256()

        # Convertir la cadena en bytes y actualizar el objeto de hash
        hasher.update(cadena.encode('utf-8'))

        # Obtener el hash resultante en formato hexadecimal
        hash_resultado = hasher.hexdigest()

        return hash_resultado

    # entrega lista de keys de diccionarios
    @staticmethod
    def keylist(dicc):
        keylist = []
        for k in dicc:
            keylist.append(k)
    
        return keylist   
        
    # retorna lista con ruts hasheados dentro de DB
    @staticmethod
    def rut_db(self, rut) -> List[Text]:
        """ruts database"""
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        cur.execute("SELECT * FROM datospersonales")
        datos = cur.fetchall()

        paciente = None
        hashedRut = self.generar_hash(rut)
        for dato in datos:
            dat = json.loads(dato[0])
            if (hashedRut == self.keylist(dat)[0]):
                paciente = dat[hashedRut]
                return paciente

    def validate_rut(                  
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
                
        """Validate rut value"""

        if (self.rut_db(self, slot_value) ==  None): 
            dispatcher.utter_message(text=f"{slot_value} Rut no Valido")
            return {'rut': None}
        else:
            usuario = self.rut_db(self, slot_value)
            nombre = usuario['nombre']
            apellido = usuario['apellido']
            userID = usuario['userID']
            # dispatcher.utter_message(template="utter_rut_slots", nombre=nombre)
            # dispatcher.utter_message(template="utter_goodbye", nombre=nombre)
            return {'nombre': nombre, 'apellido': apellido, 'userID': userID, 'marte': 'soy marciano'}

# para obtener información del tratamiento. 
# medicinas, dosis y frecuencia diaria
class Tratamiento(ValidateRut):    
    def name(self) -> Text:
        return "action_tratamiento"

    @staticmethod
    def diagnosticos(self, userID):
        userID = userID
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        cur.execute("SELECT diagnostico FROM tratamiento WHERE userID=?", (userID, ))
        userInfo = json.loads(cur.fetchall()[0][0])

        diagnosticos = self.keylist(userInfo)
        return diagnosticos
    
    def tratamientoInfo(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,) -> Dict[Text, Any]:

        heritage = ValidateRut()
        usuario = heritage.validate_rut(slot_value)
        userID = usuario['userID']
        # diagnosticos = self.diagnosticos(userID)
        print(userID)

        dispatcher.utter_message(text=f"Info Tratamiento: {usuario}")


        return {'usuarioInfo': 'ALGUNA INFORMACIÓN'}
    
        

# esta clase crea y administra los horarios de cada medicina
