import digitalocean
from secrets import DO_TOKEN

region = 'SFO2'
image = '22780196' #Change to image name
size_slug = '512mb'
tag = digitalocean.Tag(token=access_token, name="wisp")
tag.create()
class Wisp:
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

if __name__ == '__main__':
	wisp = Wisp(DO_TOKEN, 'wisp-from-api')