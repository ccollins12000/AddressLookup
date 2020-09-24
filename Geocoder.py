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
        self.address_id = None
        self.result = None

    def search(self, address):
        """Searches for a company

        Args:
            address (str): The full address of the company
            company_id (int): The id of the company
        """
        self.address = address

        # Conduct search
        # search_api_url = 'http://open.mapquestapi.com/geocoding/v1/address'
        search_api_url = 'http://www.mapquestapi.com/geocoding/v1/address'
        params = {'key': self._api_key, 'location': self.address}
        self._response = self._session.get(search_api_url, params=params)

        # Parse results
        results_data = json.loads(self._response.text)
        self.result = MapQuestLocation(results_data)

    def write_results(self, write_path):
        """Writes the json response of the google search to a text file

        Args:
            The path to write the file to
        """
        with open(write_path + '/' + str(self.address_id) + '.json', 'w') as f:
            f.write(self._response.text)


class AddressResult:
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
