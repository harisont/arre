import json
import re
from turtle import right

def read_prev_errs(json_path):
    return json.loads(open(json_path).read())

def write_prev_errs(python_dict, json_path):
    with open(json_path, "w") as f:
        f.write(json.dumps(python_dict))

def extract_prev_errs(prev_errs, txt_path, json_path):
    with open(txt_path, "r") as f:
        transcription = f.read()
    regex = re.compile(r'(?<=\[).*?(?=\])', re.MULTILINE)
    new_prev_errs = regex.findall(transcription)
    for err in new_prev_errs:
        if ">" in err:
            split = err.split(">")
            wrong = split[0]
            right = split[1]

            # update transcription string
            transcription = transcription.replace("[" + err + "]", right)

            # update prev_errs dict
            if wrong not in prev_errs:
                prev_errs[wrong] = [right]
            else:
                if right not in prev_errs[wrong]:
                    prev_errs[wrong].append(right)
    
    # update json file
    write_prev_errs(prev_errs, json_path)

    # update segment file        
    with open(txt_path, "w") as f:
        f.write(transcription)

    return prev_errs
