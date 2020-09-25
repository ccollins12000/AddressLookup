import requests
import json

class Geocoder:
    """An object for searching for companies using google's custom search engine API

    Attributes:
        company (str): The name of the company
        company_id (int): The id of the company
        results (obj): A list of search results
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
        self.company_id = 0
        self.address = None
        self.result = None

    def search(self, address):
        """Searches for a company

        Args:
            address (str): The full address of the company
            company_id (int): The id of the company

        Raises:
            Exception: If an invalid MapQuest key is provided
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
        self.result = AddressResult(results_data)

    def write_results(self, write_path):
        """Writes the json response of the google search to a text file

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
        self._location = response['results'][0]['locations'][0]

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
        self._location.get('adminArea4')

    @property
    def state(self):
        self._location.get('adminArea3')

    @property
    def country(self):
        self._location.get('adminArea1')

    @property
    def latitude(self):
        return self._location['latLng']['lat']

    @property
    def longitude(self):
        return self._location['latLng']['lng']

    @property
    def geocode_quality(self):
        self._location.get('geocodeQuality')

    @property
    def geocode_quality_code(self):
        self._location.get('geocodeQualityCode')

    @property
    def side_of_street(self):
        self._location.get('sideOfStreet')