from utils import detect_subdomain


def test_detect_subdomain():
    assert (
        detect_subdomain(host="mydomain.com", base_url="https://mydomain.com") is None
    )
    assert (
        detect_subdomain(host="mydomain.com", base_url="https://mydomain.com:8000")
        is None
    )
    assert (
        detect_subdomain(host="project1.mydomain.com", base_url="https://mydomain.com")
        == "project1"
    )
    assert (
        detect_subdomain(host="mydomain.com", base_url="https://mydomain.com:8000")
        == None
    )
    assert (
        detect_subdomain(
            host="project2.foo.bar.baz", base_url="https://foo.bar.baz:8000"
        )
        == "project2"
    )


def test_local_domains():
    host = "project1.promptsail.local:8000"
    base_url = "http://promptsail.local:8000"
    assert detect_subdomain(host, base_url) == "project1"
