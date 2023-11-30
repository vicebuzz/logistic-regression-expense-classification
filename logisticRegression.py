import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix


# Load your data (replace 'your_data.csv' with your actual file path)
data = pd.read_csv('expenses.csv')

# Display the first few rows to understand the structure of the data
# print(data.head())


X = data['description']  # Feature variable (text descriptions)
y = data['category']     # Target variable (expense categories)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)


# Make predictions on the test set
y_pred = model.predict(X_test)

results_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred, 'Description': X_test})

# Filter rows where predictions are incorrect
incorrect_predictions = results_df[results_df['Actual'] != results_df['Predicted']]

# Display incorrect predictions
results_df.to_csv('predictions.csv', index=False)
incorrect_predictions.to_csv('incorrect_pred.csv', index=False)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))



# after training and testing a model, we can use it to classify new spendings
new_spendings = pd.read_csv('predict.csv')
spendings_to_categorise = new_spendings.iloc[:, 4]

print(spendings_to_categorise)

y_pred = model.predict(spendings_to_categorise)

new_df = pd.DataFrame({'source': spendings_to_categorise, 'prediction': y_pred})
new_df.to_csv('new_pred.csv')


