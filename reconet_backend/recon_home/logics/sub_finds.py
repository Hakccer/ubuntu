import subprocess
import re
import uuid
import os


link_dectection_compiler = re.compile(
"^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")

# Removal Function For Getting Only URL From a IO Line
def removal(domain):
    try:
        data = link_dectection_compiler.search(domain)
        return data.group()
    except Exception as e:
        return None


# Function for only getting live or alive subdomains
def get_sub_domains(domain):
    try:
        key_1 = uuid.uuid4()
        key_2 = uuid.uuid4()

        # Main Command For Getting subdomains and resolving them using mass-dns or Shuffle-Dns
        os.chdir('/root/Downloads/reconet_backend/')
        subprocess.run(
            f'subfinder -d {domain} | shuffledns -d {domain} -r lists/resolvers.txt -wo {key_2}.txt | tee {key_1}.txt', shell=True)
        
        tem_dom_file = open(f"/root/Downloads/reconet_backend/{key_1}.txt")
        data = tem_dom_file.readlines()
        doms_list = list(set(map(removal, data)))

        # Deleting The Temporary Files After they are used
        return [f"{key_1}.txt", f"{key_2}.txt", doms_list]
    except Exception as e:
        print(e)
        return get_sub_domains(domain)