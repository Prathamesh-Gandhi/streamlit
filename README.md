Here’s a professional `README.md` for your **Trip Advisor** Streamlit app:

---

# ✈️ Trip Advisor – Your Personal Travel Assistant

Welcome to **Trip Advisor**, a simple and elegant Streamlit-based web app that helps you discover the **top tourist attractions** in any city within your preferred distance range. Powered by the [Geoapify Places API](https://www.geoapify.com/places-api), this app provides easy-to-read location information and categorization for your next travel adventure.

---

## 🌟 Features

* 🔤 **City-Based Search**: Enter any city to explore popular nearby attractions.
* 📏 **Customizable Radius**: Specify your preferred distance from the city center (in kilometers).
* 📍 **Tourist Highlights**: View names, addresses, distances, and types of attractions.
* 🎨 **Animated UI**: Smooth and friendly user interface with a warm welcome page and custom styling.

---

## 📦 Requirements

* Python 3.7+
* [Streamlit](https://streamlit.io)
* [Requests](https://docs.python-requests.org/en/latest/)

You can install the required packages using:

```bash
pip install streamlit requests
```

---

## 🚀 How to Run the App

1. **Clone this repository or save the script as `app.py`**:

```bash
git clone https://github.com/Prathamesh-Gandhi/trip-advisor-streamlit.git
cd trip-advisor-streamlit
```

2. **Run the app using Streamlit**:

```bash
streamlit run app.py
```

3. **Interact through the browser**:

   * A welcome animation and title will appear.
   * Click the **"Let's Go"** button to proceed to the input form.
   * Enter a **city name** and your **preferred distance in kilometers**.
   * Press **"Explore"** to view the top nearby attractions.

---

## 🔐 API Key

This app uses the [Geoapify Places API](https://apidocs.geoapify.com/). You need to sign up on Geoapify to get your **API key**.

Replace the placeholder key in the code:

```python
API_KEY = "your_actual_api_key_here"
current line
API_KEY="b19d9c7090cc4fb49f626c52a0ded81f"
```

---

