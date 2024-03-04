# Find Color Palette🎨

## 🌱Intro
A webpage build by Streamlit. On this page, users can choose an image from their device and submit it to extract the color palette using three different methods (top N, median cut, K-means).

## ⚙️Libraries
- `pandas`: For table show on webpage.
- `numpy`: For processing the image array.
- `streamlit`: For building the webpage.
- `scikit-learn`: For K-means algrithm.
- `pillow`: For loading images.

## 🦿Features
- Image color palette extraction with three method: 
    -  Top N Color
    -  Median Cut
    -  K-Means

## ⚗️Process
Using Streamlit to build a webpage. On this page, users can choose an image from their device and submit it to extract the color palette using three different methods. 
Firstly, the Top N Color method calculates the frequency of colors and returns the top N colors. However, I found that this method is not ideal for extracting a color palette, as the top N colors may not accurately represent the image. Therefore, I added two additional methods: Median Cut and K-Means, which are commonly used for color palette extraction.

## 📚Learnings
I learned about the median cut algorithm and K-means algorithm and applied them in a practical use case.

## 🛠️Improvement
☑️**Passing by URL**: Users have the option to extract a color palette by pasting a URL.

☑️**More Features**: Expanding the functionality to include features such as image resizing and changing color palettes.

## 🏃‍♂️Running the Project
Running in your local enviroment:
1. **Clone this repository:** `git clone https://github.com/jinrumiao/Find_color_palette.git`.
2. **Install libaries:** `pip install -r requirements.txt`.
3. **Start the streamlit app:** `streamlit run main.py`.
4. **Open the webpage:** Navigate to `http://localhost:8501` in your browser to access the webpage, or use the URL shown in your terminal.

or

Navigate to [app](https://jinrumiao-find-color-palette-main-gfam3z.streamlit.app/)

## 🎞️Video
https://github.com/jinrumiao/Find_color_palette/assets/122008339/a29ff629-e613-41ac-90d6-08b16e03a530
