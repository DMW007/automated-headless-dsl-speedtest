import subprocess
import re
from db import DB

def get_speed(str, prefix, unit = 'Mbit'):
    pattern_s = "{}: ([0-9\\.]+) {}".format(prefix, unit)
    pattern = re.compile(pattern_s)
    result = pattern.search(str)
    speed = result.group(1)
    return speed

cmd = ["speedtest-cli", "--simple"]
popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
popen.wait()
output = popen.stdout.read().decode('utf-8')

download = get_speed(output, 'Download')
upload = get_speed(output, 'Upload')
ping = get_speed(output, 'Ping', 'ms')
print("{}/{} Mbit, Ping: {} ms".format(upload, download, ping))

db = DB()
db.save(download, upload, ping)