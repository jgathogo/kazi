# datastore/profiles/admin.py
from django.contrib import admin
from .models import Firm, Project, Consultant, ConsultantRole, Education, Certification, Publication, Language

# --- Inlines for Consultant Admin ---
# Inlines allow us to edit related models on the same page, which is very efficient.

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1  # How many extra empty forms to show

class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1

class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 1

class LanguageInline(admin.TabularInline):
    model = Language
    extra = 1

class ConsultantRoleInline(admin.TabularInline):
    model = ConsultantRole
    extra = 1
    # To make it easier to select projects from a long list
    autocomplete_fields = ['project']

# --- Custom ModelAdmin Classes ---

@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')
    # Add all the related information as tabs on the consultant's detail page
    inlines = [ConsultantRoleInline, EducationInline, CertificationInline, PublicationInline, LanguageInline]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'firm_portfolio', 'start_date', 'end_date')
    search_fields = ('title', 'client__firm_name')
    list_filter = ('firm_portfolio',)
    autocomplete_fields = ['firm_portfolio']
    inlines = [ConsultantRoleInline]

@admin.register(Firm)
class FirmAdmin(admin.ModelAdmin):
    list_display = ('firm_name', 'website', 'email')
    search_fields = ('firm_name',)
    # Group the many fields into logical sections on the edit page
    fieldsets = (
        ('Core Identity', {'fields': ('firm_name', 'tagline', 'founded_year')}),
        ('Contact Information', {'fields': ('email', 'website', 'phone', 'address')}),
        ('Narrative & Vision', {'classes': ('collapse',), 'fields': ('vision', 'mission', 'approach_summary')}),
        ('Capabilities & Offerings', {'classes': ('collapse',), 'fields': ('services_offered', 'core_expertise', 'methodologies')}),
        ('Proof Points & Experience', {'classes': ('collapse',), 'fields': ('key_statistics', 'thematic_sectors', 'donor_experience', 'geographical_reach')}),
        ('Proposal Boilerplate', {'classes': ('collapse',), 'fields': ('quality_assurance_statement', 'ethical_commitment_statement', 'sustainability_statement')}),
    )

# We don't need to register Consultant, Project, and Firm again as the @admin.register decorator does it.
# We still register the other models so you can access them directly if needed, though editing via inlines is often easier.
admin.site.register(ConsultantRole)
admin.site.register(Education)
admin.site.register(Certification)
admin.site.register(Publication)
admin.site.register(Language)