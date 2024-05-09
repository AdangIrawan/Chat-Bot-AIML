from flask import Flask, render_template, request
import aiml

app = Flask(__name__)

kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="bot.xml")

def get_response(user_input):
    return kernel.respond(user_input)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.form['user_input']
    bot_response = get_response(user_input)
    return bot_response

if __name__ == '__main__':
    app.run(debug=True)
