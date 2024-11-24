from flask import Flask, render_template, request
import os
import redis

app = Flask(__name__)

# Connect to Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# UI Configurations
TITLE = 'Azure Voting App'
VOTE1VALUE = 'Cats'
VOTE2VALUE = 'Dogs'
SHOWHOST = 'false'

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize votes if not already set
    if not redis_client.exists('cats_votes'):
        redis_client.set('cats_votes', 0)
    if not redis_client.exists('dogs_votes'):
        redis_client.set('dogs_votes', 0)

    # Handle vote or reset
    if request.method == 'POST':
        vote = request.form.get('vote')
        if vote == VOTE1VALUE:
            redis_client.incr('cats_votes')
        elif vote == VOTE2VALUE:
            redis_client.incr('dogs_votes')
        elif vote == 'reset':
            redis_client.set('cats_votes', 0)
            redis_client.set('dogs_votes', 0)

    # Get the current vote counts
    cats_votes = redis_client.get('cats_votes')
    dogs_votes = redis_client.get('dogs_votes')

    return render_template(
        'index.html',
        title=TITLE,
        button1=VOTE1VALUE,
        button2=VOTE2VALUE,
        value1=cats_votes,
        value2=dogs_votes
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
