from django.shortcuts import render
from .models import OptimizationJob
from ortools.constraint_solver import pywrapcp
# Create your views here.
def solve(request):
    optimization_job = OptimizationJob.objects.get(pk = 1)
    #Get a List of Jobs.
    jobs = optimization_job.jobs 
    #Get a List of Machines
    machines = []
    for j in jobs:
        for m in j.machines:
            if m not in machines:
                machines.append(m)
    solver = pywrapcp.Solver("jobscheduler")
    shift_grid = dict()
    #horizon is the sum of all job lengths.
    SCHEDULING_HORIZON = sum([job.duration for job in jobs])
    
    #Start by creating fixeddurationintervalvars.
    for job in jobs:
        for resource in job.machines:
            shift_grid[(job.id,resource.id)] = solver.FixedDurationIntervalVar(job.arrival_date,
                    SCHEDULING_HORIZON,job.duration,True,"shift for job {} / resource {}".format(job.id,resource.id)) 

    #Next Add Constraints 
    #1. Job can only be performed once.
    for job in jobs:
        #Get all the jobs in the shift_grid for this job
        shift_for_this_job = [shift_grid[key] for key in shift_grid.keys() if key[0]==job.id]

        a = solver.Sum([shift.PerformedExpr() for shift in shift_for_this_job])
        solver.Add(a == 1) #Means job must run once and only once.
    #2 Disjunctive Constraint : Two jobs cannot run at the same time on one machine
    all_sequences = []
    for resource in machines:
        tasks_for_resource = []
        for job in jobs:
            if resource.id in [j.id for j in job.machines]:
                shift = shift_grid[(job.id,resource.id)]
                tasks_for_resource.append(shift)
        disj = solver.DisjunctiveConstraint(tasks_for_resource, "machine %s" %resource.id)
        solver.Add(disj)
        all_sequences.append(disj.SequenceVar())

    solution = solver.Assignment()
    shift_list = shift_grid.values() 

    db = solver.Phase(all_sequences,solver.SEQUENCE_DEFAULT)
    solver.NewSearch(db)
    num_solution = 0 
    
