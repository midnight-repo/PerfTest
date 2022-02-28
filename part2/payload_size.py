# THIS SCRIPTS SENDS A REQUEST WITH A PAYLOAD SIZE THAT GETS MULTIPLIED BY 2 EVERY ITERATION AND WRITES RESULTS
# TO A CSV IN REAL TIME, SO YOU CAN INTERRUPT IT WHEN NEEDED

import requests
from urllib.parse import urlparse
import subprocess
import time
import pandas as pd
import atexit
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-u', '--url', help='URL to test')
parser.add_argument('-o', '--outfile',  help='Name of the output file')
parser.add_argument('-T', '--timeout', type=int, default=30, help='Request timeout')
args = parser.parse_args()


url = args.url if args.url else 'http://127.0.0.1:8000/echo'
outfile = args.outfile if args.outfile else 'ps_' + url.split('/')[-1] + '.csv'
netloc = urlparse(url).netloc
server_port = netloc.split(':')[1] if ':' in netloc else '80'
server_pid = subprocess.getoutput(f'lsof -i :{server_port}').split('\n')[1].split()[1].strip()


def perf(function, *args, **kwargs):
    t0 = time.perf_counter()
    function(*args, **kwargs)
    t1 = time.perf_counter()
    return t1 - t0

def charts():
    df = pd.read_csv('../data_sample/ps_homepage.csv', index_col='Payload Size')
    df['Response Time (seconds)'].plot(kind='line', title='Response Time Depending On Payload Size', figsize=(18, 6)).get_figure().savefig(outfile[:-4] + '_response_time.jpg')
    df[['%CPU', '%MEM']].plot(kind='line', title='CPU and Memory Usage Depending On Payload Size', figsize=(18, 6)).get_figure().savefig(outfile[:-4] + '_cpumem.jpg')


atexit.register(charts)
f = open(outfile, 'w')
f.write('Payload Size,Response Time (seconds),%CPU,%MEM\n')
f.close()
payload_size = 1
r = 1
while True:
    try:
        t = perf(requests.post,
                 url='http://127.0.0.1:8000/echo',
                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
                 data=f'name={str(0)*payload_size}',
                 timeout=args.timeout)
        cpu, mem = tuple(x for x in subprocess.getoutput(f'ps -p {server_pid} -o %cpu,%mem').split('\n')[1].split(' ') if not x == '')
        with open(outfile, 'a') as f:
            f.write(f'{payload_size},{t},{cpu},{mem}\n')
            f.close()

        payload_size *= 2
        r += 1
        print(f'Request {r} of 32 :  length={payload_size} | time={t} (seconds) | %cpu={cpu} | %meme={mem}')

    except Exception as e:
        print(e)
