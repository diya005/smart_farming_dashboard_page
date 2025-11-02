from tensorflow import keras

# --- Load the problematic model ---
print("Loading model...")
old_model = keras.models.load_model('models/banana_leaf_3class_model.keras', compile=False, safe_mode=False)
print("✅ Model loaded")

# --- Inspect outputs ---
if isinstance(old_model.output, list):
    print(f"Model has {len(old_model.output)} outputs. Fixing to use only the first one...")
    new_model = keras.Model(inputs=old_model.input, outputs=old_model.output[0])
else:
    print("Model already has a single output.")
    new_model = old_model

# --- Save fixed model ---
new_model.save('models/banana_leaf_fixed.keras')
print("Saved cleaned model to models/banana_leaf_fixed.keras")
