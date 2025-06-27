import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score


df = pd.read_csv(r"/Users/admin/Projects/RunningPerformance/scraped_data.csv")
df

df = df.dropna()
df

df['Age'] = df['Age'].str.extract('(\d+)', expand=False).astype(int)
df

df['Gender'] = df['Gender'].replace({'М': 1, 'Ж': 0})
df

plt.figure(figsize=(10, 6))
sns.countplot(x='Age', data=df)
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(8, 8))
gender_counts = df['Gender'].value_counts()
plt.pie(gender_counts, labels=['Male', 'Female'], autopct='%1.1f%%', startangle=140, colors=['skyblue', 'lightpink'])
plt.title('Gender Distribution')
plt.show()

def time_to_minutes(time_str):
    parts = time_str.split(':')
    if len(parts) == 2:
        parts.insert(0, '0')  # Add hours if missing
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds / 60

df['Time'] = df['Time'].apply(time_to_minutes)
df

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

colors = df['Gender'].map({0: 'violet', 1: 'yellow'})

plt.figure(figsize=(10, 6))
plt.scatter(df['Age'], df['Time'], c=colors, alpha=1)

# Custom legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Female', markerfacecolor='violet', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Male', markerfacecolor='yellow', markersize=8)
]
plt.legend(handles=legend_elements, title='Gender')

plt.title('Age and Time')
plt.xlabel('Age')
plt.ylabel('Time (minutes)')
plt.show()

X = df[['Age', 'Gender']]
y = df['Time']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train, y_train)

y_pred_knn = knn.predict(X_test)

print("KNN Mean Squared Error:", mean_squared_error(y_test, y_pred_knn))
print("KNN R2 Score:", r2_score(y_test, y_pred_knn))

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_knn, color='purple')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
plt.xlabel('Measured')
plt.ylabel('Predicted')
plt.title('KNN: Measured vs Predicted')
plt.show()

y_pred_knn = knn.predict(X_test)

# Print actual and predicted values
print("Actual Time:", y_test[:50].values)
print("Predicted Time:", y_pred_knn[:50])