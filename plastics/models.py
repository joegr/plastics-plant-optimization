from django.db import models

# Create your models here.
class Machine(models.Model):
    name = models.CharField(max_length=100)

class Job(models.Model):
    arrival_date = models.IntegerField()
    machines = models.ManyToManyField(Machine)#compatible machines
    duration = models.IntegerField()

class OptimizationJob(models.Model):
    jobs = models.ManyToManyField(Job)

# For Each Optimization Job we choose a number of jobs.
# and then optimize for it.
