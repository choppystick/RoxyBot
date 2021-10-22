import random
import discord
import secrets
import aiohttp
import json
import requests
from akinator.async_aki import Akinator
import akinator
import asyncio


from io import BytesIO
from discord.ext import commands
from utils import lists, permissions, http, default


class Fun_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
        self.tenor_api_token = self.config["tenor_api"]
        self.aki = Akinator()

    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        answer = random.choice(lists.ballresponse)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    def gifget(self, type: str, amount:int):
        try:
            r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (type, self.tenor_api_token, 50))

        except requests.ConnectionError:
            return "https://cliparts.zone/img/1718397.png"

        if r.status_code == 200:
            selection = int(random.randint(0,amount))
            load = json.loads(r.content)
            gif = load["results"][selection]["media"][0]["gif"]["url"]
            return gif

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def hug(self, ctx, user: discord.Member = None):
        """Hugs a selected user"""
        if not user or user.id == ctx.author.id:
            e = discord.Embed(title=f"**{ctx.author.name} hugged himself, self-love is good ❤**")
            e.colour = ctx.author.top_role.colour.value
            e.set_image(url=self.gifget("animehug", 49))
            return await ctx.send(embed=e)

        if user.id == self.bot.user.id:
            e = discord.Embed(description="I will only do this once, so you better treasure it. ฅ(*°ω°*ฅ)")
            e.colour = user.top_role.colour.value
            e.set_image(url="https://i.imgur.com/Kj9bwed.png")
            return await ctx.send(embed=e)

        e = discord.Embed(title=f"**{ctx.author.name} hugs {user.name}**")
        e.colour = user.top_role.colour.value
        e.set_image(url=self.gifget("animehug", 49))
        await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def kiss(self, ctx, user: discord.Member = None, placeholder: commands.clean_content = None):
        """Kisses a selected user"""
        win = random.randint(1, 20)
        text = placeholder if placeholder else ""
        choice = random.choice(lists.imglink)
        if not user or user.id == ctx.author.id:
            e = discord.Embed(title=f"**{ctx.author.name} kissed himself.**")
            e.colour = ctx.author.top_role.colour.value
            e.set_image(url=self.gifget("anime kiss", 49))
            return await ctx.send(embed=e)

        if user.id == self.bot.user.id:
            if win == 6 or text.lower() in ["pls", "plz", "please", "cute", "qt", "love you"]: # or ctx.author.id == 159715018911252482:
                e = discord.Embed(title="Fine... Come. Only just for you ❤, okay?")
                e.colour = user.top_role.colour.value
                e.set_image(url=choice)
                return await ctx.send(embed=e)

            else:
                e = discord.Embed(title="I refuse.")
                e.colour = user.top_role.colour.value
                e.set_image(url="https://torako.wakarimasen.moe/file/torako/a/image/1611/44/1611440637046.jpg")
                return await ctx.send(embed=e)

        e = discord.Embed(title=f"**{ctx.author.name} kisses {user.name}**")
        e.colour = colour = user.top_role.colour.value
        e.set_image(url=self.gifget("anime kiss", 49))
        await ctx.send(embed=e)

    async def randomimageapi(self, ctx, url: str, endpoint: str, token: str = None):
        try:
            r = await http.get(
                url, res_method="json", no_cache=True,
                headers={"Authorization": token} if token else None
            )
        except aiohttp.ClientConnectorError:
            return await ctx.send("The API seems to be down...")
        except aiohttp.ContentTypeError:
            return await ctx.send("The API returned an error or didn't return JSON...")

        await ctx.send(r[endpoint])

    async def api_img_creator(self, ctx, url: str, filename: str, content: str = None):
        async with ctx.channel.typing():
            req = await http.get(url, res_method="read")

            if not req:
                return await ctx.send("I couldn't create the image ;-;")

            bio = BytesIO(req)
            bio.seek(0)
            await ctx.send(content=content, file=discord.File(bio, filename=filename))

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def gif(self, ctx, *, search:commands.clean_content):
        """ Sends a gif """
        e = discord.Embed(colour = ctx.author.top_role.colour.value)
        e.set_image(url=self.gifget(search, 10))
        await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def duck(self, ctx):
        """ Posts a random duck """
        await self.randomimageapi(ctx, "https://random-d.uk/api/v1/random", "url")

    @commands.command(aliases=["flip", "coin"])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ["Heads", "Tails"]
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command(aliases = ["F"])
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command(aliases=["ask"])
    async def askroxy(self, ctx):
        """quiz the bot about a chracter."""
        q = await self.aki.start_game()
        n = 0
        def check(m):
            return  m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["yes", "no", "idk", "probably", "probably not", "back", "b", "y", "n", "1", "0", "i"
                                                                                                  , "i dont know", "i don't know", "2", "p", "3", "pn", "4", "exit"]

        def react_check(m):
            return  m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["yes", "no", "y", "n", "okay", "ok"]

        while(True):
            while self.aki.progression <= 90:
                n += 1
                try:
                    await ctx.send(ctx.author.mention + " " + str(n) + ") " + q +"\nYes, No, IDK, Probably, Probably Not, Back, Exit")
                    a = await self.bot.wait_for('message', check=check, timeout=30)

                except akinator.InvalidAnswerError:
                    await ctx.send("""Invalid Answer. Please try again.
                    Accepted Answers: 
                    - "yes" OR "y" OR "0" for YES
                    - "no" OR "n" OR "1" for NO
                    - "i" OR "idk" OR "i dont know" OR "i don't know" OR "2" for I DON'T KNOW
                    - "probably" OR "p" OR "3" for PROBABLY
                    - "probably not" OR "pn" OR "4" for PROBABLY NOT""")
                    return False

                except asyncio.TimeoutError:
                    await ctx.send("Why did you ignore me. I hate you ;-;")
                    return False

                response = a.content

                if response.lower() == "b" or response.lower() == "back":
                    try:
                        q = await self.aki.back()
                        n -= 2
                    except akinator.CantGoBackAnyFurther:
                        pass

                elif response.lower() == "exit" or response.lower() == "e":
                    await ctx.send("Well fine. Try again next time. o/")
                    return False

                else:
                    q = await self.aki.answer(response)

            await self.aki.win()

            try:
                akiguess = discord.Embed(description=f"I'm {round(self.aki.progression, 2)}% sure it's **{self.aki.first_guess['name']}** from **({self.aki.first_guess['description']})**! Was I correct?\n")
                akiguess.set_image(url=self.aki.first_guess['absolute_picture_path'])
                await ctx.send(embed=akiguess)
                r = await self.bot.wait_for("message", check=check, timeout=30)
                correct = r.content

            except asyncio.TimeoutError:
                await ctx.send("Why did you ignore me. I hate you ;-;")
                return False

            if correct.lower() == "yes" or correct.lower() == "y":
                await ctx.send("Yay. Once again my intellect prevails.")
                return False
            else:
                await ctx.send("HOW!?!?!? This couldn't be.... You must have misled me. >W<. \n" + "Test me again. This time, I will get it correct. (Ok/No)")

                try:
                    ans = await self.bot.wait_for("message", timeout=30.0, check=react_check)
                    if ans.content.lower() == "yes" or ans.content.lower() == "y" or ans.content.lower() == "ok" or ans.content.lower() == "okay" :
                        await ctx.send("I will get it correct this time.")
                        self.aki.progression -= 35

                    else:
                        await ctx.send("Hmpf. No guts.")
                        return False

                except asyncio.TimeoutError:
                     await ctx.send("Are you dead? Can you respond??? Fine... Hmpf")
                     return False

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: commands.clean_content):
        """ Find the 'best' definition to any words"""
        async with ctx.channel.typing():
            try:
                url = await http.get(f"https://api.urbandictionary.com/v0/define?term={search}", res_method="json")
            except Exception:
                return await ctx.send("Urban API returned invalid data... might be down atm.")

            if not url:
                return await ctx.send("I think the API broke...")

            if not len(url["list"]):
                return await ctx.send("Couldn't find your search in the dictionary...")

            result = sorted(url["list"], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

            definition = result["definition"]
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(" ", 1)[0]
                definition += "..."

            await ctx.send(f"📚 Definitions for **{result['word']}**```fix\n{definition}```")


    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")


    @commands.command(aliases=["r", "R"])
    async def rate(self, ctx, *, thing: commands.clean_content):
        """Rate anything of your choosing"""
        rate_amount = random.uniform(0.0, 100.0)
        if "roxy" in str(thing).lower():
            rate_amount = 100

        if "zeron" in str(thing).lower():
            rate_amount = random.uniform(0, 20)
            return await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount, 2)} / 100**")

        if ("c3rs" in str(thing).lower()) or ("roger" in str(thing).lower()):
            rate_amount = random.uniform(70.0, 100.0)
            return await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount, 2)} / 100**")

        if thing == "Cloudflare" or thing == "cloudflare":
            rate_amount = random.uniform(0.0, 10.0)

        if "choppy" in str(thing).lower():
            return await ctx.send("Everything that belongs to Choppy is a straight 100. So no need to ask :>")

        await ctx.send(f"I'd rate `{thing}` a **{round(rate_amount, 2)} / 100**")

    @commands.command()
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Give someone a beer! 🍻 """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

        beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(aliases=["howhot", "hotcalc"])
    async def hot(self, ctx, *, user: discord.Member = None):
        """Returns the hotness of a discord user"""
        user = user or ctx.author

        if user.id == self.bot.user.id:
            return await ctx.send("My hotness is immeasurable by mortals such as yourself. Hmpf!")

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 25:
            emoji = "❤"
        elif hot > 50:
            emoji = "💖"
        elif hot > 75:
            emoji = "💞"
        else:
            emoji = "💔"

        if user.id == 159715018911252482:
            return await ctx.send("Choppy is always the cutest in my eyes.")

        elif user == ctx.author:
            return await ctx.send("Can you not do that? You narcissistic prick.")

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command()
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def roxy(self, ctx):
        """ Returns a random fanart of Roxy """
        choice = random.choice(lists.imglink)
        if not permissions.can_handle(ctx, "attach_files"):
            return await ctx.send("I cannot send images here ;-;")

        e = discord.Embed(color=0x00ffff)
        e.set_image(url=choice)
        await ctx.send(embed=e)

    @commands.command(aliases=["slots", "bet", "gambling"])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍈🍌🍍🥭🍏🍑🍅🥥🥝🍎🍊🍐🍋🍉🍇🍓🍒⑦"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        # if ctx.author.id == 159715018911252482:
        #     a = "⑦"
        #     b = "⑦"
        #     c = "⑦"

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == "⑦" and b == "⑦" and c == "⑦"):
            await ctx.send(f"{slotmachine} OMG. JACKPOT. 🎉YOU MEGA WON!.🎉")

        elif (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")

        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")

        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

    @commands.command()
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def gay(self, ctx, user: discord.Member = None, *, text:commands.clean_content=None):
        """Call someone gay because haha gay funny"""
        user = user or ctx.author
        rand = random.randint(50, 100)
        if user.id == 421883442486181889:
            rand = random.randint(100, 200)

        response = ""
        if text == None:
            response = f"**🌈{user.name}** is gay haha.🌈    -*{ctx.author.name}*"

        else:
            response = text

        e = discord.Embed(description="🌡️Gaymeter: " + str(rand) + "%\n**" + response + "**")
        e.set_thumbnail(url=user.avatar_url)
        e.colour = colour=user.top_role.colour.value


        if user.id == 159715018911252482:
            return await ctx.send("No u lol.")

        elif user.id == ctx.bot.user.id:
            return await ctx.send("I'm not gay (´；Д；｀). I love Rudy.(˃̥̥ω˂̥̥̥)")

        elif user == ctx.author:
            e.set_image(url="https://i.imgflip.com/5bxysd.jpg")

        else:
            e.set_image(url="https://media.giphy.com/media/BpnkuY1i2rBpm/giphy.gif")

        await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def league(self, ctx, user: discord.Member = None):
        """Chooses a random champion for you"""
        user = user or ctx.author

        herolist = ['Aatrox', 'Ahri', 'Akali', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'Aurelion Sol', 'Azir', 'Bard',
                    'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'ChoGath', 'Corki', 'Darius', 'Diana', 'Dr. Mundo',
                    'Draven', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar',
                    'Gragas', 'Graves', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'Jarvan IV', 'Jax', 'Jayce', 'Jhin',
                    'Jinx', 'KaiSa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', "Kha'Zix", 'Kindred',
                    'Kled', "Kog'Maw", 'LeBlanc', 'Lee Sin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar',
                    'Maokai', 'Master Yi', 'Miss Fortune', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee',
                    'Nocturne', 'Nunu and Willump', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan',
                    'Rammus', "Rek'Sai", 'Rell', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna',
                    'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain',
                    'Sylas', 'Syndra', 'Tahm Kench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle',
                    'Tryndamere', 'Twisted Fate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'VelKoz', 'Vi', 'Viktor',
                    'Vladimir', 'Volibear', 'Warwick', 'Wukong', 'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi',
                    'Zac', 'Zed', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']

        await ctx.send(f"`{random.choice(herolist)}`. {user.name}, this is your random hero pick. ")


def setup(bot):
    bot.add_cog(Fun_Commands(bot))
