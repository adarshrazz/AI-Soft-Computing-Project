import streamlit as st
import pandas as pd
from sugeno import calculate_irrigation
from visualizations import membership_figure, response_surface_figure

st.set_page_config(page_title="Smart Irrigation | Sugeno Fuzzy Logic", page_icon="🌱", layout="wide")

st.title("🌱 Smart Irrigation System")
st.caption("A software simulation using a zero-order Sugeno Fuzzy Inference System")

with st.sidebar:
    st.header("Environmental inputs")
    scenario = st.selectbox(
        "Load a sample scenario",
        ["Custom", "Dry soil · hot weather", "Moderate conditions", "Moist soil · hot weather", "Wet soil · cool weather"]
    )
    defaults = {
        "Custom": (35, 30),
        "Dry soil · hot weather": (15, 40),
        "Moderate conditions": (50, 25),
        "Moist soil · hot weather": (85, 40),
        "Wet soil · cool weather": (90, 15),
    }
    default_soil, default_temp = defaults[scenario]
    soil_moisture = st.slider("Soil moisture (%)", min_value=0, max_value=100, value=default_soil, step=1)
    temperature = st.slider("Temperature (°C)", min_value=0, max_value=50, value=default_temp, step=1)
    st.caption("Model ranges: soil moisture 0–100%; temperature 0–50°C.")

result = calculate_irrigation(soil_moisture, temperature)

col1, col2, col3 = st.columns(3)
col1.metric("Recommended duration", f"{result['duration_minutes']:.2f} min")
col2.metric("Model category", result["category"])
col3.metric("Active rules", str(len(result["active_rules"])))

st.info(
    f"**Interpretation:** {result['explanation']} "
    "This is a classroom simulation based on illustrative rules, not an agronomic prescription."
)

left, right = st.columns(2)
with left:
    st.subheader("Input membership degrees")
    memberships = []
    for name, degree in result["soil_memberships"].items():
        memberships.append({"Input": "Soil moisture", "Fuzzy set": name, "Membership degree": degree})
    for name, degree in result["temperature_memberships"].items():
        memberships.append({"Input": "Temperature", "Fuzzy set": name, "Membership degree": degree})
    st.dataframe(pd.DataFrame(memberships), use_container_width=True, hide_index=True)
with right:
    st.subheader("Sugeno calculation")
    st.write(f"Weighted output sum: **{result['weighted_sum']:.3f}**")
    st.write(f"Sum of firing strengths: **{result['strength_sum']:.3f}**")
    st.latex(r"z^* = \frac{\sum_i w_i z_i}{\sum_i w_i}")
    st.write("The output is the weighted average of the constant consequents of the fired rules.")

st.subheader("Fired rules")
st.dataframe(pd.DataFrame(result["active_rules"]), use_container_width=True, hide_index=True)

st.subheader("Membership functions")
st.pyplot(membership_figure(), use_container_width=True, clear_figure=True)

with st.expander("View model response surface"):
    st.write("This chart shows how the output changes over the supported input ranges.")
    st.pyplot(response_surface_figure(), use_container_width=True, clear_figure=True)

with st.expander("Model assumptions and limitations"):
    st.markdown("""
    - This application is a software-only simulation; it does not read real sensors or control a pump.
    - The membership-function parameters and Sugeno output constants are illustrative design assumptions.
    - Soil moisture percentage is treated as a normalized input; sensor calibration and soil type are not modeled.
    - The model does not account for crop species, soil type, rainfall, root depth, flow rate, or evapotranspiration.
    - A real irrigation system would require agronomic validation and safety controls before use.
    """)

st.caption("Mini-project: Smart Irrigation System Using Zero-Order Sugeno Fuzzy Logic")
