import os
import googlemaps
from typing import Dict, List, Optional
from datetime import datetime

class TransportAgent:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the TransportAgent with Google Maps API key.
        
        Args:
            api_key (str, optional): Google Maps API key. If not provided, will look for GOOGLE_MAPS_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv('GOOGLE_MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("Google Maps API key is required. Provide it as an argument or set GOOGLE_MAPS_API_KEY environment variable.")
        
        self.client = googlemaps.Client(key=self.api_key)

    def get_transport_options(
        self,
        origin: str,
        destination: str,
        mode: str = "transit",
        departure_time: Optional[datetime] = None
    ) -> Dict:
        """
        Get transport options between two locations.
        
        Args:
            origin (str): Starting location
            destination (str): End location
            mode (str): Transport mode (transit, driving, walking, bicycling)
            departure_time (datetime, optional): Time of departure
            
        Returns:
            Dict: Transport options and details
        """
        try:
            directions_result = self.client.directions(
                origin,
                destination,
                mode=mode,
                departure_time=departure_time
            )
            
            if not directions_result:
                return {"error": "No routes found"}
            
            # Process the first route
            route = directions_result[0]
            legs = route['legs']
            
            transport_options = {
                "summary": route.get('summary', ''),
                "distance": legs[0].get('distance', {}).get('text', ''),
                "duration": legs[0].get('duration', {}).get('text', ''),
                "steps": []
            }
            
            # Process each step of the journey
            for step in legs[0].get('steps', []):
                step_info = {
                    "instruction": step.get('html_instructions', ''),
                    "distance": step.get('distance', {}).get('text', ''),
                    "duration": step.get('duration', {}).get('text', ''),
                    "transport_mode": step.get('travel_mode', '')
                }
                
                # Add transit details if available
                if 'transit_details' in step:
                    transit = step['transit_details']
                    step_info['transit'] = {
                        "line": transit.get('line', {}).get('name', ''),
                        "vehicle": transit.get('line', {}).get('vehicle', {}).get('name', ''),
                        "departure_stop": transit.get('departure_stop', {}).get('name', ''),
                        "arrival_stop": transit.get('arrival_stop', {}).get('name', '')
                    }
                
                transport_options['steps'].append(step_info)
            
            return transport_options
            
        except Exception as e:
            return {"error": str(e)}

    def get_available_transport_modes(self) -> List[str]:
        """
        Get list of available transport modes.
        
        Returns:
            List[str]: List of available transport modes
        """
        return ["transit", "driving", "walking", "bicycling"]
