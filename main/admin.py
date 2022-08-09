from django.contrib import admin

from .models import *

admin.site.register(Project)

admin.site.register(ProjectEmployee)

admin.site.register(ProjectTimeEntryHistory)

admin.site.register(Team)

admin.site.register(AppUser)

admin.site.register(TimeEntry)

admin.site.register(Role)

admin.site.register(HistoryAdvance)

admin.site.register(HistoryWorker)

admin.site.register(HistoryProject)

admin.site.register(AuthData)

admin.site.register(SocialNetworks)

admin.site.register(FileUser)

admin.site.register(HistoryRate)

admin.site.register(CurrencyCourse)


