# datastore/profiles/models.py
from django.db import models

class Firm(models.Model):
    # --- Core Identity ---
    firm_name = models.CharField(max_length=255, unique=True, help_text="The official name of the firm.")
    tagline = models.CharField(max_length=500, blank=True, null=True, help_text="A short, memorable slogan or mission statement.")
    founded_year = models.PositiveIntegerField(blank=True, null=True, help_text="The year the firm was established.")
    
    # --- Contact Information ---
    email = models.EmailField(blank=True, null=True, help_text="Primary contact email for the firm.")
    website = models.URLField(max_length=2000, blank=True, null=True, help_text="Official website URL.")
    phone = models.CharField(max_length=50, blank=True, null=True, help_text="Primary contact phone number.")
    address = models.CharField(max_length=255, blank=True, null=True, help_text="Principal office address, e.g., Wilmington, Delaware, USA")

    # --- Narrative & Vision ---
    vision = models.TextField(blank=True, null=True, help_text="The firm's long-term vision statement.")
    mission = models.TextField(blank=True, null=True, help_text="The firm's core mission and purpose.")
    approach_summary = models.TextField(blank=True, null=True, help_text="A summary of the firm's unique approach and methodology.")

    # --- Capabilities & Offerings (using JSONField for flexibility) ---
    services_offered = models.JSONField(blank=True, null=True, help_text="List of key services, e.g., ['Planning', 'Monitoring', 'Evaluation']")
    core_expertise = models.JSONField(blank=True, null=True, help_text="List of cross-cutting expertise, e.g., ['MEL', 'Gender and Social Inclusion']")
    methodologies = models.JSONField(blank=True, null=True, help_text="List of specific evaluation methodologies used, e.g., ['Contribution Analysis', 'Process Tracing']")

    # --- Proof Points & Experience ---
    key_statistics = models.JSONField(blank=True, null=True, help_text="Key impact numbers, e.g., {'donor_funding': '140M', 'countries': 40}")
    thematic_sectors = models.JSONField(blank=True, null=True, help_text="List of sectors the firm works in, e.g., ['Education', 'Health', 'Human Rights']")
    donor_experience = models.JSONField(blank=True, null=True, help_text="List of funders the firm has worked with.")
    geographical_reach = models.JSONField(blank=True, null=True, help_text="List of regions or continents of operation.")

    # --- Boilerplate for Proposals ---
    quality_assurance_statement = models.TextField(blank=True, null=True, help_text="Standard text describing QA mechanisms.")
    ethical_commitment_statement = models.TextField(blank=True, null=True, help_text="Standard text on ethical and child-friendly research.")
    sustainability_statement = models.TextField(blank=True, null=True, help_text="Standard text on building for sustainability and adaptability.")

    def __str__(self):
        return self.firm_name


# --- NEW: Central Project Model ---
# This model stores the official, "firm-level" view of a project.
class Project(models.Model):
    title = models.CharField(max_length=255, unique=True)
    client = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    # The official, high-level summary for proposals
    project_summary = models.TextField(blank=True, null=True)
    
    # Technical details from the firm's perspective
    sectors = models.JSONField(blank=True, null=True)
    methodologies = models.JSONField(blank=True, null=True)
    
    # Link to the primary firm that holds this project in its portfolio
    firm_portfolio = models.ForeignKey(Firm, on_delete=models.SET_NULL, blank=True, null=True, related_name='projects', help_text="The firm that holds this project in its portfolio. Can be empty for independent projects.")

    def __str__(self):
        return self.title


# === Models based on master_cv.json ===

class Consultant(models.Model):
    # --- Personal Details ---
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    linkedin = models.URLField(max_length=2000, blank=True, null=True)

    # --- Relationships ---
    firms = models.ManyToManyField(Firm, related_name='consultants', blank=True, help_text="Firms this consultant is associated with.")

    def __str__(self):
        return self.name
    
# --- NEW: Linking Model for Consultant Roles ---
# This model connects a Consultant to a Project and describes their specific role.
# This REPLACES the old "Assignment" model.
class ConsultantRole(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='roles')
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='roles')
    
    # The consultant's specific title on this project
    role_title = models.CharField(max_length=255, help_text="e.g., Lead Evaluator, Data Analyst, Project Manager")
    
    # The consultant's personal description of their tasks and contributions
    role_description = models.TextField(blank=True, null=True)
    tasks = models.TextField(blank=True, null=True, help_text="Bulleted or paragraph list of specific tasks performed.")

    class Meta:
        # Ensures a consultant can't have two roles on the same project
        unique_together = ('project', 'consultant')

    def __str__(self):
        return f"{self.consultant.name} as {self.role_title} on {self.project.title}"

class Education(models.Model):
    consultant = models.ForeignKey(Consultant, related_name='education', on_delete=models.CASCADE)
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_year = models.DateField(blank=True, null=True)
    end_year = models.DateField(blank=True, null=True)
    field_of_study = models.CharField(max_length=255, blank=True, null=True)
    graduation_status = models.CharField(max_length=100, blank=True, null=True)
    dissertation_title = models.CharField(max_length=500, blank=True, null=True)
    dissertation_link = models.URLField(max_length=2000,blank=True, null=True)

    def __str__(self):
        return f"{self.degree} from {self.institution}"

class Certification(models.Model):
    consultant = models.ForeignKey(Consultant, related_name='certifications', on_delete=models.CASCADE)
    certification_name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    issue_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    certification_link = models.URLField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.certification_name


class Publication(models.Model):
    consultant = models.ForeignKey(Consultant, related_name='publications', on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500)
    year = models.PositiveIntegerField(blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.title

class Language(models.Model):
    consultant = models.ForeignKey(Consultant, related_name='languages', on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    level = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.language} ({self.level})"