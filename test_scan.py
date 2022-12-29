import time
from zapv2 import ZAPv2
from zapier import crawler
import uuid
import json
import sys

def passive_scanner(_target):
    once = False
    while True:
        try:
            apiKey = 'c3u2te4df0uomkt570je4pqeqk'
            zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

            zap.core.delete_all_alerts()

            for i in zap.core.hosts:
                if _target != f'https://{i}' and _target != f'http://{i}':
                    try:
                        zap.core.delete_site_node(f'https://{i}')
                    except Exception:
                        zap.core.delete_site_node(f'http://{i}')

            detector = False
            for host in zap.core.hosts:
                if host in _target:
                    detector = True
                    break
                
            if not detector:
                print(f"{str(_target)} not founded in sites list running crawler")
                crawler(_target)
            # Registering File name for alerts or results
            alert_file_data = {}

            # explore the app (Spider, etc) before using the Passive Scan API, Refer the explore section for details
            while int(zap.pscan.records_to_scan) > 0:
                # Loop until the passive scan has finished
                print('Records to passive scan : ' + zap.pscan.records_to_scan)
                time.sleep(2)
            
            # Host Detection
            print('Passive Scan completed')
            print('Hosts: {}'.format(', '.join(zap.core.hosts)))
            break
        except Exception as e:
            if not once:
                print("Retrying in 3 Seconds...")
                time.sleep(3)
                once = True
                continue
            log_file = open('/root/Downloads/log.txt', 'a+')
            log_file.write(f"{len(log_file.readlines())}: {e}")
            log_file.close()
            break

    # Adding Data to our dict-data format
    alert_file_data['hosts'] = zap.core.hosts
    alert_file_data['alerts'] = zap.core.alerts()

    # creating a json file and adding data in it
    alert_file_name = str(uuid.uuid4())
    output_file = open(f"{alert_file_name}.json", 'w', encoding='utf-8')
    json.dump(alert_file_data, output_file)
    output_file.close()
    return [alert_file_name, alert_file_data]

# Handling the FUnction Startment
try:
    data = passive_scanner(sys.argv(1))
except Exception as e:
    data = passive_scanner(str(input("Enter Your target url here -> ")))
try:
    print("Scan Results Saved succesfully...")
    print(f"Your data has saved to {data[0]}.json")
except Exception as e:
    log = open('/root/Downloads/log.txt', 'a')
    log.write(f"{len(log.readlines())}: {e}")
    log.close()