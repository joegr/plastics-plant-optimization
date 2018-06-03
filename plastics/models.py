from django.db import models
from django.contrib import admin

#Create your models here.

class OptimizationJob(models.Model):
    title = models.TextField()
    found_all_feasible = models.BooleanField(default=False)

class Machine(models.Model):
    name = models.CharField(max_length=100)
    #optimization_job = models.ForeignKey(OptimizationJob)
    def __str__(self):
        return self.name

class Job(models.Model):
    arrival_date = models.IntegerField()#earliest start date
    machines = models.ManyToManyField(Machine)#compatible machines
    duration = models.IntegerField()
    optimization_job = models.ForeignKey(OptimizationJob, on_delete=models.CASCADE)
    def get_machines_str(self):
        s = ""
        for m in self.machines.all():
            s += "| " +  m.name + " |"
        return s
# For Each Optimization Job we choose a number of jobs.
# and then optimize for it.
# 1 OptimizationJob has many solution Set
# 1 SolutionSet has all the jobs that need to be run.
class SolutionSet(models.Model):
    optimization_job = models.ForeignKey(OptimizationJob, on_delete=models.CASCADE)
    makespan = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return "%s - %s" %(self.optimization_job.title, self.makespan)

    class Meta:
        ordering=["makespan"]

class SolutionComponent(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    start_date = models.IntegerField()
    end_date = models.IntegerField()
    solutionset = models.ForeignKey(SolutionSet, on_delete=models.CASCADE)

    class Meta:
        ordering=["start_date"]

admin.site.register(OptimizationJob)
admin.site.register(Machine)
admin.site.register(Job)
admin.site.register(SolutionSet)
admin.site.register(SolutionComponent)