import digitalocean
from secrets import DO_TOKEN
from datetime import datetime
import time
import thread

region = 'SFO2'
image = '22780196' #Change to image name
size_slug = '512mb'
class Wisp:
    active = False
    def __init__(self, access_token, name):
        self.droplet = digitalocean.Droplet(token=access_token,
                               name = name,
                               region = region,
                               image = image,
                               size_slug=size_slug,
                               private_networking=True,
                               backups=False)
        self.droplet.create()
        tag = digitalocean.Tag(token=DO_TOKEN, name="wisp")
        tag.create()
        tag.add_droplets([str(self.droplet.id)])

    def kill(self):
        self.droplet.destroy()

    @property
    def created_at(self):
        if self.droplet.created_at:
            return datetime.strptime(self.droplet.created_at, "%Y-%m-%dT%H:%M:%S")
        else:
            return None

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
                wisp.active = True

def check_thread(wisps):
    while True:
        check_alive(wisps)
        time.sleep(10)

if __name__ == '__main__':
    wisp = Wisp(DO_TOKEN, 'wisp-from-api')
    wisps = [wisp]
    thread.start_new_thread(check_thread, (wisps,))
    while True:
        pass