from flask import Flask, render_template
import app

server = Flask(__name__)

@server.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

@server.route('/my-link/', methods=['GET', 'POST'])
def my_link():
  print ('I got clicked!', methods=['GET', 'POST'])
  return 'Click.'

@server.route('/ping', methods=['GET', 'POST'])
def ping():
  app.start()
  return 'pinger'

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=40133, debug=True) 