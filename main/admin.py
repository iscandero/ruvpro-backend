# Register your models here.

from django.contrib import admin

from .models import *

admin.site.register(Project)

admin.site.register(ProjectEmployee)

admin.site.register(SocialNetwork)

admin.site.register(Team)

admin.site.register(User)

admin.site.register(UsersTeam)

admin.site.register(Transactions)

admin.site.register(TimeEntry)

admin.site.register(Social)

admin.site.register(Role)

admin.site.register(Salary_employee)

admin.site.register(HistoryRate)

admin.site.register(Employee_Statistics)

admin.site.register(Project_Statistics)

admin.site.register(Advance_Statistics)

admin.site.register(HistoryAdvance)
