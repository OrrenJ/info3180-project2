import requests
from bs4 import BeautifulSoup
import urlparse

def get_images(url):

	img_list = []

	result = requests.get(url)
	soup = BeautifulSoup(result.text, "html.parser")

	# This will look for a meta tag with the og:image property
	og_image = (soup.find('meta', property='og:image') or
	                    soup.find('meta', attrs={'name': 'og:image'}))
	if og_image and og_image['content']:
	    img_list.append(og_image['content'])

	# This will look for a link tag with a rel attribute set to 'image_src'
	thumbnail_spec = soup.find('link', rel='image_src')
	if thumbnail_spec and thumbnail_spec['href']:
	    img_list.append(thumbnail_spec['href'])

	for img in soup.findAll("img", src=True):
	   img_list.append(urlparse.urljoin(url, img["src"]))

	return img_list

