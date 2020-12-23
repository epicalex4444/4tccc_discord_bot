import json
import requests
import base64
import zlib

#converts a list/tuple of strings into a comma seperated string
def list_to_string(_list):
    _str = ''
    for i in _list:
        _str += i + ', '
    return _str[:-2]