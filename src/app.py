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

dfColour = df.style.apply(lambda x: ['background: gold' if x.name == 1 else ('background: silver' if x.name == 2 else ('background: saddlebrown' if x.name == 3 else '')) for i in x],  axis=1)

with st.beta_container():
    table = st.table(dfColour)
    st.button('Reload rankings')

st.write("Match results can be added between two ranked players in the sidebar (make sure to click 'Reload rankings' afterwards). You can also add players, remove players and adjust player ratings (admin only).")
st.write("To see a complete history of ranking updates [click here](https://twitter.com/BoisePing/)")


st.header("Leadville House Rules")
st.write('Games will be played to 11 best of 3 or 5 whichever is agreed upon before the game starts')
st.subheader('Service')
st.markdown( '* Serves switch every 3 points, unless it’s game point - then serve goes to whoever is losing and they are allowed unlimited serving errors when they are facing game point.')
st.markdown( '* Serves don’t have to land in a specific quadrant. ')
st.markdown( "* If a serve hits the net it's a “let” which is a redo.")
st.markdown( '* Serves should be thrown at least 6 inches into the air from an open palm. They are then to be struck by the paddle onto your own side, over the net and onto the opponents side.')
st.subheader("Play")
st.markdown( '* You are allowed to play off of any object including, but not limited to, the rafters, bike, chairs. It just can’t hit the ground first.')
st.markdown( '* If you strike the ball with your paddle before it strikes your side of the table the point goes to your opponent. This rule is within reason, if it’s miles from hitting the table and you use your paddle to save it from going under the cars there can be exceptions.')
st.markdown( '* The ball may go around or through the gap in the net.')
st.markdown( '* The ball can play off of the net in normal play. It’s only a redo during service.')
st.markdown( '* The ball hitting the edge of the table counts as in play. It’s ruled out if it clearly hits the side or bottom of the table (if this somehow happens).')
st.markdown( '* You cannot return the ball with anything but your paddle.')
st.markdown( '* If the ball bounces on your side and back to your opponents side without you touching it the point goes to your opponent.')

st.header("How are the rankings calculated?")
st.markdown('* The Elo Rating System (Elo) is a rating system used for rating players in games. Originally developed for chess by Arpad Elo, Elo has been applied to a large array of games.')
st.markdown("* Each player is assigned a number as a rating (base rating is 1000). The system predicts the outcome of a match between two players by using an expected score formula (i.e. a player whose rating is 100 points greater than their opponent's is expected to win 64% of the time).")
st.markdown("* Everytime a game is played, the Elo rating of the participants change depending on the outcome and the expected outcome. The winner takes points from the loser; the amount is determined by the players' scores and ratings.")


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
    df = df.sort_values(by=['rating'], ascending=False, ignore_index=True)
    toTweet = df.to_csv(sep=' ', index=True, header=True)
    twitter.updateRankings(toTweet)
    st.sidebar.button('Reload rankings!')

with st.sidebar.beta_expander("Add new player"):
    newPlayer = st.text_input('Add new player name here: ')
    if st.button('Add player'):
        df = addPlayer(df, newPlayer)
        df = df.sort_values(by=['rating'], ascending=False, ignore_index=True)
        toTweet = df.to_csv(sep=' ', index=True, header=True)
        twitter.updateRankings(toTweet)

with st.sidebar.beta_expander("Remove player"):
    removeName = st.selectbox('What player do you want removed?',
                            getPlayerList(df))
    if st.button('Remove player'):
        df = removePlayer(df, removeName)
        df = df.sort_values(by=['rating'], ascending=False, ignore_index=True)
        toTweet = df.to_csv(sep=' ', index=True, header=True)
        twitter.updateRankings(toTweet)

with st.sidebar.beta_expander("Update player rating"):
    player = st.selectbox(
        'Name of player: ',
        getPlayerList(df))
    newRating = st.text_input('Add new player rating here: ')
    if st.button('Change ranking'):
        df = updatePlayerRating(df, player, newRating)
        df = df.sort_values(by=['rating'], ascending=False, ignore_index=True)
        toTweet = df.to_csv(sep=' ', index=True, header=True)
        twitter.updateRankings(toTweet)

st.text("")
st.text("")
st.text("")
st.write("App created by [Jack Leitch](https://github.com/jackmleitch)")


col1, col2, col3, col4 = st.beta_columns(4)
with col2:
    image = Image.open('./input/bronco.png')
    st.image(image)

