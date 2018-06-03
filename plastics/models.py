from django.db import models
from django.contrib import admin

#Create your models here.

class OptimizationJob(models.Model):
    title = models.TextField()
    found_all_feasible = models.BooleanField(default=False)

class Machine(models.Model):
    name = models.CharField(max_length=100)
    #optimization_job = models.ForeignKey(OptimizationJob)

class Job(models.Model):
    arrival_date = models.IntegerField()#earliest start date
    machines = models.ManyToManyField(Machine)#compatible machines
    duration = models.IntegerField()
    optimization_job = models.ForeignKey(OptimizationJob, on_delete=models.CASCADE)
    
# For Each Optimization Job we choose a number of jobs.
# and then optimize for it.
class SolutionSet(models.Model):
    optimization_job = models.ForeignKey(OptimizationJob, on_delete=models.CASCADE)
    
class SolutionComponents(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    start_date = models.IntegerField()
    end_date = models.IntegerField()
    solution = models.ForeignKey(SolutionSet, on_delete=models.CASCADE)


admin.site.register(OptimizationJob)
admin.site.register(Machine)
admin.site.register(Job)
admin.site.register(SolutionSet)
admin.site.register(SolutionComponents)