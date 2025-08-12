# Deployment Guide - MCP CTF Challenge Server

## 🚀 Render Deployment

### Prerequisites
- GitHub account with the repository
- Render account (free tier works)

### Step-by-Step Deployment

1. **Prepare Repository**
   ```bash
   git add .
   git commit -m "Initial MCP CTF server implementation"
   git push origin main
   ```

2. **Create Render Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `mcp-ctf-challenge` repository

3. **Configure Service**
   - **Name:** `mcp-ctf-server` (or your preferred name)
   - **Environment:** `Docker`
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Build Command:** (leave empty - Docker handles this)
   - **Start Command:** (leave empty - Docker handles this)

4. **Environment Variables**
   ```
   RENDER=true
   PORT=8000
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (usually 2-5 minutes)
   - Note your service URL: `https://your-app-name.onrender.com`

### Post-Deployment Verification

1. **Health Check**
   ```bash
   curl https://your-app-name.onrender.com/
   ```
   Should return: `{"message": "MCP CTF Server is running", "status": "healthy"}`

2. **Challenge List**
   ```bash
   curl https://your-app-name.onrender.com/challenges
   ```
   Should return JSON with all 7 challenges

## 🔧 Local Development

### Setup
```bash
# Clone repository
git clone <your-repo-url>
cd mcp-ctf-challenge

# Install dependencies (optional - for testing)
pip install -r requirements.txt

# Run server locally
cd src && python main.py
```

### Testing with Claude Desktop

1. **Add to MCP Settings**
   Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`
   ```json
   {
     "mcpServers": {
       "ctf-local": {
         "command": "python",
         "args": ["/full/path/to/mcp-ctf-challenge/src/main.py"],
         "cwd": "/full/path/to/mcp-ctf-challenge/src"
       }
     }
   }
   ```

2. **Restart Claude Desktop**

3. **Test Connection**
   - Open Claude Desktop
   - Look for "Connected MCP Servers" in the interface
   - Try using one of the challenge tools

## 🌐 Remote MCP Connection

### For Deployed Server

The server includes a full HTTP-to-MCP bridge for remote connections. However, Claude Desktop currently only supports stdio transport, so you need to use the provided proxy script.

See [REMOTE_SETUP.md](REMOTE_SETUP.md) for detailed instructions on:
- Setting up the HTTP proxy for remote connections
- Configuring Claude Desktop
- Testing the connection
- Troubleshooting common issues

Quick configuration example using the proxy:
```json
{
  "mcpServers": {
    "ctf-remote": {
      "command": "python3",
      "args": [
        "/path/to/mcp_http_proxy.py",
        "https://your-app-name.onrender.com"
      ]
    }
  }
}
```

**Important:** You must have the `mcp_http_proxy.py` script and `aiohttp` installed locally to connect to remote servers.

## 🔒 Security Considerations

### For CTF Organizers

1. **Isolation**
   - Deploy in isolated environment
   - Use separate Render account for CTF
   - Monitor resource usage

2. **Access Control**
   - Share URL only with participants
   - Consider adding basic authentication if needed
   - Monitor logs for abuse

3. **Resource Limits**
   - Render free tier has limitations
   - Monitor for excessive usage
   - Consider upgrading for large events

### For Participants

⚠️ **WARNING:** This server contains intentional vulnerabilities

- **Educational Use Only:** Do not use techniques on unauthorized systems
- **Responsible Disclosure:** Report any unintended vulnerabilities
- **Ethical Hacking:** Follow responsible disclosure practices

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Test imports locally
   python test_server.py
   ```

2. **Port Issues**
   - Render automatically assigns PORT environment variable
   - Local development uses port 8000 by default

3. **MCP Connection Issues**
   - Verify Claude Desktop configuration
   - Check file paths are absolute
   - Restart Claude Desktop after config changes

4. **Challenge Not Working**
   - Check server logs in Render dashboard
   - Verify tool names match exactly
   - Test with simple tools first

### Debug Commands

```bash
# Check server status
curl https://your-app-name.onrender.com/

# List available challenges
curl https://your-app-name.onrender.com/challenges

# View Render logs
# Go to Render Dashboard → Your Service → Logs
```

## 📊 Monitoring

### Render Dashboard
- Monitor deployment status
- View application logs
- Check resource usage
- Monitor response times

### Health Endpoints
- `GET /` - Basic health check
- `GET /challenges` - List all challenges
- `POST /mcp` - MCP protocol endpoint

## 🔄 Updates

### Deploying Changes
1. Push changes to GitHub
2. Render automatically redeploys
3. Monitor deployment in dashboard
4. Verify changes with health check

### Rollback
1. Go to Render Dashboard
2. Select your service
3. Go to "Deploys" tab
4. Click "Rollback" on previous successful deploy

---

## 📞 Support

For deployment issues:
- Check Render documentation
- Review server logs
- Test locally first
- Verify MCP client configuration

Happy deploying! 🚀