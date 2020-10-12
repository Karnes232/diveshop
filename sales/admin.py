from django.contrib import admin
from .models import User, Office, Hotel, Activity, Employee, Management, Sale

# Register your models here.

admin.site.register(User)
admin.site.register(Office)
admin.site.register(Hotel)
admin.site.register(Activity)
admin.site.register(Employee)
admin.site.register(Management)
admin.site.register(Sale)
