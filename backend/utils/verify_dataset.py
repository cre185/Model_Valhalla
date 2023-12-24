import csv
from io import StringIO
import json

def verify_dataset(content):
    if not content:
        raise Exception("Empty file")

    content = StringIO(content)
    reader = csv.reader(content)

    # test if the file is valid
    headers = set(c.lower() for c in next(reader))
    obj1 = set(['question', 'choices', 'answer'])
    obj2 = set(['question', 'a','b','c','d', 'answer'])
    sub1 = set(['prompt'])
    if obj1.issubset(headers) or obj2.issubset(headers):
        subjective = False
    elif sub1.issubset(headers):
        subjective = True
    else:
        raise Exception("Invalid file")
    
    line_count = 0
    for line in reader:
        if line == '':
            continue
        line_count += 1
        if len(line) != len(headers):
            print(line)
            raise Exception("Invalid file")
    return subjective, line_count

def get_first_10_rows(content):
    content = StringIO(content)
    reader = csv.reader(content)

    header_list = next(reader)
    for i in range(len(header_list)):
        header_list[i] = header_list[i].lower()
    headers = set(header_list)
    obj1 = set(['question', 'choices', 'answer'])
    obj2 = set(['question', 'a','b','c','d', 'answer'])
    sub1 = set(['prompt'])
    if obj1.issubset(headers):
        filters = ['question', 'choices', 'answer']
    elif obj2.issubset(headers):
        filters = ['question', 'a','b','c','d', 'answer']
    elif sub1.issubset(headers):
        filters = ['prompt']
    else:
        return [], False

    data = []
    for line in reader:
        if line == '':
            continue
        data.append([])
        for i in range(len(line)):
            if header_list[i] in filters:
                if header_list[i] == 'choices':
                    choices = json.loads(line[i].replace('""', '"'))
                    for choice in choices:
                        data[-1].append(choice)
                else:
                    data[-1].append(line[i])
        if len(data) == 10:
            break
    return data, filters==['prompt']

if __name__ == '__main__':
    with open('zbench_common.csv', 'r', encoding='utf-8') as f:
        try:
            content = f.read()
            print(get_first_10_rows(content))
        except Exception as e:
            print(e)