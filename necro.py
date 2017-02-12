import digitalocean
from secrets import DO_TOKEN, SSH_KEY
from datetime import datetime
from datetime import timedelta
import time
import thread
import socket

region = 'SFO2'
image = '22783408' #Wisp-B
size_slug = '512mb'
class Wisp:
    active = False
    def __init__(self, access_token, name, tag):
        self.droplet = digitalocean.Droplet(token=access_token,
                               name = name,
                               region = region,
                               image = image,
                               size_slug=size_slug,
                               ssh_keys=[SSH_KEY],
                               private_networking=True,
                               backups=False)
        self.droplet.create()

    def kill(self):
        self.droplet.destroy()

    @property
    def created_at(self):
        if self.droplet.created_at:
            return datetime.strptime(self.droplet.created_at, "%Y-%m-%dT%H:%M:%SZ")
        else:
            self.droplet.load()
            return None

    @property
    def private_ip_address(self):
        if not self.droplet.private_ip_address:
            self.droplet.load()
        return self.droplet.private_ip_address

def check_alive(wisps):
    to_remove = []
    for wisp in wisps:
        if not wisp.active and wisp.created_at:
            if (datetime.now() - wisp.created_at) > timedelta(minutes = 2):
                to_remove.append(wisp)
    for wisp in to_remove:
        wisps.remove(wisp)
        wisp.kill()
        print("Killed a wisp")

def party_wipe(wisps):
    for wisp in wisps:
        wisp.kill()

def receive_alive_signal(wisps, ip):
    for wisp in wisps:
        if not wisp.droplet.private_ip_address:
            wisp.droplet.load()
            if not wisp.droplet.private_ip_address:
                print("Node isn't loaded yet?")
                continue
        if not wisp.active:
            if ip == wisp.droplet.private_ip_address:
                print("Node Loaded")
                wisp.active = True

def udp_listener(wisps):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind(('', UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        if data == 'WHISPER':
            print("%s is alive" % addr[0])
            receive_alive_signal(wisps, addr[0])

def udp_message(wisp, message):
    UDP_IP = wisp.private_ip_address
    UDP_PORT = 5010

    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.sendto(message, (UDP_IP, UDP_PORT))

def check_thread(wisps):
    while True:
        check_alive(wisps)
        time.sleep(10)

def clean_by_tag(tag):
    manager = digitalocean.Manager(token=DO_TOKEN)
    my_droplets = manager.get_all_droplets(tag_name=tag)
    for droplet in my_droplets:
        droplet.destroy()

if __name__ == '__main__':
    clean_by_tag('wisp')
    time.sleep(5) #time for droplets to spin down
    wisps = []
    tag = digitalocean.Tag(token=DO_TOKEN, name="wisp")
    tag.create()
    try:
        manager = digitalocean.Manager(token=DO_TOKEN)
        count = len(manager.get_all_droplets())
        while count < 25:
            wisps.append(Wisp(DO_TOKEN, 'wisp-from-api-%d' % count, tag))
            count += 1
        tag.add_droplets([str(w.droplet.id) for w in wisps])
    except Exception as e:
        print(e)
    thread.start_new_thread(check_thread, (wisps,))
    thread.start_new_thread(udp_listener, (wisps,))
    # time.sleep(60)
    # for wisp in wisps:
    #     udp_message(wisp, 'touch /usr/local/bin/a')
    while True:
        pass