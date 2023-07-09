from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
import sqlite3

class ValidateRut(FormValidationAction):
    def name(self) -> Text:
       return "validate_rut_form"
    
    @staticmethod
    def rut_db() -> List[Text]:
        """ruts database"""
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/dataset_estudio.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        cur.execute("SELECT rut FROM dataset_estudio")
        rows = cur.fetchall()
        lista = []
        for row in rows:
            lista.append(row[0])

        return lista

    @staticmethod
    def get_user_info(userRut) -> tuple[Text]:
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/dataset_estudio.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        cur.execute("SELECT * FROM dataset_estudio WHERE rut=?", (userRut, ))
        userInfo = cur.fetchall()
        return userInfo

    def validate_rut(                  
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
                
        """Validate rut value"""

        if slot_value not in self.rut_db(): 
            dispatcher.utter_message(text=f"{slot_value} no existe")
            return {'rut': None}
        else:
            usuario = self.get_user_info(slot_value)
            dispatcher.utter_message(text=f"{slot_value} es un usuario activo")
            return {'rut': usuario}
        
    
