# def test_home_page(client, test_config):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert test_config.BUILD_SHA in response.text
