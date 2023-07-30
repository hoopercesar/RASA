import sqlite3
import hashlib
import json
from datetime import date, timedelta
import datetime
import time 

class ValidateRut():
    def __init__(self, rut):
        self.rut = rut

    # entrega fecha y hora actual en formato 'year-' 
    @staticmethod
    def entregaHora():
        hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        time.sleep(60)
        return hora
    
    # función que crea los horarios de las medicinas
    @staticmethod
    def creaHorarios(diaInicio, horaInicio, datosMedicina):
        ''' 
        COMMAND: creaHorarios('ahora', 'ahora', ['200mg', 8, 3])
        RETORNA: arreglo con los horarios de medicinas en formato string 'year-'   
        diaInicio: 'year, month, day'
        horaInicio: 'hh:mm'
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
            incremento = datetime.timedelta(minutes=periodo*counter) #configurado c/2 min
            diaFuturo = fechaInicio + incremento
            horarios.append(diaFuturo.strftime("%Y-%m-%d %H:%M"))
            if (diaFuturo == fechaFinalizacion):
                print('El tratamiento Finaliza ahora', diaFuturo)
                activo = False
            
            counter += 1            
            
        return horarios


    
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
    def rut_db(self, rut):
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
                # print('PACIENTE', paciente['userID'])
                return paciente

        
                
    @staticmethod
    def get_user_info(userRut):
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        cur.execute("SELECT * FROM dataset_estudio WHERE rut=?", (userRut, ))
        userInfo = cur.fetchall()
        return userInfo

    def validate_rut(self):
                
        """Validate rut value"""
        time = self.entregaHora()
        horarios = self.creaHorarios('2023, 07, 29', '21:50', ['100mg', 3, 3])
        print('HORARIOS', horarios[0:10], time)
        for t in range(0, 10):
            hora = self.entregaHora()
            print(t, hora)

            if hora in horarios:
                message = f"{hora} Hora de Medicina!"
                print(message)

        mensaje = ''
        if (self.rut_db(self, self.rut) ==  None):
            mensaje = 'Rut no válido'
            return mensaje
        else:
            return self.rut_db(self, self.rut)

#### Clase diagnóstico y tratamiento #####

class Tratamiento(ValidateRut):
    def __init__(self, rut):
  
        self.rut = rut

    path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
    con = sqlite3.connect(path, check_same_thread=False)
    cur = con.cursor()

    @staticmethod
    def keylist(dicc):
        keylist = []
        for k in dicc:
            keylist.append(k)    
        return keylist   
    
    # cur.execute("SELECT diagnostico FROM tratamiento WHERE userID=?", (userID, ))
    # userInfo = cur.fetchall()
    @staticmethod
    def userID(rut):
        val = ValidateRut(rut)
        # print('AQUI ESTA', val.rut_db(rut))
        return val.validate_rut()['userID']

    def diagnosticos(self):
        userID = self.userID(self.rut)
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        cur.execute("SELECT diagnostico FROM tratamiento WHERE userID=?", (userID, ))
        userInfo = json.loads(cur.fetchall()[0][0])

        diagnosticos = self.keylist(userInfo)
        

        return diagnosticos

    def medicamentos(self):
        userID = self.userID(self.rut)
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        cur.execute("SELECT diagnostico FROM tratamiento WHERE userID=?", (userID, ))
        userInfo = json.loads(cur.fetchall()[0][0])

        
        dd = {}
        for diag in self.diagnosticos():
            # print(diag, userInfo[diag])
            dd[diag] = self.keylist(userInfo[diag])

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

        texto = '\n '.join([tex for tex in textos])
        print(texto)

        return dd
    
    def dosis(self):
        userID = self.userID(self.rut)
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        cur.execute("SELECT diagnostico FROM tratamiento WHERE userID=?", (userID, ))
        userInfo = json.loads(cur.fetchall()[0][0])
        
        # self.keylist(userInfo) es la lista de diccionarios de cada medicina con sus dosis
        # se extrae cada diccionario de medicina (con sus dosis) y se guarda en una sola lista
        lista = []
        for diag in self.keylist(userInfo):
            lista.append(userInfo[diag])

        # lista contiene los diccionarios de las medicinas con sus dosis
        # ahora, vamor a unir todos esos diccionarios en un solo diccionario dic_final
        dic_final = {}
        for dic1 in lista:
            for sub in dic1:
                dic_final[sub] = dic1[sub]     
            
        return dic_final

    def presentacionDosis(self):
        '''en el método dosis se extraen las medicinas con sus dosis y se ordenan
        dentro de un diccionario. sin embargo, esta presentación no es adecuada para el paciente.
        en este método se presenta la información de manera entendible para el paciente.
        un mensaje con el nombre de la medicina y la dosis diaria'''
        dosis = self.dosis()
        lista = self.keylist(dosis)
        mensajes = []
        for li in lista:
            mensajes.append(dosis[li][0] + ' de ' + li.upper()  + '. ' 
                            + str(dosis[li][1]) + ' dosis al dia. Durante ' + str(dosis[li][2]) + ' dias.' + '\n')           
            # print(li, dosis[li])

        texto = ' '.join([mensaje for mensaje in mensajes])

        # print(texto)
        
        return texto
        
# fran = 12658439-3
# amore = 20502458-1
        
t = Tratamiento('13109915-0')      
v = ValidateRut('13109915-0')   
m = {'key uno': 18}
print(v.validate_rut())