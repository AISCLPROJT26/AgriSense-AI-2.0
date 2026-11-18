try:
    from PIL import Image
except ImportError:
    Image = None


def analyze_leaf_image(image_path):
    """
    Analyzes a leaf image using RGB color distribution via Pillow (PIL).
    Works 100% offline with zero heavy ML DLL dependencies.
    """
    if Image is None:
        return {"error": "Pillow is not installed. Please install the project requirements."}

    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize((150, 150))
        pixels = list(img.getdata())
        total_pixels = len(pixels)

        green_pixels = 0
        yellow_pixels = 0
        brown_dark_pixels = 0

        for r, g, b in pixels:
            # Healthy leaf green
            if g > r + 15 and g > b + 15:
                green_pixels += 1
            # Yellowing / Chlorosis / Rust
            elif r > 140 and g > 130 and b < 100:
                yellow_pixels += 1
            # Dark brown / necrotic blight spots
            elif r < 110 and g < 90 and b < 80:
                brown_dark_pixels += 1

        green_ratio = (green_pixels / total_pixels) * 100
        yellow_ratio = (yellow_pixels / total_pixels) * 100
        brown_ratio = (brown_dark_pixels / total_pixels) * 100

        if brown_ratio > 22:
            return {
                "disease": "Early / Late Blight (Fungal Necrosis)",
                "confidence": round(min(96.5, 78.0 + brown_ratio * 0.4), 1),
                "severity": "High",
                "treatment": "Remove infected lower leaves immediately. Apply Copper Oxychloride or Mancozeb (2g/L water) spray and avoid overhead irrigation."
            }
        elif yellow_ratio > 20:
            return {
                "disease": "Yellow Rust / Leaf Chlorosis",
                "confidence": round(min(94.0, 75.0 + yellow_ratio * 0.4), 1),
                "severity": "Moderate",
                "treatment": "Apply Propiconazole 25% EC (1ml/L) for fungal rust, or check soil Nitrogen & Magnesium levels if yellowing is uniform."
            }
        else:
            return {
                "disease": "Healthy Leaf",
                "confidence": round(min(98.2, 82.0 + green_ratio * 0.15), 1),
                "severity": "None",
                "treatment": "No disease detected! Maintain balanced NPK fertilization and regular morning watering."
            }
    except Exception as e:
        return {"error": f"Image processing failed: {str(e)}"}