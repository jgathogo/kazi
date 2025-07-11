"""
class Consultant(models.Model):
    firm = models.ForeignKey(Firm, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultants')
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    professional_summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Assignment(models.Model):
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_range = models.CharField(max_length=100, blank=True, null=True)
    project_summary = models.TextField(blank=True, null=True)
    tasks = models.JSONField(blank=True, null=True)
    sectors = models.JSONField(blank=True, null=True)
    methodologies = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title

class Education(models.Model):
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.degree} from {self.institution}"

class Certification(models.Model):
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='certifications')
    certification_name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    issue_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.certification_name

class Publication(models.Model):
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500, blank=True, null=True)
    year = models.IntegerField(null=True, blank=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Language(models.Model):
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=100)
    level = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.language} ({self.level})" """
