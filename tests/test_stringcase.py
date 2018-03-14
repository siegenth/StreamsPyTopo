import requests
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises

"""
https://streamsproxy.mybluemix.net/TopoDisplay
https://streamsproxy.mybluemix.net/streamsx.inet.resources/
https://streamsproxy.mybluemix.net/myStreams/TupleRequest/ports/analyze/0/lower?MiXuPpEr
https://streamsproxy.mybluemix.net/myStreams/TupleRequest/ports/analyze/0/upper?MiXuPpEr
"""
def test_upper():
    r = requests.get('https://streamsproxy.mybluemix.net/myStreams/TupleRequest/ports/analyze/0/upper?MiXuPpEr')
    assert_equal(r.status_code, 200)
    assert_equal(r.text,"MIXUPPER", True)

def test_lower():
    r = requests.get('https://streamsproxy.mybluemix.net/myStreams/TupleRequest/ports/analyze/0/lower?MiXlOwEr')
    assert_equal(r.status_code, 200)
    assert_equal(r.text,"mixlower", True)

if __name__ == "__main__":
    test_lower()
    test_upper()


