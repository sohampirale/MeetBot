import os
import re

def extract_front_matter(md):
    match = re.search(r'^(-{3,})\s*\n([\s\S]*?)\n\1', md, re.M)
    if not match:
        return None
    return f"{match.group(1)}\n{match.group(2)}\n{match.group(1)}"



front_matters = []
for filename in os.listdir('.'):
    if filename.endswith('.md'):
        with open(filename, "r", encoding="utf-8") as f:
            file_content = f.read()
            fm = extract_front_matter(file_content)
            if fm is not None:
                front_matters.append(fm)


print(f'front_matters :{front_matters}')