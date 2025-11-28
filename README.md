# Netflix Movie Data Explorer

A comprehensive data science project analyzing Netflix's content library. This project demonstrates data cleaning, exploratory data analysis (EDA), and data visualization skills using Python, Pandas, and Matplotlib.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📊 Project Overview

This project analyzes a dataset of **8,807 Netflix titles** to uncover patterns and insights about:
- Content type distribution (Movies vs TV Shows)
- Genre popularity and trends
- Release patterns over time
- Runtime clustering and distribution
- Content ratings analysis
- Netflix's content addition strategy

## 🎯 Key Features

- **Data Cleaning**: Handles duplicates, missing values, and data type conversions
- **Exploratory Data Analysis**: Comprehensive statistical analysis and pattern identification
- **Data Visualization**: 9 professional visualizations covering all major aspects
- **Insights Generation**: Automated extraction of key findings and trends

## 📈 Key Findings

1. **Content Mix**: Netflix library is 69.6% movies and 30.4% TV shows
2. **Genre Leader**: 'International Movies' dominates with 2,752 titles (31.2% of all content)
3. **Modern Focus**: 84.8% of content was released in 2010 or later
4. **Runtime Clustering**: Most movies (3,092 titles) fall in the 90-120 minute range
5. **Growth Peak**: Netflix added 1,999 titles in 2019, showing aggressive expansion
6. **Rating Focus**: TV-MA is the most common rating with 3,207 titles

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
git clone https://github.com/Eveliox/NetflixAnalysis.git
cd NetflixAnalysis2. Install required packages:
pip install -r requirements.txt### Usage

1. Ensure `netflix_titles.csv` is in the project directory
2. Run the analysis script:
python netflix_analysis.py
3. The script will:
   - Load and clean the data
   - Perform exploratory data analysis
   - Generate 9 visualizations
   - Display key insights
   - Save `netflix_analysis.png` with all visualizations

## 📁 Project Structure
NetflixAnalysis/
│
├── netflix_analysis.py      # Main analysis script
├── netflix_titles.csv       # Dataset (8,807 titles)
├── netflix_analysis.png     # Generated visualization dashboard
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
└── README.md               # This file

📊 Visualizations Generated
The script creates a comprehensive dashboard with 9 visualizations:
Content Type Distribution - Pie chart showing Movies vs TV Shows
Top 10 Genres - Horizontal bar chart of most popular genres
Releases Over Time - Line chart showing content release trends
Content Added to Netflix - Timeline of when content was added
Runtime Distribution - Histogram of movie runtimes
Average Runtime by Decade - Bar chart showing runtime trends
Top 10 Content Ratings - Distribution of content ratings
Movies vs TV Shows Over Time - Comparison of content types
Runtime Distribution by Category - Categorized runtime analysis

🛠️ Technologies Used
Pandas - Data manipulation and analysis
NumPy - Numerical computing
Matplotlib - Data visualization
Seaborn - Statistical data visualization

📝 Data Cleaning Steps
Duplicate Removal: Removed entries with identical title and release year
Missing Ratings: Filled missing ratings with 'Not Rated'
Runtime Extraction: Parsed duration strings to extract minutes for movies
Date Conversion: Converted date_added to datetime format
Genre Processing: Split comma-separated genre lists for analysis

📊 Dataset Information
Source: Kaggle (public dataset)
Total Records: 8,807 titles
Time Range: 1925 - 2021
Columns: 12 (show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description)

🎓 Skills Demonstrated
✅ Data cleaning and preprocessing
✅ Exploratory data analysis (EDA)
✅ Statistical analysis
✅ Data visualization
✅ Pattern identification
✅ Data storytelling
✅ Python programming
✅ Pandas data manipulation

📸 Sample Output
After running the script, you'll see:
Detailed console output with analysis progress
Statistical summaries of key metrics
6 key insights automatically generated
A high-resolution PNG file (netflix_analysis.png) with all visualizations

🤝 Contributing
Contributions are welcome! Feel free to:
Report bugs
Suggest new features
Submit pull requests
Improve documentation

📄 License
This project is open source and available under the MIT License.
👤 Author
Eveliox
GitHub: @Eveliox
Project Link: https://github.com/Eveliox/NetflixAnalysis

🙏 Acknowledgments
Dataset source: Kaggle Netflix Dataset
Python community for excellent data science libraries
Netflix for providing public data

📚 Additional Resources
Pandas Documentation
Matplotlib Documentation
Seaborn Documentation
