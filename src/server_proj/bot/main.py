import discord
from discord.ext import commands
from discord import app_commands
import datetime

import server_proj.com.port_check as portcheck


GUILD_ID = [discord.Object(id= 'Totally did not commit sensitive information here :)'), discord.Object(id= 'Here too maybe perhaps :*)')]
intents = discord.Intents.default()
intents.message_content = True


# first value is string for discord, second is colour of embed
status_dict = {
    "online": [str(""":white_check_mark: ```ansi\n\033[0;32mOnline```"""), discord.Colour.green()],
    "idling": [str(""":hourglass_flowing_sand: ```prolog\nIdling```"""), discord.Colour.yellow()],
    "sleeping": [str(""":zzz::zzz::zzz:```fix\nSleeping```"""), discord.Colour.blue()],
    "offline": [str(""":x: ```ml\nOffline```"""), discord.Colour.red()]
    }



class ServerGroup(app_commands.Group):
    
    @app_commands.command(description="Starts the server")
    async def start(self, interaction: discord.Interaction):
        await interaction.response.defer()


        match portcheck.status():
            case "online":
                await interaction.followup.send("Server is already online")

            case "idling":
                await interaction.followup.send("Server is starting")
                portcheck.start(prot="idling")

            case "sleeping":
                await interaction.followup.send("Server is waking up and starting.")

                portcheck.start(prot="sleeping")


            case "offline":
                await interaction.followup.send("Server is offline due to maintenance")


    @app_commands.command(description="Status checker for the server")
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer()
    
     
        status = status_dict[portcheck.status()]
        embed = discord.Embed(title="", description="", color=status[1])
        embed.add_field(name="Server satus:", value=status[0])

        await interaction.followup.send(embed=embed)


    @app_commands.command(description="retrieves the server IP")
    async def ip(self, interaction: discord.Interaction):
        embed = discord.Embed(title="", description="", color=discord.Color.blurple())
        embed.add_field(name="IP:", value="shieldbois.serveminecraft.net")

        await interaction.response.send_message(embed=embed)


    @app_commands.command(description="get modpack of the server")
    async def modpack(self, interaction: discord.Interaction):
        embed = discord.Embed(title="", description="", color=discord.Color.brand_green())
        embed.add_field(name="Modpack: ", value="The base mod pack can be downloaded from [Mod pack](https://drive.google.com/file/d/1q_kgWmKOmKaP6QQXv3OPk1Vf5viNu7og/view?usp=drive_link)\
            \n to update the mod pack, download [update](https://drive.google.com/file/d/1H2I8OAYV1_dbler4g4kb-2j8bEycJEwl/view?usp=drive_link) and copy the files into the mods folder.")
        
        await interaction.response.send_message(embed=embed)




test_client = commands.Bot(command_prefix="/", intents=intents)
server_group = ServerGroup(name="server", description="Handles server")



@test_client.event
async def on_ready():
    print(f"logged on as {test_client.user}")

    test_client.tree.add_command(server_group)

    for guild in GUILD_ID:
        test_client.tree.copy_global_to(guild=guild)

        try:
            synced = await test_client.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        
        except Exception as e:
            print(f"Error syncing commands; {e}")


TOKEN= 'Totally did not commit sensitive information here :)'
test_client.run(TOKEN)
