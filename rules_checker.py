import config
import urllib.request

IPAPI_URL = 'https://ipapi.co/'


def get_country_from_ip(ip_address):
    url = IPAPI_URL + ip_address + '/country_code'
    response = urllib.request.urlopen(url).read()
    return response.decode("utf-8")


def is_country_allowed(ip_address):
    country_code = get_country_from_ip(ip_address)
    return config.WHITE_LIST_OVERRIDE or country_code in config.WHITE_LIST_COUNTRIES
