import numpy as np
import pandas as pd
import statistics as st
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

for var in ['file_data', 'data', 'proc_data']:
    if not(var in locals()):
        exec(var + "=[]")

animation = None
pos = ""

# n = 10
global n, bins

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
    proc_data = []
    inflation = [0,3.16,2.07,1.46,1.62,0.12,1.26,2.13,2.49,1.76,1.23]
    for i in range(11):
        print(i+2010)

        factor = 1
        for pct in inflation[:i+1]:
            factor = factor * (1+pct/100)
        print("Inflation rate of {0}".format(factor))

        temp = select_data(title=pos, year=i+2010)['Salary'].values / factor
        proc_data.append(temp)

def update_data(i, x_max=40000, y_max=600):
    global animation, proc_data, n, bins
    plt.cla()

    bins = np.linspace(0, x_max, 50)
    
    if i != 10:
        plt.hist(proc_data[i], bins=bins, lw = 1, ec="darkslategray", fc = "#073642")
    else:
        (n, bins, patches) = plt.hist(proc_data[i], bins=bins, lw = 1, ec="darkslategray", fc = "#073642")
    plt.axis([0, x_max, 0, y_max])
    # plt.gca().set_ylim(bottom=0)

    print(max(proc_data[i]))
    
    plt.gca().set_title('Inflation-Adjusted Compensation for {0}s from 2010-2020'.format("".join([s[0] for s in pos.split()])), fontweight='bold')
    plt.gca().set_ylabel('count')
    plt.gca().set_xlabel('compensation in 2010 dollars')

    tick = mtick.StrMethodFormatter('${x:,.0f}')
    plt.gca().xaxis.set_major_formatter(tick)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    
    if i != 0:
        pct_change = round((np.mean(proc_data[i]) - np.mean(proc_data[i-1]))/np.mean(proc_data[i]) * 100,2)
        if pct_change > 0:
            pct_color = "green"
        elif pct_change < 0:
            pct_color = "red"
    else:
        pct_change = "n/a"
        pct_color = "black"

    plt.gca().annotate('{0}: {1} employees'.format(i+2010, len(proc_data[i])), xy=(0.60, 0.92), xycoords='axes fraction')
    plt.gca().annotate('Yearly Avg Change: {0}%'.format(pct_change), xy=(0.60, 0.87), xycoords='axes fraction', color = pct_color)
    print(i + 2010)


def run_anim(reset=False, play=True):
    # set parameters

    global pos 
    pos = "Graduate%Assistant"
    abv = "".join([s[0] for s in pos.split()])

    global animation
    # style.use('seaborn-poster')
    style.use('seaborn-muted')
    # themes.theme_solarized(scheme="dark")
    fig = plt.figure()

    if proc_data == [] or reset:
        prep_data(pos)
    animation = anim.FuncAnimation(fig, update_data, frames=11, interval=500, repeat=False)
    
    if play:
        plt.show()

    # vid = animation.to_html5_video()
    # html = display.HTML(vid)
    if not play:
        writer = anim.writers['ffmpeg'](fps=1.2)
        animation.save('{0}infla.mp4'.format(abv), writer=writer, dpi=300)
        plt.close()
    print("All Finished!")


