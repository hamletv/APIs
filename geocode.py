import httplib2
import json
import sys

def getGeocodeLocation(locationToFind):
    google_api_key = "AIzaSyB6YrgOPJezQJRAYIXLfqvL1ArN69-fUm0"
    locationString = locationToFind.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (locationString, google_api_key))
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)  # json.loads formats content in easy to read but still JSON format
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude, longitude)
