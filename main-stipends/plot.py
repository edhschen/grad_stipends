import matplotlib.pyplot as plt
# import matplotlib.animation as anim
import matplotlib.style as style
import matplotlib.ticker as mtick
from scipy import stats
# import pyplot_themes as themes
import seaborn as sns
from IPython import display

from data import *
mysql2 = lambda q: sqldf(q, globals())

# settings
start_year = 2014
unis = {
    "su": {"name": "Stanford", "color": "firebrick", "query": "Stanford"},
    "mit": {"name": "MIT", "color": "slategray", "query": "MIT"},
    "cit": {"name": "Caltech", "color": "darkorange", "query": "Cal%Tech"},
    "cal": {"name": "Berkeley", "color": "cornflowerblue", "query": "Berkeley"},
    "cornell": {"name": "Cornell", "color": "greenyellow", "query": "Cornell"},
    "nw": {"name": "Northwestern", "color": "purple", "query": "Northwestern"},
    "cmu": {"name": "CMU", "color": "green", "query": "CMU"},
    "duke": {"name": "Duke", "color": "navy", "query": "Duke"},
    "ucla": {"name": "UCLA", "color": "pink", "query": "UCLA"},
    "ucsb": {"name": "UCSB", "color": "cyan", "query": "UCSB"},
    "gt": {"name": "Georgia Tech", "color": "goldenrod", "query": "Georgia%Tech"},
    "rice": {"name": "Rice", "color": "steelblue", "query": "Rice"},
    "ucsc": {"name": "UCSC", "color": "black", "query": "Santa%Cruz"},
}

# data queries
for uni in list(unis.keys()):
    globals()["res_" + uni] = query_stip('University', unis[uni]["query"], "12 M Gross Pay")

# remove outliers
for uni in list(unis.keys()):
    df = eval("res_" + uni)
    df.drop(df[(np.abs(stats.zscore(df['12 M Gross Pay'])) < 2) == False].index, inplace=True) # remove outright liars
    df.drop(df[(np.abs(stats.zscore(df['12 M Gross Pay'])) < 2) == False].index, inplace=True) # remove actual outliers
    df.insert(0, 'Institution', unis[uni]['name'])

# initialize plot
plt.ion()
plt.cla()
style.use('seaborn-muted')

# graph swarm plot
res_main = pd.concat([eval("res_" + uni) for uni in list(unis.keys())])
res_main['Institution'].astype('category')
sns.stripplot(data=res_main, x='Academic Year', y='12 M Gross Pay', order=range(start_year,2023), hue='Institution', dodge=True, palette=[unis[uni]['color'] for uni in list(unis.keys())], size=4)
sns.despine()

# graph trend lines
avgs = mysql2('SELECT Institution, "Academic Year", AVG("12 M GROSS PAY") as Average FROM res_main WHERE "Academic Year" BETWEEN {0} AND 2022 GROUP BY Institution, "Academic Year" ORDER BY Institution, "Academic Year";'.format(start_year))
for uni in list(unis.keys()):
    df_filtered = avgs[avgs['Institution'] == unis[uni]['name']]
    plt.plot(df_filtered['Academic Year']-start_year, df_filtered['Average'], color=unis[uni]['color'], marker="1", linestyle='--', alpha=1)

# add current salary
plt.plot(2022-start_year, 49200, markersize=10, marker="x", color="black")
plt.annotate("CS CA Salary", (2022-start_year+0.1, 49200))

# plot display settings
plt.yticks(np.arange(0, max(res_main['12 M Gross Pay']) + 10000, 5000), fontsize=10)
plt.ylabel("Yearly Stipend")
plt.gca().yaxis.grid(True)
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
plt.xticks(rotation=45, fontsize=10)
plt.gca().set_title('Graduate Student Full-Year Stipend', fontweight="bold", fontsize=15)
