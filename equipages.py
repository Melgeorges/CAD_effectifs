import pandas as pd
from datetime import datetime, timedelta


date_list = [datetime.strptime(t, '%Y-%m-%d %H:%M') for t in date_list]


def get_volunteer_shift_availability(classe, availability, volunteer, date_list, skills):

    date = classe.begin
    date_available = np.array(date_list)[availability[volunteer].astype(bool)]
    volunteer_shift = 0
    counter = 0
    while date < classe.end-timedelta(hours=2):
        if date in date_available:
            volunteer_shift += 1
        else:
            pass
        date = date + timedelta(hours=2)
        counter += 1

    if counter == volunteer_shift:
        return classe.name


day_numb, day_name = 25, "mercredi"


class Shifts:
    def __init__(self, name, begin, end, priority):
        self.name=name
        self.begin=begin
        self.end=end
        self.priority=priority

        # skills for the shift
        self.ci = 0
        self.pse1 = 0
        self.pse2 = 0
        self.chauf_vpsp = 0
        self.chauf_vl = 0
        self.tsa = 0
        self.log = 0
        self.infirmier = 0
        self.noskills = 0

        #collision
        self.collision=[]


alpha_matin_a = Shifts(name= f"alpha_matin_a_{day_name}",
                     begin= datetime(2020, 3, day_numb, 10, 0),
                     end= datetime(2020, 3, day_numb, 16, 0),
                     priority= 1000)
alpha_matin_a.ci=1
alpha_matin_a.chauf_vpsp=1
alpha_matin_a.pse2=1
alpha_matin_a.collision = [f"alpha_matin_b_{day_name}"]

alpha_matin_b = Shifts(name= f"alpha_matin_b_{day_name}",
                     begin= datetime(2020, 3, day_numb, 10, 0),
                     end= datetime(2020, 3, day_numb, 16, 0),
                     priority= 1000)
alpha_matin_b.ci = 1
alpha_matin_b.chauf_vpsp=1
alpha_matin_b.pse2=1
alpha_matin_b.collision = [f"alpha_matin_a_{day_name}"]


alpha_aprem_a = Shifts(name= f"alpha_aprem_a_{day_name}",
                     begin= datetime(2020, 3, day_numb, 16, 0),
                     end= datetime(2020, 3, day_numb, 23, 0),
                     priority= 1000)
alpha_aprem_a.ci=1
alpha_aprem_a.chauf_vpsp=1
alpha_aprem_a.pse2=1
alpha_aprem_a.collision = [f"alpha_aprem_b_{day_name}"]


alpha_aprem_b = Shifts(name=f"alpha_matin_b_{day_name}",
                       begin= datetime(2020, 3, day_numb, 16, 0),
                       end= datetime(2020, 3, day_numb, 20, 0),
                       priority= 1000)
alpha_aprem_b.ci = 1
alpha_aprem_b.chauf_vpsp=1
alpha_aprem_b.pse2=1
alpha_aprem_b.collision = [f"alpha_aprem_a_{day_name}"]


shifts = [alpha_matin_a, alpha_matin_b, alpha_aprem_a, alpha_aprem_b]
volunteers_shifts = {}



for vol in volunteer_list:
    shifts_available = []
    for c in shifts:
        shifts_available.append(get_volunteer_shift_availability(c, availability, vol, date_list, skills))

    volunteers_shifts[vol] = shifts_available



