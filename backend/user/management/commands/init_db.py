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
        admin = User(
            username="realadmin",
            password="realadmin",
            mobile=11111111111,
            is_admin=True)
        admin.save()
        user = User(
            username="testuser",
            password="testuser",
            mobile=12345678901)
        user.save()
        # Create the five standard datasets
        dataset1 = Dataset(
            name="dataset1",
            description="dataset1",
            data_file="static/data/ceval_select.csv")
        dataset1.save()
        dataset2 = Dataset(
            name="dataset2",
            description="dataset2",
            data_file="static/data/cmmlu_select.csv")
        dataset2.save()
        dataset3 = Dataset(
            name="dataset3",
            description="dataset3",
            data_file="static/data/mmlu_select.csv")
        dataset3.save()
        dataset4 = Dataset(
            name="dataset4",
            description="dataset4",
            data_file="static/data/zbench_common.csv",
            subjective=True)
        dataset4.save()
        dataset5 = Dataset(
            name="dataset5",
            description="dataset5",
            data_file="static/data/zbench_emergent.csv",
            subjective=True)
        dataset5.save()
        # Create the four standard llms
        llm1 = LLMs(name="llm1", model_name="mistral_7b", logo="static/logo/mistral_7b.png", official_website="https://mistral.ai/news/announcing-mistral-7b/",
                    description="Mistral-7B是一个拥有73亿参数的语言模型，由欧洲的Mistral AI开发和发布。它使用了组查询注意力和滑动窗口注意力机制，以实现高效和高性能的文本和代码生成。 \
                        Mistral-7B的资源消耗很低，只需要6GB显存，可在MacBook上流畅运行。Mistral-7B适用于文本摘要、分类、文本补全、代码补全等各种任务。",
                    document_name="Mistral 7B", document_website="https://arxiv.org/abs/2310.06825", license="Apache-2.0", released_time="2023-10-16")
        llm1.save()
        llm2 = LLMs(name="llm2", model_name="qwen_7b_chat", logo="static/logo/qwen_7b_chat.jpg", official_website="https://github.com/QwenLM/Qwen",
                    description="通义千问-7B（Qwen-7B）是阿里云研发的通义千问大模型系列的70亿参数规模的模型。Qwen-7B是基于Transformer的大语言模型, 在超大规模的预训练数据上进行训练得到。 \
                        预训练数据类型多样，覆盖广泛，包括大量网络文本、专业书籍、代码等。同时，在Qwen-7B的基础上，我们使用对齐机制打造了基于大语言模型的AI助手Qwen-7B-Chat。",
                    document_name="Qwen Technical Report", document_website="https://arxiv.org/abs/2309.16609", license="Apache-2.0", released_time="2023-9-24")
        llm2.save()
        llm3 = LLMs(name="llm3", model_name="vicuna_7b", logo="static/logo/vicuna_7b.jpg", official_website="https://lmsys.org/blog/2023-03-30-vicuna/",
                    description="Vicuna-7B是一个基于LLaMA的聊天机器人模型，由LMSYS开发，拥有73亿参数。它使用了ShareGPT的数据进行微调，能够生成流畅和有趣的对话。 \
                        它在多个聊天机器人的评测中表现出色，超过了更大的模型。它的资源消耗很低，只需要6GB的显存，可以在MacBook上运行。它是一个开源的模型，使用Apache 2.0协议。",
                    document_name="Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", document_website="https://arxiv.org/abs/2306.05685", license="Apache-2.0", released_time="2023-6-18")
        llm3.save()
        llm4 = LLMs(name="llm4", model_name="zephyr_7b", logo="static/logo/zephyr_7b.png", official_website="https://github.com/huggingface/alignment-handbook",
                    description="Zephyr_7b是一款由Zephyr Technologies开发的语言模型，它可以生成各种类型的文本，如诗歌、故事、代码、论文、歌曲、名人模仿等。Zephyr_7b的特点是创造性和多样性， \
                        它可以根据用户的输入和偏好来调整自己的风格和内容。Zephyr_7b的目标是为用户提供有趣和有用的文本，同时保证文本的质量和合理性。Zephyr_7b是一款先进和创新的语言模型，它展示了人工智能在自然语言处理领域的潜力和可能性。",
                    document_name="Zephyr: Direct Distillation of LM Alignment", document_website="https://arxiv.org/abs/2310.16944", license="Apache-2.0", released_time="2023-10-11")
        llm4.save()
        # Create credits
        credit_list = [31, 41, 25, 29, 29, 44, 22, 28, 37, 37, 37, 42]
        for i in range(1, 6):
            for j in range(1, 5):
                credit = Credit(
                    dataset=Dataset.objects.get(
                        id=i), LLM=LLMs.objects.get(
                        id=j))
                if i * 4 + j - 5 < len(credit_list):
                    credit.credit = credit_list[i * 4 + j - 5]
                else:
                    subjective_credit = SubjectiveCredit(dataset=Dataset.objects.get(id=i), LLM=LLMs.objects.get(id=j))
                    subjective_credit.save()
                credit.save()
