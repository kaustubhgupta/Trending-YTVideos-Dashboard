import requests, sys, time, os


def clean_feature(feature):
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'


def api_request(page_token):
    request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,snippet,statistics{page_token}chart=mostPopular&regionCode=IN&maxResults=50&key={api_key}"
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Probably high number of requests!")
        sys.exit()
    return request.json()


def get_tags(tags_list):
    return clean_feature("|".join(tags_list))

def get_videos(items):
    details = []
    for video in items:

        if "statistics" not in video:
            continue

        video_id = clean_feature(video['id'])

        snippet = video.get('snippet')
        statistics = video.get('statistics')

        features = [clean_feature(snippet.get(feature, "")) for feature in snippet_features]
        description = snippet.get("description", "")
        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        trending_date = time.strftime("%y.%d.%m")
        tags = get_tags(snippet.get("tags", ["[none]"]))
        view_count = statistics.get("viewCount", 0)
        like_count = statistics.get("likeCount", 0)
        comment_count = statistics.get('commentCount', 0)

        expanded_details = [video_id] + features + [clean_feature(x) for x in [trending_date, tags, view_count, like_count,
                                                                       comment_count, thumbnail_link, description]]
        details.append(",".join(expanded_details))

    return details


def get_pages(next_page_token="&"):
    data = []
    while next_page_token is not None:
        video_data_page = api_request(next_page_token)
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token
        items = video_data_page.get('items', [])
        data += get_videos(items)

    return data


def write_to_file(country_data):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(f"{output_dir}/{time.strftime('%y.%d.%m')}_IN_videos.csv", "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write(f"{row}\n")


def get_data():
    data = [",".join(header)] + get_pages()
    write_to_file(data)


if __name__ == "__main__":
    snippet_features = ["title",
                    "publishedAt",
                    "channelId",
                    "channelTitle",
                    "categoryId"]

    unsafe_characters = ['\n', '"']

    header = ["video_id"] + snippet_features + ["trending_date", "tags", "view_count", "likes",
                                                "comment_count", "thumbnail_link", "description"]
    api_key = sys.argv[1]
    output_dir = sys.argv[2] + "/output/"

    get_data()