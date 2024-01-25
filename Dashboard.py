import constants
import tkinter as tk
import matplotlib.pyplot as plt
from RangeSlider.RangeSlider import RangeSliderH
import pandas as pd


class Dashboard:
    def __init__(self, parent, dataframe, table):
        self.__parent = parent
        self.__dataframe = dataframe
        self.__table = table

        self.__ratingLabel = None
        self.__rating_selection = None
        self.__rating = None

        self.__genreLabel = None
        self.__genre = None
        self.__genre_selection = None

        self.__runtimeLeft = tk.DoubleVar(value=self.__dataframe['Runtime'].min())
        self.__runtimeRight = tk.DoubleVar(value=self.__dataframe['Runtime'].max())
        self.__runtimeSlider = None
        self.__runtimeLabel = None

        self.__yearLeft = tk.DoubleVar(value=self.__dataframe['Year'].min())
        self.__yearRight = tk.DoubleVar(value=self.__dataframe['Year'].max())
        self.__yearSlider = None
        self.__yearLabel = None

        self.__filterButton = None
        self.__statisticButton = None

        self.__searchBox = None
        self.__searchButton = None

        self.setDashboard()
        self.__table.show_table()

    def setDashboard(self):
        # Rating label and dropdown
        self.__ratingLabel = tk.Label(self.__parent, text='Choose a Rating')
        self.__ratingLabel.grid(row=0, column=0, padx=5)
        self.__rating = tk.StringVar(self.__parent)
        self.__rating.set('(all)')
        self.__rating_selection = tk.OptionMenu(self.__parent, self.__rating, *constants.ratings)
        self.__rating_selection.grid(row=0, column=1)

        # Genre label and dropdown
        self.__genreLabel = tk.Label(self.__parent, text='Choose a Genre')
        self.__genreLabel.grid(row=1, column=0, padx=5)
        self.__genre = tk.StringVar(self.__parent)
        self.__genre.set('(all)')
        self.__genre_selection = tk.OptionMenu(self.__parent, self.__genre, *constants.genres)
        self.__genre_selection.grid(row=1, column=1)

        # Runtime label and slider
        self.__runtimeLabel = tk.Label(self.__parent, text='\nSelect a Runtime range')
        self.__runtimeLabel.grid(row=2, column=0, padx=5)
        self.__runtimeSlider = RangeSliderH(self.__parent, [self.__runtimeLeft, self.__runtimeRight],
                                            padX=15, min_val=self.__runtimeLeft.get(),
                                            max_val=self.__runtimeRight.get(),
                                            digit_precision='.0f', font_size=8, Height=43, Width=200, bgColor='#f0f1f1')
        self.__runtimeSlider.grid(row=2, column=1)

        # Year label and slider
        self.__yearLabel = tk.Label(self.__parent, text='\nSelect a Year range')
        self.__yearLabel.grid(row=3, column=0, padx=5, pady=5)
        self.__yearSlider = RangeSliderH(self.__parent, [self.__yearLeft, self.__yearRight],
                                         padX=17, min_val=self.__yearLeft.get(), max_val=self.__yearRight.get(),
                                         digit_precision='.0f', font_size=8, Height=43, Width=200, bgColor='#f0f1f1')
        self.__yearSlider.grid(row=3, column=1)

        # Filter and Close button
        self.__filterButton = tk.Button(self.__parent, text='Filter Data', command=self.filterData)
        self.__filterButton.grid(row=5, column=0)
        self.__statisticButton = tk.Button(self.__parent, text="Show Statistics", command=self.showStatistic)
        self.__statisticButton.grid(row=5, column=1)

        self.__searchBox = tk.Entry(self.__parent)
        self.__searchBox.grid(row=6, column=0, pady=10)
        self.__searchButton = tk.Button(self.__parent, text='Search', command=self.searchMovie)
        self.__searchButton.grid(row=6, column=1, pady=10)

    def searchMovie(self):
        to_search = self.__searchBox.get()
        print(to_search)
        self.__table.findMovie(to_search)

    def filterData(self):
        rating = self.__rating.get()
        genre = self.__genre.get()
        runtime_values = self.__runtimeSlider.getValues()
        runtime_low = round(runtime_values[0])
        runtime_high = round(runtime_values[1])
        year_values = self.__yearSlider.getValues()
        year_low = round(year_values[0])
        year_high = round(year_values[1])
        self.__table.filter(rating, genre, runtime_low, runtime_high, year_low, year_high)

    def showStatistic(self):
        # 1. Distribution of Ratings in the DB
        rated_distribution = self.__dataframe['Rated'].value_counts()
        rated_distribution.plot(kind='bar', xlabel='Rating', ylabel='Number of Movies', title='Distribution of Ratings')
        plt.show()

        # 2. Movies and Series per Decade
        movies_decades = pd.DataFrame(self.__dataframe['Year'])
        movies_decades['Decade'] = (movies_decades // 10) * 10
        decades = movies_decades.groupby('Decade').size()
        decades.plot(kind='bar', color='skyblue', edgecolor='black', xlabel='Decade',
                     ylabel='Number of Movies and Series',
                     title='Number of Movies and Series per Decade')
        plt.show()

        # 3. Box office revenue per Decade
        revenue_decades = pd.DataFrame(self.__dataframe['BoxOffice'] / 1000000)
        revenue_decades['Year'] = self.__dataframe['Year']
        revenue_decades['Decade'] = (revenue_decades['Year'] // 10) * 10
        rev_per_decade = revenue_decades.groupby('Decade')['BoxOffice'].sum()
        rev_per_decade.plot(kind='bar', color='orange', edgecolor='black', xlabel='Decade',
                            ylabel='Total Box Office Revenue (in million $)',
                            title='Total Box Office revenue per Decade')
        plt.show()

        # 4. Distribution of movie runtimes
        counts, bin_edges, _ = plt.hist(self.__dataframe['Runtime'], bins=10, color='green', edgecolor='black',
                                        xlabel='Number of Movies', ylabel='Movie runtime',
                                        title='Distribution of Movie runtimes')
        plt.xticks(bin_edges)
        for count, bin_edge in zip(counts, bin_edges):
            plt.text(bin_edge, count, str(int(count)), ha='center', va='bottom', fontsize=3, color='black')
        plt.show()

        # 5. Distribution of genres
        genres = pd.DataFrame(
            self.__dataframe['Genre'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame(
                'Genre'))
        print(genres)
        genre_count = genres['Genre'].value_counts()
        genre_count.plot(kind='bar', color='red', edgecolor='gray', xlabel='Genres', ylabel='Number of Movies',
                         title='Distribution of Genres')
        plt.xticks(rotation=30, ha='right')
        plt.show()

        # 6. Histograms for each rating type
        ratings = self.__dataframe[['RottenTomatoes', 'Metascore', 'IMDB']]
        ratings.hist(bins=10, figsize=(12, 6), layout=(1, 3), alpha=0.7, color='yellowgreen', edgecolor='gray')
        plt.suptitle('Distribution of Ratings', fontsize=16)
        plt.show()

        ratings['IMDB'] = ratings['IMDB'] * 10
        ratings.boxplot(figsize=(10, 6))
        plt.title('Boxplot of Ratings', fontsize=16)
        plt.show()

        # 7. Average Ratings per Genre
        ratings_genre = self.__dataframe[['Metascore', 'RottenTomatoes', 'IMDB', 'Genre']]
        ratings_genre['IMDB'] = ratings_genre['IMDB'] * 10
        genres_df = ratings_genre['Genre'].str.split(', ', expand=True).stack().reset_index(level=1,
                                                                                            drop=True).to_frame('Genre')
        average_ratings = pd.merge(ratings_genre, genres_df, left_index=True, right_index=True)
        average_ratings = average_ratings.groupby('Genre_y')[
            ['Metascore', 'RottenTomatoes', 'IMDB']].mean().reset_index()

        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.2
        bar_positions = range(len(average_ratings))
        ax.bar(bar_positions, average_ratings['IMDB'], width=bar_width, label='IMDB', color='yellow', align='center')
        ax.bar([pos + bar_width for pos in bar_positions], average_ratings['RottenTomatoes'], width=bar_width,
               label='RottenTomatoes', color='tomato', align='center')
        ax.bar([pos + 2 * bar_width for pos in bar_positions], average_ratings['Metascore'], width=bar_width,
               label='Metascore', color='dimgray', align='center')
        ax.set_xticks([pos + bar_width for pos in bar_positions])
        ax.set_xticklabels(average_ratings['Genre_y'])
        plt.xticks(rotation=30, ha='right')
        ax.set_title('Average Ratings by Genre')
        ax.set_xlabel('Genre')
        ax.set_ylabel('Average Rating')
        ax.legend()
        plt.show()

        # 8. Scatter Plot of Metascore Ratings vs. Box Office Revenue
        data = self.__dataframe[self.__dataframe['BoxOffice'] > 100000000][['Metascore', 'BoxOffice']]
        data['BoxOffice'] = data['BoxOffice'] / 10000000
        print(data['BoxOffice'])
        plt.figure(figsize=(10, 6))
        plt.scatter(x='Metascore', y='BoxOffice', data=data, alpha=0.8, edgecolors='w')
        plt.title('Scatter Plot of Metascore Ratings vs. Box Office Revenue')
        plt.xlabel('Metascore Ratings')
        plt.ylabel('Box Office Revenue (in 10M$)')
        plt.show()

        # 9. Correlation matrix Metascore vs. RottenTomatoes vs. IMDB
        correlation_matrix = ratings.corr()
        plt.figure(figsize=(8, 6))
        plt.imshow(correlation_matrix, cmap='coolwarm', vmin=0, vmax=1)
        plt.colorbar()
        plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
        plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
        plt.title('Correlation Heatmap: RottenTomatoes vs. Metascore vs. IMDB')
        plt.show()
