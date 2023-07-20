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

class Tratamiento(ValidateRut):
    def __init__(self, rut):
  
        self.rut = rut

    path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
    con = sqlite3.connect(path, check_same_thread=False)
    cur = con.cursor()
    
    # cur.execute("SELECT diagnostico FROM tratamiento WHERE userID=?", (userID, ))
    # userInfo = cur.fetchall()
    @staticmethod
    def userID(rut):
        val = ValidateRut(rut)
        return val.validate_rut()['userID']

    def tratamiento(self):
        userID = self.userID(self.rut)
        path = 'C:/Users/Cesar Hooper/Documents/STARTUP/datapacientes.db'
        con = sqlite3.connect(path, check_same_thread=False)
        cur = con.cursor()
        cur.execute("SELECT diagnostico FROM tratamiento WHERE userID=?", (userID, ))
        userInfo = cur.fetchall()

        return userInfo

        
t = Tratamiento('13109915-0')         
print(t.tratamiento())