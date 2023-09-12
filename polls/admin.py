from django.contrib import admin
from polls.models import  Insurance, Office, Agent, Contract, Object

# Register your models here.

admin.site.register(Insurance)
admin.site.register(Office)
admin.site.register(Agent)
admin.site.register(Contract)
admin.site.register(Object)

