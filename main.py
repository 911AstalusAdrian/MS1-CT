import pandas as pd
import tkinter as tk
from Dashboard import Dashboard
from DataTable import DataTable


def main():
    df = pd.read_csv('movies.csv')

    print(f"-------RUNTIME-------\n{df['Runtime'].describe()}")
    print(f"\n\n---RottenTomatoes---\n{df['RottenTomatoes'].describe()}")
    print(f"\n\n------Metascore------\n{df['Metascore'].describe()}")
    print(f"\n\n--------IMDB--------\n{df['IMDB'].describe()}")
    print(f"\n\n------BoxOffice------\n{df['BoxOffice'].describe()}")

    root = tk.Tk()
    root.geometry('350x250')

    data_table = DataTable(root, df)
    dashboard = Dashboard(root, df, data_table)
    root.mainloop()


if __name__ == "__main__":
    main()
