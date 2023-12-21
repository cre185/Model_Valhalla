import csv
from io import StringIO

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

if __name__ == '__main__':
    with open('mmlu_select.csv', 'r', encoding='utf-8') as f:
        try:
            content = f.read()
            print(verify_dataset(content))
        except Exception as e:
            print(e)
