from discord.ext import commands
import discord
import re
import random


# Check if the string has numbers within it
def hasnumbers(input_string):
    return any(char.isdigit() for char in input_string)


# Checks if the item is an actual Hay Day item
def itemexists(article):
    thing = ""
    for line in open("hay_day_data.txt", "r"):
        if "\n" in line:
            thing = line[:-1].lower().split()
        else:
            thing = line.lower().split()
        while not (hasnumbers(thing[1]) or thing[1] == "N/A"):
            thing[0] += " " + thing[1]
            del thing[1]
        if thing[0] == article.lower():
            return [True, thing]
    return [False, thing]


# Combines the parts of the item's part of a name
def rename(article):
    if len(article) == 1 or hasnumbers(article[1]):
        article = article[0]
    elif not hasnumbers(article[1]):
        new_article = article[0]
        for index in range(1, len(article)):
            if hasnumbers(article[index]):
                break
            else:
                new_article += " " + article[index]
        article = new_article
    return article


# Separates alphabetical letters from numbers
def separate_text(input_text):
    return [item for item in re.split('(\d+)', input_text) if item]


class Statistics:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx, *section):
        """
!statistic stat section
Returns the "stat" of every item within "section". Simple do !sellprices to see what categories are available
        """
        item_index = 0
        index = 0
        stat_exists = True
        channel = self.bot.get_channel(channel_id)
        info_sections = [[], [], [], [], [], [],
                         [], [], [], [], [], [],
                         [], [], [], [], [], [],
                         [], [], [], [], [], [],
                         [], [], [], [], [], [],
                         [], [], [], [], [], [],
                         [], [], []]
        limits = (31, 52, 63, 70, 75, 79, 85, 95, 107, 114,
                  120, 131, 137, 143, 151, 157, 165, 170, 179,
                  185, 188, 196, 198, 207, 211, 216, 218, 224,
                  232, 237, 246, 253, 258, 263, 268, 274, 279,
                  284, 292)
        stats = ["sellprices", "level", "time", "mtime"]

        if len(section) == 0:
            section = "nothing"
        else:
            section = " ".join(section)

        for line in open("hay_day_data.txt", "r"):
            if item_index == limits[index]:
                index += 1
            item_name = rename(line.split())
            if section.split(" ")[0].lower() not in stats:
                print(section.split(" ")[0].lower())
                stat_exists = False
                break
            else:
                start = len(item_name.split()) + stats.index(section.split(" ")[0].lower())
                end = start
                if section.split(" ")[0].lower() != "sellprices":
                    start += 3
                    end += 4
                else:
                    end += 4
                list_index = line.split()[start:end]

                line = [item_name] + list_index
                info_sections[index].append(line)
                item_index += 1

        category_list = ["crops", "supplies", "bakery", "feed mill",
                         "dairy", "sugar mill", "popcorn pot", "bbq grill", "pie oven", "loom",
                         "sewing machine", "cake oven", "mine", "smelter", "juice press",
                         "lure workbench", "ice cream maker", "net maker", "jam maker", "jeweler",
                         "honey extractor", "coffee kiosk", "lobster pool", "soup kitchen", "candle maker",
                         "flower shop", "duck salon", "candy machine", "sauce maker", "sushi bar",
                         "salad bar", "sandwich bar", "smoothie mixer", "pasta maker", "hat maker",
                         "pasta kitchen", "hot dog stand", "taco kitchen", "tea stand"]

        section1 = " ".join(section.split(" ")[1:])
        if section1.lower() not in category_list or not stat_exists:
            await channel.send("?stats {stat} {section/machines}\n"
                               "You must input a section type: \n"
                               "```Crops, Supplies```\n"
                               "Or one of the machines: \n"
                               "```Bakery, Feed Mill, Dairy, Sugar Mill, Popcorn Pot, BBQ Grill, "
                               "Pie Oven, Sewing Machine, Cake Oven, Mine, Smelter, Juice Press, "
                               "Lure Workbench, Ice Cream Maker, Net Maker, Jam Maker, Jeweler, "
                               "Honey Extractor, Coffee Kiosk, Lobster Pool, Soup Kitchen, "
                               "Candle Maker, Flower Shop, Duck Salon, Candy Machine, Sushi Bar, "
                               "Salad Bar, Sandwich Bar, Smoothie Mixer, Pasta Maker, Hat Maker, "
                               "Pasta Kitchen, Hot Dog Stand, Taco Kitchen, Tea Stand```"
                               "Or input the correct stat: \n"
                               "```sellprices, level, time, mtime```")
        else:
            start = ["BAKERY\n------------------------------------\n",
                     "FEED MILL\n------------------------------------\n",
                     "DAIRY\n----------------------------------\n",
                     "SUGAR MILL\n---------------------------------\n",
                     "POPCORN POT\n----------------------------------\n",
                     "BBQ GRILL\n----------------------------------\n",
                     "PIE OVEN\n----------------------------------\n",
                     "LOOM\n-----------------------------------\n",
                     "SEWING MACHINE\n-------------------------------------\n",
                     "CAKE OVEN\n-----------------------------------\n",
                     "MINE\n-----------------------------------\n",
                     "SMELTER\n------------------------------------------------------\n",
                     "JUICE PRESS\n----------------------------------\n",
                     "LURE WORKBENCH\n----------------------------------\n",
                     "ICE CREAM MAKER\n-------------------------------------\n",
                     "NET MAKER\n-----------------------------------\n",
                     "JAM MAKER\n-----------------------------------\n",
                     "JEWELER\n-----------------------------------\n",
                     "HONEY EXTRACTOR\n-----------------------------------\n",
                     "COFFEE KIOSK\n-----------------------------------\n",
                     "LOBSTER POOL\n------------------------------------------------------------\n",
                     "SOUP KITCHEN\n-----------------------------------\n",
                     "CANDLE MAKER\n-----------------------------------\n",
                     "FLOWER SHOP\n-----------------------------------\n",
                     "DUCK SALON\n------------------------------------------------------\n",
                     "CANDY MACHINE\n------------------------------------\n",
                     "SAUCE MAKER\n------------------------------------\n",
                     "SUSHI BAR\n------------------------------------\n",
                     "SALAD BAR\n------------------------------------\n",
                     "SANDWICH BAR\n------------------------------------\n",
                     "SMOOTHIE MIXER\n------------------------------------\n",
                     "PASTA MAKER\n------------------------------------\n",
                     "HAT MAKER\n------------------------------------\n",
                     "PASTA KITCHEN\n------------------------------------\n",
                     "HOT DOG STAND\n------------------------------------\n",
                     "TACO KITCHEN\n------------------------------------\n",
                     "TEA STAND\n------------------------------------\n"]
            intro = "```prolog" + "\n"
            ending = "``` \nAll info comes from the Hay Day Wikia! Note that all prices are maximum prices."
            category = " ".join(section.split(" ")[1:])
            if category.lower() in category_list:
                category_index = category_list.index(category.lower())
                information = ""
                for line in info_sections[category_index]:
                    spacing = (24 - len(line[0])) * " "
                    information += line[0] + spacing + " ".join(line[1:]) + "\n"
                if category_index < 2:
                    await channel.send(intro + information + ending)
                else:
                    await channel.send(intro + start[category_index - 2] + information + ending)

    @commands.command()
    async def search(self, ctx, *item):
        """
!search item
Returns a link about the item from the Hay Day Wikia in the form of "http://hayday.wikia.com/wiki/item_name"
        """
        channel = self.bot.get_channel(channel_id)
        item = rename(item).title()
        item = item.replace(" ", "_")
        if "And" in item:
            item = item.replace("And", "and")
        elif "_Di_" in item:
            item = item.replace("_Di_", "_di_")
        elif "Shepherd'S" in item:
            item = item.replace("Shepherd'S", "Shepherd's")
        link = "http://hayday.wikia.com/wiki/" + item
        await channel.send(link)

    @commands.command()
    async def info(self, ctx, *item):
        """
!info item
Returns an information box about the section.split(" ")[0].lower()s of the item, if it exists
        """
        channel = self.bot.get_channel(channel_id)
        item = rename(item)
        if itemexists(item.lower())[0]:
            item_info = itemexists(item)[1]
            color = ""
            for char in range(6):
                color += random.choice('0123456789ABCDEF')
            color = int(color, 16)

            data = discord.Embed(
                colour=discord.Colour(value=color))
            data.add_field(name="Name", value=item_info[0].title())
            data.add_field(name="Price", value=item_info[1])
            data.add_field(name="Min price for 10", value=item_info[2][1:])
            data.add_field(name="Max price for 10", value=item_info[4][:-1])
            data.add_field(name="Level", value=item_info[5])
            data.add_field(name="Time to make", value=item_info[6])
            data.add_field(name="Time in mastered machine", value=item_info[7])

            await channel.send(embed=data)
        else:
            await channel.send("Please input a valid item!")


# Adds this cog to the main program (Hermes.py)
def setup(bot):
    bot.add_cog(Statistics(bot))
