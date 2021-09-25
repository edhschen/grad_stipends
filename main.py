import numpy as np
import pandas as pd
from pandasql import sqldf
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.style as style
import matplotlib.ticker as mtick
import pyplot_themes as themes
import seaborn as sns
from IPython import display
import sqlite3
from sqlite3 import Error
import csv

con = sqlite3.connect("salary.db")
cur = con.cursor()
mysql = lambda q: sqldf(q, globals())


# file_data = []
# data = None
animation = None
# proc_data = []
pos = "Student Assistant"

# n = 10

def create_table():
    cur.execute("CREATE TABLE All_Salaries(NAME TEXT, TITLE TEXT, SALARY REAL, TRAVEL REAL, ORGANIZATION TEXT, FISCAL_YEAR INT)")

def import_data():
    global file_data, data

    with open('gt.txt', newline='') as file:
        file_data = list(csv.reader(file))
    
    data = pd.DataFrame(file_data, columns = ['Name', 'Title', 'Salary', 'Travel', 'Organization', 'Fiscal_Year'])
    data[['Salary','Travel']] = data[['Salary','Travel']].astype('float64')
    data['Fiscal_Year'] = data['Fiscal_Year'].astype('int64')

    return data

def select_data(title="", org="", year="", limit=None):
    return mysql('SELECT * FROM data WHERE Title LIKE "%{0}%" AND Organization LIKE "%{1}%" AND Fiscal_Year LIKE "%{2}%";'.format(title, org, year))
    
def prep_data(pos):
    global proc_data
    for i in range(11):
        print(i+2010)
        temp = select_data(title=pos, year=i+2010)['Salary'].values
        proc_data.append(temp)

def update_data(i):
    global animation, proc_data
    # pos = "Graduate Teaching Assistant"
    # if i == n:
    #     animation.event_source.stop()
    plt.cla()

    bins = np.linspace(0, 10000, 50)
    # proc_data = select_data(title=pos, year=i+2010)['Salary'].values
    
    plt.hist(proc_data[i], bins=bins, lw = 1, ec="darkslategray", fc = "#073642")
    plt.axis([0, 10000, 0, 500])
    # plt.gca().set_ylim(bottom=0)
    plt.gca().set_title('Compensation for SAs from 2010-2020', fontweight='bold')
    plt.gca().set_ylabel('count')
    plt.gca().set_xlabel('compensation')
    tick = mtick.StrMethodFormatter('${x:,.0f}')
    plt.gca().xaxis.set_major_formatter(tick)
    plt.gca().annotate('{0}: {1} employees'.format(i+2010, len(proc_data[i])), xy=(0.65, 0.92), xycoords='axes fraction')
    # for i in range(2010, 2021):
    print(i + 2010)
    
    # plt.hist(data, 100)

def run_anim():
    global animation
    # style.use('seaborn-poster')
    style.use('seaborn-muted')
    # themes.theme_solarized(scheme="dark")
    fig = plt.figure()

    if proc_data == []:
        prep_data(pos)
    animation = anim.FuncAnimation(fig, update_data, frames=11, interval=700)
    # plt.show()
    # vid = animation.to_html5_video()
    # html = display.HTML(vid)
    
    writer = anim.writers['ffmpeg'](fps=1.5)
    animation.save('GTA.mp4', writer=writer, dpi=300)
    plt.close()
    print("hi")


