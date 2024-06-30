from django.core.management.base import BaseCommand
from django.db import connection
from api.models import CategoryDocumentCount
from Utils.db import connect_to_mongo

class Command(BaseCommand):
    help = 'Update the document count per category'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        db = connect_to_mongo()
        nlp_analysis_collection = db['nlp_analysis']
        
        # Define the aggregation pipeline
        pipeline = [
            {
                "$group": {
                    "_id": "$category",
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "category": "$_id",
                    "document_count": "$count"
                }
            }
        ]

        # Execute the aggregation pipeline
        results = list(nlp_analysis_collection.aggregate(pipeline))

        # Clear the existing collection
        CategoryDocumentCount.objects.all().delete()

        # Insert the new counts
        for result in results:
            CategoryDocumentCount.objects.create(
                category=result['category'],
                document_count=result['document_count']
            )

        self.stdout.write(self.style.SUCCESS('Successfully updated document counts per category'))
