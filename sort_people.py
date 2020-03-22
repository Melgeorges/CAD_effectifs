import csv
from sort_utils import *
import pylab as plt
import numpy as np


def get_volunteer_skills_and_availability():
    """
    the goal of the script is to return the list of dates, the list of volunteers,
    the skills of volunteers and their availability (1 or 0) corresponding to the time of the list of dates.
    
    the output is
    date_list: simple list containing the relevant dates
    volunteer_list: simple list containing the volunteers
    skills: dictionnary skills[volunteer] is a 1d array containing 5 skills:
            is_pse1, is_pse2, is_chauf_vpsp, is_chauffeur_vl,is_ci
    availability: dictionnary, availability[volunteer] is a 1d array containing 1 if volunteer is there 0 otherwise
    """
    csvfile= open("anonymise_competence_dispos.csv", mode='r')
    csv_reader = csv.DictReader(csvfile)
    volunteer_list = []
    date_list = []
    skills = {}
    for row in csv_reader:
        volunteer = row["anon"]
        skills[volunteer] = [is_pse1(row["PSE1"]), is_pse2(row["PSE2"]), is_chauf_vpsp(row["chauf_vpsp"]), is_chauffeur_vl(row["chauffeur_vl"]), is_ci(row["ci"])]
        volunteer_list += [volunteer]
        date_list += [row["dispo"]]

    volunteer_list = list(dict.fromkeys(volunteer_list))
    date_list = list(dict.fromkeys(date_list))

    availability={}
    for volunteer in volunteer_list:
        availability[volunteer]= []

    #don't know why I need to repoen (oh well...)
    csvfile= open("anonymise_competence_dispos.csv", mode='r')
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



date_list, volunteer_list, skills, availability = get_volunteer_skills_and_availability()
n_volunteer = len(volunteer_list)
print("number of volunteer",n_volunteer)


# The aim of this plot is to start visualising the data in order to think about how
# to make groups

plt.figure(figsize=(25,20))
for count, volunteer in enumerate(volunteer_list):
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
        
    plt.plot(date_list,availability[volunteer]+2*count,color=color, linestyle= linestyle)
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
ytick_loc = np.arange(n_volunteer)*2+1
plt.yticks(ytick_loc, volunteer_list)
plt.savefig('test.png',bbox_inches='tight')
plt.clf()
plt.close()
