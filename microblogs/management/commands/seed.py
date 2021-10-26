from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from microblogs.models import User

class Command(BaseCommand):
    def _init_(self):
        super()._init_()



    def handle(self,*args,**options):
        faker = Faker('en_GB')
        for number in range(1,100):

                user = User.objects.create_user(
                f'@{faker.user_name()}',
                first_name = faker.first_name(),
                last_name = faker.last_name(),
                email = faker.email(),
                password = faker.password(),
                bio = "Hi"
                )
                user.full_clean()
                user.save()
