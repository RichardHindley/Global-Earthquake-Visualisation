import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import plotly.express as px

# Load the dataset
df = pd.read_csv('/Users/richardhindley/Desktop/My_Scripts/Global-Earthquake-Visualisation/significant_month.csv')
print(df.head())
# Check for missing values
print(df.isnull().sum())

# Drop rows with missing values
df = df.dropna()

# Convert time column to datetime
df['time'] = pd.to_datetime(df['time'])

# Display basic info
print(df.info())
print(df.describe())


# Plot the distribution of earthquake magnitudes
plt.figure(figsize=(10, 6))
sns.histplot(df['mag'], bins=50)
plt.title('Distribution of Earthquake Magnitudes')
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.show()

# Plot the number of earthquakes over time
plt.figure(figsize=(14, 7))
df['time'].groupby(df['time'].dt.to_period('M')).count().plot(kind='line')
plt.title('Number of Earthquakes Over Time')
plt.xlabel('Month')
plt.ylabel('Number of Earthquakes')
plt.show()


# Create a map centered around the average latitude and longitude
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=2)

# Add earthquake markers to the map
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['mag'] * 2,
        popup=f"Magnitude: {row['mag']}",
        color='crimson',
        fill=True,
        fill_color='crimson'
    ).add_to(m)

# Save the map to an HTML file
m.save('earthquake_map.html')


# Create a time series plot
fig = px.line(df, x='time', y='mag', title='Earthquake Magnitudes Over Time')
fig.show()
