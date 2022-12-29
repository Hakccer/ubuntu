import subprocess
import os
import re
from threading import Thread

class InternetDorking:
    # Construtor For Intializing The Dorking Result And Valid Engines 
    def __init__(self) -> None:
        self.__dork_result = []
        self.__valid_engines = ['google', 'bing', 'yahoo']
        self.__url_regex = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    
    def removal(self, ele):
        try:
            detection_compiler = re.compile(self.__url_regex)
            url = detection_compiler.search(ele)
            return url.group()
        except Exception as e:
            return None
        

    # Dorking Function to perform the dorking
    def dorking(self, query, engine):
        os.chdir('/root/Downloads/')
        subprocess.run(f'./go-dork_1.0.2_linux_amd64 -q {query} -e {engine} | tee temper.txt', shell=True)

        # Opening dorking result file and scanning it for query results
        dor_file = open('temper.txt')
        dor_lines = dor_file.readlines()
        temper_result = list(set(map(self.removal, dor_lines)))

        # Cleaning the result list
        while None in temper_result:
            temper_result.remove(None)
        
        return temper_result
    
    # RUn Dorking function the dorking function executor
    def run_dorking(self, query, engine='both'):
        if engine == 'both':
            ther = []
            for single_engine in self.__valid_engines:
                ther.append(Thread(target=self.dorking, args=(query, single_engine)))
            for single_thread in ther:
                single_thread.start()
            if len(self.__dork_result) == 0:
                print("No Queries has been runned start dorking with -> 'run_dorking()'")
            return list(set(self.__dork_result))
        if str(engine).lower() not in self.__valid_engines:
            print("Please choose a engine from 'google,bing or yahoo'")
            return self.__dork_result
        else:
            self.__dork_result = self.dorking(query, engine)
        if len(self.__dork_result) == 0:
                print("No Queries has been runned start dorking with -> 'run_dorking()'")
        return self.__dork_result

inter = InternetDorking()
decks = inter.run_dorking('running')
print("")
print("")
print("We Are Coming By Taking The Best Dorking Function")
print("")
print("")
for reses in decks:
    print(reses)
