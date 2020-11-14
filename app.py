import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.title("Calculating the Impact of Social Distancing")
st.markdown("Change values to notice the impact of social distancing")

st.sidebar.title("Calculating the Impact of Social Distancing")
st.sidebar.markdown("Change values to notice the impact of social distancing")

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