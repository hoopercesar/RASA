from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, ValidationAction
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

    @staticmethod
    async def diagnosticos(self, userID) -> Text:
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        cur.execute("SELECT diagnostico FROM tratamiento WHERE userID=?", (userID, ))
        userInfo = json.loads(cur.fetchall()[0][0])
        diag= self.keylist(userInfo)
        texto = ', '.join([d for d in diag])
        diagnosticos = 'El tratamiento es para: ' + texto

        # diagnosticos = self.keylist(userInfo)

        return diagnosticos



    def validate_rut(                  
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
                
        """Validate rut value"""

        # print('EN VALIDATE_RUT', self.rut_db(self, slot_value))

        if (self.rut_db(self, slot_value) ==  None): 
            dispatcher.utter_message(text=f"{slot_value} Rut no Valido")
            return {'rut': None}
        else:
            # diagnostico = self.diagnosticos(self, slot_value)
            usuario = self.rut_db(self, slot_value)
            nombre = usuario['nombre']
            apellido = usuario['apellido']
            userID = usuario['userID']

            path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
            con = sqlite3.connect(path, check_same_thread=False)
            cur = con.cursor()
            cur.execute("SELECT diagnostico FROM tratamiento WHERE userID=?", (userID, ))
            userInfo = json.loads(cur.fetchall()[0][0])        
            diag= self.keylist(userInfo)
            texto = ', '.join([d for d in diag])
            diagnosticos = 'El tratamiento es para: ' + texto




            return {'nombre': nombre, 'apellido': apellido, 'userID': userID, 'diagnostico': diagnosticos}

# para obtener información del tratamiento. 
# medicinas, dosis y frecuencia diaria
class Tratamiento(ValidationAction):    
    def name(self):
        return "action_tratamiento"

    
    
    print('EN TRATAMIENTOS')
    def hola(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        print(slot_value)

        return {'usuarioInfo': 'ALGO BONITO'}


# esta clase crea y administra los horarios de cada medicina
