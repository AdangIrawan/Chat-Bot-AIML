from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import bcrypt
import aiml
import csv
import os 

app = Flask(__name__)
app.secret_key = "chatbot_key"

client = MongoClient("mongodb+srv://NLP:FM5pMe0CgwFHblS7@nlp.jthvadb.mongodb.net/?retryWrites=true&w=majority&appName=NLP")
db = client.get_database("ACCOUNTS")
users_collection = db.users

# Inisialisasi kernel AIML
kernel = aiml.Kernel()
aiml_directory = 'Dataset xml'

# Memuat semua file AIML dari direktori Dataset/xml
for aiml_file in os.listdir(aiml_directory):
    if aiml_file.endswith('.xml'):
        kernel.learn(os.path.join(aiml_directory, aiml_file))

def get_response(user_input):
    return kernel.respond(user_input)


def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    if 'username' in session:
        return render_template('about.html')
    return redirect(url_for('login'))

@app.route('/about/vga')
def aboutvga():
    vga_list = []
    try:
        with open('vga.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                vga_list.append(row)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    
    return render_template('aboutvga.html', vga_list=vga_list)


@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('chat.html')
    return redirect(url_for('login'))

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.form['user_input']
    bot_response = get_response(user_input)
    return bot_response

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
        
    error_message = ""

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = encrypt_password(password)

        if users_collection.find_one({"username": username}):
            error_message = "Username already exists"

        if users_collection.find_one({"email": email}):
            error_message = "Email already exist"

        if not error_message:
            users_collection.insert_one({
                "username": username,
                "email": email,
                "password": hashed_password
            })
            return redirect(url_for('login'))

    return render_template('register.html', error_message=error_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({"username": username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Login gagal. Periksa kembali username dan password Anda."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
