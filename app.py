from flask import Flask

app = Flask(__name__)


@app.route('/homepage',methods=['GET'])
def home_page():
    return 'welcome to checkers game'

if __name__ == '__main__':
            
   app.run(debug=True)