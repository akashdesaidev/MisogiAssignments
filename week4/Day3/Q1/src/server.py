"""
Discord MCP Server
Enable AI models to interact with Discord servers
"""

import os
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
import discord
from discord.ext import commands
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

mcp = FastMCP("Discord MCP Server")

class DiscordMCP:
    def __init__(self):
        self.bot = None
        self.is_connected = False
        self.setup_discord_bot()
    
    def setup_discord_bot(self):
        """Setup Discord bot client"""
        token = os.getenv('DISCORD_BOT_TOKEN')
        if not token:
            print("Warning: DISCORD_BOT_TOKEN not found. Discord features will be unavailable.")
            return
        
        # Setup bot with necessary intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        @self.bot.event
        async def on_ready():
            print(f'{self.bot.user} has connected to Discord!')
            print(f'Bot is in {len(self.bot.guilds)} servers')
            for guild in self.bot.guilds:
                print(f'  - {guild.name} (ID: {guild.id})')
            self.is_connected = True
    
    async def start_bot(self):
        """Start the Discord bot with proper connection"""
        if not self.bot or self.is_connected:
            return {"success": True, "data": None}
        
        try:
            token = os.getenv('DISCORD_BOT_TOKEN')
            print("Connecting Discord bot...")
            
            # Start the bot in background
            bot_task = asyncio.create_task(self.bot.start(token))
            
            # Wait for bot to be ready (with timeout)
            for i in range(30):  # Wait up to 30 seconds
                if self.bot.is_ready():
                    print("Bot connected and ready!")
                    break
                await asyncio.sleep(1)
                if i == 29:
                    raise TimeoutError("Bot didn't connect within 30 seconds")
            
            return {"success": True, "data": None}
            
        except Exception as e:
            return {"success": False, "error": f"Failed to start bot: {str(e)}", "data": None}
    
    async def ensure_bot_ready(self):
        """Ensure bot is connected before operations"""
        if not self.bot:
            return {"success": False, "error": "Discord bot not configured", "data": None}
        
        if not self.bot.is_ready():
            # Try to start the bot if not ready
            start_result = await self.start_bot()
            if not start_result["success"]:
                return start_result
        
        return {"success": True, "data": None}
    
    async def send_message(self, channel_id: str, message: str) -> Dict[str, Any]:
        """Send message to Discord channel"""
        try:
            ready_check = await self.ensure_bot_ready()
            if not ready_check["success"]:
                return ready_check
            
            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                return {
                    "success": False,
                    "error": f"Channel {channel_id} not found or bot doesn't have access",
                    "data": None
                }
            
            sent_message = await channel.send(message)
            
            return {
                "success": True,
                "message": "Message sent successfully",
                "data": {
                    "message_id": str(sent_message.id),
                    "channel_id": str(sent_message.channel.id),
                    "content": sent_message.content,
                    "timestamp": sent_message.created_at.isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send message: {str(e)}",
                "data": None
            }
    
    async def get_messages(self, channel_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get recent messages from Discord channel"""
        try:
            ready_check = await self.ensure_bot_ready()
            if not ready_check["success"]:
                return ready_check
            
            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                return {
                    "success": False,
                    "error": f"Channel {channel_id} not found or bot doesn't have access",
                    "data": None
                }
            
            messages = []
            async for message in channel.history(limit=limit):
                messages.append({
                    "id": str(message.id),
                    "author": {
                        "id": str(message.author.id),
                        "name": message.author.display_name,
                        "username": message.author.name
                    },
                    "content": message.content,
                    "timestamp": message.created_at.isoformat(),
                    "edited": message.edited_at.isoformat() if message.edited_at else None,
                    "attachments": [att.url for att in message.attachments]
                })
            
            return {
                "success": True,
                "message": f"Retrieved {len(messages)} messages",
                "data": {
                    "channel_id": channel_id,
                    "messages": messages
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get messages: {str(e)}",
                "data": None
            }
    
    async def get_channel_info(self, channel_id: str) -> Dict[str, Any]:
        """Get Discord channel information"""
        try:
            ready_check = await self.ensure_bot_ready()
            if not ready_check["success"]:
                return ready_check
            
            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                return {
                    "success": False,
                    "error": f"Channel {channel_id} not found or bot doesn't have access",
                    "data": None
                }
            
            channel_info = {
                "id": str(channel.id),
                "name": channel.name,
                "type": str(channel.type),
                "guild": {
                    "id": str(channel.guild.id),
                    "name": channel.guild.name
                } if hasattr(channel, 'guild') else None,
                "topic": getattr(channel, 'topic', None),
                "position": getattr(channel, 'position', None),
                "member_count": len(channel.members) if hasattr(channel, 'members') else None,
                "created_at": channel.created_at.isoformat()
            }
            
            return {
                "success": True,
                "message": "Channel information retrieved",
                "data": channel_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get channel info: {str(e)}",
                "data": None
            }
    
    async def search_messages(self, channel_id: str, query: str, limit: int = 50) -> Dict[str, Any]:
        """Search messages in Discord channel"""
        try:
            ready_check = await self.ensure_bot_ready()
            if not ready_check["success"]:
                return ready_check
            
            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                return {
                    "success": False,
                    "error": f"Channel {channel_id} not found or bot doesn't have access",
                    "data": None
                }
            
            matching_messages = []
            search_count = 0
            
            async for message in channel.history(limit=limit):
                search_count += 1
                if query.lower() in message.content.lower():
                    matching_messages.append({
                        "id": str(message.id),
                        "author": {
                            "id": str(message.author.id),
                            "name": message.author.display_name,
                            "username": message.author.name
                        },
                        "content": message.content,
                        "timestamp": message.created_at.isoformat(),
                        "url": message.jump_url
                    })
            
            return {
                "success": True,
                "message": f"Found {len(matching_messages)} messages matching '{query}'",
                "data": {
                    "query": query,
                    "searched_messages": search_count,
                    "matches": matching_messages
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to search messages: {str(e)}",
                "data": None
            }
    
    async def moderate_content(self, channel_id: str, message_id: str, action: str = "delete") -> Dict[str, Any]:
        """Moderate Discord content (delete messages)"""
        try:
            ready_check = await self.ensure_bot_ready()
            if not ready_check["success"]:
                return ready_check
            
            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                return {
                    "success": False,
                    "error": f"Channel {channel_id} not found or bot doesn't have access",
                    "data": None
                }
            
            if action == "delete":
                try:
                    message = await channel.fetch_message(int(message_id))
                    await message.delete()
                    
                    return {
                        "success": True,
                        "message": "Message deleted successfully",
                        "data": {
                            "action": action,
                            "message_id": message_id,
                            "channel_id": channel_id
                        }
                    }
                except discord.NotFound:
                    return {
                        "success": False,
                        "error": "Message not found",
                        "data": None
                    }
                except discord.Forbidden:
                    return {
                        "success": False,
                        "error": "Bot doesn't have permission to delete messages",
                        "data": None
                    }
            else:
                return {
                    "success": False,
                    "error": f"Unsupported moderation action: {action}",
                    "data": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to moderate content: {str(e)}",
                "data": None
            }
    
    async def close_bot(self):
        """Close the Discord bot connection"""
        if self.bot and not self.bot.is_closed():
            await self.bot.close()
            self.is_connected = False

# Initialize the Discord MCP client
discord_client = DiscordMCP()

# MCP Tool definitions
@mcp.tool()
async def send_message_tool(channel_id: str, message: str) -> Dict[str, Any]:
    """Send message to Discord channel"""
    return await discord_client.send_message(channel_id, message)

@mcp.tool()
async def get_messages_tool(channel_id: str, limit: int = 10) -> Dict[str, Any]:
    """Get recent messages from Discord channel"""
    return await discord_client.get_messages(channel_id, limit)

@mcp.tool()
async def get_channel_info_tool(channel_id: str) -> Dict[str, Any]:
    """Get Discord channel information and metadata"""
    return await discord_client.get_channel_info(channel_id)

@mcp.tool()
async def search_messages_tool(channel_id: str, query: str, limit: int = 50) -> Dict[str, Any]:
    """Search messages in Discord channel with filters"""
    return await discord_client.search_messages(channel_id, query, limit)

@mcp.tool()
async def moderate_content_tool(channel_id: str, message_id: str, action: str = "delete") -> Dict[str, Any]:
    """Moderate Discord content - delete messages"""
    return await discord_client.moderate_content(channel_id, message_id, action)

def main():
    """Main function - runs MCP server"""
    print("Discord MCP Server initialized!")
    print("Available MCP tools:")
    print("1. send_message_tool - Send messages to Discord channels")
    print("2. get_messages_tool - Get recent message history")
    print("3. get_channel_info_tool - Get channel metadata")
    print("4. search_messages_tool - Search messages with filters")
    print("5. moderate_content_tool - Delete messages and moderate content")
    print("\nMake sure to set DISCORD_BOT_TOKEN in your .env file!")

if __name__ == "__main__":
    mcp.run() 