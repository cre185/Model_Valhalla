import json
import requests
import time

class AutoTest():
    def generate_test_data(self, dataPath):
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
    
    def test_with_data(self, data, target_column, api):
        test_count=0
        correct_amount=0
        subject_amount={}
        subject_correct_amount={}
        subject_accuracy={}
        test_time=time.time()
        for i in range(len(data)):
            question = data[i][target_column['QUESTION']]
            answer = data[i][target_column['ANSWER']]
            if test_count >= self.RPM:
                if time.time()-test_time <= 61:
                    time.sleep(61-(time.time()-test_time))
                test_count=0
                test_time=time.time()
            test_count+=1
            print('Testing question '+str(i))
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
            try:
                subject = data[i][target_column['SUBJECT']]
                if subject not in subject_amount:
                    subject_amount[subject]=1
                else:
                    subject_amount[subject]+=1
            except:
                pass
            if current_result == ans:
                try:
                    subject = data[i][target_column['SUBJECT']]
                    if subject not in subject_correct_amount:
                        subject_correct_amount[subject]=1
                    else:
                        subject_correct_amount[subject]+=1
                except:
                    pass
                correct_amount+=1
        for subject, amount in subject_amount.items():
            if subject not in subject_correct_amount:
                subject_correct_amount[subject]=0
            subject_accuracy[subject]=subject_correct_amount[subject]/amount
        return [correct_amount, len(data), subject_correct_amount, subject_amount, subject_accuracy]

    def api_url(self, question, choices):
        prompt='Answer the question by choosing the best answer you think and return a single character A, B, C, or D representing your choice.  '
        prompt+='Question: '+question.replace('\\', '\\\\').replace('"', '\\"')+'  '
        prompt+='Following are the four choices.  '
        for i in range(4):
            prompt+=(chr(65+i))+'. '+choices[i].replace('\\', '\\\\').replace('"', '\\"')+'  '
        prompt+='Remember only one single character is required, A, B, C, or D.'
        headers = json.loads(self.headers)
        # print(self.data.replace('$PROMPT', prompt))
        data = json.loads(self.data.replace('$PROMPT', prompt))
        # print('Starting test: '+question)
        response = requests.post(self.url, headers=headers, json=data)

        if response.status_code == 200:
            response.encoding = 'utf-8'
            result = response.json()
            # print(result['choices'][0]['message']['content'])
            for c in result['choices'][0]['message']['content']:
                if c in ['A','B','C','D']:
                    return c

        else:
            print(response.status_code)
            print(response.text)
            return 'A'

    def whole_test(self, dataPath, llm):
        self.url = llm.api_url
        self.headers = llm.api_headers
        self.data = llm.api_data
        try:
            self.RPM = llm.RPM
        except:
            self.RPM = 10^9
        data, target_column = self.generate_test_data(dataPath)
        return self.test_with_data(data, target_column, self.api_url)
