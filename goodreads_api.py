import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ypJOi1wpDOoVCD3UG0Rig", "isbns": "9781632168146"})
print(res.json())