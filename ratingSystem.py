class Player:
    """
    Represent a player in the Elo Rating System
    """

    def __init__(self, name, rating):
        """
        :param name: name of player
        :param rating: rating of player
        """
        self.name = name
        self.rating = rating

    def compareRating(self, opponent):
        """
        Compares the two ratings of the this player and the opponent.
        :param opponent: the player to compare against.
        :return: The expected score between the two players.
        """
        return (1+10**((opponent.rating - self.rating)/400.0)) ** -1


class pingPong:
    """
    This class implements the Elo Rating System to rank 
    ping pong players
    """
    def __init__(self, baseRating=1000):
        """
        :param baseRating: The rating a new player will have
        """
        self.baseRating = baseRating
        self.players = []

    def getPlayerList(self):
        """
        :return: the list of all players in the system 
        """
        return self.players

    def getPlayer(self, name):
        """
        :param name: name of the player to return.
        :return: the player with the given name.
        """
        for player in self.players:
            if player.name == name:
                return player
        return None

    def contains(self, name):
        """
        :param name: name to check for
        :return: True if system contains player, otherwise False
        """
        for player in self.players:
            if player.name == name:
                return True
        return False

    def addPlayer(self, name, rating=None):
        """
        Adds a new player to the system
        :param name: The name to identify a specific player
        :param rating: The player's rating
        """
        if rating == None:
            rating = self.baseRating

        self.players.append(Player(name=name, rating=rating))

    def removePlayer(self, name):
        """
        Removes player from the system 
        :param name: The name to identify the specific player
        """
        self.getPlayerList().remove(self.getPlayer(name))

    def recordMatch(self, name1, name2, winner=None):
        """
        This is called to record the results of a match 
        :param name1/name2: - name of the first/second player
        """
        player1 = self.getPlayer(name1)
        player2 = self.getPlayer(name2)

        expected1 = player1.compareRating(player2)
        expected2 = player2.compareRating(player1)
        
        k = len(self.getPlayerList()) * 42

        rating1 = player1.rating
        rating2 = player2.rating

        if winner == name1:
            score1 = 1.0
            score2 = 0.0
        elif winner == name2:
            score1 = 0.0
            score2 = 1.0
        else:
            raise InputError('One of the names must be the winner')

        newRating1 = rating1 + k * (score1 - expected1)
        newRating2 = rating2 + k * (score2 - expected2)

        if newRating1 < 0:
            newRating1 = 0
            newRating2 = rating2 - rating1

        elif newRating2 < 0:
            newRating2 = 0
            newRating1 = rating1 - rating2

        player1.rating = newRating1
        player2.rating = newRating2

    def getPlayerRating(self, name):
            """
            Returns the rating of the player with the given name.
            :param name: name of the player
            :return: the rating of the player with the given name
            """
            player = self.getPlayer(name)
            return player.rating

    def getRatingList(self):
        """
        Returns a list of tuples in the form of ({name},{rating})
        :return: the list of tuples
        """
        ratings = []
        for player in self.getPlayerList():
            ratings.append((player.name, player.rating))
        return ratings
    
if __name__ == "__main__":
    ping = pingPong()
    
    ping.addPlayer("Mongo")
    ping.addPlayer("Jack")

    print("Henry's rating is: ", ping.getPlayerRating("Mongo"))
    print("Jack's rating is: ", ping.getPlayerRating("Jack"))

    ping.recordMatch("Mongo", "Jack", winner="Jack")
    print(ping.getRatingList())
