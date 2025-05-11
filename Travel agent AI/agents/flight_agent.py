import os
from amadeus import Client, ResponseError
from dotenv import load_dotenv
from typing import Dict, List, Optional

class FlightAgent:
    def __init__(self):
        load_dotenv()
        self.client = None
        self.authenticate()

    def authenticate(self) -> None:
        """Authenticate with the Amadeus API using credentials from environment variables."""
        try:
            self.client = Client(
                client_id=os.getenv('AMADEUS_API_KEY'),
                client_secret=os.getenv('AMADEUS_API_SECRET')
            )
        except Exception as e:
            raise Exception(f"Failed to authenticate with Amadeus API: {str(e)}")

    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        adults: int = 1,
        max_results: int = 5
    ) -> List[Dict]:
        """
        Search for flight offers between two airports on a specific date.

        Args:
            origin (str): Origin airport IATA code (e.g., 'JFK')
            destination (str): Destination airport IATA code (e.g., 'LAX')
            departure_date (str): Departure date in YYYY-MM-DD format
            adults (int): Number of adult passengers (default: 1)
            max_results (int): Maximum number of results to return (default: 5)

        Returns:
            List[Dict]: List of flight offers with details
        """
        try:
            if not self.client:
                self.authenticate()

            response = self.client.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                adults=adults,
                max=max_results
            )

            return response.data

        except ResponseError as error:
            raise Exception(f"Amadeus API error: {error.response.body}")
        except Exception as e:
            raise Exception(f"Error searching flights: {str(e)}")

    def format_flight_offers(self, offers: List[Dict]) -> List[Dict]:
        """
        Format flight offers into a more readable structure.

        Args:
            offers (List[Dict]): Raw flight offers from Amadeus API

        Returns:
            List[Dict]: Formatted flight offers with essential information
        """
        formatted_offers = []
        
        for offer in offers:
            itineraries = offer['itineraries']
            for itinerary in itineraries:
                segments = itinerary['segments']
                for segment in segments:
                    formatted_offer = {
                        'airline': segment['carrierCode'],
                        'flight_number': segment['number'],
                        'departure': {
                            'airport': segment['departure']['iataCode'],
                            'time': segment['departure']['at']
                        },
                        'arrival': {
                            'airport': segment['arrival']['iataCode'],
                            'time': segment['arrival']['at']
                        },
                        'price': {
                            'amount': offer['price']['total'],
                            'currency': offer['price']['currency']
                        }
                    }
                    formatted_offers.append(formatted_offer)

        return formatted_offers
