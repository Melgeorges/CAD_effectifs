import csv
from sort_utils import *
import pylab as plt
import numpy as np
from datetime import datetime
from datastructures import Shifts, Volunteer

name_column = "anon"


def parse_volunteers(file_adress):
    csvfile = open(file_adress, mode='r')
    csv_reader = csv.DictReader(csvfile)
    volunteer_dict = {}
    availability_by_date = {}
    date_list = []
    for row in csv_reader:
        name = row[name_column]
        if not(name in volunteer_dict):
            skills = {"pse1": row["PSE1"], "pse2": row["PSE2"], "chauf_vpsp": row["chauf_vpsp"],
                      "chauf_vl": row["chauffeur_vl"], "ci": row["ci"], "tsa": row["tsa"],
                      "infirmier": row["infirmier"], "log": row["log"]}
            v = Volunteer(name, skills, [])
            volunteer_dict[name] = v
            availability_by_date[name] = {}
        # 2020-03-23 00:00
        dispo = datetime.strptime(row["dispo"], "%Y-%m-%d %H:%M")
        date_dispo = dispo.date()
        time_dispo = dispo.hour
        if not(date_dispo in availability_by_date[name]):
            availability_by_date[name][date_dispo] = []
        availability_by_date[name][date_dispo].append(time_dispo)
        if not(dispo.date() in date_list):
            date_list.append(date_dispo)
    return date_list, volunteer_dict, availability_by_date


def parse_shifts(file_adress):
    csvfile = open(file_adress, mode='r')
    csv_reader = csv.DictReader(csvfile)
    shift_dict = {}
    for row in csv_reader:
        name = row["name"]
        if not(name in shift_dict):
            s = Shifts(name, int(row["begin"]), int(row["end"]), int(row["priority"]))
            shift_dict[name] = s
        num_people = int(row["number"])
        if row["skill"] == "PSE1":
            shift_dict[name].pse1 = num_people
        if row["skill"] == "PSE2":
            shift_dict[name].pse2 = num_people
        if row["skill"] == "chauf_vpsp":
            shift_dict[name].chauf_vpsp = num_people
        if row["skill"] == "chauffeur_vl":
            shift_dict[name].chauf_vl = num_people
        if row["skill"] == "ci":
            shift_dict[name].ci = num_people
        if row["skill"] == "tsa":
            shift_dict[name].tsa = num_people
        if row["skill"] == "infirmier":
            shift_dict[name].infirmier = num_people
        if row["skill"] == "log":
            shift_dict[name].log = num_people
        if row["skill"] == "noskills":
            shift_dict[name].noskills = num_people
    return shift_dict


def compute_shift_availability(shifts, date_list, volunteers, availability):
    for v in volunteers:
        volunteers[v].availability = {}
        for d in date_list:
            volunteers[v].availability[d] = []
            for s in shifts:
                available = True
                debut = shifts[s].debut
                fin = shifts[s].fin
                heure = int(debut/2)
                while heure < fin:
                    if not(heure in availability[v][d]):
                        available = False
                    heure = heure + 2
                if available:
                    volunteers[v].availability[d].append(s)


def process_shifts_volunteers(shifts_file, volunteers_file):
    date_list, volunteer_dict, availability_by_date = parse_volunteers(volunteers_file)
    shift_dict = parse_shifts(shifts_file)
    compute_shift_availability(shift_dict, date_list, volunteer_dict, availability_by_date)
    return date_list, volunteer_dict, shift_dict
