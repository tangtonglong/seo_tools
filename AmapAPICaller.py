import json
import urllib


class AmapAPICaller:
    def __init__(self, key):
        self.key = 'a010d5798fc1c5035f512f37d3d6c58f'
        self.url = {
            'geo': r'https://restapi.amap.com/v3/geocode/geo',
            'convert': r'https://restapi.amap.com/v3/assistant/coordinate/convert',
            'distance': r'https://restapi.amap.com/v3/distance'
        }
        self.necessary = {
            'geo': ['address'],
            'convert': ['locations'],
            'distance': ['origins', 'destination']
        }
        self.safe_str = "/:=&?#+!$,;'@()*[]"



    def join_parameters(self, parameters_dict, symbol_str='&'):
        assert isinstance(parameters_dict, dict)
        return symbol_str.join(key + '=' + value for key, value in parameters_dict.items())


    def general_call(self, code, **parameters):
        assert isinstance(code, str)
        assert code in self.url and code in self.necessary
        for parameter_name in self.necessary[code]:
            assert parameter_name in parameters
        if 'key' not in parameters:
            parameters['key'] = self.key
        request_str = self.url[code] + '?' + self.join_parameters(parameters)
        data = urllib.request.urlopen(urllib.request.quote(request_str, safe=self.safe_str)).read()
        return json.loads(data.decode())

    def call_geo_lite(self, address, city):
            parameters = {
                'key': self.key,
                'address': address,
                'city': city
            }
            request_str = self.url['geo'] + '?' + self.join_parameters(parameters)
            data = urllib.request.urlopen(urllib.request.quote(request_str, safe=self.safe_str)).read()
            return json.loads(data.decode())
