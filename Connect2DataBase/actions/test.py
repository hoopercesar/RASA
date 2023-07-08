import sqlite3
import os
import pandas as pd
import numpy as np

path = 'C:/Users/Cesar Hooper/Documents/STARTUP/dataset_estudio.db'
con = sqlite3.connect(path, check_same_thread=False)
cur = con.cursor()

cur.execute("SELECT rut FROM dataset_estudio")
rows = cur.fetchall()

print(rows)