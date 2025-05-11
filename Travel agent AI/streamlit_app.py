import streamlit as st
from datetime import datetime
from core.coordinator import plan_trip

# Set page config
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# Title and description
st.title("✈️ AI Travel Planner")
st.markdown("Plan your perfect trip with our AI-powered travel assistant!")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    origin = st.text_input("Origin City", placeholder="e.g., New York")
    destination = st.text_input("Destination City", placeholder="e.g., Tokyo")

with col2:
    travel_date = st.date_input("Travel Date", min_value=datetime.now().date())

# Plan trip button
if st.button("Plan My Trip", type="primary"):
    if not all([origin, destination, travel_date]):
        st.error("Please fill in all fields!")
    else:
        with st.spinner("Planning your perfect trip..."):
            try:
                # Convert date to datetime
                travel_datetime = datetime.combine(travel_date, datetime.min.time())
                
                # Get trip plan
                trip_plan = plan_trip(origin, destination, travel_datetime)
                
                # Display results in tabs
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "✈️ Flights", "🏨 Hotels", "📸 Photo Spots", 
                    "🎭 Cultural Tips", "🚌 Local Transport"
                ])
                
                with tab1:
                    st.subheader("Flight Options")
                    if trip_plan["flights"]["flights"]:
                        st.json(trip_plan["flights"])
                    else:
                        st.info("No flight data available yet")
                
                with tab2:
                    st.subheader("Hotel Options")
                    if trip_plan["accommodation"]["hotels"]:
                        st.json(trip_plan["accommodation"])
                    else:
                        st.info("No hotel data available yet")
                
                with tab3:
                    st.subheader("Photo Spots")
                    if trip_plan["attractions"]["spots"]:
                        st.json(trip_plan["attractions"])
                    else:
                        st.info("No photo spots data available yet")
                
                with tab4:
                    st.subheader("Cultural Information")
                    if trip_plan["cultural_info"]["etiquette"]:
                        st.json(trip_plan["cultural_info"])
                    else:
                        st.info("No cultural information available yet")
                
                with tab5:
                    st.subheader("Local Transportation")
                    if trip_plan["transportation"]["public_transport"]:
                        st.json(trip_plan["transportation"])
                    else:
                        st.info("No transportation data available yet")
                
            except Exception as e:
                st.error(f"An error occurred while planning your trip: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ by AI Travel Planner")
