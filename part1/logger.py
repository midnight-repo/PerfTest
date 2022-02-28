import logging
from datetime import datetime
from argparser import args
from flask import request


logging.basicConfig(filename=args.log_file, level=logging.DEBUG, format='%(message)s')
logging.getLogger().addHandler(logging.StreamHandler())
logging.info(f'   {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}   '.center(80, '='))


def log_request():
    req = {}
    req['timestamp'] = str(datetime.now())
    req['remote_addr'] = request.remote_addr
    req['method'] = request.method
    req['endpoint'] = request.path
    req['args'] = request.args
    req['headers'] = dict(request.headers)
    req['cookies'] = request.cookies
    req['data'] = request.data
    #req['form'] = request.form
    logging.info(f'\n\n{" [REQUEST] ".center(80, "-")}\n')
    for detail in req:
        log_type = f'[{detail.upper()}]'
        if detail == 'headers':
            logging.info(log_type)
            for x in req[detail]:
                logging.info(f'\t{x} :  {str(req[detail][x])}')
        else:
            logging.info(f'{log_type}  {str(req[detail])}')


def log_response(response):
    resp = {}
    resp['status_code'] = response.status_code
    resp['status'] = response.status
    resp['headers'] = dict(response.headers)
    #resp['data'] = response.response
    logging.info(f'\n\n{" [RESPONSE] ".center(80, "-")}\n')
    for detail in resp:
        log_string = f'[{detail.upper()}]'
        if detail == 'headers':
            logging.info(log_string)
            for x in resp[detail]:
                logging.info(f'\t{x} :  {str(resp[detail][x])}')
        else:
            logging.info(f'{log_string}  {str(resp[detail])}')
