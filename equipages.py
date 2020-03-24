import pandas as pd
from datetime import datetime, timedelta


date_list = [datetime.strptime(t, '%Y-%m-%d %H:%M') for t in date_list]


def get_volunteer_shift_availability(shift_beginning, shift_ending, shift_name, availability, volunteer, date_list):

    date = shift_beginning
    date_available = np.array(date_list)[availability[volunteer].astype(bool)]
    volunteer_shift = 0
    counter = 0
    while date < shift_ending-timedelta(hours=2):
        if date in date_available:
            volunteer_shift += 1
        else:
            pass
        date = date + timedelta(hours=2)
        counter += 1

    if counter == volunteer_shift:
        return shift_name


day_numb, day_name = 25, "mercredi"



class Shifts:
    def __init__(self, name, begin, end, priority, skills: dict):
        self.name=name
        self.begin=begin
        self.end=end
        self.priority=priority

        # skills for the shift
        self.pse1 = skills["pse1"]
        self.pse2 = skills["pse2"]
        self.chauf_vpsp = skills["chauf_vpsp"]
        self.chauf_vl = skills["chauf_vl"]
        self.tsa = skills["tsa"]
        self.log = skills["log"]
        self.infirmier = skills["infirmier"]


alpha_matin = Shifts()

shifts = {f"alpha_matin_{day_name}": {"begin": datetime(2020, 3, day_numb, 10, 0),
                                      "end": datetime(2020, 3, day_numb, 16, 0),
                                      "skills": ["is_ci", "is_pse2", "is_chauf_vpsp"],
                                      "priority": 1000}
          f"alpha_aprem_{day_name}": {"begin": datetime(2020, 3, day_numb, 16, 0),
                                      "end": datetime(2020, 3, day_numb, 23, 0),
                                      "skills": ["is_ci", "is_pse2", "is_chauf_vpsp"]},
          f"tsa_matin_{day_name}": {"begin": datetime(2020, 3, day_numb, 10, 0),
                                      "end": datetime(2020, 3, day_numb, 16, 0),
                                      "skills": ["is_tsa"]},
          f"regul_aprem_{day_name}": {"begin": datetime(2020, 3, day_numb, 16, 0),
                                      "end": datetime(2020, 3, day_numb, 23, 0),
                                      "skills": ["is_tsa"]},
          f"coviad_{day_name}": {"begin": datetime(2020, 3, day_numb, 20, 0),
                                      "end": datetime(2020, 3, day_numb, 23, 0),
                                      "skills": ["is_pse2"]},
          f"vlums_{day_name}": {"begin": datetime(2020, 3, day_numb, 10, 0),
                                 "end": datetime(2020, 3, day_numb, 20, 0),
                                 "skills": ["is_pse2", "is_ci"]},

          }


volunteers_shifts={}
for vol in volunteer_list:
    shifts_available = []
    for i in range(len(shift_begin)):
        shifts_available.append(get_volunteer_shift_availability(shift[i][0], shift_end[i][1], shift_names[i],
                                                                 availability, vol, date_list))

    volunteers_shifts[vol] = shifts_available



