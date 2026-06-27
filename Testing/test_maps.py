from backend.maps import MapsClient

def test_get_coordinates_valid_address():
    # Assuming that passing a real location will return valid coordinates
    client = MapsClient()
    lat, lng = client.get_coordinates("London, UK")


    # Check that we received actual data, not 'None'
    assert lat is not None
    assert lng is not None

    # Check the data types are correct
    assert isinstance(lat, float)
    assert isinstance(lng, float)

def test_get_coordinates_invalid_address():
    # Passing random words should trigger error handling
    client = MapsClient()
    lat, lng = client.get_coordinates("RandomPlace_MiddleOfNowhere_Bob")
    
    assert lat is None
    assert lng is None