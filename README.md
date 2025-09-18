# XMP Interpolator for Lightroom Develop Settings

A Python script that **interpolates (blends)** Lightroom develop settings between different values.
Useful for timelapse sequences - especially holy grail timelapses - where smooth transitions between settings are important.

---

## Features

- Interpolates Lightroom develop settings across multiple images.
- Uses linear interpolation (default), but also supports multiple easing functions.
- Works with XMP sidecar files or can extract metadata into XMP from image files.
- Simple configuration via a `settings` dictionary in `main.py`.

---

## How it works

1. Provide:
   - A directory of XMP files (or images).
   - A list of keyframes.
   - A list of develop settings to interpolate.
2. The script interpolates values between the keyframes using the chosen easing function.
3. In Lightroom, use **Metadata → Read Metadata from File** to import the interpolated develop settings back into images. (make sure the XMP files are in the same folder as your images)

Easing functions are available to experiment with at https://easings.net/.

---

## Prerequisites

- Lightroom with XMP sidecar files enabled (Catalog Settings → Metadata → Automatically write changes into XMP), or use Metadata → Save Metadata to File to create sidecars.
- Python 3.x.
- exiftool (provided) - only required for XMP extraction

If you use DNG or DNG based (GPR) images (Lightroom writes metadata into the file), set `"extractXMPfromImages": True` in the settings dictionary and the script will extract XMP sidecar files for you.

---

## Usage

1. Clone or download the repository.
2. Open `main.py` in a text editor.
3. Configure the `settings` dictionary (see below).
4. Run the script:

```bash
python main.py
```

5. In Lightroom:
   Select your images → Right-click → **Metadata → Read Metadata from File**.

---

## Settings dictionary

The `settings` dictionary in `main.py` controls the script.

### `directory` (string)

Full path to the folder containing your XMP or image files.

> Important: Use the `r` prefix for Windows paths to avoid backslash escaping.

```python
"directory": r"C:\Pictures\Timelapse"
```

---

### `parameters` (list of `Parameter` objects)

Specify which develop settings to interpolate.

**Parameter object format:**

```python
Parameter(name, action = Action.Ease, actionData = Ease.Linear, namespace = "crs")
```

| Field | Type | Description |
|---|---:|---|
| `name` | string | Parameter name, e.g. `"Exposure2012"` or `"Temperature"`. |
| `action` | `Action` enum | What to do with the parameter: `Action.Ease` (default) interpolates; `Action.Set` writes a fixed value. |
| `actionData` | easing function or number | If `Action.Ease`, provide an easing function (e.g. `Ease.Linear`). If `Action.Set`, provide the value to apply. |
| `namespace` | string | XMP attribute namespace. Defaults to `"crs"` (you shouldn't need to change this). |

---

### `keyframes` (list of integers)

Zero-indexed image indices that define interpolation segments.

Example:

```python
"keyframes": [0, 49, 149]
```

This interpolates 0 → 49, then 49 → 149. At least two keyframes are required.

---

### `extractXMPfromImages` (boolean)

Set to `True` if your images embed metadata (e.g. DNG/GPR). The script will extract XMP sidecars from image files.

---

### `imageExtension` (string)

Image file extension used when extracting XMP, e.g. `"dng"`, `"gpr"`. Only required when `extractXMPfromImages` is `True`.

---

## Example configuration

```python
settings = {

    "directory":
        r"C:\Pictures\Timelapse",
    
    "parameters": 
    [
        Parameter("Exposure2012"),
        Parameter("Temperature"),
        Parameter("Contrast2012", action = Action.Set, actionData = 25)
    ],

    "keyframes":
        [0, 49, 149],

    "extractXMPfromImages":
        True,

    "imageExtension":
        "dng",

}
```

---

## Notes

- Easing functions are defined in `easing.py`. They could be fun to play with.
- The script expects your sequence images/XMP files to be ordered consistently (same naming/order as Lightroom sequence).

---

## License

This project is open source and available under the MIT License.
