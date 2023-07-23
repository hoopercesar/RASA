import sqlite3
import hashlib
import json

class ValidateRut():
    def __init__(self, rut):
        self.rut = rut
    
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
                print('PACIENTE', paciente)
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
        return 'algo'
        
# fran = 12658439-3
# amore = 20502458-1
        
t = Tratamiento('20502458-1')      
v = ValidateRut('13109915-0')   
print(v.validate_rut()['userID'])