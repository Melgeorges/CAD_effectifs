from __future__ import print_function
import sys
from ortools.sat.python import cp_model
from sort_people import get_volunteer_skills_and_availability
from datastructures import Shift, Volunteer, Problem
from equipages import *
from process_data import parse_shifts_volunteers
from global_variables import volunteers_csv, shifts_csv, skill_list, two_days_in_a_row


class ShiftModel:
    def __init__(self):
        self.assignment = {}
        self.satisfied_shifts = {}
        self.working_days = {}
        self.consecutive_days = {}
        self.number_of_variables = 0
        self.number_of_constraints = 0


# creation of boolean variables 1 variable/(volunteer, date, shift where the volunteer is available)
def add_volunteer_variables(model, problem, shift_model):
    volunteer_dict = problem.volunteers
    date_list = problem.dates
    shift_dict = problem.shifts
    candidates_for_shifts = {}

    for d in date_list:
        for sid in shift_dict:
            s = shift_dict[sid]
            skills_for_s = [sk for sk in skill_list if (s.skills[sk] > 0)]
            for skill in skills_for_s:
                candidates = [vid for vid in volunteer_dict
                              if volunteer_dict[vid].skills[skill]
                              and s.name in volunteer_dict[vid].availability[d]]
                candidates_for_shifts[(d, sid, skill)] = candidates
                for vid in candidates:
                    v = volunteer_dict[vid]
                    shift_model.assignment[(vid, d, sid, skill)] = \
                        model.NewBoolVar('%s_works_%s_on_%s_as_%s' % (v.identity, s.name, d, skill))
                    # TODO ignoring noskills on purpose for the moment
                    shift_model.number_of_variables += 1


# constraints: each shift is populated ==> optional, trying to maximize.
# shift s on day d is satisfied if satisfied[(s,d)] is True in the solution
# shift_score is the sum of the priorities of all satisfied shifts
def add_populate_shifts_constraints(model, problem, shift_model):
    volunteer_dict = problem.volunteers
    date_list = problem.dates
    shift_dict = problem.shifts

    # Simplifying the problem by not trying to add candidates that can not participate to a shift
    # (not the correct skill or not available)
    candidates_for_shifts = {}
    for d in date_list:
        for sid in shift_dict:
            s = shift_dict[sid]
            skills_for_s = [sk for sk in skill_list if (s.skills[sk] > 0)]
            for skill in skills_for_s:
                candidates = [vid for vid in volunteer_dict
                              if volunteer_dict[vid].skills[skill]
                              and s.name in volunteer_dict[vid].availability[d]]
                candidates_for_shifts[(d, sid, skill)] = candidates

    for d in date_list:
        for sid in shift_dict:
            s = shift_dict[sid]
            var_s_d = model.NewBoolVar("shift %s on day %s" % (s.name, d))
            shift_model.satisfied_shifts[(sid, d)] = var_s_d
            shift_model.number_of_variables += 1
            for skill in [sk for sk in skill_list if (s.skills[sk] > 0)]:
                available_volunteers = \
                    [vid for vid in candidates_for_shifts[(d, sid, skill)]]
                #print([(identity, d, s.name, skill) for identity in available_volunteers])
                #print(s.skills[skill])
                model.Add(
                    sum(shift_model.assignment[(vid, d, sid, skill)] for vid in available_volunteers)
                    == s.skills[skill]
                ).OnlyEnforceIf(var_s_d)
                shift_model.number_of_constraints += 1
                # TODO noskill ignored on purpose
                """
                if s.noskills > 0: 
                    available_volunteers = \
                        [volunteer_dict[vid].identity for vid in volunteer_dict if
                         s.name in volunteer_dict[vid].availability[d]]
                    model.Add(sum(assignment[(identity, d, s.name)] for identity in available_volunteers) >= s.skills[skill])
                    number_of_constraints += 1
                """
    # defining score for shift satisfaction
    shifts_score = model.NewIntVar(0, 1000000000000, "shifts score")
    shift_model.shifts_score = shifts_score
    model.Add(shifts_score == sum(
            shift_model.satisfied_shifts[sid, d]*shift_dict[sid].priority for (sid, d) in shift_model.satisfied_shifts
        )
    )


# constraints: each volunteer may only work one shift per day ==> not optional
# working_days[(vid,d)] is the number of shifts worked by volunteer vid on day d
# Populating working days variables
def add_var_constraint_working_days(model, problem, shift_model):
    volunteer_dict = problem.volunteers
    date_list = problem.dates
    shift_dict = problem.shifts
    all_shifts_skills = []
    for sid in shift_dict:
        for skill in skill_list:
            if shift_dict[sid].skills[skill] > 0:
                all_shifts_skills.append((sid, skill))
    for d in date_list:
        for vid in volunteer_dict:
            v = volunteer_dict[vid]
            var_v_d = model.NewIntVar(0, 366, "%s works on %s" % (v.identity, d))
            shift_model.working_days[(vid, d)] = var_v_d
            possible_assignments = [(vid, d, sh, sk) for (sh, sk)
                                    in all_shifts_skills if (vid, d, sh, sk) in shift_model.assignment]
            if len(possible_assignments) > 0:
                model.Add(var_v_d == sum(shift_model.assignment[assig] for assig in possible_assignments))
                model.Add(var_v_d <= 1)
                shift_model.number_of_constraints += 1
            else:
                model.Add(var_v_d == 0)


# /!\ SHOULD NOT BE CALLED BEFORE ADDING WORKING DAYS CONSTRAINTS
# Computing volunteers that work two days in a row
# Consecutive penalty = \Sigma_{v,d} (v works on d)*(v works on d+1)
# Stores whether employee vid work consecutive days d1, d2 in consecutive_days[(vid,d1,d2)]
def add_constraint_consecutive_days(model, problem, shift_model):
    volunteer_dict = problem.volunteers
    date_list = problem.dates
    shift_dict = problem.shifts
    delta = timedelta(days=1)
    consecutive_dates = [(d1, d2) for d1 in date_list for d2 in date_list if d2 - d1 == delta]
    consecutive_penalty = model.NewIntVar(0, 1000000000, "consecutive_days_penalty")
    shift_model.consecutive_penalty = consecutive_penalty
    penalty_list = []
    for (d1, d2) in consecutive_dates:
        for vid in volunteer_dict:
            v = volunteer_dict[vid]
            penalty_d_v = model.NewBoolVar("%s works on %s and %s" % (v.identity, d1, d2))
            shift_model.consecutive_days[(vid, d1, d2)] = penalty_d_v
            penalty_list.append(penalty_d_v)
            model.AddMultiplicationEquality(penalty_d_v,
                                            [shift_model.working_days[vid, d1], shift_model.working_days[vid, d2]])
    model.Add(consecutive_penalty == sum(penalty_list))


# Setting optimization parameter for the model
def set_model_objective(model, problem, shift_model):
    # Setting model objective: maximizing shift score
    shift_model.fitness = model.NewIntVar(-1000000000, 1000000000, "fitness")
    model.Add(
        shift_model.fitness ==
        shift_model.shifts_score
        - two_days_in_a_row * shift_model.consecutive_penalty
    )
    model.Maximize(shift_model.fitness)


def create_model(model, problem):
    shift_model = ShiftModel()
    add_volunteer_variables(model, problem, shift_model)
    add_populate_shifts_constraints(model, problem, shift_model)
    add_var_constraint_working_days(model, problem, shift_model)
    add_constraint_consecutive_days(model, problem, shift_model)
    print("assignment computed: %i variable, %i constraints" % (
        shift_model.number_of_variables,
        shift_model.number_of_constraints
    ))

    set_model_objective(model, problem, shift_model)
    print("Objective set !")

    return shift_model


class VolunteersPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, assignment, problem, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._assignment = assignment
        self._volunteer_dict = problem.volunteers
        self._date_list = problem.dates
        self._shifts = problem.shifts
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for d in self._date_list:
                print('date %s' % d)
                for sid in self._shifts:
                    s = self._shifts[sid]
                    for identity in self._volunteer_dict:
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


def print_sol(shift_model, problem, solver):
    for d in problem.dates:
        print('date %s' % d)
        for sid in problem.shifts:
            s = problem.shifts[sid]
            print('  %s:' % s.name)
            for vid in problem.volunteers:
                v = problem.volunteers[vid]
                for skill in skill_list:
                    if (vid, d, sid, skill) in shift_model.assignment \
                            and solver.Value(shift_model.assignment[(vid, d, sid, skill)]):
                        print('    %s: %s' % (skill, v.identity,))
            # if not is_working:
            #     print('  Volunteer {} does not work'.format(n))
        print()

    print('unpopulated shifts:')
    all_shifts_ok = True
    for (sid, d) in shift_model.satisfied_shifts:
        if not (solver.Value(shift_model.satisfied_shifts[(sid, d)])):
            all_shifts_ok = False
            print('  %s on %s' % (problem.shifts[sid].name, d))
    if all_shifts_ok:
        print('  None')
    print()

    print('people working consecutive days:')
    no_consecutive_days = True
    for (vid, d1, d2) in shift_model.consecutive_days:
        if solver.Value(shift_model.consecutive_days[(vid, d1, d2)]) == 1:
            no_consecutive_days = False
            print('  %s works on %s and %s' % (problem.volunteers[vid].identity, d1, d2))
    if no_consecutive_days:
        print('  None')
    print()


def main():
    # Data.
    problem = parse_shifts_volunteers(shifts_csv, volunteers_csv)
    model = cp_model.CpModel()

    shift_model = create_model(model, problem)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    #solver.parameters.linearization_level = 0
    # Display the first solution.
    #a_few_solutions = range(2)
    #solution_printer = VolunteersPartialSolutionPrinter(assignment, problem, a_few_solutions)
    #solver.SearchForAllSolutions(model, solution_printer)
    status = solver.Solve(model)

    print_sol(shift_model, problem, solver)
    print(solver.Value(shift_model.fitness))

    # Statistics.
    print()
    print(solver.StatusName(status))
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())
#    print('  - solutions found : %i' % solution_printer.solution_count())


if __name__ == '__main__':
    # d, v, a = parse_volunteers("anonymise_competence_dispos.csv")
    # s = parse_shifts("equipages_formatted.csv")
    #date_list, volunteer_dict, shift_dict = parse_shifts_volunteers("equipages_formatted.csv", "anonymise_competence_dispos.csv")
    #model = cp_model.CpModel()
    #assignment = create_model(model, volunteer_dict, date_list, shift_dict)
    main()
    x = 1
