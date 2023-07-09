# import sqlite3
# import os
# import pandas as pd
# import numpy as np

# ruts = ['14859287-k', '10533064-2', '11437936-0', '18218988-k', '15368887-7']

# path = 'C:/Users/Cesar Hooper/Documents/STARTUP/dataset_estudio.db'
# con = sqlite3.connect(path, check_same_thread=False)
# cur = con.cursor()
# rut = '15368887-7'

# cur.execute("SELECT * FROM dataset_estudio WHERE rut=?", (rut, ))
# rows = cur.fetchall()
# lista = []
# for row in rows:
#     lista.append(row[0])

# cur.execute("SELECT * FROM dataset_estudio")
# datos = cur.fetchall()

# k = 0 
# for dato in datos:
#     if rut == : 
#        print(k, dato)
#     k += 1