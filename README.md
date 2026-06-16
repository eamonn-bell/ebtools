# ebtools

`ebtools` is a Python helper package for electricity market and energy-industry
data analysis workflows.

It provides centralised utility functions for common data preparation tasks such
as datetime parsing, dataframe filtering, settlement period and EFA handling,
array selection, and file export. The package is intended to support other
analysis tools rather than perform one specific end-to-end analysis task itself.

## Installation

Install from PyPI:

```bash
pip install ebtools
```

Then import the package:

```python
import ebtools as ebt
```

## Requirements

`ebtools` requires Python 3.11 or later.

Core dependencies include:

- NumPy
- pandas
- pytz
- pyarrow
- fastparquet
- openpyxl

## Usage Examples

### Parse Datetime Columns

```python
import pandas as pd
import ebtools as ebt

df = pd.DataFrame({"Date": ["2024-03-14", "15/03/2024"]})

result = ebt.check_datetime_formats(
    df,
    colname="Date",
    format_list=["%Y-%m-%d", "%d/%m/%Y"],
)

print(result)
```

### Parse Timezone-Aware Datetime Columns

```python
import pandas as pd
import ebtools as ebt

df = pd.DataFrame({"Date": ["2024-03-15T01:30:00+01:00"]})

result = ebt.check_datetime_formats_tz(
    df,
    colname="Date",
    format_list_tz="%Y-%m-%dT%H:%M:%S%z",
)

print(result)
```

### Filter A Dataframe

```python
import pandas as pd
import ebtools as ebt

df = pd.DataFrame({
    "Fuel": ["Wind", "Gas", "Wind"],
    "Output": [100, 50, 120],
})

wind = ebt.df_filter(df, colname="Fuel", term="Wind")

print(wind)
```

### Force A Value To A List

```python
import ebtools as ebt

value = ebt.force_to_list("Wind")

print(value)
# ['Wind']
```

### Convert A Date To A Datetime Boundary

```python
import ebtools as ebt

start = ebt.convert_date_to_datetime("2024-03-14", position="start")
end = ebt.convert_date_to_datetime("2024-03-14", position="end")

print(start)
print(end)
```

### Convert A Delivery Date And EFA Block To An EFA Datetime

```python
import ebtools as ebt

efa_datetime = ebt.convert_date_to_efa_datetime("2023-03-14", efa=1)

print(efa_datetime)
# 2023-03-13T23:00:00
```

### Save Dataframes To Excel

```python
import pandas as pd
import ebtools as ebt

prices = pd.DataFrame({"Price": [10.5, 11.2]})
volumes = pd.DataFrame({"Volume": [100, 120]})

ebt.save_to_xlsx(
    [prices, volumes],
    location=".",
    file_name="market_data.xlsx",
    sheet_name=["Prices", "Volumes"],
)
```

### Return The Starting Date Of A Week

```python
import pandas as pd
import ebtools as ebt

df = pd.DataFrame({"Date": pd.date_range("2024-01-01", periods=14)})

week_start = ebt.week_starting(
    df,
    week=1,
    year=2024,
    weekday="Mon",
    return_format="%Y-%m-%d",
)

print(week_start)
# 2024-01-01
```

### Keep The Largest Values In Each Array Row

```python
import numpy as np
import ebtools as ebt

arr = np.array([
    [3, 1, 2],
    [9, 4, 8],
])

result = ebt.n_largest_values_per_row(arr, largest=1, replace=0)

print(result)
```

## Development

For local development, install the package in an environment containing the
runtime and development dependencies.

Run the test suite with:

```bash
PYTHONPATH=src python -m pytest
```

## Project Links

Add these links before publishing if available:

- PyPI project page
- Source repository
- Issue tracker
- Documentation site

## License

This project is licensed under the Apache License 2.0. See `LICENSE` for
details.
