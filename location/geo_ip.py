#!/usr/bin/env python 

import os
import pygeoip
import pycountry as pc
import re

class GeoIPUtil(object):
    
    CUR_PATH = os.path.dirname(os.path.abspath(__file__))
    GEO_IP_DB_PATH = os.path.join(CUR_PATH, "db", "GeoLiteCity.dat")

    def __init__(self):
        self.gi = pygeoip.GeoIP(GeoIPUtil.GEO_IP_DB_PATH)
        
    #resolve by IP    
    def get_loc_by_ip(self, ip_address):
        try:
            response = self.gi.record_by_addr(ip_address)
            return self.format(response)
        except:
            print('Unable to resolve loc for ip:', ip_address)
        return None    

    #resolve by Domain
    def get_loc_by_name(self, domain):
        try:
            response = self.gi.record_by_name(domain)
            return self.format(response)
        except:
            print('Unable to resolve loc for domain:', domain)
            return self.get_country(domain)            
        return None

    def format(self, response):
        output = {}
        output['country'] = response['country_name']
        output['region'] = response['region_code']
        output['city'] = response['city']
        output['latitude'] = response['latitude']
        output['longitude'] = response['longitude']
        return output

    def get_country(self, domain):
        pattern = re.compile("[\.|a-z|0-9]+\.([a-z]{2})$")
        match = pattern.match(domain)
        if match is None:
            return None
        try:
            country = pc.countries.get(alpha_2=str.upper(match.groups(1)[0])).name
            return {'country': country}
        except Exception as e:
            #print(e)
            return None


if __name__ == "__main__":
    geo_ip = GeoIPUtil()
    print(geo_ip.get_loc_by_name("van15423.direct.ca"))
    print(geo_ip.get_loc_by_name("www.irctc.co.in"))
    print(geo_ip.get_loc_by_name("www.umn.edu"))
