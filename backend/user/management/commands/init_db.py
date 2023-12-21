import os
import shutil
import pandas as pd
from django.core.management.base import BaseCommand

from dataset.models import *
from ranking.models import *
from testing.models import *
from user.models import *


class Command(BaseCommand):
    help = "Initialize Database with test data"

    def handle(self, *args, **options):
        # Initalize the database
        # Create users
        df = pd.read_csv("user/management/commands/data/user.csv")
        user = []
        for index, row in df.iterrows():
            user.append(User(
                username=row['username'],
                password=row['password'],
                mobile=row['mobile'],
                email=row['email'],
                avatar=row['avatar']))
            if index == 0:
                user[index].is_admin = True
            user[index].save()
        # Create the five standard datasets
        df = pd.read_csv("user/management/commands/data/dataset.csv")
        for index, row in df.iterrows():
            dataset = Dataset(
                name=row['name'],
                description=row['description'],
                author=user[0],
                domain=row['domain'],
                data_file=row['data_file'],
                subjective=row['subjective'],
                content_size=row['content_size'])
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
        credit_list = [[28.,31.5],[36.,41.],[23.5,25.5],[28.5,25.5],[27.4111675,28.9340102],[41.1167513,45.1776650],[23.8578680,23.3502538],[31.9796954,28.4263959],[42.1319797,38.0710660],[41.6243655,38.5786802],[37.5634518,37.0558376],[40.1015228,47.7157360]]
        for i in range(Dataset.objects.count()):
            for j in range(LLMs.objects.count()):
                dataset = Dataset.objects.get(id=i + 1)
                llm = LLMs.objects.get(id=j + 1)
                credit = Credit(dataset=dataset, LLM=llm)
                if i * LLMs.objects.count() + j < len(credit_list):
                    credit.credit_list = credit_list[i * LLMs.objects.count() + j]
                    credit.credit = sum(credit.credit_list) / len(credit.credit_list)
                credit.save()

        # Copy the static files
        src_dir = "user/management/commands/static"
        dst_dir = "static"

        if(os.path.exists(dst_dir)):
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)