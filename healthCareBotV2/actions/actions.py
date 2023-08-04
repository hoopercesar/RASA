from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, ValidationAction
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
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
            print(rut, nombre)
            dispatcher.utter_message(response="utter_verified", rut="ALGO TEST")

              
         

        return [SlotSet("mensaje", nombre)]  
        

        
