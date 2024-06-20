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
