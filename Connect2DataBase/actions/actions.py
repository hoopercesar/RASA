from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher

class ValidateRut(FormValidationAction):
    def name(self) -> Text:
       return "validate_rut"
    
    @staticmethod
    def ruts_db() ->List[Text]:
        """ruts database"""
        return ['']

    def validate_rut(                  
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
            ) -> Dict[Text, Any]:
        
        """Validate rut value"""

        if slot_value.isdigit() == True: 
            dispatcher.utter_message(text=f"{slot_value} es correcto")
            return {'rut': 'poto'}
        else:
            dispatcher.utter_message(text=f"{slot_value} incorrecto")
            return {'rut': None}