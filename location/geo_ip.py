#!/usr/bin/env python 

import os
import pygeoip
import pycountry as pc
import re

class GeoIPUtil(object):
    
    CUR_PATH = os.path.dirname(os.path.abspath(__file__))
    GEO_IP_DB_PATH = os.path.join(CUR_PATH, "db", "GeoLiteCity.dat")

    def __init__(self):
        self.gi = pygeoip.GeoIP(GeoIPUtil.GEO_IP_DB_PATH, pygeoip.MEMORY_CACHE)
        
    #resolve by IP    
    def get_loc_by_ip(self, ip_address):
        try:
            response = self.gi.record_by_addr(ip_address)
            return self.format(response)
        except:
            #print('Unable to resolve loc for ip:', ip_address)
            return None    

    #resolve by Domain
    def get_loc_by_domain(self, domain):
        try:
            response = self.gi.record_by_name(domain)
            return self.format(response)
        except:
            #print('Unable to resolve loc for domain:', domain)
            return self.get_country_by_domain(domain)            
        return None

    def format(self, response):
        output = {}
        output['country'] = response['country_name']
        output['region'] = response['region_code']
        output['city'] = response['city']
        output['latitude'] = response['latitude']
        output['longitude'] = response['longitude']
        return output

    def get_country_by_domain(self, domain):
        #TODO it would be simpler to do on domain ext
        pattern = re.compile("[\.|a-z|0-9|_|-]+\.([a-z]{2})$")
        match = pattern.match(domain)
        if match is None:
            return None
        try:
            country = pc.countries.get(alpha_2=str.upper(match.groups(1)[0])).name
            #print ('country is', country)
            return {'country': country}
        except Exception as e:
            #print(e)
            return None


if __name__ == "__main__":
    geo_ip = GeoIPUtil()
    print(geo_ip.get_loc_by_domain("van15423.direct.ca"))
    print(geo_ip.get_country_by_domain("wwwsv1.u-aizu.ac.jp"))
    print(geo_ip.get_country_by_domain("ppp3_186.bekkoame.or.jp"))
    print(geo_ip.get_country_by_domain("core.sci.toyama-u.ac.jp"))
    print(geo_ip.get_country_by_domain("lab1-c.ia.pw.edu.pl"))
    print(geo_ip.get_country_by_domain("dice2-f.desy.de"))
