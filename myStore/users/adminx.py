import xadmin
from . import models

xadmin.site.register(models.Passport)
xadmin.site.register(models.Address)
# Register your models here.
