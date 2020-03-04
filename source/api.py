from flask import Flask, redirect, request
from flask_restful import Resource, Api
from resources import createVideo, workDispatcher, addToQueue
from threading import Thread
from multiprocessing.pool import ThreadPool
import random
import os.path
import os
app = Flask(__name__)
api = Api(app)

# initialize work dispatcher
queueThread = Thread(target=workDispatcher, daemon=True, args=(ThreadPool(10),))
queueThread.start()

@app.route("/")
def home():
    return "I'm alive lmao :D"


@app.route('/user')
def runVideoMaker():
    twitterName = request.args.get('twittername')
    if twitterName is None:
        return "NO NAME SUPPLIED", 400

    hashCreated = str(random.getrandbits(32))
    addToQueue(hashCreated,twitterName)
    return {"videoURL" : 'http://ec2-3-16-114-144.us-east-2.compute.amazonaws.com/video/' + hashCreated + '.ogg'}

@app.route('/video/<name>')
def watchVideo(name):
    if not os.path.isfile(f'/var/www/html/videoApp/source/static/video_generated/{name}'):
        return {"Error" : "Video is still being created, wait a sec, thnx"}

    html = f"""
        <video controls width="100%">

            <source src="/static/video_generated/{name}"
                    type="video/ogg">

            Sorry, your browser doesn't support embedded videos.
        </video>
    """
    return html, 200

if __name__ == '__main__':
    app.run(debug=True)
