import math

def decode_polyline(encoded):
    """
    Decodes a Google Maps encoded polyline into a list of (latitude, longitude) tuples.
    This method handles decoding correctly, keeping more detailed points.
    """
    polyline = []
    index = 0
    lat = 0
    lng = 0
    length = len(encoded)
    
    while index < length:
        # Decode latitude
        shift = 0
        result = 0
        while True:
            byte = ord(encoded[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break
        delta_lat = (result & 1) != 0 and ~(result >> 1) or (result >> 1)
        lat += delta_lat

        # Decode longitude
        shift = 0
        result = 0
        while True:
            byte = ord(encoded[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break
        delta_lng = (result & 1) != 0 and ~(result >> 1) or (result >> 1)
        lng += delta_lng
        
        # Append the decoded lat/lng as a tuple
        polyline.append((lat / 1E5, lng / 1E5))

    return polyline
encoded_polyline = "u{v~FhhnjMk@BY?WzApN{V"

decoded_points = decode_polyline(encoded_polyline)
print(decoded_points)
