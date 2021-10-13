from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from microblogs.models import User

class Command(BaseCommand):
    def _init_(self):
        super()._init_()
        self.faker = Faker('en_GB')
        self.faker.seed()
        print("Initiated")

    def handle(self,*args,**options):
        for number in range(1,5):

                user = User.objects.create_user(
                f'@test_user{number}',
                first_name = self.faker.first_name(),
                last_name = self.faker.last_name(),
                email = self.faker.email(),
                password = self.faker.password(),
                bio = f"Hi, I am {first_name}"
                )
                user.full_clean()
                user.save()

        print("WARNING: not yet been implemented")
