from __future__ import print_function
from ortools.sat.python import cp_model
from sort_people import get_volunteer_skills_and_availability
from equipages import *


class Volunteer:
    def __init__(self, identity, skills, availability):
        self.identity = identity
        # skills order is is_pse1, is_pse2, is_chauf_vpsp, is_chauffeur_vl,is_ci
        self.pse1 = True if skills[0] == "is_pse1" else False
        self.pse2 = True if skills[1] == "is_pse2" else False
        self.chauf_vpsp = True if skills[2] == "is_chauf_vpsp" else False
        self.chauf_vl = True if skills[3] == "is_chauf_vl" else False
        self.ci = True if skills[4] == "is_ci" else False
        self.tsa = True if skills[5] == "is_tsa" else False
        self.log = True if skills[7] == "is_log" else False
        self.infirmier = True if skills[6] == "is_infirmier" else False
        self.availability = availability

    def __repr__(self):
        return "Volunteer %s, pse1: %r, pse2: %r, " \
               "chauf_vpsp: %r, chauffeur_vl: %r, " \
               "ci: %r, tsa: %r, log %r, availability: %r" % (self.identity,
                                                self.pse1,
                                                self.pse2,
                                                self.chauf_vpsp,
                                                self.chauf_vl,
                                                self.ci,
                                                self.tsa,
                                                self.log,
                                                self.availability)


def create_volunteers(volunteer_list, skills, availability):
    structured_volunteer_list = []
    for v in volunteer_list:
        new_volunteer = Volunteer(v, skills[v], availability[v])
        structured_volunteer_list.append(new_volunteer)
    return structured_volunteer_list


def create_model(model, volunteer_list, date_list, shift_list):
    # precomputations
    identity_list = []
    volunteer_dict = {vol.identity: vol for vol in volunteer_list}
    for v in volunteer_list:
        identity_list.append(v.identity)

    assignment = {}
    # creation of boolean variables 1 variable/(volunteer, date, shift where the volunteer is available)
    for v in volunteer_list:
        for d in date_list:
            for s in shift_list:
                if s.name in v.availability[d]:
                    assignment[(v.identity, d, s.name)] = model.NewBoolVar('assignment_v%rd%rs%r' % (v.identity, d, s.name))

    # constraints: each shift is populated
    for d in date_list:
        for s in shift_list:
            model.Add(sum(assignment[(identity, d, s.name)] for identity,
                    identity in enumerate(identity_list) if volunteer_dict[identity].ci and s.name in volunteer_dict[identity].availability[d]) >= s.ci)
            model.Add(sum(assignment[(identity, d, s.name)] for identity,
                    identity in enumerate(identity_list) if volunteer_dict[identity].pse1 and s.name in volunteer_dict[identity].availability[d]) >= s.pse1)
            model.Add(sum(assignment[(identity, d, s.name)] for identity,
                    identity in enumerate(identity_list) if volunteer_dict[identity].pse2 and s.name in volunteer_dict[identity].availability[d]) >= s.pse2)
            model.Add(sum(assignment[(identity, d, s.name)] for identity,
                    identity in enumerate(identity_list) if volunteer_dict[identity].chauf_vpsp and s.name in volunteer_dict[identity].availability[d]) >= s.chauf_vpsp)
            model.Add(sum(assignment[(identity, d, s.name)] for identity, identity in enumerate(identity_list) if
                          volunteer_dict[identity].chauf_vl and s.name in volunteer_dict[identity].availability[d]) >= s.chauf_vl)
            model.Add(sum(assignment[(identity, d, s.name)] for identity, identity in enumerate(identity_list) if
                          volunteer_dict[identity].tsa and s.name in volunteer_dict[identity].availability[d]) >= s.tsa)
            model.Add(sum(assignment[(identity, d, s.name)] for identity, identity in enumerate(identity_list) if
                          volunteer_dict[identity].log and s.name in volunteer_dict[identity].availability[d]) >= s.log)
            model.Add(sum(assignment[(identity, d, s.name)] for identity, identity in enumerate(identity_list) if
                          s.name in volunteer_dict[identity].availability[d]) >= s.log)

    return assignment


class VolunteersPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, assignment, volunteer_dict, date_list, shifts, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._assignment = assignment
        self._volunteer_dict = volunteer_dict
        self._date_list = date_list
        self._shifts = shifts
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for d in self._date_list:
                print('date %r' % d)
                for identity in self._volunteer_dict:
                    is_working = False
                    for s in self._shifts:
                        if s in self._volunteer_dict[identity].availability[d] and self.Value(self._assignment[(identity, d, s.name)]):
                            is_working = True
                            print('  Volunteer %r works shift %i' % (identity, s.name))
                    # if not is_working:
                    #     print('  Volunteer {} does not work'.format(n))
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count


def main():
    # Data.
    date_list, volunteer_list, skills, availability = get_volunteer_skills_and_availability()
    availability = get_shifts_availability(date_list, volunteer_list, skills, availability)
    shifts = create_shifts()
    volunteers = create_volunteers(volunteer_list, skills, availability)
    volunteer_dict = {vol.identity: vol for vol in volunteers}
    # print("date_list",len(date_list),date_list)
    # print("volunteer_list",len(volunteer_list),volunteer_list)
    # print("skills",len(skills),skills)
    # print("availability",len(availability),availability)
    model = cp_model.CpModel();
    assignment = create_model(model,volunteers, date_list, shifts)
    '''
    num_volunteers = len(volunteer_list)
    num_shifts = 12
    num_days = int(len(date_list) / num_shifts)
    # all_volunteers = range(num_volunteers)
    # all_shifts = range(num_shifts)
    # all_days = range(num_days)
    all_volunteers = range(num_volunteers)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: volunteer 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_volunteers:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))
    # print (shifts)

    # Constraints
    # Renfort Samu : plage horaire de 6 à 12h - compétences : 1 ci, 1 chauf_vpsp, 1 ou 2 PSE2
    for d in all_days:
        for s in all_shifts:
            if s >= 3 and s <= 5:
                model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if
                              skills[volunteer][4] == "is_ci") == 1)
                model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if
                              skills[volunteer][2] == "is_chauf_vpsp") == 1)
                model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if
                              skills[volunteer][1] == "is_pse2") == 1 or sum(
                    shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if
                    skills[volunteer][1] == "is_pse2") == 2)
    # VLUMS : plage horaire de 6 à 12h - 2 PSE(1 ou 2) - idealement un chauffeur_vl
    # for d in all_days:
    #     for s in all_shifts:
    #         if s>=3 and s<=5:
    #             model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if skills[volunteer][3]=="is_chauffeur_vl") == 1) #TODO: "idéalement"
    #             model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if skills[volunteer][1]=="is_pse2" or skills[volunteer][0]=="is_pse1") == 2)

    # croix rouge chez vous : plage horaire de 4 à 12h - 2 benevoles (pas de compétences particulières) - idealement un chauffeur_vl
    for d in all_days:
        for s in all_shifts:
            if s >= 2 and s <= 5:
                model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if
                              skills[volunteer][3] == "is_chauffeur_vl") == 1)  # TODO: "idéalement"
                model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list)) == 2)

    # Each volunteer works at most four shift per day.
    for n in all_volunteers:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 4)

    # min_shifts_per_volunteer is the largest integer such that every volunteer
    # can be assigned at least that many shifts. If the number of volunteers doesn't
    # divide the total number of shifts over the schedule period,
    # some volunteers have to work one more shift, for a total of
    # min_shifts_per_volunteer + 1.

    # min_shifts_per_volunteer = (num_shifts * num_days) // num_volunteers
    # max_shifts_per_volunteer = min_shifts_per_volunteer + 1
    # for n in all_volunteers:
    #     num_shifts_worked = sum(
    #         shifts[(n, d, s)] for d in all_days for s in all_shifts)
    #     model.Add(min_shifts_per_volunteer <= num_shifts_worked)
    #     model.Add(num_shifts_worked <= max_shifts_per_volunteer)
    '''
    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Display the first solution.
    a_few_solutions = range(1)
    solution_printer = VolunteersPartialSolutionPrinter(assignment, volunteer_dict,
                                                        date_list, shifts,
                                                        a_few_solutions)
    solver.SearchForAllSolutions(model, solution_printer)

    # Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())


if __name__ == '__main__':
    main()
