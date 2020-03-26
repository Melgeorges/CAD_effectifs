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
        self.pse1 = (skills["pse1"] == 'True')
        self.pse2 = (skills["pse2"] == 'True')
        self.chauf_vpsp = (skills["chauf_vpsp"] == 'True')
        self.chauf_vl = (skills["chauf_vl"] == 'True')
        self.ci = (skills["ci"] == 'True')
        self.tsa = (skills["tsa"] == 'True')
        self.log = (skills["log"] == 'True')
        self.infirmier = (skills["infirmier"] == 'True')
        self.availability = availability

    def __repr__(self):
        return "<Volunteer %s, pse1: %r, pse2: %r, " \
               "chauf_vpsp: %r, chauffeur_vl: %r, " \
               "ci: %r, tsa: %r, log %r, availability: %r>" % (self.identity,
                                                self.pse1,
                                                self.pse2,
                                                self.chauf_vpsp,
                                                self.chauf_vl,
                                                self.ci,
                                                self.tsa,
                                                self.log,
                                                self.availability)



class Shifts:
    def __init__(self, name, begin, end, priority):
        self.name = name
        self.begin = begin
        self.end = end
        self.priority = priority

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

        # collision
        self.collision = []

    def __repr__(self):
        return "<shift %r, begin: %r, end: %r, priority: %r, ci: %r, pse1: %r, pse2: %r, chauf_vpsp: %r, " \
               "chauf_vl: %r, tsa: %r, log: %r, infirmier: %r, noskills: %r, collision: %r>" % (
                   self.name, self.begin, self.end, self.priority, self.ci, self.pse1, self.pse2, self.chauf_vpsp,
                   self.chauf_vl, self.tsa, self.log, self.infirmier, self.noskills, self.collision
               )
