import streamlit as st
import numpy as np
import pandas as pd
import config
from ratingSystem import *

st.markdown("<h1 style='text-align: center; color: black;'>Boise State's Official, and Definitive, Ping Pong Rankings</h1>", unsafe_allow_html=True)

df = pd.read_csv(config.PLAYERS_FILEPATH, index_col=0)

df = df.sort_values(by=['rating'], ascending=False, ignore_index=True)
df.index = np.arange(1, len(df) + 1)

table = st.table(df)

st.subheader('Enter match results')
player1 = st.selectbox(
    'Name of player 1',
    getPlayerList(df))

player2 = st.selectbox(
    'Name of player 2',
    getPlayerList(df))

winner = st.selectbox(
    'Who won the match?',
    [player1, player2]
)

if st.button('Update rankings'):
    df = recordMatch(df, player1, player2, winner)
    df.to_csv(config.PLAYERS_FILEPATH)
