import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Features and target variable
X = df.drop(columns=['algorithm'])
y = df['algorithm']

# Encoding target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Normalizing features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Splitting data into train and test sets before cross-validation
X_train_all, X_test, y_train_all, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

# Stratified K-Fold Cross-Validation
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
fold_no = 1
accuracy_per_fold = []
best_model = None
best_val_acc = 0.0

for train, val in kfold.split(X_train_all, y_train_all):
    X_train, X_val = X_train_all[train], X_train_all[val]
    y_train, y_val = y_train_all[train], y_train_all[val]
    
    # Model Architecture with increased complexity
    model = Sequential([
        Dense(256, activation='relu', input_shape=(X_train.shape[1],), kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        BatchNormalization(),
        Dropout(0.5),
        Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        BatchNormalization(),
        Dropout(0.5),
        Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
        BatchNormalization(),
        Dropout(0.5),
        Dense(len(label_encoder.classes_), activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    early_stopping = EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5)

    history = model.fit(
        X_train, y_train,
        epochs=150,
        validation_data=(X_val, y_val),
        batch_size=32,
        callbacks=[early_stopping, reduce_lr],
        verbose=1
    )

    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
    accuracy_per_fold.append(val_acc * 100)
    print(f"Fold {fold_no} - Validation Accuracy: {val_acc * 100:.2f}%")
    
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        best_model = model
    
    fold_no += 1

avg_accuracy = np.mean(accuracy_per_fold)
print(f"Average Cross-Validation Accuracy: {avg_accuracy:.2f}%")

test_loss, test_acc = best_model.evaluate(X_test, y_test, verbose=2)
print(f'Final Test Accuracy: {test_acc * 100:.2f}%')

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.show()

best_model.save('best_model.h5')

joblib.dump(scaler, 'scaler.joblib')
