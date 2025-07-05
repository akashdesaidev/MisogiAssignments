# Discord MCP Server

Enable AI models to interact with Discord servers through the Model Context Protocol (MCP).

## Setup

1. **Install dependencies** (already done):
   ```bash
   uv add fastmcp discord.py python-dotenv aiohttp
   ```

2. **Set your Discord bot token**:
   Create a `.env` file in this directory with:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   ```

3. **Run the MCP server**:
   ```bash
   python main.py
   ```

## Available MCP Tools

1. **send_message_tool** - Send messages to Discord channels
2. **get_messages_tool** - Get recent message history from channels  
3. **get_channel_info_tool** - Get channel metadata and information
4. **search_messages_tool** - Search messages with filters
5. **moderate_content_tool** - Delete messages and moderate content

## Usage in Claude Desktop

Add this to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "discord": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/Week4/Day3/q1"
    }
  }
}
```

## Bot Permissions Required

Your Discord bot needs these permissions:
- Read Messages/View Channels
- Send Messages
- Read Message History
- Manage Messages (for moderation)
- Connect (for voice channels if needed)

## Example Usage

```python
# Send a message
await send_message_tool("123456789", "Hello from MCP!")

# Get recent messages  
await get_messages_tool("123456789", 5)

# Search messages
await search_messages_tool("123456789", "python", 20)

# Get channel info
await get_channel_info_tool("123456789")

# Delete a message
await moderate_content_tool("123456789", "987654321", "delete")
```