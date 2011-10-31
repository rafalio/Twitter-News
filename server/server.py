import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
# This is where we need to setup the main UI
def index():
  return "Index Page!"

@app.route("/story/<int:story_id>")
# This is where we need to setup the story UI. It doesn't have to be an ID, maybe we can use story name.
# But for now I'll leave it as an ID.
def show_story(story_id):
  return "This is story {}".format(story_id)


# API
@app.route("/api/1/news")
def api_main_news():
  return jsonify({'news' : [1,2,3,4,5], 'timestamp': time.time()})

@app.route("/api/1/news/<int:timestamp>")
def api_main_news_since(timestamp):
  return jsonify({'news': [0], 'timestamp': time.time()})

@app.route("/api/1/story/<int:story_id>")
@app.route("/api/1/story/<int:story_id>/short")
def api_story_short(story_id):
  title = "News Story {}".format(story_id)
  return jsonify({'title': title, 'short_summary': 'Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili'})


@app.route("/api/1/story/<int:story_id>/long")
def api_story_long(story_id):
  title = "News Story {}".format(story_id)
  return jsonify({'title': title, 'short_summary': 'Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili',
                  'long_summary': 'Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili Lorem ipsum itae interdum metus cursus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubili'})



if __name__ == "__main__":
  # Setting up debugging environment (server reloads itself and provides better error messages)
  app.debug = True
  app.run()
  # This is, so that the website is externally visible
  #app.run(host='0.0.0.0')