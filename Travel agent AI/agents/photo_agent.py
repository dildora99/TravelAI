import os
import googlemaps
from typing import List, Dict, Union, Tuple
from dotenv import load_dotenv

class PhotoAgent:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY environment variable is not set")
        self.gmaps = googlemaps.Client(key=api_key)

    def find_tourist_attractions(
        self,
        location: Union[str, Tuple[float, float]],
        radius: int = 5000,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Find tourist attractions near a location using Google Places API.
        
        Args:
            location: Either a city name (str) or coordinates (tuple of lat, lng)
            radius: Search radius in meters (default: 5000m = 5km)
            max_results: Maximum number of results to return (default: 10)
            
        Returns:
            List of dictionaries containing attraction information
        """
        # If location is a string (city name), geocode it first
        if isinstance(location, str):
            geocode_result = self.gmaps.geocode(location)
            if not geocode_result:
                raise ValueError(f"Could not find coordinates for location: {location}")
            location = (
                geocode_result[0]['geometry']['location']['lat'],
                geocode_result[0]['geometry']['location']['lng']
            )

        # Search for tourist attractions
        places_result = self.gmaps.places_nearby(
            location=location,
            radius=radius,
            type='tourist_attraction',
            rank_by='prominence'
        )

        attractions = []
        for place in places_result.get('results', [])[:max_results]:
            # Get detailed information for each place
            place_details = self.gmaps.place(place['place_id'], fields=[
                'name', 'formatted_address', 'rating', 'photos', 'website',
                'opening_hours', 'formatted_phone_number'
            ])['result']

            attraction = {
                'name': place_details.get('name'),
                'address': place_details.get('formatted_address'),
                'rating': place_details.get('rating'),
                'website': place_details.get('website'),
                'phone': place_details.get('formatted_phone_number'),
                'opening_hours': place_details.get('opening_hours', {}).get('weekday_text', []),
                'photos': [
                    f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo['photo_reference']}&key={os.getenv('GOOGLE_MAPS_API_KEY')}"
                    for photo in place_details.get('photos', [])[:3]
                ] if 'photos' in place_details else []
            }
            attractions.append(attraction)

        return attractions

    def get_place_photos(self, place_id: str, max_photos: int = 3) -> List[str]:
        """
        Get photos for a specific place.
        
        Args:
            place_id: Google Places place_id
            max_photos: Maximum number of photos to return
            
        Returns:
            List of photo URLs
        """
        place_details = self.gmaps.place(place_id, fields=['photos'])
        photos = place_details['result'].get('photos', [])[:max_photos]
        
        return [
            f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo['photo_reference']}&key={os.getenv('GOOGLE_MAPS_API_KEY')}"
            for photo in photos
        ]
