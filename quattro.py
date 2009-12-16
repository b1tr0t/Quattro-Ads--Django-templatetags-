from urlparse import urlparse
import urllib2
import socket
from django.http import QueryDict

class Quattro(object):
    QUATTRO_URL = "http://ad.qwapi.com/adserver/render"
    QUERY_STRING_KEYS = ["ua", "uip", "pid", "sid", "dma", "area", "zip", "mdn", "g", "age", "bday", "hhi", "edu", "eth", "test"]
    
    def __init__(self, request, **kwargs): 
        """
        # required kwargs
        pid="", sid="", 
        
        # optional ad targeting kwargs
        dma=None, area=None, zip=None, mdn=None, g=None, age=None, bday=None, hhi=None, edu=None, eth=None, 
        
        # optional behavioral arguments
        test="1", timeout=1, fail_silently=False  
        """
        self.request = request 
        for arg, value in kwargs.items():
            setattr(self, arg, value)

        # set defaults / request data
        self.ua = request.META.get("HTTP_USER_AGENT", "")
        self.uip = request.META.get("REMOTE_ADDR", "0.0.0.0")
        for k, v in {'timeout': 1, 'fail_silently': False, 'test': 1, 'code': 'php'}.items():
            if not hasattr(self, k):
                setattr(self, k, v)
        
    def renderAd(self):
        url = self.buildRequestUrl()
        default_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(self.timeout)
        try:
            req = urllib2.Request(url, headers=self.getClientHeaders())
            return urllib2.urlopen(req).read()
        except urllib2.URLError:
            if fail_silently:
                return ""
            raise
        finally:
            socket.setdefaulttimeout(default_timeout)

    def buildRequestUrl(self):
        qd = QueryDict("", mutable=True)
        for key in Quattro.QUERY_STRING_KEYS:
            value = getattr(self, key, None)
            if value:
                qd[key] = value
        return Quattro.QUATTRO_URL + "?" + qd.urlencode()
    
    def getClientHeaders(self):
        client_headers = {}
        for k, v in self.request.META.items():
            if 'HTTP_' in k:
                k = k.replace('_', ' ')
                k = k.replace(' ', '-')
                client_headers[k] = v
        return client_headers