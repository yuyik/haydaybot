from discord.ext import commands
import random
import asyncio
from collections import namedtuple
from random import choice, randint


class Coords(namedtuple('Coords', 'x y')):
    def is_in_bounds(self, bounds):
        return (0 < self.x <= bounds.x) and (0 < self.y <= bounds.y)

    def neighbors(self, bounds, steps=1):
        """
        Return a list of Coords that are the specified number of steps away in
        each cardinal direction and that are in bounds.
        """
        candidate_coords = [
                        Coords(self.x, self.y - steps),
        Coords(self.x - steps, self.y), Coords(self.x + steps, self.y),
                        Coords(self.x, self.y + steps),
        ]
        return [c for c in candidate_coords if c.is_in_bounds(bounds)]


class Player:
    def __init__(self, name, position, speed, character):
        self.name = name
        self.position = position
        self.speed = speed
        self.character = character

    def __str__(self):
        return self.name

    def move(self, game):
        """
        Make a move in a random cardinal direction (unless it is impossible to
        do so without running out of bounds or stepping on another player).
        """
        player_positions = [p.position for p in game.players + [game.it]]
        destinations = [
            c for c in self.position.neighbors(game.bounds, random.randint(1, self.speed))
            if c not in player_positions
        ]
        if destinations:
            self.position = choice(destinations)


class TagGame:
    def __init__(self, people, bot):
        """
        Create a game with the specified number of players (plus the
        "it" player).
        """
        self.bounds = Coords(len(people) + 4, len(people) + 4)
        self.it = Player(u"\U0001F47F", Coords(len(people) + 4, len(people) + 4), 1, u"\U0001F47F")
        player_names = [u'\U0001f600', u'\U0001F627', u'\U0001F61F', u'\U0001F634']
        self.players = [
            Player("{0}".format(people[i]), Coords(randint(1, len(people) + 1), randint(1, len(people) + 1)), 1, player_names[i])
            for i in range(len(people))
        ]
        self.turns = 0
        self.bot = bot
        self.channel = self.bot.get_channel(channel_id)
        self.people = people

    async def one_turn(self, msg):
        """
        Run one turn of the game, yielding the players who are eliminated.
        """
        dead_list = []
        kill_zone = self.it.position.neighbors(self.bounds)
        for player in self.players:
            player.move(self)
            if player.position in kill_zone:
                dead_list.append(player)
                yield player
                if len(self.players) == 1:
                    await msg.edit(content=self)
                    return
        await msg.edit(content=self)
        for loser in dead_list:
            del self.people[self.players.index(loser)]
            self.players.remove(loser)
            self.it.speed += 1
        self.it.move(self)

    async def run(self):
        """
        Run the game until one player remains, and return that winning player.
        """
        done = False
        msg = await self.channel.send(self)
        while True:
            await asyncio.sleep(1)
            self.turns += 1
            async for loser in self.one_turn(msg):
                await self.channel.send("{0} has been eliminated after {1} turns!".format(
                    loser, self.turns
                ))
                if len(self.players) == 2:
                    done = True
            if self.turns == 150:
                await self.channel.send("The tagger collapsed from exhaustion so the survivors win!")
                break
            if done:
                await self.channel.send("{0} is the winner!".format(self.people[0]))
                break

    async def printout(self, msg):
        await self.channel.send(msg)

    def __str__(self):
        arena = (
            '\n'.join(
                ''.join(
                    next((
                        p.character for p in [self.it] + self.players
                        if p.position == Coords(x, y)
                    ), u'\U0001f534')
                    for x in range(1, self.bounds.x + 1)
                )
                for y in range(1, self.bounds.y + 1)
            )
        )
        return "Turn {0}:\n{1}".format(self.turns, arena)


class Game:
    def __init__(self, bot):
        self.bot = bot
        self.timer = 10
        self.people = []
        self.status = False

    async def countdown(self):
        if len(self.people) == 1:
            await asyncio.sleep(self.timer)
            await self.start()

    async def start(self):
        if not self.status:
            self.status = True
            if len(self.people) == 1:
                self.people.append(self.people[0])
            await TagGame(self.people, self.bot).run()
            for index in range(len(self.people)):
                del self.people[index]
            self.status = False

    @commands.command()
    async def tag(self, ctx):
        self.people.append(ctx.message.author)
        await self.countdown()


def setup(bot):
    bot.add_cog(Game(bot))
