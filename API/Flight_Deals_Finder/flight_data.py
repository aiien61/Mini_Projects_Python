class FlightData:
    def __init__(self, **kwargs):
        self.price = kwargs.get("price")
        self.departure_city = kwargs.get("departure_city")
        self.departure_airport_code = kwargs.get("departure_airport_code")
        self.destination_city = kwargs.get("destination_city")
        self.destination_airport_code = kwargs.get("destination_airport_code")
        self.out_date = kwargs.get("out_date")
        self.return_date = kwargs.get("return_date")