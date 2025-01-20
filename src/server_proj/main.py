import discord
from discord.ext import commands
from discord import app_commands

import server_proj.port_check as portcheck



GUILD_ID = discord.Object(id= 'Totally did not commit sensitive information here :)')
intents = discord.Intents.default()
intents.message_content = True



# first value is string for discord, second is colour of embed
status_dict = {
    "Online": [str(""":white_check_mark: ```ansi\n \033[0;32mOnline```"""), discord.Colour.green()],
    "Idling": [str(""":hourglass_flowing_sand: ```prolog\nIdling```"""), discord.Colour.yellow()],
    "Sleeping": [str(""":zzz::zzz::zzz:```fix\nSleeping```"""), discord.Colour.blue()],
    "Offline": [str(""":x: ```ml\nOffline```"""), discord.Colour.red()]
    }



class ServerGroup(app_commands.Group):
    
    @app_commands.command(description="Starts the server")
    async def start(self, interaction: discord.Interaction):
        await interaction.response.defer()

        match portcheck.status():
            case "Online":
                await interaction.response.send_message("Server is already online")
                return 
        
            case "Idling":
                await interaction.response.send_message("Server is starting")
                return

            case "Sleeping":
                await interaction.response.send_message("Server is waking up and starting.")
                return

            case "Offline":
                await interaction.response.send_message("Server is offline due to maintenance")
                return


    @app_commands.command(description="Status checker for the server")
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer()
    
     
        status = status_dict[portcheck.status()]
        embed = discord.Embed(title="", description="", color=status[1])
        embed.add_field(name="Server satus:", value=status[0])

        await interaction.followup.send(embed=embed)




test_client = commands.Bot(command_prefix="/", intents=intents)
server_group = ServerGroup(name="server", description="Handles server")



@test_client.event
async def on_ready():
    print(f"logged on as {test_client.user}")

    test_client.tree.add_command(server_group)

    test_client.tree.copy_global_to(guild=GUILD_ID)

    try:
        synced = await test_client.tree.sync(guild=GUILD_ID)
        print(f'Synced {len(synced)} commands to guild {GUILD_ID.id}')
    
    except Exception as e:
        print(f"Error syncing commands; {e}")


TOKEN= 'Totally did not commit sensitive information here :)'
test_client.run(TOKEN)
