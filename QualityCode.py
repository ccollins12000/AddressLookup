
# https://developer.mapquest.com/documentation/geocoding-api/quality-codes/
granularity_lookup = {
    'P1' : {
        'Name': 'POINT',
        'Description': 'A specific point location.'
    },
    'L1' : {
        'Name': 'ADDRESS',
        'Description': 'A specific street address location.'
    },
    'I1' : {
        'Name': 'INTERSECTION',
        'Description': 'An intersection of two or more streets.'
    },
    'B1' : {
        'Name': 'STREET',
        'Description': 'The center of a single street block. House number ranges are returned if available.'
    },
    'B2' : {
        'Name': 'STREET',
        'Description': 'The center of a single street block, which is located closest to the geographic center of all matching street blocks. No house number range is returned.'
    },
    'B3' : {
        'Name': 'STREET',
        'Description': 'The center of a single street block whose numbered range is nearest to the input number. House number range is returned.'
    },
    'A1' : {
        'Name': 'COUNTRY',
        'Description': 'Admin area, largest. For USA, a country.'
    },
    'A3' : {
            'Name': 'STATE',
            'Description': 'Admin area. For USA, a state.'
        },
    'A4' : {
        'Name': 'COUNTY',
        'Description': 'Admin area. For USA, a county.'
    },
    'A5' : {
        'Name': 'CITY',
        'Description': 'Admin area. For USA, a city.'
    },
    'A6' : {
        'Name': 'NEIGHBORHOOD',
        'Description': 'Admin area. For USA, a neighborhood.'
    },
    'Z1' : {
        'Name': 'ZIP',
        'Description': 'Postal code, largest. For USA, a ZIP.'
    },
    'Z2' : {
        'Name': 'ZIP_EXTENDED',
        'Description': 'Postal code. For USA, a ZIP+2.'
    },
    'Z3' : {
        'Name': 'ZIP_EXTENDED',
        'Description': 'Postal code. For USA, a ZIP+4.'
    },
    'Z4' : {
        'Name': 'ZIP',
        'Description': 'Postal code, smallest. Unused in USA.'
    },
}
