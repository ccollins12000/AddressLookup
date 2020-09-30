import requests

class Geocoder:
    """An object for searching for companies using google's custom search engine API

    Attributes:
    """
    def __init__(self, api_key):
        """The constructor for the company searcher

        Args:
            api_key (str): The secret key for accessing the api
            api_app_key (str): The id for the custom search engine
        """
        self._session = requests.session()
        self._response = None
        self._api_key = api_key
        self.address = None
        self.result = None

    def search(self, address):
        """Searches for a company

        Args:
            address (str): The full address of the company
        Raises:
            Exception: If an invalid Bing key is provided
        """
        self.address = address

        # Conduct search
        # search_api_url = 'http://open.mapquestapi.com/geocoding/v1/address'
        search_api_url = 'http://dev.virtualearth.net/REST/v1/Locations'
        params = {'key': self._api_key, 'q': self.address}
        self._response = self._session.get(search_api_url, params=params)

        # Parse results
        #results_data = json.loads(self._response.text)
        #self.result = AddressResult(results_data)

    def write_results(self, write_path):
        """Writes the json response of the google search to a text file

        Args:
            The path to write the file to
        """
        with open(write_path + '.json', 'w') as f:
            f.write(self._response.text)

if __name__ == "__main__":
    api_key = input('Enter the bing api key: ')
    write_path = input('Enter an output path for the response: ')
    geocoder = Geocoder(api_key)
    geocoder.search('paris')
    geocoder.write_results(write_path)

    #rjson.get('resourceSets', [{}])[0].get('resources', [{}])[0].get('address', {})
    #.get('addressLine') #street address
    #.get('adminDistrict') #State
    #.get('adminDistrict2') #County
    #.get('countryRegion') #country
    #.get('formattedAddress') # full address
    #.get('locality') #city
    #.get('postalCode') #zip code
    #.get('formattedAddress') #full address
    #rjson.get('resourceSets', [{}])[0].get('resources', [{}])[0].get('geocodePoints', [{}])[0].get('coordinates', [None, None])

    #unauthorized
    #rjson.get('authenticationResultCode', '') == "InvalidCredentials"

    #if rjson.get('statusCode') != 200:
    #   raise Exception(rjson.get('statusDescription', 'The request returned a non-success status.')
#http://dev.virtualearth.net/REST/v1/Locations?q=100%20Main%20St.%20Somewhere,%20WA%2098001&key={BingMapsAPIKey}