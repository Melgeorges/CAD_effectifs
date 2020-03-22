from __future__ import print_function
from ortools.sat.python import cp_model
from sort_people import get_volunteer_skills_and_availability



class VolunteersPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_volunteers, num_days, num_shifts, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_volunteers = num_volunteers
        self._num_days = num_days
        self._num_shifts = num_shifts
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for d in range(self._num_days):
                print('Day %i' % d)
                for n in range(self._num_volunteers):
                    is_working = False
                    for s in range(self._num_shifts):
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            print('  Volunteer %i works shift %i' % (n, s))
                    # if not is_working:
                    #     print('  Volunteer {} does not work'.format(n))
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count




def main():
    # Data.
    date_list, volunteer_list, skills, availability = get_volunteer_skills_and_availability()
    # print("date_list",len(date_list),date_list)
    # print("volunteer_list",len(volunteer_list),volunteer_list)
    # print("skills",len(skills),skills)
    # print("availability",len(availability),availability)
    num_volunteers = len(volunteer_list)
    num_shifts = 12
    num_days = int(len(date_list)/num_shifts)
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
                shifts[(n, d,
                        s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))
    # print (shifts)

    # Constraints
    # Renfort Samu : plage horaire de 6 à 12h - compétences : 1 ci, 1 chauf_vpsp, 1 ou 2 PSE2
    for d in all_days:
        for s in all_shifts:
            if s>=3 and s<=5:
                model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if skills[volunteer][4]=="is_ci") == 1)
                model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if skills[volunteer][2]=="is_chauf_vpsp") == 1)
                model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if skills[volunteer][1]=="is_pse2") == 1 or sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if skills[volunteer][1]=="is_pse2") == 2)
    # VLUMS : plage horaire de 6 à 12h - 2 PSE(1 ou 2) - idealement un chauffeur_vl
    # for d in all_days:
    #     for s in all_shifts:
    #         if s>=3 and s<=5:
    #             model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if skills[volunteer][3]=="is_chauffeur_vl") == 1) #TODO: "idéalement"
    #             model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if skills[volunteer][1]=="is_pse2" or skills[volunteer][0]=="is_pse1") == 2)

    # croix rouge chez vous : plage horaire de 4 à 12h - 2 benevoles (pas de compétences particulières) - idealement un chauffeur_vl
    for d in all_days:
        for s in all_shifts:
            if s>=2 and s<=5:
                model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) if skills[volunteer][3]=="is_chauffeur_vl") == 1) #TODO: "idéalement"
                model.Add(sum(shifts[(n, d, s)] for n, volunteer in enumerate(volunteer_list) ) == 2)

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

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Display the first solution.
    a_few_solutions = range(1)
    solution_printer = VolunteersPartialSolutionPrinter(shifts, num_volunteers,
                                                    num_days, num_shifts,
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