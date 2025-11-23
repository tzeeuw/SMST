import discord
from discord.ext import commands
from discord import app_commands
import datetime
import json
import socket
from contextlib import closing
import traceback

import smst.com.port_check as portcheck

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

with open(BASE_DIR / 'properties.json', 'r') as file:
    properties = json.load(file)
GUILD_ID = [discord.Object(id=guild_id) for guild_id in properties["guild_ids"]]
TOKEN=properties["bot_token"]
PASSPHRASE=properties["token"]
IP=properties["local_server_ip"]
PORT=properties["com_port"]
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

        if properties["guild_ids"][f"{interaction.guild.id}"] != "nikhef":
            if not 1 < datetime.datetime.now().hour < 10:

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

            else:
                await interaction.followup.send("Ga eens slapen joh")
        else:
            await interaction.followup.send("Undergoing some surgery, will be back soon.")


    @app_commands.command(description="Status checker for the server")
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer()
    
        if not 1 < datetime.datetime.now().hour < 10:
            status = status_dict[portcheck.status()]

        else:
            status = status_dict["offline"]

        if properties["guild_ids"][f"{interaction.guild.id}"] != "nikhef":
            embed = discord.Embed(title="", description="", color=status[1])
            embed.add_field(name="Server satus:", value=status[0])
        else:
            embed = discord.Embed(title="", description="", color=discord.Color.red())
            embed.add_field(name="Server satus:", value="Current undergoing some surgery")

        await interaction.followup.send(embed=embed)


    @app_commands.command(description="retrieves the server IP")
    async def ip(self, interaction: discord.Interaction):
        if properties["guild_ids"][f"{interaction.guild.id}"] == "nikhef":
            embed = discord.Embed(title="", description="", color=discord.Color.blurple())
            embed.add_field(name="IP:", value="Undergoing some surgery will be back someday")
        else:
            embed = discord.Embed(title="", description="", color=discord.Color.blurple())
            embed.add_field(name="IP:", value="shieldbois.serveminecraft.net")

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="whitelist", description="whitelist yourself to the server")
    async def ip(self, interaction: discord.Interaction, name: str):

        if properties["guild_ids"][f"{interaction.guild.id}"] == "nikhef":
            await interaction.response.send_message("Soon")

        else:
            await interaction.response.defer()
        
            app_info = await test_client.application_info()
            user = interaction.user.name
            guild = properties["guild_ids"][f"{interaction.guild.id}"]

            # connect with terminal and send a whitelist request
            try:
                with closing(socket.socket()) as sock:
                    sock.connect((IP, int(PORT)-1))
                    sock.recv(1024).decode().strip()

                    sock.send(PASSPHRASE.encode("utf-8"))

                    # the remote shell sends two messages so recv them twice
                    sock.recv(1024).decode().strip()
                    sock.recv(1024).decode().strip()

                    sock.send(f"whitelist add {name}".encode("utf-8"))

                    sock.recv(1024).decode().strip()
                    sock.send(b"exit")
                    
                    sock.close()

                # send message to bot owner to ensure that every whitelist is documented
                await app_info.owner.send(f"**{user}** added **{name}** to the whitelist of the **{guild}** minecraft server.")
                await interaction.followup.send(f"Succesfully added: **{name}**, to the whitelist.")

            
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                # send message to bot owner to ensure that every whitelist is documented
                await app_info.owner.send(f"**{user}** tried adding **{name}** to the whitelist of the **{guild}** minecraft server, but failed. Error: {e}")
                await interaction.followup.send(f"Failed to add: **{name}**, to the whitelist.")




    # @app_commands.command(description="get modpack of the server")
    # async def modpack(self, interaction: discord.Interaction):
    #     embed = discord.Embed(title="", description="", color=discord.Color.brand_green())
    #     embed.add_field(name="Modpack: ", value="The base mod pack can be downloaded from [Mod pack](https://drive.google.com/file/d/1q_kgWmKOmKaP6QQXv3OPk1Vf5viNu7og/view?usp=drive_link)\
    #         \n to update the mod pack, download the [update](https://drive.google.com/drive/folders/1pJIBi3O2G3sV5msqE8XP7Gr5io7lEAoZ?usp=drive_link) and copy the files into the mods folder.")
        
    #     await interaction.response.send_message(embed=embed)




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



test_client.run(TOKEN)
