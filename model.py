import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.preprocessing import OrdinalEncoder,OneHotEncoder, RobustScaler, MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV,RandomizedSearchCV
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_log_error, mean_squared_error, make_scorer, mean_absolute_percentage_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, StackingRegressor, BaggingRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn import set_config; set_config(display='diagram')
from data_cleaning import clean_data
import joblib

data = pd.read_csv('housing_data_full.csv',low_memory=False)
data = data.drop_duplicates()
data = clean_data(data)
data = data.drop(index=[11038,17838,25859])
data['Metro'] = data['Metro'].str.lower()
data['District'] = data['District'].str.lower()

# Create a copy of the original data
data_processed = data.copy()
data_processed = data_processed.drop(columns=['Listing_Id',
                                              'Available From',
                                              'First_post',
                                              'Landlord lives in Shanghai',
                                              'English Speaking Landlord',
                                             'Longtitude',
                                             'Latitude'])
# Fill missing values in the 'Recently renovated' column with zeros
data_processed['Recently renovated'].fillna(0, inplace=True)
# Delete rows with missing values in the 'Price' column
data_processed = data_processed.dropna(subset=['Price'])
data_processed = data_processed.reset_index(drop=True)

# Perform ordinal encoding for 'Furnished' column
ordinal_encoder = OrdinalEncoder(categories=[['Unfurnished', 'Furnished']])
data_processed['Furnished'] = ordinal_encoder.fit_transform(data_processed[['Furnished']])

# Perform one-hot encoding for 'Metro' and 'District' columns
metro_encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
district_encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')

# Encode 'Metro' column
metro_encoded = metro_encoder.fit_transform(data_processed[['Metro']])
metro_names = metro_encoder.get_feature_names_out(['Metro'])
data_processed = pd.concat([data_processed, pd.DataFrame(metro_encoded, columns=metro_names)], axis=1)
data_processed.drop('Metro', axis=1, inplace=True)

# Encode 'District' column
district_encoded = district_encoder.fit_transform(data_processed[['District']])
district_names = district_encoder.get_feature_names_out(['District'])
data_processed = pd.concat([data_processed, pd.DataFrame(district_encoded, columns=district_names)], axis=1)
data_processed.drop('District', axis=1, inplace=True)

X = data_processed.drop(['Price'], axis=1)
y = data_processed['Price']
# Split the preprocessed data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

frame = X.drop(X.index)
frame.loc[0]=0
frame.to_csv('frame.csv',index=False)

# Train the RandomForestRegressor
rf_model = RandomForestRegressor()
rf_model.fit(X_train, y_train)
# Train the DecisionTreeRegressor
dt_model = DecisionTreeRegressor()
dt_model.fit(X_train, y_train)
# Train the XGBRegressor
xgb_model = XGBRegressor()
xgb_model.fit(X_train, y_train)
# Make predictions on the test set
rf_predictions = rf_model.predict(X_test)
dt_predictions = dt_model.predict(X_test)
xgb_predictions = xgb_model.predict(X_test)

from sklearn.metrics import mean_squared_error, mean_absolute_error

def calculate_mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Calculate MAPE for each model
rf_mape = calculate_mape(y_test, rf_predictions)
dt_mape = calculate_mape(y_test, dt_predictions)
xgb_mape = calculate_mape(y_test, xgb_predictions)

# Calculate evaluation metrics
rf_mse = mean_squared_error(y_test, rf_predictions)
rf_rmse = np.sqrt(rf_mse)
rf_mae = mean_absolute_error(y_test, rf_predictions)

dt_mse = mean_squared_error(y_test, dt_predictions)
dt_rmse = np.sqrt(dt_mse)
dt_mae = mean_absolute_error(y_test, dt_predictions)

xgb_mse = mean_squared_error(y_test, xgb_predictions)
xgb_rmse = np.sqrt(xgb_mse)
xgb_mae = mean_absolute_error(y_test, xgb_predictions)

# Print the evaluation metrics
print("Random Forest:")
print("RMSE:", rf_rmse)
print("MAE:", rf_mae)
print("MAPE:", rf_mape)

print("\nDecision Tree:")
print("RMSE:", dt_rmse)
print("MAE:", dt_mae)
print("MAPE:", dt_mape)

print("\nXGBoost:")
print("RMSE:", xgb_rmse)
print("MAE:", xgb_mae)
print("MAPE:", xgb_mape)



# Save the trained model
joblib.dump(rf_model, 'random_forest_model.joblib')
