import graphene

from graphene_django.types import DjangoObjectType
import machines.models


class MachineType(DjangoObjectType):
    class Meta:
        model = machines.models.Machine


class MachineGroupType(DjangoObjectType):
    class Meta:
        model = machines.models.MachineGroup


class InventoryType(DjangoObjectType):
    class Meta:
        model = machines.models.Inventory


class Query(object):
    all_machines = graphene.List(MachineType)
    all_machine_groups = graphene.List(MachineGroupType)
    all_inventory = graphene.List(InventoryType)

    def resolve_all_machines(self, info, **kwargs):
        return machines.models.Machine.objects.all()

    def resolve_all_inventory(self, info, **kwargs):
        return machines.models.Inventory.objects.all()

    def resolve_all_machine_groups(self, info, **kwargs):
        return machines.models.MachineGroup.objects.all()


