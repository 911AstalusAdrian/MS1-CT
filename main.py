import pandas as pd
from Dashboard import Dashboard
import tkinter as tk
from DataTable import DataTable


def main():
    df = pd.read_csv('movies.csv')

    root = tk.Tk()
    root.geometry('500x400')

    data_table = DataTable(root, df)
    dashboard = Dashboard(root, df, data_table)
    root.mainloop()


if __name__ == "__main__":
    main()

# if __name__ == '__main__':
#     df = pd.read_csv('movies.csv')
#     print(df.columns)
#
#     # 1. Number of Movies per Genre
#     genre_counts = df['Genre'].value_counts()
#     genre_counts.plot(kind='bar', xlabel='Genre', ylabel='Number of Movies', title='Number of Movies per Genre')
#     plt.show()
#
#
#     # 3. Average Runtime of Movies
#     average_runtime = df['Runtime'].mean()
#     print(f"Average Runtime of Movies: {average_runtime} minutes")
#

#
#     # 6. Average Rotten Tomatoes Score
#     # average_rotten_tomatoes = df['RottenTomatoes'].dropna().apply(lambda x: int(x.replace('%', ''))).mean()
#     # print(f"Average Rotten Tomatoes Score: {average_rotten_tomatoes}%")
#
#     # 7. Correlation between Metascore and IMDB Score
#     metascore_imdb_correlation = df[['Metascore', 'IMDB']].dropna().astype(float).corr().iloc[0, 1]
#     print(f"Correlation between Metascore and IMDB Score: {metascore_imdb_correlation}")
#
#
#     # 9. Top 10 Movies by IMDB Score
#     top_imdb_movies = df[['Title', 'IMDB']].dropna().sort_values(by='IMDB', ascending=False).head(10)
#     print("Top 10 Movies by IMDB Score:")
#     print(top_imdb_movies)

#
#     # 13. Relationship between Rotten Tomatoes Score and Box Office Revenue
#     plt.scatter(df['RottenTomatoes'].dropna().apply(lambda x: int(x.replace('%', ''))), df['BoxOffice'].dropna())
#     plt.xlabel('Rotten Tomatoes Score')
#     plt.ylabel('Box Office Revenue')
#     plt.title('Relationship between Rotten Tomatoes Score and Box Office Revenue')
#     plt.show()
#
#
#     # 15. Distribution of IMDb Scores
#     df['IMDB'] = df['IMDB'].apply(lambda x: float(x) if pd.notna(x) else x)
#     df['IMDB'].plot(kind='hist', bins=20, xlabel='IMDb Score', ylabel='Number of Movies',
#                     title='Distribution of IMDb Scores')
#     plt.show()
