from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, ValidationAction
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import hashlib
import json
import datetime
import time 
from datetime import date, timedelta



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
    
    @staticmethod
    def keylist(dicc):
        keylist = []
        for k in dicc:
            keylist.append(k)
    
        return keylist   

    # retorna diccionario {nombreMedicina: [datos de tratamiento], ... }
    @staticmethod
    def nombreDatosMedicina(self, userID):
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        cur.execute("SELECT diagnostico FROM tratamiento WHERE userID=?", (userID, ))
        userInfo = json.loads(cur.fetchall()[0][0])        
        diag= self.keylist(userInfo)
        return diag

    # entrega fecha y hora actual en formato 'year-' 
    @staticmethod
    def entregaHora():
        hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        time.sleep(60)
        return hora
    
    # este método guarda datos de inicio de tratamiento en DB/tabla->gestionMedicamentos
    @staticmethod
    def guardaDatosInicioMedicinas(userID, nombreMedicina, diaInicio, horaInicio, datosMedicina):
        '''
        nombreMedicina: string -> nombre de la medicina
        userID: ID del usuario
        diaInicio: 'yyyy, mm, dd'
        horaInicio: 'hh:mm'
        datosMedicina: ['dosis mg', freq(int), duracion(int)]

        --------------------------
        userID | {'nombreMedicina': [diaInicio, horaInicio, ['dosis', freq, duracion]], 'nombreMedicina2':[...etc]}

        '''
        datos = {}
        datos[nombreMedicina] = [diaInicio, horaInicio, datosMedicina]

        # pasar datos a JSON
        datos = json.dumps(datos)

        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        
        # crea tabla con horarios y datos de medicinas
        cur.execute("CREATE TABLE IF NOT EXISTS gestionMedicamentos (userID VARCHAR(36) NOT NULL, datos TEXT)")
        cur.execute("INSERT INTO gestionMedicamentos (userID, datos) VALUES (?, ?)", (userID, datos))

        con.commit()
        con.close()


        return []
    
    # método que extrae información de gestión de medicamentos de DB/tabla->gestionMedicamentos
    @staticmethod
    def extraeDatosInicioMedicinas(userID, nombreMedicina):
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()

        cur.execute("SELECT * FROM gestionMedicamentos WHERE userID=?", (userID, ))
        datos = cur.fetchall()

        # sacar de JSON los datos para transformarlos en objeto nuevamente

        datosInicio = None
        if datos[nombreMedicina]:
            datosInicio = datos[nombreMedicina]

        return datosInicio



    @staticmethod
    def creaHorarios(diaInicio, horaInicio, datosMedicina):          
          
          ''' 
        COMMAND: creaHorarios('fechaInicio', 'horaInicio', ['200mg', 8, 3])
        diaInicio: string -> 'yyyy, mm, dd' (default: 'ahora' -> fecha actual)
        horaInicio: string -> 'hh:mm' (default: 'ahora'-> hora actual)
        RETORNA: arreglo con los horarios de medicinas en formato string 'year-month-day hh:mm'   
        datosMedicina: ['cantidadmg', frecuencia, duracion] 
        '''    
        # Configuración de inicio de las fechas de inicio y de finalización
        # en formato datetime
        # IMPORTANTE: al escribir código final, el paciente debe tener clariad
        # de lo que significa que el tratamiento inicie a las 00:00 hrs. 
        # p.ej. si el tratamiento inicia a las 00 hra del 31 de julio, son las 0 horas del inicio del día 31
        # y no las 00 hrs del inicio del día 01 de agosto. 
          if diaInicio == 'ahora' and horaInicio == 'ahora':

            fechaInicio = datetime.datetime.now()
            fechaFinalizacion = datetime.timedelta(days=datosMedicina[2]) + fechaInicio
          else:
                inicio = [int(k) for k in diaInicio.split(',')]
                hora = [int(k) for k in horaInicio.split(':')]
                fechaInicio = datetime.datetime(inicio[0], inicio[1], inicio[2], hora[0], hora[1])
                fechaFinalizacion = datetime.timedelta(days=datosMedicina[2]) + fechaInicio
            
        # inicio de conteo
        # mensaje de finalización de tratamiento con esa medicina
          mensajeInicio = f"Inicio Tratamiento: {fechaInicio}"
          mensajeFinalizacion = f"Finalizacion del Tratamiento: {fechaFinalizacion}"
    #     print('Inicio de tratamiento', fechaInicio)
    #     print('El tratamiento con este medicamento finaliza: ', fechaFinalizacion)
          print('------------------------------------------------')

         # periodo de las dosis
          periodo = 24/datosMedicina[1]
        
        #switch de encendido y apagado de la funcion
          activo = True
          counter = 1 # contador
          horarios = []
        
          while (activo == True):

            incremento = datetime.timedelta(hours=periodo*counter) #configurado c/2 min
            diaFuturo = fechaInicio + incremento
            horarios.append(diaFuturo.strftime("%Y-%m-%d %H:%M"))
            if (diaFuturo == fechaFinalizacion):
                print('El tratamiento Finaliza ahora', diaFuturo)
                activo = False
            
            counter += 1            
            
          return horarios
        

    # SE PUEDE USAR CLASSES DE ESTE TIPO PARA ENVIAR INFORMACIÓN ESPECÍFICA
    # EN ALGÚN UTTER ESPECÍFICO, PREPARADO PARA RECIBIR SÓLO ESA INFORMACIÓN.
    # POR EJEMPLO, SI USER PREGUNTA CUÁNDO ES MI CUMPLEAÑOS
    # ENTONCES, SE ENVÍA LA RESPUESTA DESDE UN ACTION DE ESTE TIPO.
    # A TENER EN CUENTA: EL RUT NO SE CARGA INMEDIATAMENTE CUANDO EL USUARIO LO INGRESA
    # ES NECESARIO QUE EL USUARIO DIGITE ALGO MÁS PARA QUE ESTA ACCIÓN
    # RECIBA EL SLOT. O SEA, SI SE LE PREGUNTA POR UN SLOT, USUARIO RESPONDE
    # LUEGO BOT DEBE PEDIR QUE USUARIO INGRESE ALGUNA INFORMACIÓN MÁS (CUALQUIER COSA, PRESIONAR UNA LETRA Y DAR ENTER)
    # Y SÓLO AHÍ ESTA ACCIÓN RECIBE LA INFORMACIÓN DEL SLOT SOLICITADO
    # NO SÉ SI SE TRATA DE UNA PARTICULARIDAD DE ESTE PROCESO, O ES QUE YO NO LO ESTOY ENTENDIENDO BIEN!!
    def run(self,
            #    slot_value: Any,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: DomainDict) -> Dict[Text, Any]:

       
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()

        cur.execute("SELECT * FROM datospersonales")
        datos = cur.fetchall()
        
        # recupera slot nombreMedicina
        medicina = tracker.get_slot("medicina")
        # print(medicina)


        rut = tracker.get_slot("rut")
        validate = ValidateRut()
        paciente = None
        hashedRut = None
        if rut:
            hashedRut = validate.generar_hash(rut)            
            for dato in datos:
                dat = json.loads(dato[0])
                if (hashedRut == validate.keylist(dat)[0]):
                    paciente = dat[hashedRut]
                    userID = paciente['userID']
                    datosmedicinas = None
                    if userID: 
                        datosmedicinas = self.nombreDatosMedicina(self, userID)
                        print(datosmedicinas)

                    # print(userID)

        horarios = self.creaHorarios('2023,8,8', '8:00', ['100mg', 3, 5])
        # print(horarios)
                
        return [SlotSet("usuarioInfo", horarios)]


# esta clase muestra los horarios de cada medicamento
class HorarioMedicinas(Action):
    def name(self) -> Text:
        return "action_horario_medicinas"    

    def run(self,
        #    slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> Dict[Text, Any]:
        trat = Tratatamiento()

        rut = tracker.get_slot("rut")
        if rut: print("Horarios Medicinas")
        
        return []


# esta clase crea los horarios de las medicinas
class CreaHorarioMedicinas(Action):
    def name(self):
        return "action_crea_horario_medicinas"
    
    def run(self,
        #    slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> Dict[Text, Any]:

        age = tracker.get_slot("age")
        if age: print("Crea horarios medicinas")
        
        return []
    


# esta clase crea y administra los horarios de cada medicina
