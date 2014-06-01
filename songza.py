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
    import ipdb; ipdb.set_trace()
    listen_url = response_json['listen_url']
    song = response_json['song']

    print "song is %s by %s" % (song[u'title'], song[u'artist'][u'name'])
    cookie_str = ":".join(map(str, cookies.items()[0]))
    #call(["/usr/bin/mplayer", '-cookies', cookie_str, '-really-quiet', listen_url])
    call(["/usr/bin/mplayer", '-really-quiet', listen_url])
    #call(["/usr/bin/mplayer", listen_url])
    play_station(num_code, cookies=cookies)

if __name__ == "__main__":
    try:
        play_station(sys.argv[1])
    except KeyboardInterrupt:
        sys.exit(0)
