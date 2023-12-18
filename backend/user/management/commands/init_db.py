from django.core.management.base import BaseCommand

from dataset.models import *
from ranking.models import *
from testing.models import *
from user.models import *
import pandas as pd


class Command(BaseCommand):
    help = "Initialize Database with test data"

    def handle(self, *args, **options):
        # Initalize the database
        # Create users
        df = pd.read_csv("user/management/commands/data/user.csv")
        user=[]
        for index, row in df.iterrows():
            user.append(User(
                username = row['username'],
                password = row['password'],
                mobile = row['mobile'],
                email = row['email'],
                avatar = row['avatar']))
            if index == 0:
                user[index].is_admin = True
            user[index].save()
        # Create the five standard datasets
        df = pd.read_csv("user/management/commands/data/dataset.csv")
        for index, row in df.iterrows():
            dataset = Dataset(
                name=row['name'],
                description=row['description'],
                author = user[0],
                domain = row['domain'],
                data_file=row['data_file'],
                subjective=row['subjective'])
            dataset.save()  
        # Create the four standard llms
        df = pd.read_csv("user/management/commands/data/llm.csv")
        for index, row in df.iterrows():
            llm = LLMs(
                name=row['name'],
                model_name=row['model_name'],
                logo=row['logo'],
                official_website=row['official_website'],
                description=row['description'],
                document_name=row['document_name'],
                document_website=row['document_website'],
                license=row['license'],
                released_time=row['released_time'])
            llm.save()
        # Create credits
        credit_list = [31, 41, 25, 29, 29, 44, 22, 28, 37, 37, 37, 42]
        for i in range(Dataset.objects.count()):
            for j in range(LLMs.objects.count()):
                dataset = Dataset.objects.get(id=i+1)
                llm = LLMs.objects.get(id=j+1)
                credit = Credit(dataset=dataset, LLM=llm)
                if i * LLMs.objects.count() + j < len(credit_list):
                    credit.credit = credit_list[i * LLMs.objects.count() + j]
                if dataset.subjective:
                    subjective_credit = SubjectiveCredit(dataset=dataset, LLM=llm)
                    subjective_credit.save()
                credit.save()
