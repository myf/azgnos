#!/usr/bin/python2
from optparse import OptionParser
import subprocess
import requests
import sys
try:
    import simplejson as json
except:
    import json
USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36'

def play_station(num_code, cookies=None, proxy=None, download=None):
    if proxy:
        proxies = {
            "http": proxy
        }
    else:
        proxies = None
    headers = {'User-Agent' : USER_AGENT}
    url = "http://songza.com/api/1/station/%s/next" % num_code
    if cookies:
        response = requests.get(url, headers=headers, cookies=cookies, 
                                proxies=proxies)
    else:
        response = requests.get(url, headers=headers, proxies=proxies)
        cookies = response.cookies
    response_json = json.loads(response.text)
    listen_url = response_json['listen_url']
    song = response_json['song']

    print "song is %s by %s" % (song[u'title'], song[u'artist'][u'name'])
    cookie_str = ":".join(map(str, cookies.items()[0]))
    #call(["/usr/bin/mplayer", '-cookies', cookie_str, '-really-quiet', listen_url])
    #call(["/usr/bin/mplayer", '-really-quiet', listen_url])
    #import ipdb;ipdb.set_trace()
    #curl = subprocess.call(["/usr/bin/curl", listen_url], stdout=subprocess.PIPE)
    #mplayer = subprocess.call(["/usr/bin/mplayer", '-really-quiet', "-"], stdin=curl.stdout, stdout=subprocess.PIPE)
    #mplayer.communicate()[0]

    subprocess.call(['/usr/bin/wget', listen_url])
    play_station(num_code, cookies=cookies, proxy=proxy, download=download)

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [options] station_number")
    parser.add_option("-p", "--proxy", dest="proxy", default=None,
            type="string", help="optional http proxy")
    parser.add_option("-d", "--download", dest="download", default=None,
            type="string", help="download flag")
    (options, args) = parser.parse_args()
    try:
        play_station(args[0], proxy=options.proxy, download=options.download)
    except KeyboardInterrupt:
        sys.exit(0)
