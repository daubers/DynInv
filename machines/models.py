from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import hvac
import consul
import uuid


def get_hvac_client():
    v_connection = hvac.Client(url=settings.HVAC_URI, token=settings.HVAC_TOKEN)
    v_connection.secrets.kv.v2.configure(
        mount_point=settings.HVAC_KV_MOUNT_POINT,
    )
    return v_connection


# Create your models here.
class CommonVars(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField(null=True)
    is_in_vault = models.BooleanField()
    vault_path = models.CharField(max_length=255, blank=True, default='')

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = cls(*values)
        instance._state.adding = False
        instance._state.db = db
        # customization to store the original field values on the instance
        instance._loaded_values = dict(zip(field_names, values))
        if instance.is_in_vault:
            try:
                v_connection = get_hvac_client()
                read_response = v_connection.secrets.kv.v2.read_secret_version(path=instance.vault_path,
                                                                               mount_point=settings.HVAC_KV_MOUNT_POINT)
                instance.value = read_response['data']['data'][instance.key]
            except:
                pass
        return instance

    class Meta:
        abstract = True


class Machine(models.Model):
    hostname = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    use_consul = models.BooleanField()
    update_address = models.BooleanField()
    use_vault_for_credentials = models.BooleanField(default=False)
    enabled = models.BooleanField()
    last_update = models.DateTimeField()
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.hostname

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = cls(*values)
        instance._state.adding = False
        instance._state.db = db
        # customization to store the original field values on the instance
        if instance.use_consul:
            try:
                c = consul.Consul()
                consul_data = c.catalog.node(instance.hostname)
                print(instance.hostname)
                instance.ip_address = consul_data[1]['Node']['Address']
            except Exception as e:
                print(e)
                pass
        return instance


class HostVars(CommonVars):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.is_in_vault:
            v_connection = get_hvac_client()
            if self.vault_path is '':
                self.vault_path = "{}::{}::{}".format(settings.HVAC_KV_MOUNT_POINT, uuid.uuid4(), self.key,
                                                      self.machine.hostname)
            print(self.vault_path)
            create_response = v_connection.secrets.kv.v2.create_or_update_secret(
                path=self.vault_path,
                secret={self.key: self.value},
                mount_point=settings.HVAC_KV_MOUNT_POINT
            )
            print(create_response)
            self.value = None
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {}".format(self.machine, self.key)


class MachineGroup(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    machines = models.ManyToManyField(Machine, blank=True)

    def __str__(self):
        return self.name


class GroupVars(CommonVars):
    machine_group = models.ForeignKey(MachineGroup, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.is_in_vault:
            v_connection = get_hvac_client()
            if self.vault_path is '':
                self.vault_path = "{}::{}::{}".format(uuid.uuid4(), self.key, self.machine_group.name)
            create_response = v_connection.secrets.kv.v2.create_or_update_secret(
                path=settings.HVAC_KV_MOUNT_POINT,
                secret={self.key: self.value},
                mount_point=settings.HVAC_KV_MOUNT_POINT
            )
            print(create_response)
            self.value = None
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {}".format(self.machine_group, self.key)


class Inventory(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    machines = models.ManyToManyField(Machine, blank=True)
    machine_groups = models.ManyToManyField(MachineGroup, blank=True)

    def __str__(self):
        return self.name

