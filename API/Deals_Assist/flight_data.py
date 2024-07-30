from dataclasses import dataclass

@dataclass
class FlightData:
    price: int
    departure_airport_code: str
    destination_airport_code: str
    out_date: str
    return_date: str
    stops: int


def generate_flight_data(flight: dict) -> FlightData:
    price: float = float(flight['price']['grandTotal'])
    departure_city_code: str = flight['itineraries'][0]['segments'][0]['departure']['iataCode']
    destination_city_code: str = flight['itineraries'][0]['segments'][0]['arrival']['iataCode']
    out_date: str = flight['itineraries'][0]['segments'][0]['departure']['at'].split('T')[0]
    return_date: str = flight['itineraries'][0]['segments'][0]['arrival']['at'].split('T')[0]
    stops: int = len(flight["itineraries"][0]["segments"]) - 1

    return FlightData(
        price=price,
        departure_airport_code=departure_city_code,
        destination_airport_code=destination_city_code,
        out_date=out_date,
        return_date=return_date,
        stops=stops
    )
