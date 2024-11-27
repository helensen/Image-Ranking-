
# Printhead Quality Assessor
# Overview
_The Printhead Quality Assessor is a Python-based tool designed to evaluate the quality of printheads by analyzing images of their output. It uses Tkinter for its user interface and Pillow for image processing. The program calculates the total number of pixels and dark pixels in a selected area of an image and assigns a quality rank to the printhead based on the proportion of dark pixels._

# Features
User-friendly interface for selecting and analyzing images.
Allows users to draw a rectangular selection over the image to analyze specific areas.
Counts total pixels and dark pixels within the selected area.
Highlights dark pixels in blue for easy visualization.
Automatically assigns a rank to the printhead based on the percentage of dark pixels:
Rank 1: ≤ 10% dark pixels.
Rank 2: 10% - 20% dark pixels.
Rank 3: 20% - 30% dark pixels.
Rank 4: > 30% dark pixels.
Provides a summary of the total pixel count, dark pixel count, and rank for each analyzed selection.

## Requirements
Python 3.8 or later
Pillow (Python Imaging Library)
Tkinter (comes pre-installed with Python)
NumPy (for numerical operations)

# How to Use
Run the program:

    python <script_name>.py

Open an image by selecting File > Open Image in the menu.
Use the mouse to draw a rectangular selection over the image.
After releasing the mouse, the program will:
Calculate the total pixels and dark pixels within the selected area.
Highlight dark pixels in blue.
Display the results (total pixels, dark pixels, and rank) in the control panel.
Adjust the darkness threshold using the slider to refine the definition of "dark pixels."

# Example Output

    Total Pixels: 10,000
    Dark Pixels: 800
    Rank: 1

# Customization
The darkness threshold can be adjusted via the slider to accommodate varying image lighting conditions.
The ranking thresholds can be modified by updating the rank_image method in the code.
Future Improvements
Add functionality to analyze multiple areas in a single session.
Support batch processing for multiple images.
Provide export options for analysis results (e.g., CSV or JSON).

# Acknowledgments
This program was developed by Abel Muanda to support quality assessment in the foundry by analyzing printhead outputs.




