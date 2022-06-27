from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .database import Database

app = Flask(__name__)

# Initialize limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per min"]
)

db = Database()     # Initialize database connection


# Passwords route is limited to 5 requests per minute
@app.route('/passwords')
@limiter.limit("5 per minute")
def get_passwords():
    _from = request.args.get('from', default=0, type=int)
    limit = request.args.get('limit', default=1000, type=int)
    return {'data': db.get_passwords(_from, limit)}
