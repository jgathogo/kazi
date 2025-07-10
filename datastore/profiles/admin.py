# datastore/profiles/admin.py
from django.contrib import admin
from .models import Firm, Consultant, Education, Certification, Assignment, Publication, Language

admin.site.register(Firm)
admin.site.register(Consultant)
admin.site.register(Education)
admin.site.register(Certification)
admin.site.register(Assignment)
admin.site.register(Publication)
admin.site.register(Language)