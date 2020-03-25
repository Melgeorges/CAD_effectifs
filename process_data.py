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
            availability_by_date[name] = []
        # 2020-03-23 00:00
        dispo = datetime.strptime(row["dispo"], "%Y-%m-%d %H:%M")
        availability_by_date[name].append(dispo)
        if not(dispo.date() in date_list):
            date_list.append(dispo.date())
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
