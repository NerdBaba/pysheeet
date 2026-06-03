---
title: Pandas
---

# Pandas

[[toc]]
Pandas is the premier library for data manipulation and analysis in Python. It provides two primary data structures — `Series` (1D labeled arrays) and `DataFrame` (2D tabular data) — that make working with structured data intuitive and efficient. These cheat sheets cover the most common data wrangling patterns.

## Series and DataFrame Creation

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on series and dataframe creation](https://realpython.com/search?q=series+and+dataframe+creation).
:::

Construct data structures from Python objects, NumPy arrays, or external files.

```python
>>> import pandas as pd
>>> import numpy as np

# Series from list
>>> s = pd.Series([1, 3, 5, np.nan, 6, 8])
0    1.0
1    3.0
2    5.0
3    NaN
4    6.0
5    8.0
dtype: float64

# Series with index
>>> s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])

# DataFrame from dict of lists/Series
>>> df = pd.DataFrame({
...     'name': ['Alice', 'Bob', 'Charlie'],
...     'age': [25, 30, 35],
...     'city': ['NYC', 'LA', 'Chicago']
... })

# DataFrame from list of dicts
>>> df = pd.DataFrame([
...     {'name': 'Alice', 'age': 25},
...     {'name': 'Bob', 'age': 30},
... ])

# From NumPy array with column names
>>> df = pd.DataFrame(np.random.randn(3, 4),
...                   columns=['A', 'B', 'C', 'D'])

# Specify index
>>> df = pd.DataFrame(data, index=['row1', 'row2', 'row3'])
```

## Reading Data

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on reading data](https://realpython.com/search?q=reading+data).
:::

Pandas supports many file formats. CSV and Excel are the most common.

```python
# CSV
>>> df = pd.read_csv('data.csv')
>>> df = pd.read_csv('data.csv', sep=';', header=None)
>>> df = pd.read_csv('data.csv', index_col=0, parse_dates=['date'])
>>> df = pd.read_csv('data.csv', usecols=['name', 'age'])  # Only specific columns
>>> df = pd.read_csv('data.csv', nrows=100)                 # First 100 rows

# Excel
>>> df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
>>> df = pd.read_excel('data.xlsx', sheet_name=None)  # All sheets → dict of DataFrames

# Other formats
>>> df = pd.read_json('data.json')
>>> df = pd.read_parquet('data.parquet')
>>> df = pd.read_sql('SELECT * FROM table', connection)
```

## Basic Inspection

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on basic inspection](https://realpython.com/search?q=basic+inspection).
:::

Get a quick understanding of your data's shape, types, and summary statistics.

```python
>>> df.head()            # First 5 rows
>>> df.head(10)          # First 10 rows
>>> df.tail()            # Last 5 rows
>>> df.sample(5)         # Random 5 rows

>>> df.info()            # Column dtypes, non-null counts, memory usage
>>> df.dtypes            # Data types of each column
>>> df.shape             # (rows, columns)
>>> df.columns           # Column labels
>>> df.index             # Row labels

>>> df.describe()        # Summary statistics (numeric columns)
>>> df.describe(include='all')  # Include categorical and object columns

>>> df.nunique()         # Count of unique values per column
>>> df['col'].value_counts()    # Frequency counts
>>> df['col'].unique()          # Unique values as array
```

## Column Selection and Filtering

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on column selection and filtering](https://realpython.com/search?q=column+selection+and+filtering).
:::

Select columns and filter rows using various techniques.

```python
# Column selection
>>> df['name']               # Single column → Series
>>> df[['name', 'age']]      # Multiple columns → DataFrame
>>> df.name                  # Attribute-style access (if no spaces)

# Row filtering
>>> df[df['age'] > 30]                       # Boolean condition
>>> df[(df['age'] > 25) & (df['city'] == 'NYC')]   # AND
>>> df[(df['age'] < 25) | (df['city'] == 'LA')]    # OR
>>> df[df['name'].isin(['Alice', 'Bob'])]           # Is in list
>>> df[df['name'].str.contains('Ali', na=False)]    # String contains

# Assignment
>>> df['age_group'] = df['age'].apply(lambda x: 'young' if x < 30 else 'old')
>>> df.rename(columns={'name': 'full_name'}, inplace=True)
```

## loc and iloc Indexing

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on loc and iloc indexing](https://realpython.com/search?q=loc+and+iloc+indexing).
:::

Label-based (`loc`) and integer position-based (`iloc`) indexing for precise data access.

```python
>>> df = pd.DataFrame({
...     'name': ['Alice', 'Bob', 'Charlie'],
...     'age': [25, 30, 35],
... }, index=['a', 'b', 'c'])

# loc — label-based
>>> df.loc['a']                    # Row with index 'a'
>>> df.loc[['a', 'c']]             # Multiple rows
>>> df.loc['a':'b']                # Slice inclusive of both endpoints
>>> df.loc['a', 'name']            # Single value
>>> df.loc['a':'b', ['name']]      # Row slice, column subset

# iloc — integer-based
>>> df.iloc[0]                     # First row
>>> df.iloc[[0, 2]]                # First and third rows
>>> df.iloc[0:2]                   # First two rows (exclusive slice)
>>> df.iloc[0, 1]                  # Single value at (0, 1)
>>> df.iloc[:, 0:2]                # All rows, first two columns

# Boolean with loc
>>> df.loc[df['age'] > 25, 'name']
```

## Handling Missing Data

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on handling missing data](https://realpython.com/search?q=handling+missing+data).
:::

Detect, drop, or fill missing values (represented as `NaN`).

```python
>>> df = pd.DataFrame({
...     'A': [1, 2, np.nan, 4],
...     'B': [np.nan, 2, 3, 4],
...     'C': [1, np.nan, np.nan, 4]
... })

# Detection
>>> df.isna()              # Boolean DataFrame of missing values
>>> df.isna().sum()        # Count per column
>>> df.notna()             # Inverse of isna()

# Dropping
>>> df.dropna()            # Drop rows with any NaN
>>> df.dropna(how='all')   # Drop rows where ALL values are NaN
>>> df.dropna(thresh=2)    # Keep rows with at least 2 non-NA values
>>> df.dropna(axis=1)      # Drop columns with any NaN
>>> df.dropna(subset=['A', 'B'])  # Drop if NaN in specific columns

# Filling
>>> df.fillna(0)                      # Fill with constant
>>> df.fillna({'A': 0, 'B': 1})       # Per-column fill values
>>> df.fillna(method='ffill')         # Forward fill
>>> df.fillna(method='bfill')         # Backward fill
>>> df['A'].interpolate()             # Linear interpolation

# In-place operation
>>> df.fillna(0, inplace=True)
```

::: warning
`inplace=True` modifies the DataFrame directly and is not recommended in chained operations. Prefer `df = df.fillna(0)` for clarity.
:::

## GroupBy Operations

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on groupby operations](https://realpython.com/search?q=groupby+operations).
:::

Split-apply-combine for aggregating data by groups.

```python
>>> df = pd.DataFrame({
...     'category': ['A', 'A', 'B', 'B', 'A'],
...     'value': [10, 20, 30, 40, 50],
...     'qty': [1, 2, 3, 4, 5]
... })

>>> grouped = df.groupby('category')

# Aggregation
>>> grouped['value'].sum()             # Sum per group
>>> grouped['value'].agg(['sum', 'mean', 'std'])  # Multiple stats
>>> grouped.agg({'value': 'sum', 'qty': 'mean'})  # Per-column agg

# Named aggregation (Pandas 0.25+)
>>> grouped.agg(
...     total_value=('value', 'sum'),
...     avg_qty=('qty', 'mean')
... )

# Transform — same shape as original
>>> df['pct'] = df.groupby('category')['value'].transform(
...     lambda x: x / x.sum()
... )

# Apply — flexible but slower
>>> df.groupby('category')['value'].apply(lambda x: x.sort_values())

# Multiple group keys
>>> df.groupby(['category', 'region']).sum()

# Filter groups
>>> df.groupby('category').filter(lambda x: x['value'].sum() > 50)
```

## Merge, Join, and Concat

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on merge join and concat](https://realpython.com/search?q=merge+join+and+concat).
:::

Combine multiple DataFrames using SQL-like joins or stacking operations.

```python
>>> left = pd.DataFrame({'key': ['a', 'b', 'c'], 'val1': [1, 2, 3]})
>>> right = pd.DataFrame({'key': ['b', 'c', 'd'], 'val2': [4, 5, 6]})

# Merge (SQL-style joins)
>>> pd.merge(left, right, on='key')              # Inner join
>>> pd.merge(left, right, on='key', how='left')  # Left join
>>> pd.merge(left, right, on='key', how='right') # Right join
>>> pd.merge(left, right, on='key', how='outer') # Outer join

# Merge on index
>>> pd.merge(left, right, left_index=True, right_index=True)

# Merge with different key names
>>> pd.merge(left, right, left_on='key', right_on='key2')

# Concat — stack rows or columns
>>> pd.concat([df1, df2])                # Stack vertically (rows)
>>> pd.concat([df1, df2], axis=1)        # Stack horizontally (columns)
>>> pd.concat([df1, df2], ignore_index=True)  # Reset index

# Join — merge on index (wrapper around merge)
>>> left.join(right, how='inner', lsuffix='_left', rsuffix='_right')
```

## Pivot Tables and Melt

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on pivot tables and melt](https://realpython.com/search?q=pivot+tables+and+melt).
:::

Reshape data between wide and long formats.

```python
>>> df = pd.DataFrame({
...     'date': ['2023-01', '2023-01', '2023-02', '2023-02'],
...     'product': ['A', 'B', 'A', 'B'],
...     'sales': [100, 200, 150, 250]
... })

# Pivot — reshape from long to wide
>>> df.pivot(index='date', columns='product', values='sales')
product     A    B
date
2023-01   100  200
2023-02   150  250

# pivot_table — handles duplicates with aggregation
>>> df = pd.concat([df, pd.DataFrame([['2023-01', 'A', 50]], columns=df.columns)])
>>> df.pivot_table(index='date', columns='product', values='sales', aggfunc='sum')

# Melt — reshape from wide to long
>>> wide = pd.DataFrame({
...     'city': ['NYC', 'LA'],
...     '2022': [100, 200],
...     '2023': [150, 250],
... })
>>> pd.melt(wide, id_vars=['city'], var_name='year', value_name='sales')
   city  year  sales
0   NYC  2022    100
1    LA  2022    200
2   NYC  2023    150
3    LA  2023    250
```

## Datetime Handling

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on datetime handling](https://realpython.com/search?q=datetime+handling).
:::

Work with dates and times using `pd.to_datetime` and the `.dt` accessor.

```python
>>> df = pd.DataFrame({'date': ['2023-01-01', '2023-02-15', '2023-03-20']})

# Parse strings to datetime
>>> df['date'] = pd.to_datetime(df['date'])
>>> df['date'].dtype
datetime64[ns]

# dt accessor — extract components
>>> df['year'] = df['date'].dt.year
>>> df['month'] = df['date'].dt.month
>>> df['day'] = df['date'].dt.day
>>> df['dayofweek'] = df['date'].dt.dayofweek    # Monday=0, Sunday=6
>>> df['quarter'] = df['date'].dt.quarter
>>> df['is_weekend'] = df['date'].dt.dayofweek >= 5

# Date ranges
>>> dates = pd.date_range('2023-01-01', periods=5, freq='D')
>>> dates = pd.date_range('2023-01-01', '2023-12-31', freq='ME')  # Month ends

# Time arithmetic
>>> df['date'] + pd.Timedelta(days=7)
>>> (df['date'].max() - df['date'].min()).days

# Set datetime index and resample
>>> df = df.set_index('date')
>>> df.resample('ME').sum()   # Resample to month end
>>> df.resample('W').mean()   # Resample to weekly
```

## Apply, Map, and Applymap

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on apply map and applymap](https://realpython.com/search?q=apply+map+and+applymap).
:::

Apply functions element-wise, column-wise, or row-wise.

```python
>>> df = pd.DataFrame({
...     'name': ['alice', 'bob', 'charlie'],
...     'age': [25, 30, 35],
...     'salary': [50000, 60000, 70000]
... })

# map — Series only, element-wise substitution
>>> df['name'] = df['name'].str.capitalize()
>>> df['name'].map({'Alice': 'A', 'Bob': 'B', 'Charlie': 'C'})

# apply — works on Series or DataFrame
>>> df['age'].apply(lambda x: 'young' if x < 30 else 'senior')
>>> df[['age', 'salary']].apply(np.mean)      # Column-wise
>>> df[['age', 'salary']].apply(np.sum, axis=1)  # Row-wise

# applymap — element-wise on DataFrame (deprecated in Pandas 2.1+)
>>> df[['age', 'salary']].applymap(lambda x: f"${x}")

# Preferred replacement for applymap — map on DataFrame
>>> df[['age', 'salary']].map(lambda x: f"${x}")
```

## Plotting with Matplotlib

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on plotting with matplotlib](https://realpython.com/search?q=plotting+with+matplotlib).
:::

Pandas integrates with Matplotlib for quick visualizations directly from DataFrames.

```python
>>> import matplotlib.pyplot as plt

# line plot (default for Series)
>>> df['age'].plot()
>>> df.plot(x='name', y='age', kind='line')

# bar plot
>>> df.groupby('name')['age'].sum().plot(kind='bar')
>>> df.groupby('name')['age'].sum().plot.bar()

# histogram
>>> df['age'].plot(kind='hist', bins=10)
>>> df['age'].hist(bins=10)

# scatter
>>> df.plot(kind='scatter', x='age', y='salary')

# box plot
>>> df[['age', 'salary']].plot(kind='box')

# Customization
>>> df.plot(figsize=(10, 6), title='My Plot', grid=True, legend=True)
>>> plt.xlabel('X Label')
>>> plt.ylabel('Y Label')
>>> plt.show()

# Subplots
>>> df[['age', 'salary']].plot(subplots=True, layout=(1, 2), figsize=(12, 4))
```

::: warning
Call `plt.show()` explicitly when not in a Jupyter notebook. Use `%matplotlib inline` in Jupyter for inline display.
:::

## References

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pandas API Reference](https://pandas.pydata.org/docs/reference/index.html)
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Pandas Visualization](https://pandas.pydata.org/docs/user_guide/visualization.html)
