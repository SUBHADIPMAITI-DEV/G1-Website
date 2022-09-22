# MongoDB Username: CodeMaster Password: Dz7VClOKiF7Qh6Ge
#mongodb+srv://<username>:<password>@cluster0.jqbembb.mongodb.net/test
   
# from base64 import encode
# from crypt import method
# from Crypto.Cipher import AES
# from Cryptodome.Cipher import AES 
from flask import Flask, render_template, url_for, request, session, redirect 
from flask_pymongo import PyMongo
import bcrypt

   
app = Flask(__name__)

app.config['MONGO_DBNAME']= 'CodeMaster'
app.config['MONGO_URL']= 'mongodb+srv://CodeMaster:codemaster@cluster0.jqbembb.mongodb.net/test'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as the following user:' + session['username']
    
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    
    users = mongo.db.users
    login_user = users.find_one({'name' :request.form['username']})
    
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'Invalid username or password combination'
    
    
@app.route('/registration', methods=['POST','GET'])
def registration():
    if request.method== 'POST':
        users=mongo.db.users
        existing_user = users.find_one({'name':request.form['username']})
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'),bcrypt.gensalt())
            users.insert({'name':request.form['username'], 'password':hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        
if __name__ == '__main__':
    app.secret_key='secretivekeyagain'
    app.run(debug=True)
            
        