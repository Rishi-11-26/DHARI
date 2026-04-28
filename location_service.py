from streamlit_js_eval import streamlit_js_eval


def get_device_location():

    location = streamlit_js_eval(
        js_expressions="navigator.geolocation.getCurrentPosition((pos) => pos.coords)",
        key="get_location"
    )

    if location:
        lat = location["latitude"]
        lon = location["longitude"]

        return lat, lon

    return None, None