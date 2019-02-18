from stem.control import Controller
import stem.process
import requests
import datetime
import traceback
import sys
from stem.util import term

debug = '-v' in sys.argv
SOCKS_PORT_START = 7000


def test_tor(cfg):

    def bootstrap(line):
        if "Bootstrapped " in line:
            print(term.format(line, 'Green'))

    global debug
    tor_process = None
    try:
        port = SOCKS_PORT_START + int(cfg['id'])
        if debug:
            print("Starting Tor {c}:".format(c=cfg['country']))
        cfg_tor = {
            'SocksPort': str(port), 
            'ExitNodes': cfg['country']
        }
        if debug:
            tor_process = stem.process.launch_tor_with_config(
                config = cfg_tor,
                init_msg_handler = bootstrap
            )
        else:
            tor_process = stem.process.launch_tor_with_config(
                config = cfg_tor
            )

        address = 'socks5://127.0.0.1:{p}'.format(p=port)
        session = requests.session()
        session.proxies = {'http': address, 'https': address}

        r = session.get('http://ipecho.net/plain')
        print(term.format('TOR IP is: {ip}'.format(ip=str(r.text)), 'Yellow'))

        if debug:
            print('Killing TOR Process')
        tor_process.kill()

    except:
        print('TOR AGENT EXCEPTION: {e}'.format(e=traceback.format_exc()))
        print('CONFIG: ' + str(cfg))
    try:
        tor_process.kill()
    except:
        pass


def main():
    try:
        print('[{d}] - START -'.format(d=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        cfg = {
            'id': 1,
            'color': term.Color.RED,
            'country': '{ru}'
        }
        test_tor(cfg)
        print('[{d}] - END -'.format(d=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        return 0
    except:
        print('{e}'.format(e=traceback.format_exc()))
    return 1
    

if __name__ == '__main__':
    sys.exit(main())
