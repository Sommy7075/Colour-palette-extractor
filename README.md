# Colour Palette Extractor

Upload an image and get its 10 most common colours as HEX codes. Click any swatch to copy it.

## Features
- In-memory image processing (nothing saved to disk)
- Colour bucketing with NumPy to group near-identical shades
- Click-to-copy HEX codes
- File type and 5 MB size validation

## Tech
Python, Flask, Pillow, NumPy

## Run locally
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python app.py

Then open http://127.0.0.1:5000

## How it works
The image is shrunk to 200x200, flattened into a list of RGB pixels, and rounded into buckets of 8 so similar shades count together. `np.unique` counts each bucket and the top 10 are returned as HEX codes.