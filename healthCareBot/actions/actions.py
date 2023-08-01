from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, ValidationAction
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import EventType, SlotSet
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
    def diagnosticos(self, userID) -> Text:
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

            ## DIAGNOSTICO
            path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
            con = sqlite3.connect(path, check_same_thread=False)
            cur = con.cursor()
            cur.execute("SELECT diagnostico FROM tratamiento WHERE userID=?", (userID, ))
            userInfo = json.loads(cur.fetchall()[0][0])        
            diag= self.keylist(userInfo)
            texto = ', '.join([d for d in diag])
            diagnosticos = 'El tratamiento es para: ' + texto
            ####################

            ## DOSIS
            lista = []
            for k in self.keylist(userInfo):
                lista.append(userInfo[k])
            
            dicc = {}
            for dic1 in lista:
                for sub in dic1:
                    dicc[sub] = dic1[sub] 
            dosis = dicc
            lista = self.keylist(dosis)
            mensajes = []
            for li in lista:
                mensajes.append(dosis[li][0] + ' de ' + li.upper()  + '. ' 
                                + str(dosis[li][1]) + ' dosis al dia. Durante ' + str(dosis[li][2]) + ' dias.' + '\n')           

            texto_dosis = ' '.join([mensaje for mensaje in mensajes])
            ###########################################

            ## FUNCIÓN QUE GENERA TEXTOS DE DIAGNÓSTICOS Y TRATAMIENTO (MEDICAMENTOS) INDICADOS POR MÉDICO  
            dd = {}
            for dig in diag:
                # print(diag, userInfo[diag])
                dd[dig] = self.keylist(userInfo[dig])
            
            ## IDEA: CUANDO PACIENTE PREGUNTE POR DIAGNÓSTIO
            ## EL BOT RESPONDE CON EL MÉTODO DIAGNÓSTICO: UNA LISTA DE LAS ENFERMEDADES...
            ## CUANDO PACIENTE PREGUNTA POR MEDICAMENTOS, SE ENTREGA LA ENFERMEDAD
            ## JUNTO CON LA LISTA DE LOS MEDICAMENTOS PARA EL TRATAMIENTO. 

            # salida de los medicamentos: 'enfermedad y los medicamentos indicados por el médico'
            # enfs lista de enfrmedades
            enfs = self.keylist(dd)
            textos = []
            for enf in enfs:
                textos.append(' Para el cuadro de ' + enf.upper() + ' el tratamiento es con: ' + ', '.join([k for k in dd[enf]]) + '.')
                # print('Para el cuadro de ' + enf.upper() + ' el tratamiento es con: ' + ', '.join([k for k in dd[enf]]))
            
            # #este testo contiene la enfermedad y los medicamentos prescritos.
            # # al estilo ej. Para la GRIPE se te prescribió el tratamiento con: aspirina, etc 
            texto_medicamentos = '\n '.join([tex for tex in textos])
            # texto_medicamentos = userInfo 
            ##########################
            # pp = GerenciaHorarios()
            # nome = pp.prueba()
            # print(nome)

            ## diagnostico: va en utter_tratamiento
            ## dosis: va en utter_horarios

            return {'nombre': nombre, 'apellido': apellido, 
                    'userID': userID, 'diagnostico': diagnosticos, 
                    'dosis': texto_dosis, 'medicinas': texto_medicamentos}

# para obtener información del tratamiento. 
# medicinas, dosis y frecuencia diaria

class Tratatamiento(Action):
    def name(self) -> Text:
        return "action_tratamiento"
    
    def run(self,
            #    slot_value: Any,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: DomainDict) -> Dict[Text, Any]:
                
        
        # print('Estoy activo, tratamiento')
        return [SlotSet("usuarioInfo", "ALGO")]


    


# esta clase crea y administra los horarios de cada medicina
