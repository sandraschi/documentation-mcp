# Troubleshooting Guide

## Table of Contents

- [Common Issues](#common-issues)
- [Claude Desktop Integration](#claude-desktop-integration)
- [Error Messages](#error-messages)
- [Performance Problems](#performance-problems)
- [Backup Failures](#backup-failures)
- [Restoration Issues](#restoration-issues)
- [Network Problems](#network-problems)
- [Debugging](#debugging)
- [Getting Help](#getting-help)

## Common Issues

### Server Won't Start

**Symptoms:**

- Server fails to start
- Port already in use error
- Permission denied errors

**Solutions:**

1. **Port in use**

   ```bash
   # Find process using port 8000
   netstat -ano | findstr :8000
   # Then kill the process
   taskkill /PID <PID> /F
   ```

2. **Permission issues**
   - Run as administrator
   - Check file permissions on the installation directory

3. **Missing dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Authentication Problems

**Symptoms:**

- 401 Unauthorized errors
- Invalid API key messages

**Solutions:**

1. Verify API key in requests
2. Check server logs for authentication errors
3. Regenerate API key if needed

## Claude Desktop Integration

### Installation Issues

**Symptoms:**

- DXT package fails to install
- Extension doesn't appear in Claude Desktop
- Permission errors during installation

**Solutions:**

1. **DXT Installation Fails**
   - Ensure you're using a recent version of Claude Desktop with DXT support
   - Check the console output in Claude Desktop (View > Toggle Developer Tools > Console)
   - Verify the DXT package isn't corrupted by redownloading it

2. **Extension Not Appearing**
   - Restart Claude Desktop after installation
   - Check the extensions list in Settings > Extensions
   - Look for any error messages in the developer console

3. **Permission Issues**
   - Run Claude Desktop as administrator
   - Check file permissions in the extension directory:
     - Windows: `%APPDATA%\Claude\extensions`
     - macOS: `~/Library/Application Support/Claude/extensions`
     - Linux: `~/.config/Claude/extensions`

### Runtime Issues

**Symptoms:**

- MCP server doesn't start automatically
- Web UI is not accessible
- Console shows connection errors

**Solutions:**

1. **Server Not Starting**
   - Check the server logs in the extension directory
   - Verify Python is installed and in the system PATH
   - Look for port conflicts (default port is 8000)

2. **Web UI Issues**
   - Clear browser cache if UI doesn't load
   - Check for JavaScript errors in the browser console
   - Verify CORS headers are properly set in the server response

3. **Connection Problems**
   - Check if the server is running and listening on the correct port
   - Verify the URL in the browser matches the server configuration
   - Look for firewall rules blocking the connection

## Error Messages

### "Backup job failed: Insufficient disk space"

**Solution:**

- Free up disk space on the destination drive
- Adjust retention policy to keep fewer backups
- Use compression to reduce backup size

### "Permission denied when accessing backup location"

**Solution:**

```bash
# On Linux/macOS
chmod -R 755 /path/to/backup/location
chown -R username:group /path/to/backup/location

# On Windows
icacls "D:\Backups" /grant "Users:(OI)(CI)F" /T
```

### "Failed to connect to database"

**Solution:**

1. Check if database service is running
2. Verify connection string in config
3. Check database user permissions

## Performance Problems

### Slow Backups

**Possible causes and solutions:**

1. **Network latency**
   - Use local backup if possible
   - Check network connection

2. **High system load**
   - Schedule backups during off-hours
   - Adjust compression level
   - Exclude unnecessary files

3. **Disk I/O bottlenecks**
   - Use faster storage (SSD)
   - Defragment HDD
   - Check for disk errors

## Backup Failures

### Incomplete Backups

**Checklist:**

1. Verify source files are accessible
2. Check available disk space
3. Review backup logs for errors
4. Check file permissions

### Corrupted Backups

**Recovery steps:**

1. Try restoring to a different location
2. Use built-in repair tools
3. Restore from a previous backup

## Network Problems

### Connection Timeouts

**Troubleshooting steps:**

1. Verify network connectivity
2. Check firewall settings

   ```bash
   # Windows
   netsh advfirewall firewall show rule name=all | findstr "8000"

   # Linux
   sudo ufw status
   ```

3. Test with different network

### Slow Network Transfers

**Optimization tips:**

1. Use wired connection instead of WiFi
2. Adjust MTU size
3. Enable network compression if available

## Debugging

### Server Logs

Logs are stored in the following locations:

- **Windows**: `%APPDATA%\HasleoBackupMCP\logs\`
- **macOS/Linux**: `~/.hasleo_backup_mcp/logs/`

### Enabling Debug Mode

1. **Using Environment Variable**

   ```bash
   set HASLEO_LOG_LEVEL=DEBUG
   ```

2. **In Configuration**

   ```yaml
   logging:
     level: DEBUG
     file: multi_backup_mcp.log
   ```

### Common Log Patterns

1. **Port Already in Use**

   ```
   [ERROR] Address already in use: ('0.0.0.0', 8000)
   ```

   - Another process is using the port
   - Change the port in config or stop the conflicting process

2. **Permission Denied**

   ```
   [ERROR] [Errno 13] Permission denied: '/path/to/file'
   ```

   - The server doesn't have permission to access the specified path
   - Run as administrator or adjust file permissions

3. **Connection Refused**

   ```
   [ERROR] ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
   ```

   - Server is not running
   - Check server logs for startup errors

## Getting Help

### Gathering Information

Before seeking help, collect:

1. Log files
2. Configuration (redact sensitive data)
3. Exact error messages
4. Steps to reproduce

### Support Channels

1. [GitHub Issues](https://github.com/sandraschi/hasleo-backup-mcp/issues)
2. Documentation
3. Community Forum (if available)

### Debug Mode

Enable debug logging in `config.yaml`:

```yaml
logging:
  level: debug
  file: debug.log
```

Then restart the server and reproduce the issue.
