import os
from threading import Timer
from urllib2 import urlopen
from bs4 import BeautifulSoup
from flask import Flask
from jinja2 import Template

# Create jinja2 template from file
with open("template.html", 'r') as f:
    template = Template(f.read())

# Initialize at global scope
page_data = ""

# Get data from metacritic and fill in template
def update_page():
  print "updating page"
  data = BeautifulSoup(urlopen("http://www.metacritic.com/browse/games/score/metascore/90day/all").read())
  game_list = data.select(".list_products")[0]
  games = game_list.select(".product")

  review_data = []

  for game in games:
    review = {}
    score = game.select(".textscore")[0].string

    if score == "tbd":
      continue # Ignore unreviewed games
    else:
      score = float(score)
    
    if score >= 7.5:
      adj = "GOOD"
      css_class = "good"
    elif score >= 5:
      adj = "...ALRIGHT"
      css_class = "avg"
    else:
      adj = "SHIT"
      css_class = "bad"

    review['title'] = game.a.string
    review['platform'] = game.a['href'].split('/')[-2]
    review['score'] = score
    review['adj'] = adj
    review['css_class'] = css_class

    review_data.append(review)

  global page_data
  page_data = template.render(games=review_data)
  Timer(600, update_page).start()

# Create flask app with routes
app = Flask(__name__)

@app.route('/')
def index():
  return page_data

if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 8000
  update_page()
  port = int(os.environ.get('PORT', 8000))
  app.run(host="0.0.0.0", port=port)