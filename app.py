import numpy as np
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.title("#1. Calculating the Impact of Social Distancing")
st.markdown("Change values to notice the impact of social distancing")

st.sidebar.title("#1. Calculating the Impact of Social Distancing")
st.sidebar.markdown("Change values to notice the impact of social distancing")
st.sidebar.markdown("**Note: Sidebar is meant to be used only for #1**")

n_days = int(st.sidebar.text_input("No. of days", 31, key='n_days'))
x_idx = ["Day "+str(i+1) for i in range(int(n_days))]

N = int(st.sidebar.text_input("No. of cases in the beginning", 1, key='N'))

ir = int(st.sidebar.slider("Infection rate (%)", 0, 100, key='ir'))
ir /= 100

rsexp = int(st.sidebar.slider("Social distancing factor (%)", 0, 100, key='rsexp'))
rsexp /= 100

n_days = int(n_days)
x_idx = ["Day "+str(i+1) for i in range(n_days)]

Ni, t, dt = N, 0, 0.1
infected = []

while t < n_days:
    infected.append(int(Ni))
    Ni = Ni*np.exp(ir*dt)
    t += dt

li = len(infected)
st1 = int(li/len(x_idx))
infected = infected[0:li:st1]


Ns, sdf, t, dt = N, ir*(1-rsexp), 0, 0.1
distance = []

while t < n_days:
    distance.append(int(Ns))
    Ns = Ns*np.exp(sdf*dt)
    t += dt

di = len(distance)
st2 = int(di/len(x_idx))
distance = distance[0:di:st2]

fig = go.Figure()
fig.add_trace(go.Scatter(x = x_idx, y = infected, name="Infections"))
fig.add_trace(go.Scatter(x = x_idx, y = distance, name="Social Distancing"))

fig.update_xaxes(tickangle=295)

fig.update_layout(xaxis = dict(tickmode = 'linear'))

st.write(fig)

st.write("No. of cases after", n_days, "days:", infected[-1])
st.write("No. of cases after", n_days, "days with social distancing:", distance[-1])
st.write("Difference:", infected[-1]-distance[-1], "less cases")



st.title("#2. Social Distancing Violation Detection from Video - Demo")
st.header("Input #1")
st.image("vid/vid1.gif")
st.header("Output #1")
st.image("vid/vid1o.gif")
st.write("\n\n")
st.header("Input #2")
st.image("vid/vid2.gif")
st.header("Output #2")
st.image("vid/vid2o.gif")

st.header("The violation data collected from cameras can be used for further analysis as seen below.")


DATA_URL = ("toy_data.csv")

st.title("#3. Social Distancing Violations in Montreal")
st.markdown("Dashboard that can be used to analyze violations of social distancing in MTL")
st.header("**Note: This is just a randomly generated toy dataset!**")

@st.cache(persist=True)
def load_data():
	data = pd.read_csv(DATA_URL, parse_dates=[["date", "time"]])
	data.rename(columns={"date_time":"date/time"}, inplace=True)
	return data

data = load_data()

st.header("How many violations occur during a given time of day?")
hour = st.slider("Hour to look at", 0, 23)
data = data[data["date/time"].dt.hour == hour]

st.markdown("Social distancing violations between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data = data[["date/time", "latitude", "longitude"]],
            get_position=["longitude", "latitude"],
            radius=100,
            extruded=True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0,1000],
        ),
    ],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) %24))
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'violations': hist})
fig = px.bar(chart_data, x='minute', y='violations', hover_data=['minute', 'violations'], height=400)
st.write(fig)