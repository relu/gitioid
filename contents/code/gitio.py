import sys, urllib

class gitio:
	def __init__(self, url):
		param = urllib.urlencode({'url': url})
		self.response = urllib.urlopen('http://git.io', param)

	def shorturl(self):
		return self.response.info().getheader('Location')

