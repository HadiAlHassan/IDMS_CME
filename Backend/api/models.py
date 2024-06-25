from djongo import models
import random

class DocGeneralInfo(models.Model):
    general_info_id = models.IntegerField(unique=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    source = models.TextField()
    title = models.TextField()
    author = models.TextField()
    nlp_id = models.IntegerField(unique=True)

    class Meta:
        db_table = 'general_info'

    def save(self, *args, **kwargs):
        if self.general_info_id is None:
            self.general_info_id = self.generate_unique_id()
        if self.nlp_id is None:
            self.nlp_id = self.generate_unique_nlp_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_id():
        while True:
            random_id = random.randint(0, 999999999)
            if not DocGeneralInfo.objects.filter(general_info_id=random_id).exists():
                return random_id

    @staticmethod
    def generate_unique_nlp_id():
        while True:
            random_id = random.randint(0, 999999999)
            if not DocGeneralInfo.objects.filter(nlp_id=random_id).exists():
                return random_id



class NlpAnalysis(models.Model):
    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('French', 'French'),
        ('Spanish', 'Spanish'),
        # Add other languages as needed
    ]

    CONFIDENTIALITY_CHOICES = [
        ('Public', 'Public'),
        ('Confidential', 'Confidential'),
        ('Secret', 'Secret'),
    ]

    CATEGORY_CHOICES = [
        ('Legal', 'Legal'),
        ('Finance', 'Finance'),
        ('Healthcare', 'Healthcare'),
        # Add other categories as needed
    ]

    nlp_id = models.OneToOneField(DocGeneralInfo, on_delete=models.CASCADE, to_field='nlp_id', primary_key=True)
    document_type = models.CharField(max_length=100)
    keywords = models.JSONField()
    summary = models.TextField()
    document_date = models.DateField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    related_documents = models.JSONField()
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    version = models.CharField(max_length=50)
    confidentiality_level = models.CharField(max_length=50, choices=CONFIDENTIALITY_CHOICES)
    location = models.CharField(max_length=255)
    references = models.JSONField()
    uploaded_by = models.CharField(max_length=100)
    related_projects = models.JSONField()

    class Meta:
        db_table = 'nlp_analysis'