from flask import Flask, request, render_template
from html import escape
from argparser import args
import logger


app = Flask(
    __name__,
    template_folder='templates',
)
app.before_request(logger.log_request)
# app.after_request(logger.log_response)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/pretty_echo', methods=['GET', 'POST'])
def echo():
    if request.method == 'GET':
        return render_template('echo.html')
    elif request.method == 'POST':
        return render_template('hello.html', name=escape(request.form['name']))


@app.route('/echo', methods=['GET', 'POST'])
def minimal_echo():
    if request.method == 'GET':
        return render_template('minimal_echo.html')
    elif request.method == 'POST':
        return render_template('minimal_hello.html', name=escape(request.form['name']))


if __name__ == '__main__':
    app.run(
        host=args.host,
        port=args.port,
        debug=False,
        ssl_context=None if not args.cert and not args.key else (args.cert, args.key)
    )
