# -*- coding: utf-8 -*-

import bing as b
import csv
import pandas as pd

api_key = input('Enter the bing api key: ')

route_retriever = b.RouteRetriever(api_key)
start = 'Mall of America'
end = 'Minneapolis Airport'

route_retriever.calculate_route(
            start, 
            end, 
            'Driving', 
            optmz = 'timeWithTraffic',
            dt ='07:00:00',
            tt='Arrival')
route1 = route_retriever.route
        
route_retriever.calculate_route(
            start, 
            end, 
            'Driving', 
            optmz = 'distance')
route2 = route_retriever.route

route3 = route_retriever.calculate_route(
            start, 
            end, 
            'Walking', 
            dt ='07:00:00',
            tt='Arrival')
route3 = route_retriever.route
    
route4 = route_retriever.calculate_route(
            start, 
            end, 
            'Transit', 
            dt ='07:00:00',
            tt='Arrival')
route4 = route_retriever.route
        
data = {
        "address1":start,
        "address2":end,
        "Driving1_Distance":route1.distance,
        "Driving1_Duration":route1.duration,
        "Driving1_Instructions":route1.print_instructions,
        "Driving1_Start":str(route1.start_location),
        "Driving1_End":str(route1.end_location),
        "Driving2_Distance":route2.distance,
        "Driving2_Duration":route2.duration,
        "Driving2_Instructions":route2.print_instructions,
        "Driving2_Start":str(route2.start_location),
        "Driving2_End":str(route2.end_location),
        "Walking_Distance":route3.distance,
        "Walking_Duration":route3.duration,
        "Walking_Instructions":route3.print_instructions,
        "Walking_Start":str(route3.start_location),
        "Walking_End":str(route3.end_location),
        "Transit_Distance":route4.distance,
        "Transit_Duration":route4.duration,
        "Transit_Instructions":route4.print_instructions,
        "Transit_Start":str(route4.start_location),
        "Transit_End":str(route4.end_location),
        }

data2 = pd.DataFrame.from_dict(data, orient='index')
data2.to_csv('sample_data.csv')
