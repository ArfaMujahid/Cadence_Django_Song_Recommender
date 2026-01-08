# Cadence
Cadence is a music recommender that uses K-Nearest Neighbors (KNN), content-based filtering and custom similarity algorithms to suggest 20 songs similar to a user-provided song. The recommendations are drawn exclusively from the dataset, with comparisons based on various audio and song features within that dataset.
 
## Installation
 
1. Make sure you have Python 3.8+ installed
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
 
## Usage
 
1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
2. Open your browser and navigate to `http://127.0.0.1:8000/`
3. Enter a song name and artist name in the form
4. Click "Get Recommendations" to see 20 similar songs based on:
   - Custom similarity scoring
   - Two-layer KNN with scikit-learn
   - Custom KNN implementation
 
## Features
 
- **Minimalist UI**: Clean, modern dark theme design
- **Three Recommendation Methods**: Combines multiple algorithms for better results
- **CSV-based**: No database required - works directly with the dataset
- **Responsive Design**: Works on desktop and mobile devices
 
## Screenshots
 
![loading](loading.png)![results](results.png)![results1](results1.png)