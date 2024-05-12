from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import bcrypt
import aiml

app = Flask(__name__)
app.secret_key = "chatbot_key"

# Inisialisasi koneksi MongoDB
client = MongoClient("mongodb+srv://NLP:FM5pMe0CgwFHblS7@nlp.jthvadb.mongodb.net/?retryWrites=true&w=majority&appName=NLP")
db = client.get_database("ACCOUNTS")
users_collection = db.users  # Koleksi untuk pengguna

kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="bot.xml")

def get_response(user_input):
    return kernel.respond(user_input)

# Fungsi untuk mengenkripsi password
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
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Enkripsi password sebelum disimpan
        hashed_password = encrypt_password(password)

        # Cek apakah username sudah ada
        if users_collection.find_one({"username": username}):
            error_message = "Username sudah digunakan. Silakan pilih username lain."
            return render_template('register.html', error_message=error_message)

        # Cek apakah email sudah terdaftar
        if users_collection.find_one({"email": email}):
            error_message = "Email sudah terdaftar. Silakan gunakan email lain."
            return render_template('register.html', error_message=error_message)

        # Insert data pengguna baru ke dalam koleksi
        users_collection.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Cari pengguna berdasarkan username
        user = users_collection.find_one({"username": username})

        # Periksa apakah pengguna ada dan password cocok
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
