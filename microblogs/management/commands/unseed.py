from django.core.management.base import BaseCommand, CommandError
from microblogs.models import User

class Command(BaseCommand):
    def _init_(self):
        super()._init_()

    def handle(self,*args,**options):
        for user in User.objects.all():
            if user.is_superuser != True:
                user.delete()
