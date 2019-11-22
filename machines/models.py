from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Machine(models.Model):
    hostname = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    update_address = models.BooleanField()
    enabled = models.BooleanField()
    last_update = models.DateTimeField()
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.hostname


class MachineGroup(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    machines = models.ManyToManyField(Machine, blank=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    machines = models.ManyToManyField(Machine, blank=True)
    machine_groups = models.ManyToManyField(MachineGroup, blank=True)

    def __str__(self):
        return self.name

