import pytest
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

def test_url(url,status):
   req = Request(url)
   try:
    resp = urlopen(req)
   except HTTPError as e:
      print('The server couldn\'t fulfill the request')
      print('Error code: ', e.code)
      assert status == "not_found"
   except URLError as e:
      print('Failed to reach server')
      print('Reason: ', e.reason)
      assert status == "not_found"
   else:
      if (status == "found"):
       assert (resp.code == 200),"url not reachable"
      elif (status == "not_found"):
       assert (resp.code != 200),"url reachable"
      else:
         print("Cannot determine url status to check")
         assert True == False
