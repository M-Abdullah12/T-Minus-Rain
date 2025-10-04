import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Will It Rain On My Parade?",
    page_icon="🌦️",
    layout="wide"
)

# Title and team info
st.title("🌦️ Will It Rain On My Parade?")
st.markdown("**Team T-Minus Rain** | NASA Space Apps 2025")
st.markdown("---")

# Create sample weather data for demonstration
@st.cache_data
def create_sample_data():
    """Create sample weather data for NYC"""
    np.random.seed(42)
    
    # Generate dates for the past year
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    data = []
    for date in dates:
        # Seasonal patterns
        month = date.month
        day_of_year = date.dayofyear
        
        # Temperature patterns (seasonal)
        temp = 50 + 30 * np.sin(2 * np.pi * (day_of_year - 80) / 365) + np.random.normal(0, 5)
        
        # Humidity patterns
        humidity = 60 + 20 * np.sin(2 * np.pi * (day_of_year - 120) / 365) + np.random.normal(0, 10)
        humidity = np.clip(humidity, 20, 95)
        
        # Pressure patterns
        pressure = 1013 + np.random.normal(0, 15)
        
        # Wind speed
        wind_speed = np.abs(np.random.normal(8, 4))
        
        # Weather condition based on patterns
        rain_prob = 0.3
        if month in [3, 4, 5]:  # Spring - more rain
            rain_prob = 0.4
        elif month in [6, 7, 8]:  # Summer - less rain, more clear
            rain_prob = 0.25
        elif month in [12, 1, 2]:  # Winter - snow possible
            rain_prob = 0.3
        
        # Adjust probability based on humidity and pressure
        if humidity > 80:
            rain_prob += 0.2
        if pressure < 1000:
            rain_prob += 0.15
            
        rand = np.random.random()
        if rand < rain_prob:
            if month in [12, 1, 2] and temp < 35:
                condition = 'Snow'
            else:
                condition = 'Rain'
        elif rand < rain_prob + 0.3:
            condition = 'Cloudy'
        else:
            condition = 'Clear'
        
        data.append({
            'date': date,
            'temperature': round(temp, 1),
            'humidity': round(humidity, 1),
            'pressure': round(pressure, 1),
            'wind_speed': round(wind_speed, 1),
            'month': month,
            'day_of_year': day_of_year,
            'condition': condition
        })
    
    return pd.DataFrame(data)

# Load and prepare data
@st.cache_data
def prepare_model():
    """Prepare and train the weather prediction model"""
    df = create_sample_data()
    
    # Feature engineering
    features = ['temperature', 'humidity', 'pressure', 'wind_speed', 'month', 'day_of_year']
    X = df[features]
    y = df['condition']
    
    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Calculate accuracy
    accuracy = model.score(X_test_scaled, y_test)
    
    return model, scaler, le, accuracy, df

# Initialize model
model, scaler, label_encoder, accuracy, historical_data = prepare_model()

# Sidebar with model info
st.sidebar.header("🤖 Model Information")
st.sidebar.write(f"**Model Accuracy:** {accuracy:.2%}")
st.sidebar.write(f"**Training Data:** {len(historical_data)} days")
st.sidebar.write("**Features Used:**")
st.sidebar.write("- Temperature")
st.sidebar.write("- Humidity") 
st.sidebar.write("- Pressure")
st.sidebar.write("- Wind Speed")
st.sidebar.write("- Seasonal Patterns")

# Main forecast interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 Forecast Your Event")
    
    # Input form
    with st.form("forecast_form"):
        city = st.text_input("City", value="New York City", disabled=True, help="Currently supports NYC only")
        
        col_date, col_time = st.columns(2)
        with col_date:
            event_date = st.date_input("Event Date", min_value=datetime.now().date())
        with col_time:
            event_time = st.time_input("Event Time")
        
        submit_button = st.form_submit_button("🌦️ Check My Parade Weather", use_container_width=True)
    
    if submit_button:
        # Combine date and time
        event_datetime = datetime.combine(event_date, event_time)
        
        # Generate prediction features based on seasonal patterns
        month = event_datetime.month
        day_of_year = event_datetime.timetuple().tm_yday
        
        # Estimate features based on historical patterns and season
        seasonal_temp = 50 + 30 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
        seasonal_humidity = 60 + 20 * np.sin(2 * np.pi * (day_of_year - 120) / 365)
        seasonal_pressure = 1013 + np.random.normal(0, 5)  # Small variation
        seasonal_wind = 8 + np.random.normal(0, 2)
        
        # Create feature vector
        features = np.array([[seasonal_temp, seasonal_humidity, seasonal_pressure, seasonal_wind, month, day_of_year]])
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction_proba = model.predict_proba(features_scaled)[0]
        prediction = model.predict(features_scaled)[0]
        predicted_condition = label_encoder.inverse_transform([prediction])[0]
        
        # Display results
        st.success("🎉 Forecast Generated!")
        
        # Event details
        st.subheader("📅 Event Details")
        st.write(f"**Date & Time:** {event_datetime.strftime('%A, %B %d, %Y at %I:%M %p')}")
        st.write(f"**Location:** {city}")
        
        # Main prediction
        st.subheader("🌤️ Weather Forecast")
        
        # Weather icons
        weather_icons = {
            'Clear': '☀️',
            'Cloudy': '☁️', 
            'Rain': '🌧️',
            'Snow': '❄️'
        }
        
        icon = weather_icons.get(predicted_condition, '🌤️')
        st.markdown(f"## {icon} {predicted_condition}")
        
        # Probability breakdown
        st.subheader("📊 Probability Breakdown")
        
        prob_data = {}
        for i, condition in enumerate(label_encoder.classes_):
            prob_data[condition] = prediction_proba[i] * 100
        
        # Sort by probability
        sorted_probs = sorted(prob_data.items(), key=lambda x: x[1], reverse=True)
        
        for condition, prob in sorted_probs:
            icon = weather_icons.get(condition, '🌤️')
            st.write(f"{icon} **{condition}:** {prob:.1f}%")
            st.progress(prob / 100)
        
        # Seasonal context
        st.subheader("🍂 Seasonal Context")
        season_info = {
            (12, 1, 2): ("Winter", "❄️", "Cold temperatures with possible snow and rain"),
            (3, 4, 5): ("Spring", "🌸", "Mild temperatures with frequent rain showers"),
            (6, 7, 8): ("Summer", "☀️", "Warm and humid with afternoon thunderstorms"),
            (9, 10, 11): ("Fall", "🍁", "Cool and crisp with occasional rain")
        }
        
        for months, (season, emoji, desc) in season_info.items():
            if month in months:
                st.info(f"{emoji} **{season} in NYC:** {desc}")
                break

with col2:
    st.header("📈 Historical Trends")
    
    # Show recent weather patterns
    recent_data = historical_data.tail(30)
    
    # Weather condition distribution
    condition_counts = recent_data['condition'].value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#FFD700', '#87CEEB', '#4682B4', '#B0E0E6']
    condition_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=colors)
    ax.set_title('Recent 30-Day Weather Distribution')
    ax.set_ylabel('')
    st.pyplot(fig)
    
    # Temperature trend
    st.subheader("🌡️ Temperature Trend")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(recent_data['date'], recent_data['temperature'], color='#FF6B6B', linewidth=2)
    ax2.set_title('Temperature Over Last 30 Days')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Temperature (°F)')
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

# Footer
st.markdown("---")
st.markdown("**Team T-Minus Rain** | NASA Space Apps Challenge 2025")
st.markdown("*Forecasts are model predictions and should be used alongside official weather services for critical decisions.*")