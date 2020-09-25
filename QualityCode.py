"""A module for parsing a geocode quality code from a MapQuest request

For the reference around geocode quality codes view https://developer.mapquest.com/documentation/geocoding-api/quality-codes/

Attributes:
    granularity_lookup (dict):
        Give a description for and long name for each granularity code. The granularity code is the first two characters
        of the geocode quality code
    confidence_lookup (dict):
        Give a confidence code to see the description and additional considerations. The confidence codes are contained
        in the last three characters of the geocoding quality code.
"""

granularity_lookup = {
    'P1': {
        'Name': 'POINT',
        'Description': 'A specific point location.'
    },
    'L1': {
        'Name': 'ADDRESS',
        'Description': 'A specific street address location.'
    },
    'I1': {
        'Name': 'INTERSECTION',
        'Description': 'An intersection of two or more streets.'
    },
    'B1': {
        'Name': 'STREET',
        'Description': 'The center of a single street block. House number ranges are returned if available.'
    },
    'B2': {
        'Name': 'STREET',
        'Description': 'The center of a single street block, which is located closest to the geographic center of all matching street blocks. No house number range is returned.'
    },
    'B3': {
        'Name': 'STREET',
        'Description': 'The center of a single street block whose numbered range is nearest to the input number. House number range is returned.'
    },
    'A1': {
        'Name': 'COUNTRY',
        'Description': 'Admin area, largest. For USA, a country.'
    },
    'A3': {
        'Name': 'STATE',
        'Description': 'Admin area. For USA, a state.'
    },
    'A4': {
        'Name': 'COUNTY',
        'Description': 'Admin area. For USA, a county.'
    },
    'A5': {
        'Name': 'CITY',
        'Description': 'Admin area. For USA, a city.'
    },
    'A6': {
        'Name': 'NEIGHBORHOOD',
        'Description': 'Admin area. For USA, a neighborhood.'
    },
    'Z1': {
        'Name': 'ZIP',
        'Description': 'Postal code, largest. For USA, a ZIP.'
    },
    'Z2': {
        'Name': 'ZIP_EXTENDED',
        'Description': 'Postal code. For USA, a ZIP+2.'
    },
    'Z3': {
        'Name': 'ZIP_EXTENDED',
        'Description': 'Postal code. For USA, a ZIP+4.'
    },
    'Z4': {
        'Name': 'ZIP',
        'Description': 'Postal code, smallest. Unused in USA.'
    },
}

confidence_lookup = {
    'A': {
        'Confidence': 'Exact',
        'Description': 'Match locations that exactly correspond to the input location, as defined by the address elements specified.',
        'StreetCon': 'Exact matches, although the geocoding engine allows standard variations of road types, directionals, numbered roads, and common abbreviations. Examples include Road vs. RD, North vs. N, Second vs. 2nd, and Mount vs. MT.',
        'AdminCon': 'Exact matches, although common abbreviations are acceptable. For instance, "Mount View" is the same as "Mt. View."',
        'PostalCon': 'The postal code matches at the granularity of the input. The matched postal code may be even more precise than the postal code specified in the input.'
    },
    'B': {
        'Confidence': 'Good',
        'Description': 'Matches should be fairly similar, even if not exactly as specified.',
        'StreetCon': 'Good matches, ignoring differences in road type and directionals. EG: Road vs. Street,North vs. South. Includes matches where type & directional are supplied but not found, or found but not supplied.',
        'AdminCon': 'Good matches, even if administrative area names do not exactly match. This includes sound-alike matches, partial, slight misspellings, or other fuzzy matching. Details vary by geocoding data.',
        'PostalCon': 'Postal code does not exactly match at the granularity of the input. However, the postal code likely matches the input address at a lower granularity level than at the requested granularity.'
    },
    'C': {
        'Confidence': 'Approx',
        'Description': 'Matches should be somewhat similar to the input location as specified.',
        'StreetCon': 'Sound-alike matches, partial matches, slight misspellings, and fuzzy matching. Details vary by geocoding data.',
        'AdminCon': 'Matched administrative areas do not match the input administrative areas. This may occur when the postal code input determines the match.',
        'PostalCon': 'Postal codes do not match. This may occur when the administrative area input determines the match.'
    },
    'X': {
        'Confidence': 'None',
        'Description': 'Confidence level has no meaning for this granularity level or was not used.',
        'StreetCon': 'Confidence level has no meaning for this granularity level or was not used.',
        'AdminCon': 'Confidence level has no meaning for this granularity level or was not used.',
        'PostalCon': 'Confidence level has no meaning for this granularity level or was not used.'
    }
}


class GeocodeQuality:
    """An object for translating and storing a MapQuest geocode quality code.

    """
    def __init__(self, quality_code):
        """The constructor for the geocode quality code

        Args:
            quality_code (str): 5 character quality code from the MapQuest geocode request.
        """
        self._quality_code = quality_code

    def __str__(self):
        granularity = granularity_lookup.get(self._quality_code[0:2])
        granularity = 'Granularity: ' + self._quality_code[0:2] + '\n' + \
                      granularity['Name'] + '\n' + \
                      granularity['Description']
        street_confidence_code = self._quality_code[2]
        street_confidence = 'Full Street Level Confidence: ' + street_confidence_code + '\n' + \
                            confidence_lookup[street_confidence_code]['Description'] + '\n' + \
                            confidence_lookup[street_confidence_code]['StreetCon']
        admin_confidence_code = self._quality_code[3]
        admin_confidence = 'Administrative Area Level Confidence: ' + admin_confidence_code + '\n' + \
                           confidence_lookup[admin_confidence_code]['Description'] + '\n' + \
                           confidence_lookup[admin_confidence_code]['AdminCon']
        postal_confidence_code = self._quality_code[4]
        postal_confidence = 'Postal Code Level Confidence: ' + postal_confidence_code + '\n' + \
                            confidence_lookup[postal_confidence_code]['Description'] + '\n' + \
                            confidence_lookup[postal_confidence_code]['PostalCon']
        return granularity + '\n\n' + street_confidence + '\n\n' + admin_confidence + '\n\n' + postal_confidence


if __name__ == '__main__':
    quality = GeocodeQuality('P1AAA')
    print(quality)