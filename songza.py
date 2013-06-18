from subprocess import call
import requests
import sys
try:
    import simplejson as json
except:
    import json
USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36'

def play_station(num_code, cookies=None):
    headers = {'User-Agent' : USER_AGENT}
    url = "http://songza.com/api/1/station/%s/next" % num_code
    if cookies:
        response = requests.get(url, headers=headers, cookies=cookies)
    else:
        response = requests.get(url, headers=headers)
        cookies = response.cookies
    response_json = json.loads(response.text)
    listen_url = response_json['listen_url']
    song = response_json['song']
    #{u'album': u'Genesis', u'status': u'ADD', u'title': u'Genesis', u'artist': {u'name': u'Grimes'}, u'cover_url': u'http://images.musicnet.com/albums/064/478/333/a.jpeg', u'duration': 255, u'formats': [{u'available': True, u'format': u'aac'}, {u'available': True, u'format': u'mp3'}], u'genre': u'Electronica/Dance', u'new': False, u'id': 18617187, u'added_by': None}

    print "song is %s by %s" % (song[u'title'], song[u'artist'][u'name'])
    cookie_str = ":".join(map(str, cookies.items()[0]))
    #call(["/usr/bin/mplayer", '-cookies', cookie_str, '-really-quiet', listen_url])
    call(["/usr/bin/mplayer", '-really-quiet', listen_url])
    #call(["/usr/bin/mplayer", listen_url])
    play_station(num_code, cookies=cookies)

if __name__ == "__main__":
    play_station(sys.argv[1])
