class Volunteer:
    """
    def __init__(self, identity, skills, availability):
        self.identity = identity
        # skills order is is_pse1, is_pse2, is_chauf_vpsp, is_chauffeur_vl,is_ci
        self.pse1 = True if skills[0] == "pse1" else False
        self.pse2 = True if skills[1] == "pse2" else False
        self.chauf_vpsp = True if skills[2] == "chauf_vpsp" else False
        self.chauf_vl = True if skills[3] == "chauf_vl" else False
        self.ci = True if skills[4] == "ci" else False
        self.tsa = True if skills[5] == "tsa" else False
        self.log = True if skills[7] == "log" else False
        self.infirmier = True if skills[6] == "infirmier" else False
        self.availability = availability
    """
    def __init__(self, identity, skills, availability):
        self.identity = identity
        # skills order is is_pse1, is_pse2, is_chauf_vpsp, is_chauffeur_vl,is_ci
        self.skills = skills
        self.availability = availability

    def __repr__(self):
        return "<Volunteer %s, %r, availability: %r>" % (self.identity, self.skills, self.availability)



class Shift:
    def __init__(self, name, begin, end, priority, required_skills):
        self.name = name
        self.begin = begin
        self.end = end
        self.priority = priority

        # skills for the shift
        self.skills = required_skills
        self.noskills = 0

    def __repr__(self):
        return "<shift %r, begin: %r, end: %r, priority: %r, %r, noskills: %r>" % (
                   self.name, self.begin, self.end, self.priority, self.skills, self.noskills
               )


class Problem:
    def __init__(self, volunteers, shifts, dates):
        self.volunteers = volunteers
        self.shifts = shifts
        self.dates = dates
