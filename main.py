import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text


# ************ GLOBAL VARIABLES ***************

# Main dictionary
QB_STATS = {}

# Team colors map (2TM for Baker Mayfield since he was traded mid-season)
TEAM_COLORS = { 'KAN': 'red', 'LAC': 'gold', 'TAM': 'darkred', 'MIN': 'purple', 'CIN': 'darkorange', 'DET': 'lightskyblue',
                'BUF': 'blue', 'SEA': 'limegreen', 'JAX': 'mediumturquoise', 'PHI': 'teal', 'GNB': 'green', 'MIA': 'aquamarine',
                'DEN': 'orange', 'LVR': 'black', 'NYG': 'midnightblue', 'HOU': 'crimson', 'IND': 'royalblue', 'NWE': 'navy',
                'NOR': 'tan', 'DAL': 'silver', 'CLE': 'darkorange', 'TEN': 'cornflowerblue', 'SFO': 'firebrick', 'PIT': 'yellow',
                'ARI': 'red', 'CHI': 'navy', 'BAL': 'rebeccapurple', 'ATL': 'firebrick', 'CAR': 'deepskyblue', 'LAR': 'mediumblue',
                'WAS': 'goldenrod', 'NYJ': 'darkgreen', '2TM': 'black'}

# URLs to retrieve html from
URL_QB_STATS = 'https://www.pro-football-reference.com/years/2022/passing.htm'
URL_ADVANCED_QB_STATS = 'https://www.pro-football-reference.com/years/2022/passing_advanced.htm'


# *************** FUNCTIONS USED ******************

def ConvertQBName(qb_name):

    new_string = ''
    new_string += qb_name.split(' ')[0][0]
    new_string += '. '
    new_string += qb_name.split(' ')[1]

    return new_string
def MakeScatterPlot(stat_index_1, stat_index_2, title, x_label, y_label):

    f = plt.figure()
    f.set_figwidth(11.2)
    f.set_figheight(8.4)

    for qb in QB_STATS:

        plt.scatter(QB_STATS[qb][stat_index_1], QB_STATS[qb][stat_index_2], c = QB_STATS[qb][7])

    x = np.array([QB_STATS[qb][stat_index_1] for qb in QB_STATS])
    y = np.array([QB_STATS[qb][stat_index_2] for qb in QB_STATS])

    texts = [plt.text(x[i], y[i], ConvertQBName(list(QB_STATS)[i])) for i in range(len(x))]

    adjust_text(texts, expand_points = (1.0, 2.3), autoalign = 'y', precision = 0.001,
                arrowprops = dict(arrowstyle = '-', color = 'gray', lw = 1.25))

    plt.axvline(x=np.average(x), color='r', linestyle='--', label="red line", lw=0.5)
    plt.axhline(y=np.average(y), color='b', linestyle='--', label="blue line", lw=0.5)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.show()


# ********** INITIAL INFO AND STATS ON QBS *************

data = requests.get(URL_QB_STATS)
html = BeautifulSoup(data.text, 'html.parser')
qb_stat_rows = html.select('.table_container tbody tr')

for row in qb_stat_rows:

    if len(row) == 31:

        qb_name = row.select('.left')[0].get_text()
        qb_name = qb_name.replace('*', '')
        qb_name = qb_name.replace('+', '')
        qb_team = row.select('.left')[1].get_text()
        qb_attempts = int(row.select('.right')[6].get_text())

        if qb_attempts >= 200:

            qb_rating = float(row.select('.right')[19].get_text())
            qb_adjusted_yards_per_attempt = float(row.select('.right')[15].get_text())
                                   # first and secondgraph  |       # third and fourth graph
            temp_array = [qb_attempts, None, None, qb_rating, None, None, qb_adjusted_yards_per_attempt, TEAM_COLORS[qb_team]]

            QB_STATS[qb_name] = temp_array


# *********** ADVANCED STATS ON QBS *************

data = requests.get(URL_ADVANCED_QB_STATS)
html = BeautifulSoup(data.text, 'html.parser')

advanced_qb_stat_rows_accuracy = html.select('.table_container')[1]
advanced_qb_stat_rows_accuracy = advanced_qb_stat_rows_accuracy.select('tr')

advanced_qb_stat_rows_pressure = html.select('.table_container')[2]
advanced_qb_stat_rows_pressure = advanced_qb_stat_rows_pressure.select('tr')

advanced_qb_stat_rows_playtype = html.select('.table_container')[3]
advanced_qb_stat_rows_playtype = advanced_qb_stat_rows_playtype.select('tr')

# GETTING INFO FROM ACCURACY TAB
for row in advanced_qb_stat_rows_accuracy:

    if len(row) == 19:

        qb_name = row.select('.left')[0].get_text()
        qb_name = qb_name.replace('*', '')
        qb_name = qb_name.replace('+', '')

        if qb_name in QB_STATS:

            qb_on_target_percentage = row.select('.right')[15].get_text()
            qb_on_target_percentage = float(qb_on_target_percentage.replace('%', ''))

            QB_STATS[qb_name][2] = qb_on_target_percentage  # third graph

# GETTING INFO FROM PRESSURE TAB
for row in advanced_qb_stat_rows_pressure:

    if len(row) == 19:

        qb_name = row.select('.left')[0].get_text()
        qb_name = qb_name.replace('*', '')
        qb_name = qb_name.replace('+', '')

        if qb_name in QB_STATS:

            qb_pressure_rate = row.select('.right')[13].get_text()
            qb_pressure_rate = float(qb_pressure_rate.replace('%', ''))

            QB_STATS[qb_name][1] = qb_pressure_rate  # first and second graphs

# GETTING INFO FROM PLAY TYPE TAB
for row in advanced_qb_stat_rows_playtype:

    if len(row) == 18:

        qb_name = row.select('.left')[0].get_text()
        qb_name = qb_name.replace('*', '')
        qb_name = qb_name.replace('+', '')

        if qb_name in QB_STATS:

            qb_rpo_attempts = int(row.select('.right')[9].get_text())
            qb_pa_attempts = int(row.select('.right')[13].get_text())

            qb_rpo_rate = qb_rpo_attempts / QB_STATS[qb_name][0]
            qb_pa_rate = qb_pa_attempts / QB_STATS[qb_name][0]

            QB_STATS[qb_name][4] = qb_rpo_rate
            QB_STATS[qb_name][5] = qb_pa_rate


# Need to tidy up these function titles and axe labels
MakeScatterPlot(1, 2, '2022 QB Pressure and on Target Throw Rates', 'Pressure Rate(%)', 'On Target Throw Rate(%)')
MakeScatterPlot(1, 3, '2022 QB Pressure Rates and Ratings', 'Pressure Rate(%)', 'Quarterback Rating')
MakeScatterPlot(4, 6, '2022 QB RPO Pass Attempt Rates and Adjusted Yards Per Attempt', 'RPO Pass Attempt Rate(%)', 'Adjusted Yards Per Attempt')
MakeScatterPlot(5, 6, '2022 QB Play-Action Pass Attempt Rates and Adjusted Yards Per Attempt', 'Play-Action Pass Attempt Rate(%)', 'Adjusted Yards Per Attempt')


