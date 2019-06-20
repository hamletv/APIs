from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "2EU3RQFM2PQFXB5OJVUXZQYC0BSYYUAYNPRQ4YHN4WFG1RQ0"
foursquare_client_secret = "TYPL2UGSJDQBLGR1KNZ1NDTO4HSDRSASVCCII00KKLKGQ0C3"


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	latitude, longitude = getGeocodeLocation(location)
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	mealQuery = mealType.replace(" ", "+")
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20190601&ll=%s&query=%s' % (foursquare_client_id, foursquare_client_secret,latitude, longitude, mealQuery ))
	h = httplib2.Http()
	results = json.loads(h.request(url, 'GET')[1])
	#3. Grab the first restaurant
	if results['response']['venues']:
		resto = results['response']['venues'][0]
		venue_id = resto['id']
		resto_name = resto['name']
		resto_address = resto['location']['formattedAddress']
		address = ""
		for i in resto_address:
			address += i + " "
		resto_address = address
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % (venue_id, foursquare_client_id, foursquare_client_secret))
	results = json.loads(h.request(url, 'GET')[1])
	#5. Grab the first image
	if results['response']['photos']['items']:
		first_pic = results['response']['photos']['items'][0]
		prefix = first_pic['prefix']
		suffix = first_pic['suffix']
		photoURL = prefix + '300x300' + suffix
	else:
	#6. If no image is available, insert default a image url
		imageURL = ('https://cdn.pixabay.com/photo/2014/08/14/14/21/shish-kebab-417994_1280.jpg')
	#7. Return a dictionary containing the restaurant name, address, and image url
	resto_details = {'name': resto_name, 'address': resto_address, 'image': imageURL}
	print resto_details['name']
	print resto_details['address']
	print resto_details['image']
	return resto_details

	print 'No restaurants found in %' location
	return 'No restaurant'

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney, Australia")
