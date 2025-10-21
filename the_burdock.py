# This example requires the 'message_content' intent.
from modules.config import Config
from modules.redmine import RedmineAPI
import discord
import importlib
import asyncio

class TheBurdock(discord.Client):
    def __init__(self, config, **kwargs):
        self.config = config
        self.last_issue = 0

        super().__init__(**kwargs)

    async def on_ready(self):
        # Imports the REST API library and creates an instance of it.
        rest_module = importlib.import_module(self.config.rest.module_path)
        rest = getattr(rest_module, self.config.rest.module_class)
        self.rest = rest(self.config.rest.url, self.config.rest.api_key)
        
        # Collects the last issue ID from the Rest API.
        """last_issue = self.rest.get_last_issue(self.config.rest.project_id)

       	if last_issue is None:
            self.last_issue = 0
        else:
            self.last_issue = last_issue['id']"""

        # Starts the update issues runtime.
        await self.update_issues()

    async def update_issues(self):
        while True:
            last_issues = self.rest.get_last_issues(self.last_issue, self.config.rest.project_id)
            length = len(last_issues)

            if length > 0:
                # Collects all the issues reported after the last logged issue ID.
                self.last_issue = last_issues[-1]['id']

                # Accesses the corresponding channel by its provided ID
                channel = self.get_channel(self.config.channel_id)
                
                if channel is None:
                    return
                
                # Populates the target channel with the latest collected issues.
                for issue in last_issues:
                    await channel.send(self.format_message(issue))

            await asyncio.sleep(self.config.timeout)
    
    def format_message(self, issue):
        issue_id = issue['id']
        tracker = issue['tracker']['name']
        subject = issue['subject']
        tester = issue['custom_fields'][1]['value']

        return f'**{tracker} #{issue_id}**: {subject} by @{tester}'

config = Config('config.json')
intents = discord.Intents.default()
intents.message_content = True

client = TheBurdock(config, intents=intents)
client.run(client.config.token)
