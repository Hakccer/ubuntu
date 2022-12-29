import time
from pprint import pprint
from zapv2 import ZAPv2
from zapier import crawler

apiKey = 'c3u2te4df0uomkt570je4pqeqk'
target = 'https://symphonious-sunflower-173e5c.netlify.app'
zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

print('Active Scanning target {}'.format(target))
zap.core.delete_all_alerts()
scanID = zap.ascan.scan(f"{target}")
if zap.ascan.status(scanID) == "does_not_exist":
    crawler(f'{target}')
    scanID = zap.ascan.scan(target)
while int(zap.ascan.status(scanID)) < 100:
    # Loop until the scanner has finished
    print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
    time.sleep(5)

print('Active Scan completed')
# Print vulnerabilities found by the scanning
print('Hosts: {}'.format(', '.join(zap.core.hosts)))
print('Alerts: ')
pprint(zap.core.alerts(baseurl=target))