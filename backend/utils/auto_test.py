
def generate_test_data(dataPath):
    target_column = {}
    data = []
    data_file = open(dataPath, 'rb')
    data_lines = data_file.readlines()
    data_file.close()
    header = data_lines[0].decode('utf-8')[:-1].split(',')
    for i in range(len(header)):
        target_column[header[i].upper()] = i
    data_lines = data_lines[2:]
    for i in range(len(data_lines)):
        data.append([])
        data_lines[i] = data_lines[i].decode('utf-8')
        is_inside=False
        last_index=0
        for index, chr in enumerate(data_lines[i]):
            if chr == '"':
                is_inside = not is_inside
            if chr == ',' and not is_inside:
                data[i].append(data_lines[i][last_index:index])
                last_index = index+1
        data[i].append(data_lines[i][last_index:-1])
    return data, target_column

def fake_api(question, choices):
    return 'A'

def test_with_data(data, target_column, api):
    correct_amount=0
    subject_amount={}
    for i in range(len(data)):
        try:
            question = data[i][target_column['QUESTION']]
            answer = data[i][target_column['ANSWER']]
            if 'CHOICES' in target_column:
                choices = data[i][target_column['CHOICES']][2:-2].replace('"", ""','"",""').split('"",""')
                choices = [choice.replace('"" ','').replace(' ""','') for choice in choices]
                current_result = api(question, choices)
            else:
                choices = [data[i][target_column['A']], data[i][target_column['B']], data[i][target_column['C']], data[i][target_column['D']]]
                current_result = api(question, choices)
            for ans in ['A','B','C','D']:
                if ans in current_result:
                    current_result = ans
                    break
            for ans in ['A','B','C','D']:
                if ans in answer:
                    answer = ans
                    break
            if current_result == ans:
                try:
                    subject = data[i][target_column['SUBJECT']]
                    if subject not in subject_amount:
                        subject_amount[subject]=1
                    else:
                        subject_amount[subject]+=1
                except:
                    pass
                correct_amount+=1
        except:
            print("error")
    return correct_amount, subject_amount


if __name__ == "__main__":
    data, target_column = generate_test_data("../static/data/cmmlu_select.csv")
    print(test_with_data(data, target_column, fake_api))