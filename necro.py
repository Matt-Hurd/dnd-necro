import digitalocean
from secrets import DO_TOKEN

region = 'SFO2'
image = '22780196' #Change to image name
size_slug = '512mb'
tag = digitalocean.Tag(token=DO_TOKEN, name="wisp")
tag.create()
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
        tag.add_droplets([str(self.droplet.id)])

    def kill(self):
        self.droplet.destroy()

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

if __name__ == '__main__':
    # wisp = Wisp(DO_TOKEN, 'wisp-from-api')
    pass