import pandas as pd
import numpy as np
import glob
import re
import json


def loadDataFiles(folder_path: str = "output/") -> pd.DataFrame:
    file_list = glob.glob(folder_path + "/*.csv")

    main_dataframe = pd.DataFrame(pd.read_csv(file_list[0]))
    for i in range(1, len(file_list)):
        data = pd.read_csv(file_list[i])
        df = pd.DataFrame(data)
        main_dataframe = pd.concat([main_dataframe, df], axis=0)
        main_dataframe.reset_index(drop=True, inplace=True)

    return main_dataframe


def reduce_mem_usage(df: pd.DataFrame, verbose=True) -> pd.DataFrame:
    numerics = ["int16", "int32", "int64", "float16", "float32", "float64"]
    start_mem = df.memory_usage(deep=True).sum() / 1024 ** 2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == "int":
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if (
                    c_min > np.finfo(np.float16).min
                    and c_max < np.finfo(np.float16).max
                ):
                    df[col] = df[col].astype(np.float16)
                elif (
                    c_min > np.finfo(np.float32).min
                    and c_max < np.finfo(np.float32).max
                ):
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage(deep=True).sum() / 1024 ** 2
    if verbose:
        print(
            "Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)".format(
                end_mem, 100 * (start_mem - end_mem) / start_mem
            )
        )
    return df


def emoji_free_text(text: str) -> str:
    return re.sub(
        r"[!@#$&|\-\.():,’0-9\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002500-\U00002BEF"
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"
        "\u3030"
        "]+",
        "",
        text,
    )


def addCategories(df: pd.DataFrame) -> pd.DataFrame:
    with open("utils/in_category_ids.json") as f:
        categories = json.load(f)["items"]
    cat_dict = {}
    for cat in categories:
        cat_dict[int(cat["id"])] = cat["snippet"]["title"]
    df["category_name"] = df["categoryId"].map(cat_dict)

    return df


def capitalizedTitle(s: str) -> bool:
    state = True
    for w in s.split():
        if w.isupper():
            state = True
        else:
            state = False
            break
    return state


def cleanTags(tagString: str) -> list:
    if re.search(r"\[\w+\]", tagString):
        return np.NaN

    return tagString.replace("#", "").split("|")


def dataClean_Filling(df: pd.DataFrame) -> pd.DataFrame:
    df["description"] = df["description"].fillna(value="")
    df["channelTitle"] = df["channelTitle"].fillna(value="")
    df["tags"] = df["tags"].fillna(value="")
    df["trending_date"] = pd.to_datetime(df["trending_date"], utc=True, format="%y.%d.%m")
    df["publishedAt"] = pd.to_datetime(df["publishedAt"])
    df["publishedAt"] = df.set_index("publishedAt").tz_convert("Asia/Kolkata").index
    df["cleanedTitle"] = df["title"].apply(emoji_free_text)
    df["cleanedDescription"] = df["description"].apply(emoji_free_text)
    df = addCategories(df)
    df["fullyCapitalizedTitle"] = df["cleanedTitle"].apply(capitalizedTitle)
    df["cleanedTags"] = df["tags"].apply(cleanTags)
    df["title_length"] = df["cleanedTitle"].apply(lambda x: len(x.split()))
    return df


def fetchData() -> pd.DataFrame:
    df = loadDataFiles()
    df_reduced = reduce_mem_usage(df)
    df_cleaned = dataClean_Filling(df_reduced)
    return df_cleaned


def fetchStats(df: pd.DataFrame) -> pd.DataFrame:
    stats = df.describe().reset_index()
    stats = stats[["index", "view_count", "likes", "comment_count"]]
    stats = stats.rename(
        columns={
            "index": "Metric",
            "view_count": "Views",
            "likes": "Likes",
            "comment_count": "Comments",
        }
    )
    stats = stats.round(2)
    return stats
