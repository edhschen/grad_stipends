import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from sqlite3 import Error
import csv

con = sqlite3.connect("salary.db")
cur = con.cursor()
file_data = []
data = None

def create_table():
    cur.execute("CREATE TABLE All_Salaries(NAME TEXT, TITLE TEXT, SALARY REAL, TRAVEL REAL, ORGANIZATION TEXT, FISCAL_YEAR INT)")

def import_data():
    # file_data = [i.strip('\n').split(',') for i in open('SalaryTravelDataExportAllYears.txt')]
    # with open('gt.txt', 'r') as file:
    #     # reader = unicodecsv.reader(file, delimiter = "\n")
    #     # file_data = [i for i in reader]
    #     file_data = file.read().split('\n')
    #     file_data = [list(eval(i)) for i in file_data]

    # for i in range(len(file_data)):
    #     try:
    #         file_data[i] = [file_data[i][0], file_data[i][1], float(file_data[i][2]), float(file_data[i][3]), file_data[i][4], int(file_data[i][5])]
    #     except:
    #         print(file_data[i])
    #         break

    global file_data, data
    with open('gt.txt', newline='') as file:
        file_data = list(csv.reader(file))
    
    data = pd.DataFrame(file_data, columns = ['Name', 'Title', 'Salary', 'Travel', 'Organization', 'Fiscal_Year'])
    data['Salary'] = data['Salary'].astype('float64')
    data['Travel'] = data['Travel'].astype('float64')
    data['Fiscal_Year'] = data['Fiscal_Year'].astype('int64')

    return data

    
    