import csv
from global_variables import skill_list, size_time_slot, name_column
from datetime import datetime
from datastructures import Shifts, Volunteer




def parse_volunteers(file_adress):
    csvfile = open(file_adress, mode='r')
    csv_reader = csv.DictReader(csvfile)
    volunteer_dict = {}
    availability_by_date = {}
    date_list = []
    for row in csv_reader:
        name = row[name_column]
        if not (name in volunteer_dict):
            skills = {}
            for s in skill_list:
                skills[s] = (row[s] == "True")
            v = Volunteer(name, skills, [])
            volunteer_dict[name] = v
            availability_by_date[name] = {}
        # 2020-03-23 00:00
        dispo = datetime.strptime(row["dispo"], "%Y-%m-%d %H:%M")
        date_dispo = dispo.date()
        time_dispo = dispo.hour
        if not (date_dispo in availability_by_date[name]):
            availability_by_date[name][date_dispo] = []
        if row["Value"] == "OUI":
            availability_by_date[name][date_dispo].append(time_dispo)
        if not (dispo.date() in date_list):
            date_list.append(date_dispo)
    return date_list, volunteer_dict, availability_by_date


def parse_shifts(file_adress):
    csvfile = open(file_adress, mode='r')
    csv_reader = csv.DictReader(csvfile)
    shift_dict = {}
    for row in csv_reader:
        name = row["name"]
        if not (name in shift_dict):
            required_skills = {skill: 0 for skill in skill_list}
            s = Shifts(name, int(row["begin"]), int(row["end"]), int(row["priority"]), required_skills)

            shift_dict[name] = s
        num_people = int(row["number"])
        skill = row["skill"]
        if skill in skill_list:
            shift_dict[name].skills[skill] == num_people
        elif skill == "noskills":
            shift_dict[name].noskills = num_people
        else:
            print("Warning: Unknown skill '%s' encountered when parsing shifts, ignoring the line" % skill)
    return shift_dict


def compute_shift_availability(shifts, date_list, volunteers, availability):
    for v in volunteers:
        volunteers[v].availability = {}
        for d in date_list:
            volunteers[v].availability[d] = []
            for s in shifts:
                available = True
                debut = shifts[s].begin
                fin = shifts[s].end
                heure = size_time_slot * int(debut / size_time_slot)
                #TODO mark as available only if volunteer has a skill in the skill list
                while heure < fin:
                    if not (heure in availability[v][d]):
                        available = False
                    heure = heure + size_time_slot
                if available:
                    volunteers[v].availability[d].append(s)


def parse_shifts_volunteers(shifts_file, volunteers_file):
    date_list, volunteer_dict, availability_by_date = parse_volunteers(volunteers_file)
    shift_dict = parse_shifts(shifts_file)
    compute_shift_availability(shift_dict, date_list, volunteer_dict, availability_by_date)
    return date_list, volunteer_dict, shift_dict
