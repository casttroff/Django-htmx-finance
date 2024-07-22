from django.core.management.base import BaseCommand
from tracker.models import Category

class Command(BaseCommand):
    help = 'Delete all categories'

    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all categories'))