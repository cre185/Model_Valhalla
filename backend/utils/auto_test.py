import json
import time

import requests

from Model_Valhalla.settings import DEBUG, SILENCE


class AutoTest():
    def __init__(self, llm):
        self.url = llm.api_url
        self.model_name = llm.model_name
        try:
            self.RPM = llm.RPM
        except BaseException:
            self.RPM = 10**9

    def generate_test_data(self, dataPath):
        target_column = {}
        data = []
        data_file = open(dataPath, 'rb')
        data_lines = data_file.readlines()
        data_file.close()
        header = data_lines[0].decode('utf-8').split(',')
        if header[-1][-1] == '\n':
            header[-1] = header[-1][:-1]
        if header[-1][-1] == '\r':
            header[-1] = header[-1][:-1]
        for i in range(len(header)):
            target_column[header[i].upper()] = i
        data_lines = data_lines[1:]
        i = 0
        while i < len(data_lines):
            data.append([])
            data_lines[i] = data_lines[i].decode('utf-8')
            is_inside = False
            rec_i = i
            i -= 1
            index = 0
            last_index = 0
            while len(data[rec_i]) < len(header) - 1 or is_inside:
                i += 1
                if i >= len(data_lines):
                    break
                if i != rec_i:
                    data_lines[rec_i] += data_lines[i].decode('utf-8')
                while index < len(data_lines[rec_i]):
                    chr = data_lines[rec_i][index]
                    if chr == '"':
                        is_inside = not is_inside
                    if chr == ',' and not is_inside:
                        data[rec_i].append(data_lines[rec_i][last_index:index])
                        last_index = index + 1
                    index += 1
            data[rec_i].append(data_lines[rec_i][last_index:-1])
            i += 1
        return data, target_column

    def test_with_data(self, data, target_column, api):
        test_count = 0
        correct_amount = 0
        subject_amount = {}
        subject_correct_amount = {}
        subject_accuracy = {}
        test_time = time.time()
        for i in range(len(data)):
            try:
                question = data[i][target_column['QUESTION']]
                answer = data[i][target_column['ANSWER']]
            except BaseException:
                break
            if test_count >= self.RPM:
                if time.time() - test_time <= 61:
                    time.sleep(61 - (time.time() - test_time))
                test_count = 0
                test_time = time.time()
            test_count += 1
            # print('Testing question ' + str(i))
            if 'CHOICES' in target_column:
                choices = data[i][target_column['CHOICES']][2:- \
                    2].replace('"", ""', '"",""').split('"",""')
                choices = [
                    choice.replace(
                        '"" ',
                        '').replace(
                        ' ""',
                        '') for choice in choices]
                current_result = api(question, choices)
            else:
                choices = [data[i][target_column['A']],
                           data[i][target_column['B']],
                           data[i][target_column['C']],
                           data[i][target_column['D']]]
                current_result = api(question, choices)
            # print('Current result: ' + str(current_result))
            if not current_result:
                continue
            for ans in ['A', 'B', 'C', 'D']:
                if ans in current_result:
                    current_result = ans
                    break
            for ans in ['A', 'B', 'C', 'D']:
                if ans in answer:
                    answer = ans
                    break
            try:
                subject = data[i][target_column['SUBJECT']]
                if not subject:
                    raise Exception
                if subject not in subject_amount:
                    subject_amount[subject] = 1
                else:
                    subject_amount[subject] += 1
            except BaseException:
                pass
            if current_result == answer:
                try:
                    subject = data[i][target_column['SUBJECT']]
                    if not subject:
                        raise Exception
                    if subject not in subject_correct_amount:
                        subject_correct_amount[subject] = 1
                    else:
                        subject_correct_amount[subject] += 1
                except BaseException:
                    pass
                correct_amount += 1
        for subject, amount in subject_amount.items():
            if subject not in subject_correct_amount:
                subject_correct_amount[subject] = 0
            subject_accuracy[subject] = subject_correct_amount[subject] / amount
        return [
            correct_amount,
            len(data),
            subject_correct_amount,
            subject_amount,
            subject_accuracy]

    def api_url(self, question, choices):
        prompt = 'Answer the question by choosing the best answer you think and return a single character A, B, C, or D representing your choice.  '
        prompt += 'Question: ' + \
            question.replace('\\', '\\\\').replace('"', '\\"') + '  '
        prompt += 'Following are the four choices.  '
        for i in range(4):
            prompt += (chr(65 + i)) + '. ' + \
                choices[i].replace('\\', '\\\\').replace('"', '\\"') + '  '
        prompt += 'Remember only one single character is required, A, B, C, or D.'

        result = self.call_api(prompt)
        return result

    def stream_call_api(self, prompt):
        data_json = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "top_p": 1,
            "top_k": -1,
            "n": 1,
            "max_tokens": 200,
            "stop": [
                "\n\n"
            ],
            "stream": True,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "user": "user"
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            data = json.dumps(data_json)
        except BaseException:
            # print('json error')
            return None
        response = requests.post(
            self.url,
            headers=headers,
            data=data,
            stream=True)
        for line in response.iter_lines():
            try:
                json_str = line.decode('utf-8')
                if json_str.startswith('data: '):
                    json_str = json_str[6:]
                result = json.loads(json_str)
                if 'choices' in result:
                    yield result['choices'][0]['delta']['content']
            except BaseException:
                pass

    def call_api(self, prompt):
        data_json = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "top_p": 1,
            "top_k": -1,
            "n": 1,
            "max_tokens": 200,
            "stop": [
                "\n\n"
            ],
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "user": "user"
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            data = json.dumps(data_json)
        except BaseException:
            # print('json error')
            return None
        response = requests.post(self.url, headers=headers, data=data)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            result = response.json()
            try:
                return result['choices'][0]['message']['content']
            except BaseException:
                return None
        else:
            # print(response.status_code)
            # print(response.text)
            return None

    def whole_test(self, dataPath):
        data, target_column = self.generate_test_data(dataPath)
        return self.test_with_data(data, target_column, self.api_url)
