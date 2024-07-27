from django.core.management.base import BaseCommand
from tracker.models import User

class Command(BaseCommand):
    help = 'Delete all users'

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all users'))