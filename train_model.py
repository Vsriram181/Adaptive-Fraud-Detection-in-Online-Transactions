import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load your dataset
# Assuming your dataset is a CSV file, update the path as needed
df = pd.read_csv('dataset.csv')

# Data Preprocessing
# Ensure that the necessary columns are present in the dataset
# Here we assume that 'type' is categorical and needs encoding
# and 'isFraud' is the target column

# Encode categorical 'type' feature
label_encoder = LabelEncoder()
df['type'] = label_encoder.fit_transform(df['type'])

# Drop non-numeric columns like 'nameOrig' and 'nameDest'
# You can either drop or encode them; for now, we'll drop them since they are likely identifiers
df = df.drop(columns=['nameOrig', 'nameDest'])

# Define feature columns and target column
feature_columns = [
     'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 
    'oldbalanceDest', 'newbalanceDest'
]
X = df[feature_columns]  # Features
y = df['isFraud']  # Target

# Handle missing values if any (e.g., replace NaNs with the mean)
X = X.fillna(X.mean())

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data (scaling)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a machine learning model (Random Forest Classifier)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate the model
train_accuracy = model.score(X_train_scaled, y_train)
test_accuracy = model.score(X_test_scaled, y_test)

print(f'Training Accuracy: {train_accuracy}')
print(f'Test Accuracy: {test_accuracy}')

# Save the model, scaler, and label encoder
joblib.dump(model, 'model/fraud_detection_model.pkl')
joblib.dump(scaler, 'model/scaler.pkl')
joblib.dump(label_encoder, 'model/type_encoder.pkl')

print("Model and necessary components have been saved!")
