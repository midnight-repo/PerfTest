from argparse import ArgumentParser
import datetime


# the timestamp below is used as default name for the log file
# FORMAT : {year}{month}{day}_{hour}{minute}{second}.log
timestamp = str(datetime.datetime.now()).split('.')[0].replace('-', '').replace(':', '').replace(' ', '_')


parser = ArgumentParser()
parser.add_argument('-p', '--port', default=8000,  help='Port to listen on [default: 80]')
parser.add_argument('--host', '-i', default='127.0.0.1', help='Default host to listen on [default: 127.0.0.1 (localhost)]')
parser.add_argument('-l', '-o', '--log-file', default=f'logs/{timestamp}.log', help='File to output the server logs [default: <timestamp>.log]')
parser.add_argument('-c', '--cert', default=None,  help='Server TLS/SSL certificate')
parser.add_argument('-k', '--key', default=None, help='TLS/SSL certificate\'s private key file')
args = parser.parse_args()
