import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("mai_news.csv")

df["date"] = pd.to_datetime(df["date"])

df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year


sns.countplot(data=df, x="month", hue="month", palette="rocket_r")

plt.legend().remove()
plt.xlabel("Month")
plt.ylabel("News")
plt.title("News by months")
plt.xticks(rotation=30)
plt.show()