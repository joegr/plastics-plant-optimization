from django.shortcuts import render
from .models import OptimizationJob, Job, Machine, SolutionSet, SolutionComponents
from ortools.constraint_solver import pywrapcp

# Create your views here.
def solve(request):
    optimization_job = OptimizationJob.objects.get(pk = 1)
    #create a new solution set each time.
    solutionset = SolutionSet.objects.create(optimization_job=optimization_job)
    #Get a List of Jobs.
    jobs = Job.objects.filter(optimization_job=optimization_job)

    #Get a List of Machines
    machines = []
    for j in jobs:
        for m in j.machines:
            if m not in machines:
                machines.append(m) #Machines will be in 
    solver = pywrapcp.Solver("jobscheduler")
    shift_grid = dict()
    #horizon is the sum of all job lengths.
    SCHEDULING_HORIZON = sum([job.duration for job in jobs])
    
    #Start by creating fixeddurationintervalvars.
    for job in jobs:
        for machine in job.machines:
            shift_grid[(job.id,machine.id)] = solver.FixedDurationIntervalVar(job.arrival_date,
                    SCHEDULING_HORIZON,job.duration,True,"shift for job {} / machine {}".format(job.id,machine.id)) 

    #Next Add Constraints 
    #1. Job can only be performed once.
    for job in jobs:
        #Get all the jobs in the shift_grid for this job
        shift_for_this_job = [shift_grid[key] for key in shift_grid.keys() if key[0]==job.id]

        a = solver.Sum([shift.PerformedExpr() for shift in shift_for_this_job])
        solver.Add(a == 1) #Means job must run once and only once.
    
    #2 Disjunctive Constraint : Two jobs cannot run at the same time on one machine
    all_sequences = []
    for machine in machines:
        tasks_for_machine = []
        for job in jobs:
            if machine.id in [m.id for m in job.machines]:
                shift = shift_grid[(job.id,machine.id)]
                tasks_for_machine.append(shift)
        disj = solver.DisjunctiveConstraint(tasks_for_machine, "machine %s" %machine.id)
        solver.Add(disj)
        all_sequences.append(disj.SequenceVar())

    solution = solver.Assignment()
    shift_list = shift_grid.values() 

    db = solver.Phase(all_sequences,solver.SEQUENCE_DEFAULT)
    solver.NewSearch(db)
    num_solution = 0

    solver.NewSearch(db,)

    ### Solver Example when using collector.


    ### Solver Example when using NextSolution()
    num_solution = 0
    while solver.NextSolution():
        num_solution += 1
        #if num_solution > 2:
        #    sys.exit()
        #print("meh")
        machines = {}
        for i in [1,2]:
            machines[i] = [0,]
            #machine_spans = []
            for j in range(len(jobs)):       
                shift_var = shift_grid[(j+1,i)]
                if shift_var.MustBePerformed():
                    print(shift_var)
                    start = shift_var.StartMin()
                    end = start + jobs[j].length
                    length = jobs[j].length
                    #print("End time ", end)
                    machines[i].append(end)
                    #print(machines[i])
                    
                    #lll= shift_var.StartMin()                
                    #print(lll)

        print("Machines : " , machines )
        max_of_1 = max(machines[1])
        max_of_2 = max(machines[2])
        makespan = max([max(machines[i]) for i in [1,2] ]  )
        print("makeSpan : ", makespan)


    
