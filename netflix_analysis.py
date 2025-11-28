"""
Netflix Movie Data Explorer
A comprehensive analysis of Netflix titles dataset
Skills: Data cleaning, EDA, and visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    plt.style.use('seaborn-darkgrid')
sns.set_palette("husl")

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("=" * 80)
print("NETFLIX MOVIE DATA EXPLORER")
print("=" * 80)
print("\n1. LOADING DATA...")
print("-" * 80)

df = pd.read_csv('netflix_titles.csv')
print(f"✓ Loaded {len(df):,} records with {len(df.columns)} columns")
print(f"✓ Columns: {', '.join(df.columns.tolist())}")

# ============================================================================
# 2. INITIAL DATA EXPLORATION
# ============================================================================
print("\n2. INITIAL DATA EXPLORATION")
print("-" * 80)
print(f"Dataset shape: {df.shape}")
print(f"\nMissing values:")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Percentage': missing_pct
})
print(missing_df[missing_df['Missing Count'] > 0])

# ============================================================================
# 3. DATA CLEANING
# ============================================================================
print("\n3. DATA CLEANING")
print("-" * 80)

# Create a copy for cleaning
df_clean = df.copy()

# 3.1 Handle duplicates
print("\n3.1 Checking for duplicates...")
duplicates = df_clean.duplicated(subset=['title', 'release_year'], keep=False)
num_duplicates = duplicates.sum()
print(f"  Found {num_duplicates} duplicate entries (same title + release_year)")
if num_duplicates > 0:
    print("  Removing duplicates (keeping first occurrence)...")
    df_clean = df_clean.drop_duplicates(subset=['title', 'release_year'], keep='first')
    print(f"  ✓ Removed {num_duplicates - duplicates.sum()} duplicates")
    print(f"  ✓ Remaining records: {len(df_clean):,}")

# 3.2 Handle missing ratings
print("\n3.2 Handling missing ratings...")
missing_ratings = df_clean['rating'].isnull().sum()
print(f"  Found {missing_ratings} missing ratings")
if missing_ratings > 0:
    # Fill with 'Not Rated' for missing values
    df_clean['rating'] = df_clean['rating'].fillna('Not Rated')
    print(f"  ✓ Filled {missing_ratings} missing ratings with 'Not Rated'")

# 3.3 Clean and extract runtime
print("\n3.3 Cleaning duration/runtime data...")
# Separate Movies and TV Shows
df_clean['is_movie'] = df_clean['type'] == 'Movie'

# Extract runtime for movies (in minutes)
def extract_runtime(duration_str):
    if pd.isna(duration_str):
        return np.nan
    if 'min' in str(duration_str).lower():
        try:
            return int(str(duration_str).split()[0])
        except:
            return np.nan
    return np.nan

df_clean['runtime_minutes'] = df_clean[df_clean['is_movie']]['duration'].apply(extract_runtime)

# Extract seasons for TV shows
def extract_seasons(duration_str):
    if pd.isna(duration_str):
        return np.nan
    if 'season' in str(duration_str).lower():
        try:
            return int(str(duration_str).split()[0])
        except:
            return np.nan
    return np.nan

df_clean['num_seasons'] = df_clean[~df_clean['is_movie']]['duration'].apply(extract_seasons)

print(f"  ✓ Extracted runtime for {df_clean['runtime_minutes'].notna().sum():,} movies")
print(f"  ✓ Extracted seasons for {df_clean['num_seasons'].notna().sum():,} TV shows")

# 3.4 Clean date_added
print("\n3.4 Cleaning date_added...")
df_clean['date_added'] = pd.to_datetime(df_clean['date_added'], errors='coerce')
df_clean['year_added'] = df_clean['date_added'].dt.year
print(f"  ✓ Converted date_added to datetime format")

# 3.5 Clean genres (listed_in)
print("\n3.5 Processing genres...")
df_clean['genres'] = df_clean['listed_in'].str.split(', ').apply(lambda x: [g.strip() for g in x] if isinstance(x, list) else [])
print(f"  ✓ Processed genres for analysis")

print("\n✓ Data cleaning complete!")

# ============================================================================
# 4. EXPLORATORY DATA ANALYSIS
# ============================================================================
print("\n4. EXPLORATORY DATA ANALYSIS")
print("-" * 80)

# 4.1 Content Type Distribution
print("\n4.1 Content Type Distribution:")
type_counts = df_clean['type'].value_counts()
print(type_counts)
print(f"  Movies: {type_counts.get('Movie', 0):,} ({type_counts.get('Movie', 0)/len(df_clean)*100:.1f}%)")
print(f"  TV Shows: {type_counts.get('TV Show', 0):,} ({type_counts.get('TV Show', 0)/len(df_clean)*100:.1f}%)")

# 4.2 Genre Analysis
print("\n4.2 Genre Analysis:")
all_genres = []
for genres_list in df_clean['genres']:
    if isinstance(genres_list, list):
        all_genres.extend(genres_list)
genre_counts = Counter(all_genres)
top_genres = genre_counts.most_common(15)
print(f"  Total unique genres: {len(genre_counts)}")
print(f"  Top 10 genres:")
for i, (genre, count) in enumerate(top_genres[:10], 1):
    print(f"    {i}. {genre}: {count:,} titles")

# 4.3 Release Year Analysis
print("\n4.3 Release Year Analysis:")
print(f"  Release years range: {df_clean['release_year'].min()} - {df_clean['release_year'].max()}")
print(f"  Most content released in: {df_clean['release_year'].mode()[0]} ({df_clean['release_year'].value_counts().iloc[0]} titles)")

# 4.4 Runtime Analysis (Movies only)
movies_df = df_clean[df_clean['is_movie'] & df_clean['runtime_minutes'].notna()]
if len(movies_df) > 0:
    print("\n4.4 Runtime Analysis (Movies):")
    print(f"  Total movies with runtime data: {len(movies_df):,}")
    print(f"  Average runtime: {movies_df['runtime_minutes'].mean():.1f} minutes")
    print(f"  Median runtime: {movies_df['runtime_minutes'].median():.1f} minutes")
    print(f"  Min runtime: {movies_df['runtime_minutes'].min()} minutes")
    print(f"  Max runtime: {movies_df['runtime_minutes'].max()} minutes")

# ============================================================================
# 5. VISUALIZATIONS
# ============================================================================
print("\n5. CREATING VISUALIZATIONS...")
print("-" * 80)

# Create figure with subplots
fig = plt.figure(figsize=(20, 16))

# 5.1 Content Type Distribution (Pie Chart)
ax1 = plt.subplot(3, 3, 1)
type_counts = df_clean['type'].value_counts()
colors = ['#E50914', '#564d4d']  # Netflix red and gray
ax1.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', 
        startangle=90, colors=colors, textprops={'fontsize': 12, 'weight': 'bold'})
ax1.set_title('Content Type Distribution', fontsize=14, fontweight='bold', pad=20)

# 5.2 Top Genres (Bar Chart)
ax2 = plt.subplot(3, 3, 2)
top_genres_df = pd.DataFrame(top_genres[:10], columns=['Genre', 'Count'])
ax2.barh(range(len(top_genres_df)), top_genres_df['Count'], color='#E50914')
ax2.set_yticks(range(len(top_genres_df)))
ax2.set_yticklabels(top_genres_df['Genre'], fontsize=10)
ax2.set_xlabel('Number of Titles', fontsize=11, fontweight='bold')
ax2.set_title('Top 10 Genres on Netflix', fontsize=14, fontweight='bold', pad=20)
ax2.invert_yaxis()
for i, v in enumerate(top_genres_df['Count']):
    ax2.text(v + 20, i, f'{v:,}', va='center', fontsize=9)

# 5.3 Releases Over Time (Line Chart)
ax3 = plt.subplot(3, 3, 3)
releases_by_year = df_clean.groupby('release_year').size()
ax3.plot(releases_by_year.index, releases_by_year.values, 
         linewidth=2.5, color='#E50914', marker='o', markersize=4)
ax3.fill_between(releases_by_year.index, releases_by_year.values, alpha=0.3, color='#E50914')
ax3.set_xlabel('Release Year', fontsize=11, fontweight='bold')
ax3.set_ylabel('Number of Titles', fontsize=11, fontweight='bold')
ax3.set_title('Content Releases Over Time', fontsize=14, fontweight='bold', pad=20)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(releases_by_year.index.min(), releases_by_year.index.max())

# 5.4 Content Added to Netflix Over Time
ax4 = plt.subplot(3, 3, 4)
added_by_year = df_clean[df_clean['year_added'].notna()].groupby('year_added').size()
ax4.plot(added_by_year.index, added_by_year.values, 
         linewidth=2.5, color='#E50914', marker='s', markersize=5)
ax4.fill_between(added_by_year.index, added_by_year.values, alpha=0.3, color='#E50914')
ax4.set_xlabel('Year Added to Netflix', fontsize=11, fontweight='bold')
ax4.set_ylabel('Number of Titles Added', fontsize=11, fontweight='bold')
ax4.set_title('Content Added to Netflix Over Time', fontsize=14, fontweight='bold', pad=20)
ax4.grid(True, alpha=0.3)

# 5.5 Runtime Distribution (Histogram)
ax5 = plt.subplot(3, 3, 5)
if len(movies_df) > 0:
    ax5.hist(movies_df['runtime_minutes'], bins=50, color='#E50914', edgecolor='black', alpha=0.7)
    ax5.axvline(movies_df['runtime_minutes'].mean(), color='blue', linestyle='--', 
                linewidth=2, label=f'Mean: {movies_df["runtime_minutes"].mean():.0f} min')
    ax5.axvline(movies_df['runtime_minutes'].median(), color='green', linestyle='--', 
                linewidth=2, label=f'Median: {movies_df["runtime_minutes"].median():.0f} min')
    ax5.set_xlabel('Runtime (minutes)', fontsize=11, fontweight='bold')
    ax5.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax5.set_title('Movie Runtime Distribution', fontsize=14, fontweight='bold', pad=20)
    ax5.legend()
    ax5.grid(True, alpha=0.3)

# 5.6 Runtime by Decade
ax6 = plt.subplot(3, 3, 6)
if len(movies_df) > 0:
    movies_df['decade'] = (movies_df['release_year'] // 10) * 10
    runtime_by_decade = movies_df.groupby('decade')['runtime_minutes'].mean()
    ax6.bar(runtime_by_decade.index, runtime_by_decade.values, 
            color='#E50914', edgecolor='black', alpha=0.7)
    ax6.set_xlabel('Decade', fontsize=11, fontweight='bold')
    ax6.set_ylabel('Average Runtime (minutes)', fontsize=11, fontweight='bold')
    ax6.set_title('Average Movie Runtime by Decade', fontsize=14, fontweight='bold', pad=20)
    ax6.set_xticks(runtime_by_decade.index)
    ax6.set_xticklabels([f"{int(d)}s" for d in runtime_by_decade.index], rotation=45)
    ax6.grid(True, alpha=0.3, axis='y')

# 5.7 Rating Distribution
ax7 = plt.subplot(3, 3, 7)
rating_counts = df_clean['rating'].value_counts().head(10)
ax7.barh(range(len(rating_counts)), rating_counts.values, color='#E50914')
ax7.set_yticks(range(len(rating_counts)))
ax7.set_yticklabels(rating_counts.index, fontsize=10)
ax7.set_xlabel('Number of Titles', fontsize=11, fontweight='bold')
ax7.set_title('Top 10 Content Ratings', fontsize=14, fontweight='bold', pad=20)
ax7.invert_yaxis()
for i, v in enumerate(rating_counts.values):
    ax7.text(v + 10, i, f'{v:,}', va='center', fontsize=9)

# 5.8 Movies vs TV Shows Over Time
ax8 = plt.subplot(3, 3, 8)
movies_by_year = df_clean[df_clean['is_movie']].groupby('release_year').size()
tv_by_year = df_clean[~df_clean['is_movie']].groupby('release_year').size()
ax8.plot(movies_by_year.index, movies_by_year.values, 
         label='Movies', linewidth=2.5, color='#E50914', marker='o', markersize=3)
ax8.plot(tv_by_year.index, tv_by_year.values, 
         label='TV Shows', linewidth=2.5, color='#564d4d', marker='s', markersize=3)
ax8.set_xlabel('Release Year', fontsize=11, fontweight='bold')
ax8.set_ylabel('Number of Titles', fontsize=11, fontweight='bold')
ax8.set_title('Movies vs TV Shows Over Time', fontsize=14, fontweight='bold', pad=20)
ax8.legend(fontsize=10)
ax8.grid(True, alpha=0.3)

# 5.9 Runtime Clusters (Box Plot)
ax9 = plt.subplot(3, 3, 9)
if len(movies_df) > 0:
    # Create runtime categories
    movies_df['runtime_category'] = pd.cut(movies_df['runtime_minutes'], 
                                       bins=[0, 60, 90, 120, 150, 300],
                                       labels=['<60 min', '60-90 min', '90-120 min', 
                                              '120-150 min', '>150 min'])
    runtime_cat_counts = movies_df['runtime_category'].value_counts().sort_index()
    ax9.bar(range(len(runtime_cat_counts)), runtime_cat_counts.values, 
            color='#E50914', edgecolor='black', alpha=0.7)
    ax9.set_xticks(range(len(runtime_cat_counts)))
    ax9.set_xticklabels(runtime_cat_counts.index, rotation=45, ha='right', fontsize=9)
    ax9.set_ylabel('Number of Movies', fontsize=11, fontweight='bold')
    ax9.set_title('Runtime Distribution by Category', fontsize=14, fontweight='bold', pad=20)
    ax9.grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(runtime_cat_counts.values):
        ax9.text(i, v + 10, f'{v:,}', ha='center', fontsize=9, fontweight='bold')

plt.suptitle('Netflix Data Explorer - Comprehensive Analysis', 
             fontsize=18, fontweight='bold', y=0.995)
plt.tight_layout(rect=[0, 0, 1, 0.99])
plt.savefig('netflix_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved visualization: netflix_analysis.png")

# ============================================================================
# 6. KEY INSIGHTS
# ============================================================================
print("\n6. KEY INSIGHTS & FINDINGS")
print("=" * 80)

insights = []

# Insight 1: Content Type
movies_pct = (df_clean['is_movie'].sum() / len(df_clean)) * 100
insights.append(f"📊 Content Mix: Netflix library is {movies_pct:.1f}% movies and {100-movies_pct:.1f}% TV shows, "
                f"showing a balanced content strategy.")

# Insight 2: Genre Dominance
top_genre = top_genres[0][0]
top_genre_count = top_genres[0][1]
insights.append(f"🎬 Genre Leader: '{top_genre}' dominates with {top_genre_count:,} titles, "
                f"representing {top_genre_count/len(df_clean)*100:.1f}% of all content.")

# Insight 3: Release Trends
recent_years = df_clean[df_clean['release_year'] >= 2010]
old_years = df_clean[df_clean['release_year'] < 2010]
insights.append(f"📈 Content Growth: {len(recent_years):,} titles ({len(recent_years)/len(df_clean)*100:.1f}%) "
                f"were released in 2010 or later, indicating Netflix's focus on modern content.")

# Insight 4: Runtime Patterns
if len(movies_df) > 0:
    avg_runtime = movies_df['runtime_minutes'].mean()
    median_runtime = movies_df['runtime_minutes'].median()
    # Find most common runtime range
    runtime_60_90 = ((movies_df['runtime_minutes'] >= 60) & (movies_df['runtime_minutes'] < 90)).sum()
    runtime_90_120 = ((movies_df['runtime_minutes'] >= 90) & (movies_df['runtime_minutes'] < 120)).sum()
    
    if runtime_90_120 > runtime_60_90:
        insights.append(f"⏱️  Runtime Clustering: Most movies ({runtime_90_120:,} titles) fall in the 90-120 minute range, "
                        f"with an average of {avg_runtime:.0f} minutes - the classic feature film length.")
    else:
        insights.append(f"⏱️  Runtime Clustering: Most movies ({runtime_60_90:,} titles) fall in the 60-90 minute range, "
                        f"with an average of {avg_runtime:.0f} minutes.")

# Insight 5: Netflix Addition Trends
if df_clean['year_added'].notna().sum() > 0:
    recent_additions = df_clean[df_clean['year_added'] >= 2018]
    peak_year = df_clean['year_added'].mode()[0] if df_clean['year_added'].notna().any() else None
    if peak_year:
        peak_count = (df_clean['year_added'] == peak_year).sum()
        insights.append(f"🚀 Growth Peak: Netflix added {peak_count:,} titles in {int(peak_year)}, "
                        f"showing aggressive content expansion during this period.")

# Insight 6: Rating Distribution
top_rating = df_clean['rating'].value_counts().index[0]
top_rating_count = df_clean['rating'].value_counts().iloc[0]
insights.append(f"🎭 Rating Focus: '{top_rating}' is the most common rating with {top_rating_count:,} titles, "
                f"suggesting Netflix targets a {top_rating.lower()}-friendly audience.")

for i, insight in enumerate(insights, 1):
    print(f"\n{i}. {insight}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print(f"\n✓ Processed {len(df_clean):,} titles")
print(f"✓ Generated 9 comprehensive visualizations")
print(f"✓ Identified {len(insights)} key insights")
print(f"\nFiles created:")
print(f"  - netflix_analysis.png (visualization dashboard)")
print(f"\nThis analysis demonstrates:")
print("  • Data cleaning and preprocessing skills")
print("  • Exploratory data analysis techniques")
print("  • Data visualization best practices")
print("  • Storytelling through data insights")

