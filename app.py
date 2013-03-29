from urllib2 import urlopen
from bs4 import BeautifulSoup

out_file = open("index.html", 'w')

out_file.write("""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>FUCKING GAME REVIEWS</title>
</head>
<body>
<h1>FUCKING GAME REVIEWS</h1>""")

data = BeautifulSoup(urlopen("http://www.metacritic.com/browse/games/score/metascore/90day/all").read())
game_list = data.select(".list_product_condensed")[0]
games = game_list.select(".product")

for game in games:
  title = game.a.string
  score = game.select(".textscore")[0].string

  if score == "tbd":
    continue # Ignore unreviewed games
  else:
    score = float(score)
  
  if score >= 7.5:
    adj = "GOOD"
  elif score >= 5:
    adj = "...ALRIGHT"
  else:
    adj = "SHIT"

  out_file.write("""
  <h3>%s</h3>
  IT'S FUCKING %s""" % (title, adj))

out_file.write("""
</body>
</html>""")

