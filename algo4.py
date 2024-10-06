from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from corpora import amazon_polarity

# Prepare the data
train = amazon_polarity['train']
tests = amazon_polarity['test']
train_texts = [item['content'] for item in train]
train_labels = [item['label'] for item in train]
test_texts = [item['content'] for item in tests]
test_labels = [item['label'] for item in tests]

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(train_texts, train_labels, test_size=0.2)

# Convert text data to TF-IDF features
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a logistic regression model
model = DecisionTreeClassifier()
model.fit(X_train_tfidf, y_train)

# Predict and evaluate the model
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')