# Structure du projet : data-analyzer

# 1. data_loader.py
# src/data_loader.py
import pandas as pd
from datetime import datetime

class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.filepath)
        self._validate()
        self._clean()
        return self.df

    def _validate(self):
        required_columns = {'date', 'category', 'amount', 'customer_id'}
        if not required_columns.issubset(self.df.columns):
            raise ValueError(f"Missing columns: {required_columns - set(self.df.columns)}")

    def _clean(self):
        self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        self.df.dropna(inplace=True)
        self.df['amount'] = self.df['amount'].astype(float)

    def filter_by_date_range(self, start_date, end_date):
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        return self.df[(self.df['date'] >= start) & (self.df['date'] <= end)]

    def filter_by_category(self, categories):
        return self.df[self.df['category'].isin(categories)]


# 2. analyzer.py
# src/analyzer.py
import pandas as pd

class DataAnalyzer:
    def __init__(self, dataframe):
        self.df = dataframe

    def summary_statistics(self):
        return self.df.groupby('category')['amount'].agg(['mean', 'median', 'std'])

    def time_series_analysis(self):
        return self.df.groupby('date')['amount'].sum()

    def spending_distribution(self):
        return self.df['amount'].describe()

    def top_spending_categories(self, n=3):
        return self.df.groupby('category')['amount'].sum().sort_values(ascending=False).head(n)

    def customer_segmentation(self):
        return self.df.groupby('customer_id')['amount'].sum().sort_values(ascending=False)


# 3. visualizer.py
# src/visualizer.py
import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualizer:
    def __init__(self):
        sns.set(style="whitegrid")

    def bar_chart(self, data, title="Spending by Category"):
        fig, ax = plt.subplots()
        data.plot(kind='bar', ax=ax)
        ax.set_title(title)
        ax.set_ylabel("Amount")
        return fig

    def line_chart(self, data, title="Spending Over Time"):
        fig, ax = plt.subplots()
        data.plot(ax=ax)
        ax.set_title(title)
        ax.set_ylabel("Amount")
        return fig

    def pie_chart(self, data, title="Spending Distribution"):
        fig, ax = plt.subplots()
        data.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title(title)
        ax.set_ylabel("")
        return fig

    def heatmap(self, data, title="Correlation Heatmap"):
        fig, ax = plt.subplots()
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title(title)
        return fig


# 4. main.py
# main.py
import argparse
from src.data_loader import DataLoader
from src.analyzer import DataAnalyzer
from src.visualizer import DataVisualizer

import os

def main():
    parser = argparse.ArgumentParser(description="CSV Data Analyzer")
    parser.add_argument('csv_path', help='Path to the CSV file')
    parser.add_argument('--analysis', choices=['summary', 'time', 'distribution', 'top', 'segment'], required=True)
    parser.add_argument('--plot', choices=['bar', 'line', 'pie', 'heatmap'])
    parser.add_argument('--output', help='Directory to save results')
    args = parser.parse_args()

    dl = DataLoader(args.csv_path)
    df = dl.load_data()

    da = DataAnalyzer(df)
    vis = DataVisualizer()

    analysis_result = None
    if args.analysis == 'summary':
        analysis_result = da.summary_statistics()
    elif args.analysis == 'time':
        analysis_result = da.time_series_analysis()
    elif args.analysis == 'distribution':
        analysis_result = da.spending_distribution()
    elif args.analysis == 'top':
        analysis_result = da.top_spending_categories()
    elif args.analysis == 'segment':
        analysis_result = da.customer_segmentation()

    print(analysis_result)

    if args.plot:
        if args.plot == 'bar':
            fig = vis.bar_chart(analysis_result)
        elif args.plot == 'line':
            fig = vis.line_chart(analysis_result)
        elif args.plot == 'pie':
            fig = vis.pie_chart(analysis_result)
        elif args.plot == 'heatmap':
            fig = vis.heatmap(df)

        if args.output:
            os.makedirs(args.output, exist_ok=True)
            fig_path = os.path.join(args.output, f"{args.analysis}_{args.plot}.png")
            fig.savefig(fig_path)

if __name__ == '__main__':
    main()


# 5. Tests - Exemple pour DataLoader
# tests/test_data_loader.py
import pytest
from src.data_loader import DataLoader
import pandas as pd

def test_load_data():
    dl = DataLoader("data/sample_data.csv")
    df = dl.load_data()
    assert not df.empty
    assert set(['date', 'category', 'amount', 'customer_id']).issubset(df.columns)

def test_filter_by_date():
    dl = DataLoader("data/sample_data.csv")
    df = dl.load_data()
    filtered = dl.filter_by_date_range("2023-01-01", "2023-01-31")
    assert not filtered.empty

def test_filter_by_category():
    dl = DataLoader("data/sample_data.csv")
    df = dl.load_data()
    filtered = dl.filter_by_category(['groceries'])
    assert (filtered['category'] == 'groceries').all()

# Tests similaires peuvent être ajoutés pour analyzer.py et visualizer.py
