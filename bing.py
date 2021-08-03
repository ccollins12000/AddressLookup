import requests
import json

class RouteRetriever:
    """An object for retrieving the route between two locations using Bing's custom search API"""

    def __init__(self, api_key):
        """The constructor for the route retriever utilizing bing
        
        Args:
            api_key (str): The secret key for accessing the api
        
        """
        self._session = requests.session()
        self._response = None
        self._api_key = api_key
        self.start_location = None
        self.end_location = None
        self.route = None

    def calculate_route(self, start_location, end_location, travelMode, **kwargs):
        """Finds the route between two address. Note this object is only setup to handle two waypoints.
        The _response attribute can be accessed to work with the raw response from bing for additional functionality
        
        Args:
            start_location (str): The address of the location to start at
            end_location (str): The address of the location to end at
            travelMode (str): Specifies the mode od travel for the route. Can be Driving, Transit or Walking.
            
            See https://docs.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-a-route
            for full list of additional parameters and details that can be passed to request. 
            Some possible additional parameters:
                
                optmz (optimize) (str): 
                    - distance: The route is calculated to minimize the distance. Traffic information is not used.
                    - time [default]: The route is calculated to minimize the time. Traffic information is not used.
                    - timeWithTraffic: The route is calculated to minimize the time and uses current traffic information.
                    - timeAvoidClosure: The route is calculated to minimize the time and avoid road closures. Traffic not used
                
                du (distanceUnit) (str): mi or km (specifies what unit the distance is returned in)
        
                dt (dateTime) (str): Specifies the time to use for calculating the route Example: dateTime=03/01/2011 05:42:00
                                Use with tt parameter. If only time component is giving, it is assumed to be current day
                
                tt (timeType) (str):
                    - Arrival: The dateTime parameter contains the desired arrival time for a transit request.
                    - Departure: The dateTime parameter contains the desired departure time for a transit request.
                    - LastAvailable: The dateTime parameter contains the latest departure time available for a transit request.
        """
        search_api_url = 'http://dev.virtualearth.net/REST/v1/Routes/{travelMode}'.format(travelMode = travelMode)
        params = {'key': self._api_key, 
                  'wp.0':start_location, 
                  'wp.1':end_location
                  }
        if kwargs:
            params.update(**kwargs)
            
        self._response = self._session.get(search_api_url, params=params)
        
        #Parse Results
        results_data = json.loads(self._response.text)
        if results_data.get('statusCode') != 200:
            raise Exception(results_data.get('statusDescription', 'The request returned a non-success status.'))
    
        self.route = RouteResult(results_data)


class Geocoder:
    """An object for searching for companies using Bing's custom search engine API

    Attributes:
    """
    def __init__(self, api_key):
        """The constructor for the address geocoder utilizing bing

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
            address (str): The address to search for
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
        results_data = json.loads(self._response.text)
        if results_data.get('statusCode') != 200:
            raise Exception(results_data.get('statusDescription', 'The request returned a non-success status.'))

        self.result = AddressResult(results_data.get('resourceSets', [{}])[0].get('resources', [{}])[0])

    def write_results(self, write_path):
        """Writes the json response of the google search to a text file

        Args:
            The path to write the file to
        """
        with open(write_path + '.json', 'w') as f:
            f.write(self._response.text)


class RouteResult:
    """A route object, which contains the details on how to navigate from one address to another. The object will only return
    the first result set.

    Attributes:
        distance_unit (str): The unit of distance used (km or mile)
        duration_unit (str): The unit of duraction used (seconds)
        distance (str): The total distance of the route
        duration (str): The total duration of the route
        duration_traffic (str): The total duration of the route with traffic data
        mode (str): The mode of travel required for the route
        start_location (obj): The address that bing utilized as the start address as an AddressObject
        end_location (obj): The address that bing utilized as the end address as an AddressObject
        print_instructions (str): A step by step print out of instructions to travel the route

    """
    def __init__(self, response):
        self._response = response
        self._results = self._response.get('resourceSets', [{}])[0].get('resources', [{}])
        
    @property
    def distance_unit(self):
        return self._results[0].get('distanceUnit')
        
    @property
    def duration_unit(self):
        return self._results[0].get('durationUnit')
        
    @property
    def distance(self):
        return self._results[0].get('travelDistance')
    
    @property
    def duration(self):
        return self._results[0].get('travelDuration')
    
    @property
    def duration_traffic(self):
        return self._results[0].get('travelDurationTraffic')
    
    @property
    def mode(self):
        return self._results[0].get('travelMode')
    
    @property
    def start_location(self):
        return AddressResult(self._results[0].get('routeLegs', [{}])[0].get('endLocation', {}))
        
    @property
    def end_location(self):
        return AddressResult(self._results[0].get('routeLegs', [{}])[0].get('startLocation', {}))
        
    @property
    def print_instructions(self):
        all_instructions = ''
        
        #Each segement between two waypoints requested is considered a route leg
        for routeLeg in self._results[0].get('routeLegs', [{}]):
            #each route leg has multiple steps
            for direction in routeLeg.get('itineraryItems',[{}]):
                all_instructions += "(" + str(direction.get('travelDistance',{})) + ") "
                all_instructions += direction.get('instruction',{}).get('text') + '\n'
        
        return all_instructions

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
        self._location = response.get('address', {})
        self._coordinates = response.get('geocodePoints', [{}])[0].get('coordinates', [None, None])

    @property
    def street_address(self):
        return self._location.get('addressLine')

    @property
    def zip_code(self):
        return self._location.get('postalCode')

    @property
    def neighborhood(self):
        return self._location.get('adminArea6')

    @property
    def city(self):
        return self._location.get('locality')

    @property
    def county(self):
        return self._location.get('adminDistrict2')

    @property
    def state(self):
        return self._location.get('adminDistrict')

    @property
    def country(self):
        return self._location.get('countryRegion')

    @property
    def latitude(self):
        return self._coordinates[0]

    @property
    def longitude(self):
        return self._coordinates[1]

    @property
    def geocode_quality(self):
        return self._response.get('confidence', '')

    @property
    def geocode_quality_code(self):
        return str(self._response.get('matchCodes', str([])))

    def __str__(self):
        return self._location.get('formattedAddress')


if __name__ == "__main__":
    #Testing the code:
    api_key = input('Enter the bing api key: ')
    write_path = input('Enter the output path ')
    
    #write_path = input('Enter an output path for the response: ')
    geocoder = Geocoder(api_key)
    geocoder.search('81 1st st N, Paris')
    geocoder.write_results(write_path)
    print(geocoder.result)
    print(geocoder.result.longitude)
    print(geocoder.result.latitude)
    print(geocoder.result.geocode_quality)
    print(geocoder.result.country)
    print(geocoder.result.state)
    print(geocoder.result.county)
    print(geocoder.result.city)
    print(geocoder.result.neighborhood)
    print(geocoder.result.zip_code)
    print(geocoder.result.street_address)
    print(str(geocoder.result))
    start = 'Mall of America'
    end = 'Minneapolis Airport'
    route_retriever = RouteRetriever(api_key)
    route_retriever.calculate_route(start, end, 'Driving', dt ='07:00:00',tt='Arrival')
    route_retriever.calculate_route(start, end, 'Driving', optmz = 'distance')
    
    
    print(route_retriever.route.distance_unit)
    print(route_retriever.route.duration_unit)
    print(route_retriever.route.distance)
    print(route_retriever.route.duration)
    print(route_retriever.route.duration_traffic)
    print(route_retriever.route.mode)
    print(str(route_retriever.route.start_location))
    print(str(route_retriever.route.end_location))
    print(route_retriever.route.print_instructions)
    
    text = json.dumps(json.loads(route_retriever._response.text), indent=2)
    with open(write_path + '.json', 'w') as f:
            f.write(text)
            
            