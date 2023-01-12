import numpy as np
import pandas as pd
import statistics as st
from pandasql import sqldf
import sqlite3
from sqlite3 import Error
import csv

# import datafiles
mysql = lambda q: sqldf(q, globals())
df_stip = pd.read_csv('data-phdstipends.csv')#.convert_dtypes()
df_acas = pd.read_csv('data-academicsalaries.csv')#.convert_dtypes()

# convert salary and year to integers
df_stip = df_stip.dropna(subset=['Academic Year', '12 M Gross Pay'])
df_stip['12 M Gross Pay'] = df_stip['12 M Gross Pay'].map(lambda x: x[1:].replace(",","")).astype(int)
df_stip['Academic Year'] = df_stip['Academic Year'].map(lambda x: x.split("-")[0]).astype(int)

# datapoint summary
for df in [df_stip, df_acas]:
    print("\033[1mImported csv with", len(df.index), "entries\033[0m")
    print("columns", list(df.columns), "detected")

# query for phdstipends.com
query_stip = lambda col, input, sort="id": mysql('SELECT * FROM df_stip WHERE LOWER("{0}") LIKE "%{1}%" AND "12 M Gross Pay" IS NOT NULL ORDER BY "{2}" ASC;'.format(col, input, sort))

# query for academicsalaries
query_acas = lambda col, input, sort="id": mysql('SELECT * FROM df_acas WHERE LOWER("{0}") LIKE "%{1}%" AND salary is NOT NULL ORDER BY "{2}" ASC;'.format(col, input, sort))

