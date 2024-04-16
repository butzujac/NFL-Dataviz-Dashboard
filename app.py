import streamlit as st 
import pandas as pd
import plotly.express as px 
import seaborn as sns
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
league_data = pd.read_csv("/home/jack/MSU/CMSE402/Semester_proj/leauge_data.csv")
list_of_stats = ['comppc', 'redznpct', '3rddownpct', 'Sc%', 'pass%']
cowboys_2023 = [69.7, 56.3, 48.3, 50.3, 56.7]
chiefs_2003 = [67, 62.7, 42.7, 46.3, 55.2]
inj = pd.read_csv("/home/jack/MSU/CMSE402/Semester_proj/Streamlit_folder/injuries.csv")




st.title('NFL Changes Over time')

with st.sidebar:
    st.markdown('## Navigation')
    section = st.radio('Go to', ['Section 1', 'Section 2', 'Section 3'])

# Main content sections
if section == 'Section 1':
    st.markdown('## League Efficiency Analysis')
    # first line plot
    fig = px.line(league_data, x = 'Year', y = 'TO%')
    fig.update_layout(title = "Turnover Percentage Over Time", yaxis_title  = "League Average Turnover Percentage")
    st.plotly_chart(fig)
    # second radar chart
    list_of_stats = ['comppc', 'redznpct', '3rddownpct', 'Sc%', 'pass%']
    cowboys_2023 = [69.7, 56.3, 48.3, 50.3, 56.7]
    chiefs_2003 = [67, 62.7, 42.7, 46.3, 55.2]

    # Create subplots with two columns and radar subplot type
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}]*2], subplot_titles=('Cowboys 2023', 'Chiefs 2003'))

    # Add radar chart for Cowboys 2023
    fig.add_trace(go.Scatterpolar(r=cowboys_2023,theta=list_of_stats,fill='toself',name='Cowboys 2023'), row=1, col=1)

    # Add radar chart for Chiefs 2003
    fig.add_trace(go.Scatterpolar(r=chiefs_2003,theta=list_of_stats,fill='toself',name='Chiefs 2003'), row=1, col=2)

    # Update layout with title
    fig.update_layout(
    title='Comparison of Offensive efficiency of the two best offenses from two differnet eras',
    polar=dict(
        radialaxis=dict(
            range=[20, 70]  # Adjust the range as needed
        )
    ),
    polar2=dict(
        radialaxis=dict(
            range=[20, 70]  # Adjust the range as needed
        )
    ),
    showlegend=False
    )
    st.plotly_chart(fig)

    


elif section == 'Section 2':
    st.markdown('## Injury Analysis')
    # Add content specific to Section 2
    inj['season'] = inj['season'].astype(int)
    top_positions = inj['position'].value_counts().head(10).index.tolist()

    # Get the top 10 most common injuries in the whole dataset
    top_injuries = inj['report_primary_injury'].value_counts().head(10).index.tolist()

    # Get unique years in the dataset
    years_available = inj['season'].unique()

    # Tabs - Year selection
    selected_year = st.selectbox('Select Year', years_available)

    # Filter data based on the selected year
    filtered_data_year = inj[inj['season'] == selected_year]

    # Filter the data to include only the top 10 positions and top 10 injuries
    filtered_data_year = filtered_data_year[filtered_data_year['position'].isin(top_positions)]
    filtered_data_year = filtered_data_year[filtered_data_year['report_primary_injury'].isin(top_injuries)]

    # Group the data by position and injury type and count occurrences
    heatmap_data_year = filtered_data_year.groupby(['position', 'report_primary_injury']).size().unstack(fill_value=0)

    # Convert the heatmap data to long format for Plotly
    heatmap_data_year = heatmap_data_year.reset_index().melt(id_vars='position', var_name='report_primary_injury', value_name='count')

    # Plot the heatmap using Plotly
    fig = px.imshow(heatmap_data_year.pivot("position", "report_primary_injury", "count"),labels=dict(x="Type of Injury", y="Position", color="Count"),title=f'Top 10 Injury Heatmap by Position and Type ({selected_year})',
                color_continuous_scale='Blues')  # Use Blues colormap

    # Customize layout
    fig.update_xaxes(tickangle=45)
    fig.update_layout(width=1000, height=800)

    # Show plot
    st.plotly_chart(fig)

else:
    st.markdown('## Matchup Analysis')
    # Add content specific to Section 3
    x = [9.9, 2.1, 8.6, 2.0, 0.9, 2.1, 2.0, 11.0, 0.9, -0.1, 3.5, -4.6, -2.6, -0.3, 11.0, -0.9]
    y = [9.0, 2.0, 5.6, 8.4, 1.9, 10.0, 7.6, 3.6, -0.8, -1.6, 3.5, -8.9, -3.5, -3.8, -6.3, -8.6]
    sizes = [100] * len(y)
    # Sample matchup labels
    matchup_labels = ['Steelers @ Ravens', 'Texans @ Colts', 'Buccaneers @ Panthers', 'Browns @ Bengals', 'Vikings @ Lions','Jets @ Patriots', 'Falcons @ Saints', 'Jaguars @ Titans', 'Seahawks @ Cardinals', 'Bears @ Packers', 'Cheifs @ Chargers', 'Broncos @ Raiders', 'Eagles @ Giants', 'Rams @ 49ers', 'Cowboys @ Commanders', 'Bills @ Dolpins']

    # Sample spreads for each game
    spreads = [-4, -1.5, -3, -2.5, -4.5, -7, -5, -3, -13, -3, -2.5, -3, -13, -3, -2.5, -4]

    # Sample list of boolean values
    boolean_list = [True, True, True, False, True,False,True, True, True, True,False,False, False, False, False, False]

    # Convert boolean values to colors
    colors = ['Yes' if value else 'No' for value in boolean_list]

    # Create a DataFrame with x, y, matchup labels, and spread columns
    data = {'x': x, 'y': y, 'Matchup': matchup_labels, 'Spread': spreads, 'Playoff Implications': colors}

    # Create scatter plot with Plotly Express
    fig = px.scatter(data, x='x', y='y', color='Playoff Implications', hover_name='Matchup', hover_data={'Spread': True},
                color_discrete_map={'Yes': 'blue', 'No': 'gray'}, size=sizes, size_max = 50)

    # Add shape annotations
    fig.add_annotation(
    x=11, y=-9,
    text='One Sided',
    showarrow=False,
    font=dict(size=10)
    )

    fig.add_annotation(
    x=-4, y=10,
    text='One Sided',
    showarrow=False,
    font=dict(size=10)
    )

    fig.add_annotation(
    x=5, y=0,
    text='Competitive Matchup',
    showarrow=False,
    font=dict(size=10)
    )
    fig.update_layout(
    width=1100,  # Specify the width of the plot
    height=1000,  # Specify the height of the plot
    )
    # Increase size of the dots
    fig.update_traces(marker=dict(size=15))

    # Add a line along the diagonal
    fig.add_shape(
    type='line',
    x0=min(x), y0=min(y),
    x1=max(x), y1=max(y),
    line=dict(color='black', width=1, dash='dash')
    )

    # Customize layout
    fig.update_layout(
    title='Visualizing Matchups Week 18 in The 3rd Most Viewed NFL Season Ever',
    xaxis_title='Home PFF',
    yaxis_title='Away PFF',
    legend_title='Playoff Implications'
    )

    # Show plot
    st.plotly_chart(fig)



