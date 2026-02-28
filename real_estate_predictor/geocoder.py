"""
Geocoding utility for Indian cities
Maps city names to approximate coordinates
"""

CITY_COORDINATES = {
    'Agra': (27.1767, 78.0081),
    'Ahmedabad': (23.0225, 72.5714),
    'Ajmer': (26.4499, 74.6399),
    'Ambala': (29.3776, 76.7709),
    'Amritsar': (31.6340, 74.8723),
    'Asansol': (23.6856, 86.9632),
    'Bangalore': (12.9716, 77.5946),
    'Belgaum': (15.8497, 74.4977),
    'Bhavnagar': (21.7645, 71.9137),
    'Chandigarh': (30.7333, 76.7794),
    'Chennai': (13.0827, 80.2707),
    'Coimbatore': (11.0081, 76.9877),
    'Delhi NCR': (28.6139, 77.2090),
    'Durgapur': (23.5204, 87.3119),
    'Faridabad': (28.4089, 77.3178),
    'Ghaziabad': (28.6692, 77.4538),
    'Gurgaon': (28.4595, 77.0266),
    'Howrah': (22.5958, 88.2636),
    'Hubli': (15.3647, 75.1240),
    'Jaipur': (26.9124, 75.7873),
    'Jalandhar': (31.7260, 75.5762),
    'Jodhpur': (26.2389, 73.0243),
    'Kanpur': (26.4499, 80.3319),
    'Karnal': (29.6200, 77.1040),
    'Kolkata': (22.5726, 88.3639),
    'Kota': (25.2138, 75.8648),
    'Lucknow': (26.8467, 80.9462),
    'Ludhiana': (30.9010, 75.8573),
    'Madurai': (9.9252, 78.1198),
    'Mangalore': (12.8628, 74.8454),
    'Mumbai': (19.0760, 72.8777),
    'Mysore': (12.2958, 76.6394),
    'Nagpur': (21.1458, 79.0882),
    'Nashik': (19.9975, 73.7898),
    'New Delhi': (28.6139, 77.2090),
    'Noida': (28.5355, 77.3910),
    'Panipat': (29.3910, 77.0940),
    'Patiala': (30.3398, 76.3869),
    'Pune': (18.5204, 73.8567),
    'Rajkot': (22.3039, 70.8022),
    'Salem': (11.6643, 78.1460),
    'Siliguri': (26.5273, 88.4100),
    'Surat': (21.1702, 72.8311),
    'Thane': (19.2183, 72.9781),
    'Tiruchirappalli': (10.7905, 78.7047),
    'Udaipur': (24.5854, 73.7125),
    'Vadodara': (22.3072, 73.1812),
    'Varanasi': (25.3201, 82.9789),
}

def add_coordinates_to_dataframe(df):
    """
    Add latitude and longitude columns to dataframe based on city names
    """
    if 'city' not in df.columns:
        return df
    
    # Check if coordinates already exist
    if 'latitude' not in df.columns:
        df['latitude'] = df['city'].map(lambda x: CITY_COORDINATES.get(x, (20.5937, 78.9629))[0])
    
    if 'longitude' not in df.columns:
        df['longitude'] = df['city'].map(lambda x: CITY_COORDINATES.get(x, (20.5937, 78.9629))[1])
    
    return df

def get_city_coordinates(city_name):
    """Get coordinates for a city"""
    return CITY_COORDINATES.get(city_name, (20.5937, 78.9629))  # Default to India center
