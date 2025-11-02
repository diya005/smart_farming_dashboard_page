from tensorflow import keras

# --- Load the problematic model ---
# Make sure the path has a "/" between "models" and the filename
model = keras.models.load_model('models/banana_leaf_3class_model.keras', compile=False, safe_mode=True)

# --- Inspect structure ---
model.summary()

# --- Fix: If model has multiple outputs, keep the first one ---
if isinstance(model.output, list):
    fixed_model = keras.Model(inputs=model.input, outputs=model.output[0])
else:
    fixed_model = model

# --- Save cleaned model ---
fixed_model.save('models/banana_leaf_fixed.keras')
print("Saved cleaned model to models/banana_leaf_fixed.keras")
