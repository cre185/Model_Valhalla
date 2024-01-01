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
        # Copy the static files
        src_dir = "user/management/commands/static"
        dst_dir = "media"

        if(os.path.exists(dst_dir)):
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)

        # Initalize the database
        if User.objects.count() > 0:
            return
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
        credit_list = [
            [
                28.0, 31.5, 26.0, 28.0, 31.0], [
                36.0, 41.0, 43.5, 36.5, 40.0], [
                31.0, 23.5, 29.0], [
                    23.5, 25.5, 27.5, 23.5, 25.5], [
                        28.5, 25.5, 27.0, 30.5, 32.0], [
                            27.4111675, 28.9340102, 25.888324873096447, 28.934010152284262, 25.380710659898476], [
                                41.1167513, 45.177665, 44.67005076142132, 43.14720812182741, 44.16243654822335], [
                                    28.426395939086294, 26.903553299492387, 23.3502538071066], [
                                        23.857868, 23.3502538, 24.873096446700508, 20.304568527918782, 21.82741116751269], [
                                            31.9796954, 28.4263959, 31.472081218274113, 30.96446700507614, 29.949238578680202], [
                                                42.1319797, 38.071066, 35.53299492385787, 42.131979695431475, 41.11675126903553], [
                                                    41.6243655, 38.5786802, 36.04060913705584, 36.54822335025381, 40.101522842639596], [
                                                        37.56345177664975, 31.97969543147208, 36.04060913705584], [
                                                            37.5634518, 37.0558376, 35.025380710659896, 28.426395939086294, 36.04060913705584], [
                                                                40.1015228, 47.715736, 41.6243654822335, 38.578680203045685, 43.65482233502538]]
        for i in range(Dataset.objects.count()):
            for j in range(LLMs.objects.count()):
                dataset = Dataset.objects.get(id=i + 1)
                llm = LLMs.objects.get(id=j + 1)
                credit = Credit(dataset=dataset, LLM=llm)
                if i * LLMs.objects.count() + j < len(credit_list):
                    credit.credit_list = credit_list[i *
                                                     LLMs.objects.count() + j]
                    if len(credit.credit_list) > 0:
                        credit.credit = sum(
                            credit.credit_list) / len(credit.credit_list)
                credit.save()
