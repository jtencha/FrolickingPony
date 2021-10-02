from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return "I'm in"

def run():
    app.run(host="0.0.0.0", port=8000)

def live():
    server = Thread(target=run)
    server.start()