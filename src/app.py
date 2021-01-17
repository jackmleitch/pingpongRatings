import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import tweepy
import io

import config
from ratingSystem import *
from tweetData import connectTwitter 

st.markdown("<h1 style='text-align: center; color: black;'>Boise State's Official and Definitive Ping Pong Rankings</h1>", unsafe_allow_html=True)


twitter = connectTwitter()
df = twitter.fetchRankings()
df = df.sort_values(by=['rating'], ascending=False, ignore_index=True)
df.index = np.arange(1, len(df) + 1)

st.text("")

with st.beta_container():
    table = st.table(df)
    st.button('Reload rankings')

st.sidebar.subheader('Enter match results')
player1 = st.sidebar.selectbox(
    'Name of player 1: ',
    getPlayerList(df))

player2 = st.sidebar.selectbox(
    'Name of player 2: ',
    getPlayerList(df))

winner = st.sidebar.selectbox(
    'Who won the match?',
    [player1, player2]
)

if st.sidebar.button('Update rankings'):
    df = recordMatch(df, player1, player2, winner)
    toTweet = df.to_csv(sep=' ', index=True, header=True)
    twitter.updateRankings(toTweet)
    st.sidebar.button('Reload rankings!')

with st.beta_expander("Add new player"):
    newPlayer = st.text_input('Add new player name here: ')
    if st.button('Add player'):
        df = addPlayer(df, newPlayer)
        df.to_csv(config.PLAYERS_FILEPATH)

with st.beta_expander("Remove player"):
    removeName = st.selectbox('What player do you want removed?',
                            getPlayerList(df))
    if st.button('Remove player'):
        df = removePlayer(df, removeName)
        df.to_csv(config.PLAYERS_FILEPATH)

with st.beta_expander("Update player rating"):
    player = st.selectbox(
        'Name of player: ',
        getPlayerList(df))
    newRating = st.text_input('Add new player rating here: ')
    if st.button('Change ranking'):
        df = updatePlayerRating(df, player, newRating)
        df.to_csv(config.PLAYERS_FILEPATH)
st.text("")
st.text("")
st.text("")
st.write("App created by [Jack Leitch](https://github.com/jackmleitch)")


col1, col2, col3, col4 = st.beta_columns(4)
with col2:
    image = Image.open('../input/bronco.png')
    st.image(image)

