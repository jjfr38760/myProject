import pytest

def pytest_addoption(parser):
    parser.addoption("--url", action="store")
    parser.addoption("--status", action="store")

@pytest.fixture(scope='session')
def url(request):
    url_value = request.config.option.url
    if url_value is None:
        return "http://localhost:8080/sample"
    return url_value

@pytest.fixture(scope='session')
def status(request):
    status_value = request.config.option.status
    if status_value is None:
       return "found" 
    return status_value
