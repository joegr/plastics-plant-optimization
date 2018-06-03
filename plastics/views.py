from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import OptimizationJob, Job, Machine, SolutionSet, SolutionComponent
from ortools.constraint_solver import pywrapcp
from .forms import OptimizationJobForm, JobForm

def home(request):
    """List all your existing Optimization Jobs.
    Button to create new Optimization Job
    """
    context = {}
    optimization_jobs = OptimizationJob.objects.all()
    context["optimization_jobs"] = optimization_jobs
    return render(request, "plastics/home.html",context)
    

def optimization_job(request, pk):
    """Details of Optimization  Job
    Fully Solved?
    All solutions sorted by makespan?"""
    optimization_job = OptimizationJob.objects.get(pk=pk)
    
    context = {}
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.optimization_job = optimization_job
            instance.save()
            redirect("optimization_job_details", pk=pk )
    else:
        form = JobForm()
    
    jobs = Job.objects.filter(optimization_job = optimization_job)
    solutionsets = SolutionSet.objects.filter(optimization_job=optimization_job)

    context["optimization_job"] = optimization_job
    context["solutionsets"] = solutionsets
    context["jobs"] = jobs
    context["machines"] = Machine.objects.all()
    context["form"] = form
    # Do we need to convert this into////NAHHH...

    return render(request, "plastics/optimization_details.html",context)

def create_new_optimization_job(request):
    """
    1. Create Tasks that need to be performed, and add what machines they can run at. 
    2. Machines are created seperately. Machines are available here to choose from.
    """
    if request.method == "POST":
        print("Got here")
        form = OptimizationJobForm(request.POST)
        if form.is_valid():
            instance = form.save()
            #If saved, lets take to edit optimization job page.
            return redirect("") #Redirect to Edit Optimization Job.
    else:
        form = OptimizationJobForm()

    context = {}
    context["form"] = form 
    return render(request, "plastics/new_optimization_job.html",context)




# Create your views here.
def solve(request, pk):
    print("Got to solve.")
    optimization_job = OptimizationJob.objects.get(pk = pk)
    print(optimization_job)
    #create a new solution set each time.
    #Get a List of Jobs.
    jobs = Job.objects.filter(optimization_job=optimization_job)
    print("jobs are:")
    print(jobs)
    #Get a List of Machines
    machines = []
    for j in jobs:
        print(j.machines.all())
        for m in j.machines.all():
            if m not in machines:
                machines.append(m) #Machines will be in 
    print(machines)
    solver = pywrapcp.Solver("jobscheduler")
    shift_grid = dict()
    #horizon is the sum of all job lengths.
    SCHEDULING_HORIZON = sum([job.duration for job in jobs])
    
    #Start by creating fixeddurationintervalvars.
    for job in jobs:
        for machine in job.machines.all():
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
            if machine.id in [m.id for m in job.machines.all()]:
                shift = shift_grid[(job.id,machine.id)]
                tasks_for_machine.append(shift)
        disj = solver.DisjunctiveConstraint(tasks_for_machine, "machine %s" %machine.id)
        solver.Add(disj)
        all_sequences.append(disj.SequenceVar())

    solution = solver.Assignment()
    shift_list = shift_grid.values() 

    db = solver.Phase(all_sequences,solver.SEQUENCE_DEFAULT)
    #solver.NewSearch(db)
    #num_solution = 0


    ### Solver Example when using collector.


    ### Solver Example when using NextSolution()
    solver.NewSearch(db,)
    num_solution = 0
    print("starting to search")
    print(shift_grid)
    while solver.NextSolution():
        print("solution")
        solutionset = SolutionSet.objects.create(optimization_job=optimization_job)
        num_solution += 1
        #if num_solution > 2:
        #    sys.exit()
        #print("meh")
        makespan = 0 
        for key in shift_grid.keys():
            shift_var = shift_grid[key]
            if shift_var.MustBePerformed():
                start_date = shift_var.StartMin()
                job = Job.objects.get(pk=key[0])
                end_date = start_date + job.duration 

                solution_comp = SolutionComponent.objects.create(
                    job = job,
                    machine = Machine.objects.get(pk=key[1]),
                    start_date = start_date ,
                    end_date = end_date,
                    solutionset = solutionset)
                if end_date > makespan:
                    makespan = end_date
        solutionset.makespan = makespan 
        solutionset.save()

        #Could also produce makespan by doing some sql post processing.
        #sol_comps = SolutionComponents.objects.filter(solutionset = SolutionSet )

        # machines = {}
        # for i in [m.id for m in machines]:
        #     machines[i] = [0,]
        #     machine = machines[i]
        #     #machine_spans = []
        #     for j in range(len(jobs)):
        #         job = jobs[j]       
        #         shift_var = shift_grid[(job.id,machine.id)]
        #         if shift_var.MustBePerformed():
        #             print(shift_var)
        #             start = shift_var.StartMin()
        #             end = start + job.duration
        #             length = jobs.duration
        #             #print("End time ", end)
        #             machines[i].append(end)
        #             #print(machines[i])
                    
        #             #lll= shift_var.StartMin()                
        #             #print(lll)

        # print("Machines : " , machines )
        # max_of_1 = max(machines[1])
        # max_of_2 = max(machines[2])
        # makespan = max([max(machines[i]) for i in [m.id for m in machines]  ]  )
        # print("makeSpan : ", makespan)
    #return redirect("optimization_job_details" , pk=pk)
    return HttpResponse("Done")


    
