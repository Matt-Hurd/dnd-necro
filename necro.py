import digitalocean

region = 'sf2'
image = 'ubuntu-16-06-x32' #Change to image name
size_slug = '512mb'
class Wisp:
	def __init__(access_token, name):
		self.droplet = digitalocean.Droplet(token=access_token,
                               name = name,
                               region = region,
                               image = image,
                               size_slug=size_slug,  # 512MB
                               backups=False)
		self.droplet.create()