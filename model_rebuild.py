from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow import keras

print("🔧 Rebuilding clean architecture...")

# --- Rebuild your original architecture ---
base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(200,200,3))
base.trainable = False

clean_model = Sequential([
    base,
    GlobalAveragePooling2D(),
    Dropout(0.3),
    Dense(3, activation='softmax')  # 3-class classifier
])

clean_model.compile(optimizer=Adam(1e-4),
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])

print("Model rebuilt successfully")

# --- Load weights from the corrupted model ---
try:
    old_model = keras.models.load_model('models/banana_leaf_3class_model.keras', compile=False, safe_mode=False)
    clean_model.set_weights(old_model.get_weights())
    print("Weights loaded from old model")
except Exception as e:
    print("⚠️ Failed to load weights:", e)

# --- Save a clean working model ---
clean_model.save('models/banana_leaf_fixed.keras')
print(" Saved fixed model to models/banana_leaf_fixed.keras")
