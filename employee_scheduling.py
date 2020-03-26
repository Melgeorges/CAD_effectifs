from __future__ import print_function
from ortools.sat.python import cp_model
from sort_people import get_volunteer_skills_and_availability
from datastructures import Shift, Volunteer
from equipages import *
from process_data import *
from global_variables import volunteers_csv, shifts_csv, skill_list



def create_model(model, volunteer_dict, date_list, shift_dict):
    # stats
    number_of_variables = 0
    number_of_constraints = 0
    assignment = {}
    candidates_for_shifts = {}
    #date_list = list(set([d.split(" ")[0] for d in date_list]))
    # creation of boolean variables 1 variable/(volunteer, date, shift where the volunteer is available)

    for d in date_list:
        for sid in shift_dict:
            s = shift_dict[sid]
            skills_for_s = [sk for sk in skill_list if (s.skills[sk] > 0)]
            for skill in skills_for_s:
                candidates = [vid for vid in volunteer_dict
                              if volunteer_dict[vid].skills[skill]
                              and s.name in volunteer_dict[vid].availability[d]]
                candidates_for_shifts[(d, s.name, skill)] = candidates
                for vid in candidates:
                    v = volunteer_dict[vid]
                    assignment[(v.identity, d, s.name, skill)] = model.NewBoolVar('%s_works_%s_on_%s_as_%s' % (v.identity, s.name, d, skill))
                    # TODO ignoring noskills on purpose for the moment
                    print('var: %s_works_%s_on_%s_as_%s' % (v.identity, s.name, d, skill))
                    number_of_variables += 1


    # constraints: each shift is populated
    for d in date_list:
        for sid in shift_dict:
            s = shift_dict[sid]
            for skill in [sk for sk in skill_list if (s.skills[sk] > 0)]:
                available_volunteers = \
                    [volunteer_dict[vid].identity for vid in candidates_for_shifts[(d, s.name, skill)]]
                print([(identity, d, s.name, skill) for identity in available_volunteers])
                print(s.skills[skill])
                model.Add(sum(assignment[(identity, d, s.name, skill)] for identity in available_volunteers) >= s.skills[skill])
                number_of_constraints += 1
                # TODO noskill ignored on purpose
                """
                if s.noskills > 0: 
                    available_volunteers = \
                        [volunteer_dict[vid].identity for vid in volunteer_dict if
                         s.name in volunteer_dict[vid].availability[d]]
                    model.Add(sum(assignment[(identity, d, s.name)] for identity in available_volunteers) >= s.skills[skill])
                    number_of_constraints += 1
                """
            #available_ci = [identity for identity in volunteer_dict if volunteer_dict[identity].ci and s.name in volunteer_dict[identity].availability[d]]
            #model.Add(sum(assignment[(identity, d, s.name)] for identity in available_ci) >= s.ci)
            #model.Add(sum(assignment[(identity, d, s.name)] for identity in identity_list if volunteer_dict[identity].pse1 and s.name in volunteer_dict[identity].availability[d]) >= s.pse1)
            #model.Add(sum(assignment[(identity, d, s.name)] for identity in identity_list if volunteer_dict[identity].pse2 and s.name in volunteer_dict[identity].availability[d]) >= s.pse2)
            #model.Add(sum(assignment[(identity, d, s.name)] for identity in identity_list if volunteer_dict[identity].chauf_vpsp and s.name in volunteer_dict[identity].availability[d]) >= s.chauf_vpsp)
            #model.Add(sum(assignment[(identity, d, s.name)] for identity in identity_list if volunteer_dict[identity].chauf_vl and s.name in volunteer_dict[identity].availability[d]) >= s.chauf_vl)
            #model.Add(sum(assignment[(identity, d, s.name)] for identity in identity_list if volunteer_dict[identity].tsa and s.name in volunteer_dict[identity].availability[d]) >= s.tsa)
            #model.Add(sum(assignment[(identity, d, s.name)] for identity in identity_list if volunteer_dict[identity].log and s.name in volunteer_dict[identity].availability[d]) >= s.log)
            #model.Add(sum(assignment[(identity, d, s.name)] for identity in identity_list if s.name in volunteer_dict[identity].availability[d]) >= s.noskills)
    #print(assignment)
    #print(date_list)
    #print(shift_list)
    #print(volunteer_list)
    print("assignment computed: %i variable, %i constraints" % (number_of_variables, number_of_constraints))
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
                print('date %s' % d)
                for identity in self._volunteer_dict:
                    is_working = False
                    for sid in self._shifts:
                        s = self._shifts[sid]
                        for skill in skill_list:
                            if (identity, d, s.name, skill) in self._assignment\
                                    and self.Value(self._assignment[(identity, d, s.name, skill)]):
                                print('  Volunteer %s works shift %s as %s' % (identity, s.name, skill))
                            """
                            if s.name in self._volunteer_dict[identity].availability[d] \
                                    and (identity, s, s.name, skill) in self._assignment \
                                    and self.Value(self._assignment[(identity, d, s.name, skill)]):
                                is_working = True
                                print('  Volunteer %s works shift %s as %s' % (identity, s.name, skill))
                            """
                    # if not is_working:
                    #     print('  Volunteer {} does not work'.format(n))
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count


def main():
    # Data.
    date_list, volunteer_dict, shift_dict = parse_shifts_volunteers(shifts_csv, volunteers_csv)
    model = cp_model.CpModel()

    assignment = create_model(model, volunteer_dict, date_list, shift_dict)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Display the first solution.
    a_few_solutions = range(1)
    solution_printer = VolunteersPartialSolutionPrinter(assignment, volunteer_dict,
                                                        date_list, shift_dict,
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
    # d, v, a = parse_volunteers("anonymise_competence_dispos.csv")
    # s = parse_shifts("equipages_formatted.csv")
    #date_list, volunteer_dict, shift_dict = parse_shifts_volunteers("equipages_formatted.csv", "anonymise_competence_dispos.csv")
    #model = cp_model.CpModel()
    #assignment = create_model(model, volunteer_dict, date_list, shift_dict)
    main()
    x = 1
