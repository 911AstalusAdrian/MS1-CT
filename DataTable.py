import constants
import requests
import tkinter as tk
import pandas as pd
from pandastable import Table, TableModel


class DataTable:
    def __init__(self, parent, dataframe):
        self.__parent = parent
        self.__dataframe = dataframe
        self.__tempDataframe = dataframe

        self.__main = tk.Toplevel(self.__parent)
        self.__main.geometry('1350x600+300+50')
        self.__main.title('Movies and Series')

        self.__f = tk.Frame(self.__main)
        self.__f.pack(fill=tk.BOTH, expand=1)

        self.__table = Table(self.__f, dataframe=self.__tempDataframe, showtoolbar=False, showstatusbar=False)
        self.__table.unbind("<Double-Button-1>")
        self.__table.bind("<Double-Button-1>", self.getSelectedRowDetails)

    def getSelectedRowDetails(self, event):
        row = self.__table.get_row_clicked(event)
        selected_movie = self.__tempDataframe.iloc[row].values[0]
        response = requests.get(f"{constants.omdb_api}{selected_movie}")
        self.openPopup(response.json())
        # print(response.json())

    def openPopup(self, json_response):
        top = tk.Toplevel(self.__table)
        tk.Label(top, text=f"Movie title: {json_response['Title']}").pack()
        tk.Label(top, text=f"Movie plot: {json_response['Plot']}").pack()
        tk.Label(top, text=f"Director: {json_response['Director']}").pack()
        tk.Label(top, text=f"Actors: {json_response['Actors']}").pack()
        tk.Label(top, text=f"Awards: {json_response['Awards']}").pack()

    def show_table(self):
        self.__table.show()
        return self.__table

    def findMovie(self, to_search):
        self.__table.unbind("<Double-Button-1>")
        filtered_df = self.__dataframe[self.__dataframe['Title'].str.contains(to_search, case=False)]
        self.__tempDataframe = filtered_df
        self.__table.updateModel(TableModel(self.__tempDataframe))
        self.__table.redraw()
        self.__table.bind("<Double-Button-1>", self.getSelectedRowDetails)

    def filter(self, rating, genre, runtime_low, runtime_high, year_low, year_high):
        self.__table.unbind("<Double-Button-1>")
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

        self.__tempDataframe = filtered_df
        self.__table.updateModel(TableModel(self.__tempDataframe))
        self.__table.redraw()
        self.__table.bind("<Double-Button-1>", self.getSelectedRowDetails)
