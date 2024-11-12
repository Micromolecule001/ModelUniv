import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Завантаження даних
df = pd.read_csv("Abalone.csv")


# 1

print("Опис статистичної інформації:")
print(df.describe())

print(f"Кількість записів у вибірці: {df.shape[0]}")
print(f"Кількість ознак: {df.shape[1]}")
print(f"Назви ознак: {df.columns.tolist()}")

categorical_columns = df.select_dtypes(include=['object']).columns
print(f"Категоріальні ознаки: {categorical_columns.tolist()}")

encoder = LabelEncoder()
df['Sex'] = encoder.fit_transform(df['Sex'])

print(f"Пропущені значення: {df.isnull().sum().sum()}")
df = df.dropna()

print(f"Кількість дублікатів: {df.duplicated().sum()}")
df = df.drop_duplicates()

print(f"Кількість записів після очищення: {df.shape[0]}")
print(f"Кількість ознак після очищення: {df.shape[1]}")

print("Кількість екземплярів у кожному класі:")
print(df['Sex'].value_counts())


# 2

# sns.pairplot(df, hue="Sex")
# plt.show()


# 3 

X = df.drop(columns="Sex")
y = df["Sex"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Точність класифікатора:", accuracy)

comparison_df = pd.DataFrame({"Реальні значення": y_test[:10].values, "Прогнозовані значення": y_pred[:10]})
print("Порівняння реальних та прогнозованих значень:\n", comparison_df)

# 4

print("Звіт про продуктивність класифікатора:")
print(classification_report(y_test, y_pred))


# 5 

conf_matrix = confusion_matrix(y_test, y_pred)
print("Матриця неточностей:")
print(conf_matrix)
sns.heatmap(conf_matrix, annot=True, cmap="Blues", fmt="d")
plt.show()


# 6

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Розподіл на тренувальний і тестовий набори
X_train_scaled, X_test_scaled, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Навчання класифікатора на масштабованих даних
classifier.fit(X_train_scaled, y_train)
y_pred_scaled = classifier.predict(X_test_scaled)

# Оцінка продуктивності
print("Звіт продуктивності після масштабування:")
print(classification_report(y_test, y_pred_scaled))


# 7

best_accuracy = 0
best_k = 1
for k in range(1, 21):
    classifier = KNeighborsClassifier(n_neighbors=k)
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    if score > best_accuracy:
        best_accuracy = score
        best_k = k

print(f"Найкраще значення k: {best_k}, точність: {best_accuracy}")


# 9 

#   def euclidean_distance(a, b):
#       return np.sqrt(np.sum((a - b) ** 2))

#   test_samples = X_test.sample(n=9, random_state=1)
#   for i, test_sample in test_samples.iterrows():
#       distances = []
#       for j, train_sample in X_train.iterrows():
#           distance = euclidean_distance(test_sample.values, train_sample.values)
#           distances.append((distance, y_train.iloc[j]))
#       nearest_neighbor = min(distances, key=lambda x: x[0])

