from django.core.handlers.wsgi import WSGIRequest
from django.template import Template, Context
from django.test import TestCase, Client
from quattro import Quattro

try:
    import wingdbstub
except:
    pass


IPHONE_UA = """Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3"""

class RequestFactory(Client):
    def request(self, **request):
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)

test_request_params = {
    "HTTP_USER_AGENT": IPHONE_UA,
    "REMOTE_ADDR": "127.0.0.1"
}

test_request = RequestFactory(**test_request_params).get("/")
test_publisher_id = "fe8d7e84da8543f597945ff5ab686db5"
test_site_id = "mobify-g396es2r"

class TestQuattro(TestCase):
    def test_quattro(self):
        kwargs = {'pid': test_publisher_id, 'sid': test_site_id,
                  'test': '1', 'dma': '232', 'area': '310', 'zip': '90292',
                  'g': 'm', 'age': '22'
                  }
        quattro = Quattro(test_request, **kwargs)
        response = quattro.renderAd()
        print response
        self.assertTrue(len(response))
        self.assertFalse('message code' in response)
    
class TemplateTagTest(TestCase):
    def test_quattro(self):
        t = Template('{%% load quattro_tags %%}{%% quattro "%s" "%s" %%}' % (test_publisher_id, test_site_id))
        c = Context({"request": test_request})
        response = t.render(c)
        self.assertFalse('message code' in response)
        self.assertTrue(len(response))