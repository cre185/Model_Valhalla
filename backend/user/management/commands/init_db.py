from django.core.management.base import BaseCommand

from dataset.models import *
from ranking.models import *
from testing.models import *
from user.models import *


class Command(BaseCommand):
    help = "Initialize Database with test data"

    def handle(self, *args, **options):
        # Initalize the database
        # Create the admin user
        admin = User(username="realadmin", password="realadmin", mobile=11111111111, is_admin=True)
        admin.save()
        user = User(username="testuser", password="testuser", mobile=12345678901)
        user.save()
        # Create the five standard datasets
        dataset1 = Dataset(name="dataset1", description="dataset1", data_file="static/data/ceval_select.csv")
        dataset1.save()
        dataset2 = Dataset(name="dataset2", description="dataset2", data_file="static/data/cmmlu_select.csv")
        dataset2.save()
        dataset3 = Dataset(name="dataset3", description="dataset3", data_file="static/data/mmlu_select.csv")
        dataset3.save()
        dataset4 = Dataset(name="dataset4", description="dataset4", data_file="static/data/zbench_common.csv", subjective=True)
        dataset4.save()
        dataset5 = Dataset(name="dataset5", description="dataset5", data_file="static/data/zbench_emergent.csv", subjective=True)
        dataset5.save()
        # Create the four standard llms
        llm1 = LLMs(name="llm1", description="llm1", model_name="mistral_7b")
        llm1.save()
        llm2 = LLMs(name="llm2", description="llm2", model_name="qwen_7b_chat")
        llm2.save()
        llm3 = LLMs(name="llm3", description="llm3", model_name="vicuna_7b")
        llm3.save()
        llm4 = LLMs(name="llm4", description="llm4", model_name="zephyr_7b")
        llm4.save()
        # Create credits
        credit_list=[31,41,25,29,29,44,22,28,37,37,37,42]
        for i in range(1,6):
            for j in range(1,5):
                credit = Credit(dataset=Dataset.objects.get(id=i), LLM=LLMs.objects.get(id=j))
                if i*4+j-5<len(credit_list):
                    credit.credit=credit_list[i*4+j-5]
                credit.save()