from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(DictionaryPage)
admin.site.register(User)
admin.site.register(GuidebookTopics)
admin.site.register(TaskSimple)
admin.site.register(TaskCategory)
admin.site.register(TaskCompleted)
admin.site.register(Theory)


#admin.site.register(GuidebookTopics)