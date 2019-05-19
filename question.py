from database import db, test_db
from config import PREFIX
import random
import discord


class IqQuiz:
    def __init__(self, db, author_id, question):
        self.db = db
        self.author_id = author_id
        self.question = question
        self.votes = {}
        self.bets = {}

    def add_bet(self, voter_id, iq_offered):

        # Cannot bet twice
        if voter_id in self.bets:
            return f"<@{voter_id}> You already voted, y'goof."

        # Cannot vote more iq than you have
        if iq_offered > self.db.get_iq(voter_id):
            return f"<@{voter_id}> You don't have enough iq for that."
        
        if iq_offered < 0:
            return f"<@{voter_id}> You can't vote negative iq, dingus."

        # Create voting set for voter
        self.votes.setdefault(voter_id, set())

        # Record the bet
        self.bets.setdefault(voter_id, iq_offered)
        return f"<@{voter_id}> Successfully added bet of {iq_offered} iq."

    def add_vote(self, voter_id, nominee_id):

        # Cannot vote without offering iq
        if voter_id not in self.bets:
            return f"You have to bet iq points before voting, <@{voter_id}>."

        # Cannot vote for yourself
        if voter_id == nominee_id:
            return f"You can't vote for yourself, <@{voter_id}>."

        # Create voting set for nominee
        self.votes.setdefault(nominee_id, set())

        # Cannot vote twice 
        if voter_id in self.votes[nominee_id]:
            return f"<@{voter_id}> You already voted for <@{nominee_id}>."

        # Cannot vote for someone more than once 
        if voter_id in self.votes[nominee_id]:
            return f"<@{voter_id}> you can only vote for <@{nominee_id}> once."

        # Add voter's id to nominee's voting set
        self.votes[nominee_id].add(voter_id)
        return f"<@{voter_id}> Vote for <@{nominee_id}> successful."

    def end_quiz(self):
        """
        When voting ends, the iq offered by each user will be multiplied by the
        number of votes each user accumulated, and that will be added to each
        user's iq bank.
        If the user got 0 votes, they lose the iq they offered for that question.
        """

        votes = []
               #[nominee[name, iq_offered]]
        # Turn voting sets into tallies
        for nominee, vote_set in self.votes.items():
            if nominee in self.bets:
                earned_iq = self.bets[nominee]*(len(vote_set) or -1)
                votes.append([nominee, earned_iq])


        # Sort nominees by number of tallies
        votes.sort(key=lambda x: x[1], reverse=True) 

        if len(votes) == 0:
            return "Nobody voted!"

        end_message = "IQ earned:\n"
        
        # List the points earned/lost in bet
        for nominee in votes:
            end_message += f"\t{nominee[0]}: +{nominee[1]}\n"
            self.db.delta_iq(nominee[0], nominee[1])
            self.bets.pop(nominee[0])

        # List all the points people lost
        end_message += "IQ lost:\n"
        for user, bet in self.bets.items():
            end_message += f"\t{user}: {bet*-1}\n"
            self.db.delta_iq(user, bet*-1)

        return end_message

def test_IqQuiz_class():
    print("Testing the IqQuiz class:")
    testIqQuiz = IqQuiz(test_db, 'ryan', 'How many eggs')
    print(testIqQuiz.add_bet('ryan', 10))
    print(testIqQuiz.add_bet('john', 10))
    print(testIqQuiz.add_bet('jacob', 102))
    print(testIqQuiz.add_bet('jacob', 100))
    print(testIqQuiz.add_vote('ryan', 'ryan'))
    print(testIqQuiz.add_vote('jacob', 'john'))
    print(testIqQuiz.add_vote('john', 'ryan'))
    print(testIqQuiz.add_vote('ryan', 'john'))
    print(testIqQuiz.end_quiz())


class IqQuizClient:
    def __init__(self, db):
        self.db = db
        self.quizzes = {}

    async def handle_message(self, client, message):
        response = self.parse(message)
        if response is not None:
            await client.send_message(message.channel, response)

    def parse(self, message):
        author_id = message.author.id
        channel = message.channel
        channel_id = channel.id
        args = message.content.split()
        if len(args[0]) > 1:
            command = args[0][1:]

        else:
            return


        if command == 'quiz':
            question = ' '.join(args[1:])
            return self.add_quiz(channel_id, author_id, question)

        elif command == 'bet':
            iq_offered = int(args[1])
            return self.add_bet(channel_id, author_id, iq_offered)

        elif command == 'vote':
            nominee_id = ''.join(i for i in args[1] if i.isdigit())
            return self.add_vote(channel_id, author_id, nominee_id)

        elif command == 'endquiz':
            server = message.channel.server
            return self.end_quiz(server, channel_id)

    def add_quiz(self, channel_id, author_id, question):
        if channel_id in self.quizzes:
            return "There's already an active quiz in this channel."

        self.quizzes[channel_id] = IqQuiz(self.db, author_id, question)
        return f"Quiz: {question}"
    
    def add_bet(self, channel_id, user_id, iq_offered):
        if channel_id not in self.quizzes:
            return "You can't bet when there's no quiz."

        else:
            return self.quizzes[channel_id].add_bet(user_id, iq_offered)

    def add_vote(self, channel_id, user_id, nominee_id):
        if channel_id not in self.quizzes:
            return "You can't vote when there's no quiz."
        else:
            return self.quizzes[channel_id].add_vote(user_id, nominee_id)

    def end_quiz(self, server, channel_id):
        if channel_id not in self.quizzes:
            return "You can't end a quiz that doesn't exist."

        else:
            self.quizzes[channel_id].end_quiz()
            self.quizzes.pop(channel_id)
            if self.db == test_db:
                return "Okie doke, test is over. However list_iqs was skipped"
            return self.db.list_iqs(server)


def test_IqQuizClient_class():
    print("Testing the IqQuiz Client:")
    test_count = 10
    channel_id = "test_channel"
    server = "test_server"
    users = ["Jacob", "Ryan", "John", "Peter", "Kyle", "Evan"]
    tests = ["add_bet", "add_vote"]


    quiz_client = IqQuizClient(test_db)

    # Shouldn't work
    print(quiz_client.add_bet(channel_id, users[0], random.randrange(-25, 125)))
    print(quiz_client.add_vote(channel_id, users[0], users[1]))

    # Should work
    print(quiz_client.add_quiz(channel_id, users[0], "Will this code run?"))

    for i in range(test_count):
        test_type = random.choice(tests)
        user_id = random.choice(users)
        if test_type == "add_bet":
            print(quiz_client.add_bet(channel_id, user_id, random.randrange(-25, 125)))

        elif test_type == "add_vote":
            nominee_id = random.choice(users)
            print(quiz_client.add_vote(channel_id, user_id, nominee_id))


    print(quiz_client.end_quiz(server, channel_id))

    # Shouldn't work
    print(quiz_client.add_bet(channel_id, users[0], random.randrange(-25, 125)))
    print(quiz_client.add_vote(channel_id, users[0], users[1]))

if __name__ == "__main__":
    test_db.clear_iq()
    test_IqQuiz_class()
    test_db.clear_iq()
    test_IqQuizClient_class()

quiz_client = IqQuizClient(db)
