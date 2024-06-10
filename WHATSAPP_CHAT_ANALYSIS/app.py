import streamlit as st
import Preprocessor,Utility
import matplotlib.pyplot as plt
import seaborn as sns
import pyttsx3
from googletrans import Translator, Translator
from Preprocessor import main
from Preprocessor import analyze_hourly_activity
from Preprocessor import analyze_top_active_days
from Preprocessor import perform_sentiment_analysis

st.sidebar.title("whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    #st.text(data)
    df=Preprocessor.preprocess(data)
    data=Preprocessor.preprocess_data(data)
    st.dataframe(df)
    user_list = df['Usernames'].unique().tolist()

    # List of messages to remove
    msgs_to_remove = [
        "Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.",
        "Bhutto created group EMBEDDED KI CHUSS","Bhutto added Mahagula","Barirah Uni changed the group name from Shik shak shook 💃 to Shik shak shook",
        "Barirah Uni changed the group name from sheikh ki 5 biwiyaan (pehli Mahgul dosri omama) to sheikh ki 4 biwiyaan1 kisi or ki (pehli Mahgul dosri omama)",
        "Bhutto added you","You changed this group's icon","You changed the group name from sheikh ki 5 biwiyaan to sheikh ki 5 biwiyaan (pehli Omama)",
        "You changed the group name from sheikh ki 5 biwiyaan to sheikh ki 5 biwiyaan (pehli Omama)","Mariya changed this group's icon",
        "Mariya changed the group name from EMBEDDED KI CHUSS to ........... KI CHUSS"
        "Mariya changed the group name from 'EMBEDDED KI CHUSS' to '........... KI CHUSS'",
        'Bhutto created group "EMBEDDED KI CHUSS"',
        'Barirah Uni changed the group name from "Shik shak shook 💃" to "Shik shak shook"',
        'Barirah Uni changed the group name from "sheikh ki 5 biwiyaan (pehli Mahgul dosri omama)" to "sheikh ki 4 biwiyaan1 kisi or ki (pehli Mahgul dosri omama)"',
        'Barirah Uni changed the group name from "sheikh ki 5 biwiyaan (pehli Omama)" to "sheikh ki 5 biwiyaan (pehli Mahgul dosri omama)"',
        'Bhutto changed the group name from "Shik shak shok" to "4 biwiyan sheikh ki 1 kisi aur ki"'
        'Bhutto changed the group name from "Shik shak shook" to "sheikh ki 5 biwiyaan"','Bhutto changed the group name from "sheikh ki 4 biwiyaan1 kisi or ki (pehli Mahgul dosri omama)" to "4 biwiyaan sheikh ki, 1 kisi or ki"',
        'You changed the group name from "sheikh ki 5 biwiyaan" to "sheikh ki 5 biwiyaan (pehli Omama)"',
        'Mariya changed the group name from "EMBEDDED KI CHUSS" to "........... KI CHUSS"',
        'Mariya changed the group name from "4 biwiyaan sheikh ki, 1 kisi or ki" to "Shik shak shok"',
        "Mahagula changed this group's icon",'Mahagula changed the group name from "Barirah phupho ban gyi 💃" to "Shik shak shook 💃"',
        'Bhutto changed the group name from "Shik shak shok" to "4 biwiyan sheikh ki 1 kisi aur ki"',
        'Bhutto changed the group name from "Shik shak shook" to "sheikh ki 5 biwiyaan"',
        "Bhutto changed this group's icon",'Mahagula changed the group name from "........... KI CHUSS" to "Barirah phupho ban gyi 💃"',

    ]

    # Remove multiple messages from the list
    user_list = [user for user in user_list if user not in msgs_to_remove]

    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # Stats Area
        num_messages, words, num_media_messages, num_links = Utility.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4= st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)


        # monthly timeline
        st.title("Monthly Timeline")
        timeline = Utility.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['Messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = Utility.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['Only_date'], daily_timeline['Messages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = Utility.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = Utility.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = Utility.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = Utility.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = Utility.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = Utility.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most commmon words')
        st.pyplot(fig)

        # Analyze and display data based on user selection
        top_days = analyze_top_active_days(df.copy(), selected_user)  # Avoid modifying original df

        # Calculate the overall message count for each day
        overall_message_counts = df.groupby(df['Date'].dt.date)['Messages'].count().sort_values(ascending=False)

        # Update title based on selected user
        if selected_user == "Overall":
            title = "Top 5 Most Active Days (Overall)"
        else:
            title = f"Top 5 Most Active Days for {selected_user} in WhatsApp Chat"  # Use f-string for dynamic title

        st.title(title)  # Display title

        # Display title based on user selection
        col1, col2 = st.columns(2)
        if selected_user == "Overall":
            if not overall_message_counts.empty:
                # Display DataFrame in the first column
                with col1:
                    st.dataframe(overall_message_counts.head(5))

                # Visualize the top 5 active days using a bar plot in the second column
                with col2:
                    import matplotlib.pyplot as plt

                    plt.figure(figsize=(10, 6))
                    colors = ['#8B008B', '#FF00FF', '#BA55D3', '#9370DB', '#663399']  # Define colors for each bar
                    overall_message_counts.head(5).plot(kind='bar', color=colors)
                    plt.title(title)
                    plt.xlabel('Date')
                    plt.ylabel('Message Count')
                    st.pyplot(plt)

            else:
                st.write("No messages found for the overall chat.")
        else:
            if top_days is not None:
                # Apply bold styling with increased font size using HTML

                # Create a single column layout with Streamlit
                col1, col2 = st.columns(2)

                # Display DataFrame in the first column
                with col1:
                    st.dataframe(top_days)

                # Visualize the top 5 active days for the selected user using a bar plot in the second column
                with col2:
                    import matplotlib.pyplot as plt

                    plt.figure(figsize=(10, 6))  # Adjust figure size for better alignment
                    colors = ['#8B008B', '#FF00FF', '#BA55D3', '#9370DB', '#663399']  # Define colors for each bar
                    top_days.plot(kind='bar', color=colors)
                    plt.title(title)
                    plt.xlabel('Date')
                    plt.ylabel('Message Count')
                    st.pyplot(plt)

            else:
                st.write(f"No messages found for {selected_user}.")

        # Define colors for each hour
        hourly_colors = {
            0: '#F94144',
            1: '#F3722C',
            2: '#F8961E',
            3: '#FDC500',
            4: '#F9C74F',
            5: '#90BE6D',
            6: '#43AA8B',
            7: '#577590',
            8: '#6D597A',
            9: '#003F88',
            10: '#00509D',
            11: '#FF6361',
            12: '#58508D',
            13: '#BC5090',
            14: '#FFA600',
            15: '#FFD662',
            16: '#A05195',
            17: '#665191',
            18: '#2F4B7C',
            19: '#6C757D',
            20: '#D45087',
            21: '#FF7A5A',
            22: '#FFB07C',
            23: '#FFD271'
        }

        # Analyze and display data based on user selection
        top_hours = analyze_hourly_activity(df.copy(), selected_user)  # Avoid modifying original df

        # Calculate the overall message count for each hour
        overall_hourly_message_counts = df.groupby(df['Date'].dt.hour)['Messages'].count()

        # Update title based on selected user
        if selected_user == "Overall":
            title = "Message Count by Hour (Overall)"
        else:
            title = f"Message Count by Hour for {selected_user}"  # Use f-string for dynamic title

        st.title(title)  # Display title

        # Display title based on user selection
        col1, col2 = st.columns(2)
        if selected_user == "Overall":
            if not overall_hourly_message_counts.empty:
                # Visualize the overall message count by hour using a bar plot in the first column
                with col1:
                    import matplotlib.pyplot as plt

                    plt.figure(figsize=(10, 6))
                    overall_hourly_message_counts.plot(kind='bar', color=[hourly_colors.get(i, '#999999') for i in
                                                                          overall_hourly_message_counts.index])
                    plt.title(title)
                    plt.xlabel('Hour')
                    plt.ylabel('Message Count')
                    plt.xticks(range(24), [str(i) for i in range(24)])  # Display hour labels
                    st.pyplot(plt)

                # Display the DataFrame of overall message count by hour in the second column
                with col2:
                    st.dataframe(overall_hourly_message_counts)
        else:
            if top_hours is not None:
                # Visualize the selected user's message count by hour using a bar plot in the first column
                with col1:
                    import matplotlib.pyplot as plt

                    plt.figure(figsize=(10, 6))
                    top_hours.plot(kind='bar', color=[hourly_colors.get(i, '#999999') for i in top_hours.index])
                    plt.title(title)
                    plt.xlabel('Hour')
                    plt.ylabel('Message Count')
                    plt.xticks(range(24), [str(i) for i in range(24)])  # Display hour labels
                    st.pyplot(plt)

                # Display the DataFrame of selected user's message count by hour in the second column
                with col2:
                    st.dataframe(top_hours)
            else:
                st.write(f"No messages found for {selected_user}.")
        # emoji analysis
        emoji_df = Utility.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)


        # Update title based on selected user
        if selected_user == "Overall":
            title = "Sentiment Analysis (Overall Chat)"
        else:
            title = f"Sentiment Analysis ({selected_user})"  # Use f-string for dynamic title

        st.title(title)  # Display title

        col1, col2 = st.columns(2)
        if selected_user == "Overall":
            # Perform sentiment analysis for all users (overall chat)
            df_sentiment = perform_sentiment_analysis(df.copy())  # Avoid modifying original df
            sentiment_counts = df_sentiment["sentiment_label"].value_counts()

            # Display results for overall chat
            with col1:
                st.write(sentiment_counts)  # Display Series content directly
            with col2:
                if st is not None:  # Optional check for Streamlit availability
                    if sentiment_counts.empty:  # Handle case with no messages
                        st.write("No messages found for sentiment analysis.")
                    else:
                        fig, ax = plt.subplots()
                        ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%")
                        ax.set_title("Sentiment Distribution")  # Add pie chart title
                        st.pyplot(fig)
                else:
                    print("Streamlit not available for visualization. Consider upgrading Streamlit.")

        else:
            # Perform sentiment analysis for selected user
            df_sentiment = perform_sentiment_analysis(df[df['Usernames'] == selected_user])
            sentiment_counts = df_sentiment["sentiment_label"].value_counts()

            # Display results for selected user
            with col1:
                st.write(sentiment_counts)  # Display Series content directly
            with col2:
                if st is not None:  # Optional check for Streamlit availability
                    if sentiment_counts.empty:  # Handle case with no messages
                        st.write("No messages found for sentiment analysis.")
                    else:
                        fig, ax = plt.subplots()
                        ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%")
                        ax.set_title("Sentiment Distribution")  # Add pie chart title
                        st.pyplot(fig)
                else:
                    print("Streamlit not available for visualization. Consider upgrading Streamlit.")

    languages = {
        'af': 'Afrikaans',
        'sq': 'Albanian',
        'zu': 'Zulu',
        'ur': 'Urdu',
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'zh-CN': 'Chinese (Simplified)',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'bn': 'Bengali',
        'vi': 'Vietnamese',
        'tr': 'Turkish',
        'nl': 'Dutch',
        'pl': 'Polish'
    }

    # Display the unique title
    st.title('Streamlit Speaks Your Language: WhatsApp Chat Translator')

    if selected_user == "Overall":
        st.title("Overall Chat")
        st.dataframe(data)
    else:
        st.title(f"{selected_user}'s Messages")
        filtered_data = data[data['Usernames'] == selected_user]
        st.dataframe(filtered_data)

    # Select target language for translation
    language_choice = st.selectbox('Choose the language to translate messages to', list(languages.values()))

    # Select a message to translate
    if selected_user == "Overall":
        message_options = data['Messages'].unique()
    else:
        message_options = filtered_data['Messages'].unique()

    selected_message = st.selectbox('Select a message to translate', message_options)

    # Select voice for audio output
    voice_choice = st.radio('Choose the voice for audio output', ('Female', 'Male'))

    # Button to trigger translation and audio output
    if st.button('Translate Message'):
        target_lang = [key for key, value in languages.items() if value == language_choice][0]
        translator = Translator()
        translated_message = translator.translate(selected_message, dest=target_lang).text
        st.write(f"Translated Message for {selected_user}: {translated_message}")

        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            if voice_choice == 'Female':
                engine.setProperty('voice', voices[1].id)  # Female voice
            else:
                engine.setProperty('voice', voices[0].id)  # Male voice

            engine.save_to_file(translated_message, 'translated_message.mp3')
            engine.runAndWait()  # Wait for the audio to be generated

            audio_file = open("translated_message.mp3", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.write(f"Error generating audio for {languages[target_lang]}: {e}")
            st.write("Falling back to displaying the translated text.")


if __name__ == '__main__':
    main()
