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

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Usernames'] == selected_user]

    temp = df[df['Usernames'] != 'group_notification']
    temp = temp[temp['Messages'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['Messages'] = temp['Messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

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















