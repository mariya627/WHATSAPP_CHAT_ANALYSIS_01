from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter
extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Usernames'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['Messages']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['Messages'].str.contains('<Media omitted>')].shape[0]

    # fetch number of links shared
    links = []
    for message in df['Messages']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['Usernames'].value_counts().head()
    df = round((df['Usernames'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

stop_words = [
    "the", "a", "to", "and", "is", "in", "it", "you", "that", "this",
    "was", "for", "on", "with", "have", "from", "be", "by", "not", "are",
    "at", "as", "your", "all", "have", "new", "more", "an", "was", "we",
    "will", "home", "can", "up", "what", "time", "there", "day", "if",
    "they", "we", "out", "some", "when", "who", "get", "one", "her", "him",
    "has", "had", "she", "which", "do", "their", "said", "or", "has", "my",
    "me", "him", "him", "his", "them", "then", "so", "would", "about",
    "get", "just", "how", "been", "other", "some", "its", "like", "only",
    "other", "our", "two", "make", "them", "see", "use", "into", "very",
    "after", "back", "also", "good", "well", "way", "even", "any", "these",
    "most", "many", "some", "such", "were", "here", "him", "because",
    "before", "being", "below", "between", "both", "but", "by", "can",
    "did", "does", "doing", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "he'd", "he'll",
    "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
    "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in",
    "into", "is", "it", "it's", "its", "itself", "let's", "me", "more",
    "most", "my", "myself", "nor", "of", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
    "same", "she", "she'd", "she'll", "she's", "should", "so", "some",
    "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd",
    "they'll", "they're", "they've", "this", "those", "through", "to",
    "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll",
    "we're", "we've", "were", "what", "what's", "when", "when's", "where",
    "where's", "which", "while", "who", "who's", "whom", "why", "why's",
    "with", "would", "you", "you'd", "you'll", "you're", "you've", "your",
    "yours", "yourself", "yourselves"
]

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Usernames'] == selected_user]

    temp = df[df['Usernames'] != 'group_notification']
    temp = temp[temp['Messages'] != '<Media omitted>\n']

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['Messages'] = temp['Messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Messages'].str.cat(sep=" "))
    return df_wc

def remove_stop_words(message):
    y = []
    for word in message.lower().split():
        if word not in stop_words:
            y.append(word)
    return " ".join(y)

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Usernames'] == selected_user]

    temp = df[df['Usernames'] != 'group_notification']
    temp = temp[temp['Messages'] != '<Media omitted>\n']

    words = []

    for message in temp['Messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Usernames'] == selected_user]

    emojis = []
    for message in df['Messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df



def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Usernames'] == selected_user]

    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['Messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Usernames'] == selected_user]

    daily_timeline = df.groupby('Only_date').count()['Messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Usernames'] == selected_user]

    return df['Day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Usernames'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Usernames'] == selected_user]

    user_heatmap = df.pivot_table(index='Day_name', columns='period', values='Messages', aggfunc='count').fillna(0)

    return user_heatmap















