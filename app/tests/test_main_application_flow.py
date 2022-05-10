import pytest
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from bs4 import BeautifulSoup
from app import APP_ROOT_PATH


def safe_request_status(url):
    s = Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))

    return s.get(url)


def assert_app_status(url, status_code):
    response = safe_request_status(url)

    assert response.status_code == status_code, "Could not get a proper response from url. returned body: {}" \
        .format(BeautifulSoup(response.content).prettify())


@pytest.fixture
def run_docker():
    import docker
    client = docker.from_env()

    try:
        client.images.build(tag="opsschool/kandula-test-app", path=str(APP_ROOT_PATH.parent.expanduser()))
        client.containers.run(image="opsschool/kandula-test-app",
                              name='pytest_tests',
                              detach=True,
                              stdout=True,
                              ports={'5000': 5000},
                              environment={'FLASK_ENV': 'development', 'AWS_ACCESS_KEY_ID': "test",
                                           'AWS_SECRET_ACCESS_KEY': 'test'})

        yield
    except Exception as e:
        raise AssertionError(e)

    for container in client.containers.list():
        if 'pytest_tests' in container.name:
            print('Cleaning', container.name, '...')
            container.kill()

    client.containers.prune()


@pytest.mark.usefixtures('run_docker')
class TestLiveServer:

    def test_application_is_up_and_running(self):
        assert_app_status("http://127.0.0.1:5000/", 200)

    def test_application_health_is_good(self):
        assert_app_status("http://127.0.0.1:5000/health", 200)
