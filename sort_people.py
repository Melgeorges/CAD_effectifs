import csv
from sort_utils import *
import pylab as plt
import numpy as np


def get_volunteer_skills_and_availability():
    """
    the goal of the script is to return the list of dates, the list of volunteers,
    the skills of volunteers and their availability (1 or 0) corr*esponding to the time of the list of dates.
    
    the output is
    date_list: simple list containing the relevant dates
    volunteer_list: simple list containing the volunteers
    skills: dictionnary skills[volunteer] is a 1d array containing 5 skills:
            is_pse1, is_pse2, is_chauf_vpsp, is_chauffeur_vl,is_ci
    availability: dictionnary, availability[volunteer] is a 1d array containing 1 if volunteer is there 0 otherwise
    """
    csvfile= open("competence_dispos.csv", mode='r')
    csv_reader = csv.DictReader(csvfile)
    volunteer_list = []
    date_list = []
    skills = {}
    for row in csv_reader:
        volunteer = row["anon"]
        skills[volunteer] = [is_pse1(row["PSE1"]), is_pse2(row["PSE2"]), is_chauf_vpsp(row["chauf_vpsp"]),
                             is_chauffeur_vl(row["chauffeur_vl"]), is_ci(row["ci"]), is_tsa(row["tsa"]),
                             is_infirmier(row["infirmier"]), is_log(row["log"])]
        volunteer_list += [volunteer]
        date_list += [row["dispo"]]

    volunteer_list = list(dict.fromkeys(volunteer_list))
    date_list = list(dict.fromkeys(date_list))

    availability={}
    for volunteer in volunteer_list:
        availability[volunteer]= []

    #don't know why I need to repoen (oh well...)
    csvfile= open("competence_dispos.csv", mode='r')
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        volunteer = row["anon"]
        if row["Value"] == "OUI":
            availability[volunteer] += [row["dispo"]]
    
    
    for volunteer in volunteer_list:
        dispo =  {date: 0. for date in date_list}
        for av in availability[volunteer]:
            dispo[av]  = 1.
        dispo = np.array(list(dispo.values()))
        availability[volunteer] = dispo

    return(date_list, volunteer_list, skills, availability)


def keep_one_skill(to_keep: str, to_remove=[]):
    # only keep one kind of skills
    vol = []
    for key, value in skills.items():
        if to_keep in value:
            if to_remove!=[] :
                if set(to_remove).intersection(set(value)) == set():
                    vol.append(key)
            else:
                vol.append(key)
    return vol


def remove_skills(to_remove: list):
    # only keep one kind of skills
    vol = []
    for key, value in skills.items():
        if set(to_remove).intersection(value) == set():
            vol.append(key)
    return vol


# The aim of this plot is to start visualising the data in order to think about how
# to make groups

def make_plots(df, plot_name, n):
    step=50
    i=0
    j=step

    while j<=n:
        to_plot=df[i:j]
        n_to_plot= len(to_plot)
        make_a_plot(to_plot, f"{plot_name}_{j}", n_to_plot)
        i=j
        j=j+step


def make_a_plot(to_plot, plot_name, n_to_plot):

    plt.figure(figsize=(25,20))
    for count, volunteer in enumerate(to_plot):
        linestyle = "-"
        color = "gray"

        if skills[volunteer][2] == "is_chauf_vpsp":
            linestyle ="--"
        elif skills[volunteer][3] == "is_chauffeur_vl":
            linestyle = ":"

        if skills[volunteer][4] == "is_ci":
            color = "red"
        elif skills[volunteer][1] == "is_pse2":
            color = "blue"
        elif skills[volunteer][0] == "is_pse1":
            color = "green"

        # we will put zero to np.nan in order to make the plot cleaner
        id= np.where(availability[volunteer]==0)
        availability[volunteer][id]= np.nan

        plt.plot(date_list,availability[volunteer]+2*count, color=color, linestyle= linestyle)
        plt.xticks(rotation=90)

    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D

    legend_elements = [Line2D([0], [0], color='red', linestyle= "-", lw=1, label='ci'),
                       Line2D([0], [0], color='blue', linestyle= "-", lw=1, label='pse2'),
                       Line2D([0], [0], color='green', linestyle= "-", lw=1, label='pse1'),
                       Line2D([0], [0], color='grey', linestyle= "-", lw=1, label='no skills'),
                       Line2D([0], [0], color='black', linestyle= "-", lw=1, label='pas chauffeur'),
                       Line2D([0], [0], color='black', linestyle= "--", lw=1, label='chauffeur vpsp'),
                       Line2D([0], [0], color='black', linestyle= ":", lw=1, label='chauffeur vl')]

    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.1, 1.1))
    ytick_loc = np.arange(n_to_plot)*2+1
    plt.yticks(ytick_loc, to_plot)
    plt.savefig(f'{plot_name}.png',bbox_inches='tight')
    plt.clf()
    plt.close()












