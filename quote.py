import json
import urllib.request

r = urllib.request.urlopen("http://quotes.stormconsultancy.co.uk/random.json").read()

j = json.loads(r.decode())

print(j['quote'] + "\n\n" + "-- " + j['author'])
