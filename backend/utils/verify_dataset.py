def verify_dataset(content):
    if not content:
        raise Exception("Empty file")
    # test if the file is valid
    headers = set(content.replace('\r\n', '\n').split('\n')[0].lower().split(','))
    obj1 = set(['question', 'choices', 'answer'])
    obj2 = set(['question', 'a','b','c','d', 'answer'])
    sub1 = set(['prompt'])
    if obj1.issubset(headers) or obj2.issubset(headers):
        subjective = False
    elif sub1.issubset(headers):
        subjective = True
    else:
        raise Exception("Invalid file")
    lines = content.split('\n')[1:]
    line_count = 0
    for line in lines:
        if line == '':
            continue
        line_count += 1
        i = 0
        inside = False
        count = 0
        while i < len(line):
            if line[i] == '"':
                inside = not inside
            elif line[i] == ',' and not inside:
                count += 1
            i += 1
        if count != len(headers) - 1:
            raise Exception("Invalid file")
    return subjective, line_count