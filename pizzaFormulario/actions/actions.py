from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher


tamanos_de_pizza = ['grande', 'mediana', 'mediano', 'pequeña', 'chica', 'pequeño']
tipos_de_pizza = ['vegana', 'chocolate', 'calabresa', 'frutillas', "queso_catupiry"]

class ValidateSimplePizza(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_pizza_form"
    
    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate pizza_size value"""

        if slot_value.lower() not in tamanos_de_pizza:
            dispatcher.utter_message(text=f"Sólo tenemos pizza grande, meddiana o pequeña")
            return {"pizza_size": None}
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

        if slot_value.lower() not in tipos_de_pizza:
            dispatcher.utter_message(text=f"Sólo tenemos pizza vegana, de chocolate, calabresa, frutillas, chocolate y queso_catupiry")
            return {"pizza_type": None}
        dispatcher.utter_message(text=f"Ok, has elegido la pizza {slot_value}")
        return {"pizza_type": slot_value}



