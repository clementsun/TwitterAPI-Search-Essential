# TwitterAPI-Search-Essential
 A script for user with ESSENTIAL access level to extract tweets in the past 7 days using Twitter API v2 and save them into an JSON file (.json).



### Reading the JSON file into dataframe

```python
with open(<<YOUR_JSON_FILE_PATH_HERE>>) as f:
        data = json.load(f)
        df = pd.DataFrame.from_dict(data, orient='columns')
```