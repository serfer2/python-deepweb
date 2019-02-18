import stem.process
import requests
import datetime
import traceback
import sys
from stem.util import term
from stem.control import Controller
from stem import Signal

CONTROLLER_PORT = 9051
PROXIES = {
  'http': 'http://127.0.0.1:8118',
  'https': 'http://127.0.0.1:8118'
}
HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11'
}
PASS = 'aVerySecurePassword'

debug = '-v' in sys.argv


def test_connection():
    session = requests.session()
    session.proxies = PROXIES
    r = session.get(
        'http://ipecho.net/plain',
        proxies = PROXIES,
        headers = HEADERS
    )
    print(term.format('TOR IP is: {ip}'.format(ip=str(r.text)), 'Yellow'))


def main():

    try:

        print('[{d}] - START -'.format(d=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        test_connection()

        with Controller.from_port(port = CONTROLLER_PORT) as controller:
            controller.authenticate(password = PASS)
            controller.signal(Signal.NEWNYM)
        
        test_connection()

        print('[{d}] - END -'.format(d=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        return 0
    except:
        print('{e}'.format(e=traceback.format_exc()))
    return 1
    

if __name__ == '__main__':
    sys.exit(main())
