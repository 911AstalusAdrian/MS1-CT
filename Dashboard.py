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
        self.__closeButton = None
        self.__statisticButton = None

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
        self.__yearLabel.grid(row=3, column=0, padx=5, pady=20)
        self.__yearSlider = RangeSliderH(self.__parent, [self.__yearLeft, self.__yearRight],
                                         padX=17, min_val=self.__yearLeft.get(), max_val=self.__yearRight.get(),
                                         digit_precision='.0f', font_size=8, Height=43, Width=200, bgColor='#f0f1f1')
        self.__yearSlider.grid(row=3, column=1, pady=20)

        # Filter and Close button
        self.__filterButton = tk.Button(self.__parent, text='Filter Data', command=self.filterData)
        self.__filterButton.grid(row=5, column=0)
        self.__statisticButton = tk.Button(self.__parent, text="Show Statistics", command=self.showStatistic)
        self.__statisticButton.grid(row=5, column=1)
        self.__closeButton = tk.Button(self.__parent, text='Close', command=self.__parent.destroy)
        self.__closeButton.grid(row=5, column=2)

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
        # Distribution of Ratings in the DB
        # rated_distribution = self.__dataframe['Rated'].value_counts()
        # rated_distribution.plot(kind='bar', xlabel='Rating', ylabel='Number of Movies', title='Distribution of Ratings')
        # plt.show()

        # Movies and Series per Decade
        # movies_decades = pd.DataFrame(self.__dataframe['Year'])
        # movies_decades['Decade'] = (movies_decades // 10) * 10
        # decades = movies_decades.groupby('Decade').size()
        # decades.plot(kind='bar', color='skyblue', edgecolor='black', xlabel='Decade',
        #              ylabel='Number of Movies and Series',
        #              title='Number of Movies and Series per Decade')
        # plt.show()

        # Box office revenue per Decade
        # revenue_decades = pd.DataFrame(self.__dataframe['BoxOffice'] / 1000000)
        # revenue_decades['Year'] = self.__dataframe['Year']
        # revenue_decades['Decade'] = (revenue_decades['Year'] // 10) * 10
        # rev_per_decade = revenue_decades.groupby('Decade')['BoxOffice'].sum()
        # rev_per_decade.plot(kind='bar', color='orange', edgecolor='black', xlabel='Decade',
        #                     ylabel='Total Box Office Revenue (in million $)',
        #                     title='Total Box Office revenue per Decade')
        # plt.show()

        # Distribution of movie runtimes
        # counts, bin_edges, _ = plt.hist(self.__dataframe['Runtime'], bins=10, color='green', edgecolor='black')
        # plt.xticks(bin_edges)
        # for count, bin_edge in zip(counts, bin_edges):
        #     plt.text(bin_edge, count, str(int(count)), ha='center', va='bottom', fontsize=3, color='black')
        # plt.show()

        # Distribution of genres
        # genres = pd.DataFrame(self.__dataframe['Genre'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Genre'))
        # print(genres)
        # genre_count = genres['Genre'].value_counts()
        # genre_count.plot(kind='bar', color='red', edgecolor='gray')
        # plt.show()

        # Average Metascore per Genre
        # metascore_genres = self.__dataframe[self.__dataframe['Metascore'] != 0][['Metascore', 'Genre']]
        # genres_df = metascore_genres['Genre'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).to_frame('Genre')
        # merged_df = pd.merge(metascore_genres, genres_df, left_index=True, right_index=True)
        # avg_metascore_per_genre = merged_df.groupby('Genre_y')['Metascore'].mean().reset_index()
        # plt.bar(avg_metascore_per_genre['Genre_y'], avg_metascore_per_genre['Metascore'])
        # plt.show()

