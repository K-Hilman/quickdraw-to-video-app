# quickdraw-to-video-app

A web app to generate videos mosaics from the Google QuickDraw dataset, using country- and category-filtered doodles.  
Powered by Flask, Pillow, MoviePy, and Tailwind CSS for a modern, responsive UI.

## Features

- 🖼️ Search and select from all QuickDraw categories (200+)
- 🌍 Filter doodles by country
- 🟦 Choose grid sizes (Square, Story, Landscape)
- 🔢 Seeded randomization for reproducibility
- 🟦 Modern, responsive interface (Tailwind CSS + Choices.js)
- ⏳ Generates an MP4 video for download right in the browser!

## Demo

### Example Output

Below is a sample video mosaic generated using the "Cat" category, filtered for Malaysia, in a square grid:

![Cat Doodle Mosaic (Malaysia, Square)](static/quick_draw/cat_MY_sq.gif)

## Getting Started

### Prerequisites

- Python 3.8+
- Pip

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/quickdraw-video-generator.git
   cd quickdraw-video-generator
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

### Running the App Locally

```sh
python app.py
```
Visit [http://localhost:5000](http://localhost:5000) in your browser.

### Usage

1. Choose your **category**, **country**, **grid size**, and (optionally) a random seed.
2. Click `Generate Video`.
3. Wait for your video; then view, download, or share!

## File Structure

```
├── app.py                # Flask app entry point
├── quick_draw.py         # QuickDraw video logic
├── requirements.txt      # Project dependencies
├── templates/
│   └── index.html        # Main UI template
├── static/
│   └── quick_draw/       # Output files (videos, images)
```

## License

MIT License.  
QuickDraw data © Google, used under the terms of the [QuickDraw Dataset license](https://quickdraw.withgoogle.com/data).

## Credits

- [QuickDraw Dataset by Google](https://quickdraw.withgoogle.com/data)
- [Pillow](https://python-pillow.org/), [moviepy](https://zulko.github.io/moviepy/), [Choices.js](https://choices-js.github.io/Choices/), [Tailwind CSS](https://tailwindcss.com/)

---
