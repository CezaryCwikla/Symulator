import pandas
import plotly.graph_objects as go

leach = pandas.read_csv('csvs\LEACH.csv', index_col=0)
mfleach4 = pandas.read_csv('csvs\MFLEACH4.csv', index_col=0)
mfleachrand = pandas.read_csv('csvs\MFLEACHRandom.csv', index_col=0)

fig = go.Figure()
fig.add_trace(go.Scatter(x=leach.index, y=leach.SDP,
                    mode='lines', name='LEACH'))
fig.add_trace(go.Scatter(x=mfleach4.index, y=mfleach4.SDP,
                    mode='lines', name='MF-LEACH'))
fig.add_trace(go.Scatter(x=mfleachrand.index, y=mfleachrand.SDP,
                    mode='lines', name='MF-LEACH-R')).update_layout(
                    xaxis_title="Round number", yaxis_title="Sent Data Packets")
fig.show()
# fig = px.line(x=leach.index, y=[leach.SDP,mfleach4['SDP']], labels={'leach.SDP':'LEACH', 'wide_variable_1':'MFLEACH 4 Functions in nodes'})
# # fig.add_scatter(x=mfleach4.index, y=mfleach4['SDP'], label='MFLEACH 4 Functions in nodes') # Not what is desired - need a line
# # fig.add_scatter(x=mfleachrand.index, y=mfleachrand['SDP'], label='MFLEACH Random number of functions')
# # # Show plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=leach.index, y=leach.RDP,
                    mode='lines', name='LEACH'))
fig.add_trace(go.Scatter(x=mfleach4.index, y=mfleach4.RDP,
                    mode='lines', name='MF-LEACH'))
fig.add_trace(go.Scatter(x=mfleachrand.index, y=mfleachrand.RDP,
                    mode='lines', name='MF-LEACH-R')).update_layout(
                    xaxis_title="Round number", yaxis_title="Received Data Packets")
fig.show()

fig = go.Figure()
fig.add_trace(go.Scatter(x=leach.index, y=leach['Dead nodes'],
                    mode='lines', name='LEACH'))
fig.add_trace(go.Scatter(x=mfleach4.index, y=mfleach4['Dead nodes'],
                    mode='lines', name='MF-LEACH'))
fig.add_trace(go.Scatter(x=mfleachrand.index, y=mfleachrand['Dead nodes'],
                    mode='lines', name='MF-LEACH-R')).update_layout(
                    xaxis_title="Round number", yaxis_title="Number of dead nodes")
fig.show()

fig = go.Figure()
fig.add_trace(go.Scatter(x=leach.index, y=leach['Average energy'],
                    mode='lines', name='LEACH'))
fig.add_trace(go.Scatter(x=mfleach4.index, y=mfleach4['Average energy'],
                    mode='lines', name='MF-LEACH'))
fig.add_trace(go.Scatter(x=mfleachrand.index, y=mfleachrand['Average energy'],
                    mode='lines', name='MF-LEACH-R')).update_layout(
                    xaxis_title="Round number", yaxis_title="Average energy in nodes")
fig.show()

fig = go.Figure()
fig.add_trace(go.Scatter(x=leach.index, y=leach['Consumed Energy'],
                    mode='lines', name='LEACH'))
fig.add_trace(go.Scatter(x=mfleach4.index, y=mfleach4['Consumed Energy'],
                    mode='lines', name='MF-LEACH'))
fig.add_trace(go.Scatter(x=mfleachrand.index, y=mfleachrand['Consumed Energy'],
                    mode='lines', name='MF-LEACH-R')).update_layout(
                    xaxis_title="Round number", yaxis_title="Consumed energy in nodes")
fig.show()