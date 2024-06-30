from djongo import models
from Utils.db import connect_to_mongo
import random

class DocGeneralInfo(models.Model):
    _id = models.ObjectIdField(primary_key=True)
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
        ('Contract','Contract'),
        ('Technology','Technology'),
        ('Politics', 'Politics'),
        ('Court Case', 'Business'),
        ('Agreement', 'Agreement'),
        ('Sport', 'Sport'),
        ('Business', 'Business'),
        ('Other','Other')
        # Add other categories as needed
    ]
    _id = models.ObjectIdField(primary_key=True)
    nlp_id = models.OneToOneField(DocGeneralInfo, on_delete=models.CASCADE, to_field='nlp_id', db_column='nlp_id')
    document_type = models.CharField(max_length=100)
    summary = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    language = models.TextField()
    ner = models.JSONField()
    confidentiality_level = models.BooleanField()
    location = models.JSONField()
    references = models.JSONField()
    in_text_citations=models.JSONField()
    word_count = models.IntegerField()
    
    class Meta:
        db_table = 'nlp_analysis'

    def save(self, *args, **kwargs):
        if not self._state.adding:  # If updating an existing document
            previous = NlpAnalysis.objects.get(pk=self.pk)
            if previous.category != self.category:
                self.decrement_category_count(previous.category)
                self.increment_category_count(self.category)
        else:
            self.increment_category_count(self.category)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.decrement_category_count(self.category)
        super().delete(*args, **kwargs)

    @staticmethod
    def increment_category_count(category):
        db = connect_to_mongo()
        category_document_count = db['category_document_count']
        category_document_count.update_one(
            {'category': category},
            {'$inc': {'document_count': 1}},
            upsert=True
        )

    @staticmethod
    def decrement_category_count(category):
        db = connect_to_mongo()
        category_document_count = db['category_document_count']
        category_document_count.update_one(
            {'category': category},
            {'$inc': {'document_count': -1}}
        )

class CategoryDocumentCount(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    category = models.CharField(max_length=100, unique=True)
    document_count = models.IntegerField()

    class Meta:
        db_table = 'category_document_count'



