import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# 1. Sample historical data generation
np.random.seed(42)
n_samples = 1000
data = {
    'day_of_year': np.random.randint(1, 366, n_samples),
    'humidity': np.random.uniform(40, 95, n_samples),
    'wind_speed': np.random.uniform(2, 25, n_samples),
    'prev_temp': np.random.uniform(20, 42, n_samples),
    'prev_rainfall': np.random.uniform(0, 100, n_samples),
}
df = pd.DataFrame(data)

# Targets
df['target_temp'] = df['prev_temp'] * 0.9 + np.random.normal(0, 2, n_samples)
df['target_rainfall'] = (df['humidity'] * 0.5 + df['prev_rainfall'] * 0.4 + np.random.normal(0, 5, n_samples)).clip(lower=0)

# 2. Features & Targets
X = df[['day_of_year', 'humidity', 'wind_speed', 'prev_temp', 'prev_rainfall']]
y_temp = df['target_temp']
y_rain = df['target_rainfall']

# 3. Train Models
temp_model = RandomForestRegressor(n_estimators=100, random_state=42)
temp_model.fit(X, y_temp)

rain_model = RandomForestRegressor(n_estimators=100, random_state=42)
rain_model.fit(X, y_rain)

# 4. Save models
with open('models_temp.pkl', 'wb') as f:
    pickle.dump(temp_model, f)
with open('models_rain.pkl', 'wb') as f:
    pickle.dump(rain_model, f)

print("Models trained and saved successfully!")