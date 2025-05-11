# AI Travel Planner

An intelligent multi-agent travel planning system that helps users create comprehensive travel itineraries using various AI agents specialized in different aspects of travel planning.

## 🚀 Features

- **Flight Planning**: Search and book flights using the Amadeus API
- **Hotel Booking**: Find and reserve accommodations through the Amadeus API
- **Photo Spots Discovery**: Locate Instagram-worthy spots using Google Places API
- **Cultural Insights**: Get local cultural information and tips from Wikipedia
- **Local Transportation**: Plan local travel routes using Google Directions API
- **User-Friendly Interface**: Clean and intuitive Streamlit-based UI

## 🛠️ Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-travel-planner.git
cd ai-travel-planner
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the root directory with the following API keys:

```env
# Amadeus API Credentials
AMADEUS_API_KEY=your_amadeus_api_key
AMADEUS_API_SECRET=your_amadeus_api_secret

# Google API Credentials
GOOGLE_PLACES_API_KEY=your_google_places_api_key
GOOGLE_DIRECTIONS_API_KEY=your_google_directions_api_key

# Wikipedia API (no key required)
```

## 🏃‍♂️ Running the Application

1. Ensure your virtual environment is activated
2. Start the Streamlit app:
```bash
streamlit run app.py
```
3. Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
ai-travel-planner/
├── agents/
│   ├── flight_agent.py
│   ├── hotel_agent.py
│   ├── photo_spots_agent.py
│   ├── cultural_tips_agent.py
│   └── transport_agent.py
├── utils/
│   └── api_helpers.py
├── app.py
├── requirements.txt
├── .env
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Note

Make sure to keep your API keys secure and never commit them to version control. The `.env` file is included in `.gitignore` by default.
