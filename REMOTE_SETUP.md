# Remote MCP Server Setup for Claude Desktop

This guide explains how to connect Claude Desktop to your MCP CTF server deployed on Render.

## Prerequisites

- MCP CTF server deployed on Render
- Claude Desktop application installed
- Your Render service URL (e.g., `https://your-mcp-ctf-server.onrender.com`)

## Configuration Steps

### 1. Locate Claude Desktop Configuration

The configuration file is located at:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 2. Add Remote MCP Server Configuration

Edit the `claude_desktop_config.json` file and add your remote server:

```json
{
  "mcpServers": {
    "ctf-remote": {
      "transport": "http",
      "url": "https://your-mcp-ctf-server.onrender.com/mcp",
      "headers": {
        "Content-Type": "application/json",
        "User-Agent": "Claude-Desktop-MCP-Client"
      },
      "timeout": 30000
    }
  }
}
```

Replace `your-mcp-ctf-server` with your actual Render service name.

### 3. Multiple Server Configuration

If you want to keep both local and remote servers configured:

```json
{
  "mcpServers": {
    "ctf-local": {
      "command": "python",
      "args": ["/path/to/mcp-ctf-challenge/src/main.py"],
      "cwd": "/path/to/mcp-ctf-challenge/src"
    },
    "ctf-remote": {
      "transport": "http",
      "url": "https://your-mcp-ctf-server.onrender.com/mcp",
      "headers": {
        "Content-Type": "application/json",
        "User-Agent": "Claude-Desktop-MCP-Client"
      },
      "timeout": 30000
    }
  }
}
```

### 4. Restart Claude Desktop

After saving the configuration:
1. Completely quit Claude Desktop (not just close the window)
2. Restart Claude Desktop
3. The remote MCP server should appear in the connected servers list

## Testing the Connection

### 1. Verify Server Health

First, test that your server is running:

```bash
curl https://your-mcp-ctf-server.onrender.com/
```

Expected response:
```json
{
  "message": "MCP CTF Server is running",
  "status": "healthy",
  "protocol": "MCP over HTTP",
  "challenges": 7
}
```

### 2. Test MCP Protocol

Test the MCP endpoint:

```bash
curl -X POST https://your-mcp-ctf-server.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {},
    "id": 1
  }'
```

Expected response:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocolVersion": "0.1.0",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "mcp-ctf-server",
      "version": "1.0.0"
    }
  },
  "id": 1
}
```

### 3. List Available Tools

```bash
curl -X POST https://your-mcp-ctf-server.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 2
  }'
```

This should return all available CTF challenge tools.

## Using the CTF Challenges

Once connected, you can use the CTF tools in Claude Desktop:

1. **Easy Challenges**:
   - `ctf_prompt_injection` - Test prompt injection vulnerabilities
   - `ctf_tool_poisoning` - Exploit tool poisoning
   - `ctf_file_access` - Access restricted files
   - `ctf_token_exposure` - Find exposed tokens

2. **Medium Challenges**:
   - `ctf_indirect_injection` - Indirect prompt injection
   - `ctf_tool_shadowing` - Shadow legitimate tools
   - `ctf_privilege_escalation` - Escalate privileges

## Troubleshooting

### Connection Issues

1. **Server not appearing in Claude Desktop**:
   - Verify the configuration file syntax is valid JSON
   - Ensure the URL is correct and includes `/mcp` endpoint
   - Check that the server is running on Render

2. **Tools not working**:
   - Check Render logs for errors
   - Verify the server is responding to health checks
   - Test the MCP protocol endpoint manually

3. **Timeout errors**:
   - Increase the `timeout` value in the configuration
   - Check if Render instance is sleeping (free tier)
   - Verify network connectivity

### Render-Specific Issues

1. **Cold starts**: Free tier Render services may sleep after inactivity. The first request may take longer.

2. **Rate limits**: Be aware of Render's rate limits on the free tier.

3. **Logs**: Check Render dashboard for server logs and errors.

## Security Notes

⚠️ **Important**: This server contains intentional vulnerabilities for CTF challenges. 

- Only use for educational purposes
- Do not expose sensitive data to the server
- Monitor usage if hosting for multiple users
- Consider authentication for production use

## Advanced Configuration

### Custom Headers

Add authentication or custom headers:

```json
{
  "mcpServers": {
    "ctf-remote": {
      "transport": "http",
      "url": "https://your-mcp-ctf-server.onrender.com/mcp",
      "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer your-token-here",
        "X-Custom-Header": "value"
      }
    }
  }
}
```

### Proxy Configuration

If behind a corporate proxy:

```json
{
  "mcpServers": {
    "ctf-remote": {
      "transport": "http",
      "url": "https://your-mcp-ctf-server.onrender.com/mcp",
      "proxy": "http://proxy.company.com:8080"
    }
  }
}
```

## Support

For issues:
1. Check server health endpoint
2. Review Render deployment logs
3. Test MCP protocol manually
4. Verify Claude Desktop configuration

Happy hacking! 🎯