import pandas as pd
import csv
import pymysql
import sqlalchemy
import sys

comando = sys.argv[1:]

engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/etl') # conecta no banco 
df = pd.read_sql_table('dados', engine)

# consulta feita no proprio dataframe 
if comando[0] == 'Preco':
    print(df[df[comando[0]] == float(comando[1])])
else:
    produto = " ".join(comando[1:])
    print(df[df[comando[0]] == produto])
    