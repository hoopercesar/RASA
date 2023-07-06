from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher



class ValidateSimplePizza(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_pizza_form"
    
    @staticmethod
    def tipos_pizza() -> List[Text]:
        """DataBase de los tipos de pizza"""
        return ['vegana', 'chocolate', 'calabresa', 'frutillas', "queso_catupiry"]

    @staticmethod
    def tamanhos_pizza() -> List[Text]:
        """DataBase de los tamaños de pizza"""
        return ['grande', 'mediana', 'mediano', 'pequeña', 'chica', 'pequeño']

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate pizza_size value"""

        if slot_value.lower() not in self.tamanhos_pizza():
            dispatcher.utter_message(text=f"Sólo tenemos pizza grande, meddiana o pequeña")
            return {"pizza_size": None}
        else:
           dispatcher.utter_message(text=f"Perfecto, has solicitado una pizza {slot_value}")
           return {"pizza_size": slot_value}
    

    def validate_pizza_type(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict, 
    ) -> Dict[Text, Any]:
        """Validate pizza_type value"""

        if slot_value.lower() not in self.tipos_pizza():
            dispatcher.utter_message(text=f"Sólo tenemos pizza vegana, de chocolate, calabresa, frutillas, chocolate y queso_catupiry")
            return {"pizza_type": None}
        else: 
            dispatcher.utter_message(text=f"Ok, has elegido la pizza {slot_value}")
            return {"pizza_type": slot_value}



