### General definitions for the problem ###
# skill list. Be careful, skills must have that exact name in volunteer csv and shifts csv
skill_list = ["pse1", "pse2", "chauf_vpsp", "chauf_vl", "ci", "tsa", "log", "infirmier"]

### CSV parsing and data format ###
# name (of volunteer) column in volunteer availability data
name_column = "anon"

# granularity of scheduling timeslots (number of hours, integer)
# slots start at 0:00 and are of the for [n*size_time_slot, (n+1)*size_time_slot]
size_time_slot = 2

# volunteer availability and skills file
volunteers_csv = "anonymise_competence_dispos.csv"

# shifts definition file
shifts_csv = "equipages_formatted.csv"


