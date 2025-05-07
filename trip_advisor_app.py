import streamlit as st
import requests

# --- SETTINGS ---
API_KEY = "b19d9c7090cc4fb49f626c52a0ded81f"
CATEGORIES = "tourism.attraction"

if "page" not in st.session_state:
    st.session_state["page"] = "Welcome"
# --- Welcome Page ---
if st.session_state["page"] == "Welcome":
    st.set_page_config(page_title="Trip Advisor", layout="wide", initial_sidebar_state="collapsed")

    # --- Custom CSS for animations and button ---
    st.markdown("""
        <style>
            .pink-title {
                font-size: 6em;
                color: #FFB6C1;
                text-align: center;
                font-weight: bold;
                
            }
            .small-sub {
                font-size: 2.5em;
                color: #FFB6C1;
                text-align: center;
                
            }

            .button-container {
                display: flex;
                justify-content: center;
                margin-top: 50px;
                
            }

            .stButton>button {
                background-color: #FFB6C1;
                color: black;
                font-size: 1.5em;
                font-weight: bold;
                padding: 0.75em 2em;
                border-radius: 12px;
                border: none;
            }

           
        </style>
    """, unsafe_allow_html=True)

    # --- Animated Title & Subtitle ---
    st.markdown('<div class="pink-title">✈️ Trip Advisor ✈️</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-sub">Welcome, Your Trip Assistant to Dream Vacation</div>', unsafe_allow_html=True)

    # --- Hidden then visible button ---
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Let's Go"):
        st.session_state["page"] = "Trip Inputs"
    st.markdown('</div>', unsafe_allow_html=True)


# --- Trip Inputs Page ---
if st.session_state["page"] == "Trip Inputs":
    st.markdown("### 🌍 Enter your destination city:")
    city_input = st.text_input("City Name:")
    
    st.markdown("### 📏 Now enter your preferred distance from the city center (in kilometers):")
    radius_input = st.text_input("Distance in km:")

    # Button to trigger exploration
    if st.button("🔍 Explore"):
        if city_input and radius_input:
            try:
                radius_km = int(radius_input)
                radius_meters = radius_km * 1000
                st.session_state["city"] = city_input
                st.session_state["radius"] = radius_meters
                st.session_state["trigger_explore"] = True
            except ValueError:
                st.error("Please enter a valid number for distance (in km).")
        else:
            st.warning("Please fill in both fields before exploring.")

    # Show results only if 'Explore' has been triggered
    if st.session_state.get("trigger_explore", False):
        city_input = st.session_state["city"]
        radius_meters = st.session_state["radius"]

        geo_url = f"https://api.geoapify.com/v1/geocode/search?text={city_input}&apiKey={API_KEY}"
        geo_resp = requests.get(geo_url).json()

        if geo_resp.get("features"):
            lon, lat = geo_resp["features"][0]["geometry"]["coordinates"]

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
                    address_line1 = props.get("address_line1", "")
                    dist = props.get("distance", "N/A")
                    categories = props.get("categories", [])

                    if name and address_line1 and address_line1 not in name:
                        name_display = f"{name} ({address_line1})"
                    else:
                        name_display = name

                    printed = set()
                    category_labels = []

                    for cat in categories:
                        label = None
                        if "artwork" in cat:
                            label = props.get('artwork', {}).get('artwork_type')
                        elif "memorial" in cat:
                            label = props.get('memorial', {}).get('memorial_type')
                        elif "historic" in cat:
                            historic = props.get('historic')
                            if isinstance(historic, dict):
                                label = historic.get('type')

                        if label:
                            label = str(label).capitalize()
                        else:
                            label = cat.split('.')[-1].replace('_', ' ').capitalize()

                        if label not in printed:
                            category_labels.append(label)
                            printed.add(label)

                    category_clean = category_labels[-1] if category_labels else "Unknown"
                    output = f"""
                    🏷️ <b>{name_display}</b><br>
                    🏠 Address : {address}<br>
                    📐 Distance: {dist} meters<br>
                    🧭 Type    : {category_clean}<br>
                        <hr>
                    """
                    st.markdown(output, unsafe_allow_html=True)
            else:
                st.warning("No tourist attractions found nearby.")
        else:
            st.error(f"Could not find coordinates for the city: {city_input}")

