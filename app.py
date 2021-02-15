from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from auth import init_routes

app = Flask(__name__)

init_routes(app)

if __name__ == '__main__':
    app.run(port = 8080)