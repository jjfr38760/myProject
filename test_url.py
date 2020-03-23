import pytest
import urllib3

def test_url(url,status):
   http = urllib3.PoolManager()
   try:
    resp = http.request('GET', url)
   except urllib3.exceptions.HTTPError as e:
      print('The server couldn\'t fulfill the request')
      print('Error code: ', e)
      assert status == "not_found"
   else:
      if (status == "found"):
       assert (resp.status == 200),"URL not reachable"
      elif (status == "not_found"):
       assert (resp.status != 200),"URL reachable"
      else:
         print("Cannot determine URL status to check")
         assert True == False
