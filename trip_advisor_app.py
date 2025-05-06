import streamlit as st
import requests
import time

# --- SETTINGS ---
API_KEY = "b19d9c7090cc4fb49f626c52a0ded81f"  # Replace with your actual Geoapify API key
CATEGORIES = "tourism.attraction"

# --- PAGE CONFIG ---
st.set_page_config(page_title="Trip Advisor", layout="wide", initial_sidebar_state="collapsed")

# --- Initialize session state for page navigation ---
if "page" not in st.session_state:
    st.session_state["page"] = "Welcome"  # Start on the welcome page

# --- Welcome Page ---
if st.session_state["page"] == "Welcome":
    # --- Logo Animation ---
    st.markdown("""
        <style>
            .pink-title {
                font-size: 6em;
                color: #FFB6C1;
                text-align: center;
                font-weight: bold;
                animation: logoFadeIn 3s ease-in-out forwards;
                opacity: 0;
            }

            .small-sub {
                font-size: 2.5em;
                color: #FAFAFA;
                text-align: center;
                animation: subFadeIn 3s ease-in-out forwards;
                animation-delay: 3s;
                opacity: 0;
            }

            @keyframes logoFadeIn {
                0% { opacity: 0; transform: scale(0.8); }
                100% { opacity: 1; transform: scale(1); }
            }

            @keyframes subFadeIn {
                0% { opacity: 0; transform: translateY(20px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            input[type="text"], .stTextInput input {
                background-color: #262730 !important;
                color: #FAFAFA !important;
                border: 1px solid #FAFAFA !important;
                font-size: 1.25em;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Display Welcome Animation ---
    st.markdown('<div class="pink-title">✈️ Trip Advisor ✈️</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-sub">Welcome, Your Trip Assistant to Dream Vacation</div>', unsafe_allow_html=True)

    # --- Small Delay for Animations to Feel Smooth ---
    time.sleep(6)

    # --- Button to Transition to Next Page ---
    st.markdown("### Get started by clicking below to plan your trip!")
    
    if st.button("Start Planning"):
        st.session_state["page"] = "Trip Inputs"  # Move to the next page automatically

# --- Trip Inputs Page ---
elif st.session_state["page"] == "Trip Inputs":
    # --- City and Distance Input Page (No animations) ---
    st.markdown("### 🌍 Enter your destination city:")
    city_input = st.text_input("City Name:")

    if city_input:
        st.session_state["city"] = city_input

        st.markdown("### 📏 Now enter your preferred distance from the city center (in kilometers):")
        radius_input = st.text_input("Distance in km:")

        if radius_input:
            try:
                radius_km = int(radius_input)
                radius_meters = radius_km * 1000

                # --- Get Coordinates ---
                geo_url = f"https://api.geoapify.com/v1/geocode/search?text={city_input}&apiKey={API_KEY}"
                geo_resp = requests.get(geo_url).json()

                if geo_resp.get("features"):
                    lon, lat = geo_resp["features"][0]["geometry"]["coordinates"]
                    # --- Get Places ---
                    places_url = (
                        f"https://api.geoapify.com/v2/places?"
                        f"categories={CATEGORIES}&"
                        f"filter=circle:{lon},{lat},{radius_meters}&"
                        f"bias=proximity:{lon},{lat}&"
                        f"limit=10&apiKey={API_KEY}"
                    )
                    places_resp = requests.get(places_url).json()
                    places = places_resp.get("features", [])

                    if places:
                        st.subheader(f"Top Tourist Attractions in {city_input.title()}:")
                        for place in places:
                            props = place["properties"]
                            name = props.get("name", "Unnamed Location")
                            if not name or name.strip().lower() == "unnamed location":
                                continue
                            address = props.get("formatted", "No address available")
                            dist = props.get("distance", "N/A")
                            categories = props.get("categories", [])
                            category_clean = categories[-1].split(".")[-1] if categories else "Unknown"

                            output = f"""
                            🏷️  {name}
                            🏠 Address : {address}
                            📐 Distance: {dist} meters
                            🧭 Type    : {category_clean}
                            """
                            st.markdown(f"```text\n{output}\n```")

                        # --- MAP DISPLAY ---
                        import folium
                        from streamlit_folium import st_folium

                        st.subheader("🗺️ View on Map:")
                        m = folium.Map(location=[lat, lon], zoom_start=13)
                        for place in places:
                            props = place["properties"]
                            name = props.get("name")
                            if not name or name.strip().lower() == "unnamed location":
                                continue
                            loc = place["geometry"]["coordinates"]
                            folium.Marker(
                                [loc[1], loc[0]],
                                tooltip=name,
                                popup=props.get("formatted", "")
                            ).add_to(m)
                        st_folium(m, width=700, height=500)

                    else:
                        st.warning("No tourist attractions found nearby.")
                else:
                    st.error(f"Could not find coordinates for the city: {city_input}")
            except ValueError:
                st.error("Please enter a valid number for distance (in km).")
