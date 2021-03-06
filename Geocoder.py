import requests
import json
import QualityCode

class Geocoder:
    """An object for searching for companies using MapQuests's custom search engine API

    Attributes:
        result (obj): Address result from search method
        address (str): The last address searched for
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
        """Searches for an address

        Args:
            address (str): The full address

        Raises:
            Exception: If an invalid MapQuest key is provided or if MapQuest response contains an error message
        """
        self.address = address

        # Conduct search
        # search_api_url = 'http://open.mapquestapi.com/geocoding/v1/address'
        search_api_url = 'http://www.mapquestapi.com/geocoding/v1/address'
        params = {'key': self._api_key, 'location': self.address}
        self._response = self._session.get(search_api_url, params=params)

        if self._response.text == 'The AppKey submitted with this request is invalid.':
            raise Exception('An invalid api key was provided for MapQuest')

        # Parse results
        results_data = json.loads(self._response.text)
        if results_data.get('info', {}).get('statuscode') != 0:
            raise Exception(results_data.get('info', {}).get('messages', 'There was an error with the MapQuest request'))

        self.result = AddressResult(results_data)

    def write_results(self, write_path):
        """Writes the json response of the geocode search to a text file

        Args:
            The path to write the file to
        """
        with open(write_path + '.json', 'w') as f:
            f.write(self._response.text)


class AddressResult:
    """An address object

    Attributes:
        street_address (str): The street address. Example: 1 Main St
        neighborhood (str): The neighborhood of the address result
        city (str): The city
        county (str): The county
        state (str): The state
        country (str): The country
        latitude (str): The latitude of the address
        longitude (str): The longitude of the address
        geocode_quality (str): The quality of the result found
        geocode_quality_code (str): The quality of the result found
        side_of_street (str): which side of the street the result is on
    """
    def __init__(self, response):
        self._response = response
        self._location = response.get('results', [{}])[0].get('locations', [{}])[0]

    @property
    def street_address(self):
        return self._location.get('street')

    @property
    def neighborhood(self):
        return self._location.get('adminArea6')

    @property
    def city(self):
        return self._location.get('adminArea5')

    @property
    def county(self):
        return self._location.get('adminArea4')

    @property
    def state(self):
        return self._location.get('adminArea3')

    @property
    def country(self):
        return self._location.get('adminArea1')

    @property
    def latitude(self):
        return self._location.get('latLng', {}).get('lat')

    @property
    def longitude(self):
        return self._location.get('latLng', {}).get('lng')

    @property
    def geocode_quality(self):
        return QualityCode.GeocodeQuality(self._location.get('geocodeQualityCode', 'A1XXX'))

    @property
    def geocode_quality_code(self):
        return self._location.get('geocodeQualityCode')

    @property
    def side_of_street(self):
        return self._location.get('sideOfStreet')


if __name__ == "__main__":
    api_key = input('Enter the MapQuest key: ')
    write_path = input('Enter an output path for the response: ')
    geocoder = Geocoder(api_key)
    geocoder.search('Paris')
    geocoder.write_results(write_path)