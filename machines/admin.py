from django.contrib import admin
from machines.models import MachineGroup, Machine, Inventory
# Register your models here.

admin.site.register(Machine)

admin.site.register(MachineGroup)

admin.site.register(Inventory)
