import tkinter as tk
import pandas as pd
from pandastable import Table, TableModel


class DataTable:
    def __init__(self, parent, dataframe):
        self.__parent = parent
        self.__dataframe = dataframe

        self.__main = tk.Toplevel(self.__parent)
        self.__main.geometry('1350x600+300+50')
        self.__main.title('Movies and Series')

        self.__f = tk.Frame(self.__main)
        self.__f.pack(fill=tk.BOTH, expand=1)

        # global table
        self.__table = Table(self.__f, dataframe=self.__dataframe, showtoolbar=False, showstatusbar=False)

    def show_table(self):
        self.__table.show()
        return self.__table

    def filter(self, rating, genre, runtime_low, runtime_high, year_low, year_high):
        conditions = []

        if rating != '(all)':
            conditions.append(self.__dataframe['Rated'] == rating)
        if genre != '(all)':
            conditions.append((self.__dataframe['Genre'].str.contains(genre)))
        if runtime_low is not None and runtime_high is not None:
            conditions.append((self.__dataframe['Runtime'] >= runtime_low) & (self.__dataframe['Runtime'] <= runtime_high))
        if year_low is not None and year_low is not None:
            conditions.append((self.__dataframe['Year'] >= year_low) & (self.__dataframe['Year'] <= year_high))

        if conditions:
            filtered_df = pd.concat(conditions, axis=1).all(axis=1)
            filtered_df = self.__dataframe[filtered_df]
        else:
            filtered_df = self.__dataframe

        self.__table.updateModel(TableModel(filtered_df))
        self.__table.redraw()
