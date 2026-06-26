# Email MCP Integration Guide

## Overview

Email MCP is a comprehensive multi-service email platform supporting SMTP/IMAP providers, transactional email APIs, local testing services, and webhook integrations.

**Version**: 0.2.2
**Status**: Production Ready with MCPB Packaging
**Category**: Communication & Productivity
**FastMCP**: 3.1.1+.1 (Server-to-Server Communication)

## Features

### Core Functionality
- **Multi-Service Support**: SMTP/IMAP, SendGrid, Mailgun, Resend, Amazon SES, Postmark
- **Local Testing**: MailHog, Mailpit, MailCatcher, Inbucket
- **Webhook Integrations**: Slack, Discord, Telegram, GitHub
- **Header Decoding**: Automatically decodes UTF-8 Base64 and Quoted-Printable encoded email headers
- **Dynamic Configuration**: Add services at runtime without restart
- **Async Operations**: Non-blocking email operations

### AI Email Management (Orchestrator)
- **`weed_trash`**: AI-powered intelligent email cleanup
- **`email_summarizer`**: Smart inbox summaries by topic and sender
- **`smart_email_filter`**: AI-generated filtering rules
- **Server Compositing**: Combines email-mcp + local-llm-mcp
- **Direct Server Communication**: FastMCP 3.1.1+.1 enables cross-server collaboration for:
  - AI-assisted email composition and drafting
  - Intelligent email analysis and categorization
  - Automated response generation
  - Email content summarization and prioritization

## Installation

### MCPB Packaging (Recommended)
```bash
# Download and install MCPB package
curl -O https://github.com/your-org/email-mcp/releases/download/v0.2.2/email-mcp.mcpb
# Install via Claude Desktop or compatible MCP client
```

### Manual Installation
```bash
git clone https://github.com/your-org/email-mcp.git
cd email-mcp
pip install -e .
```

## Configuration

### Environment Variables
```bash
# SMTP/IMAP Configuration
export SMTP_SERVER="smtp.gmail.com"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export IMAP_SERVER="imap.gmail.com"

# API Services
export SENDGRID_API_KEY="your-sendgrid-key"
export MAILGUN_API_KEY="your-mailgun-key"
export RESEND_API_KEY="your-resend-key"
```

### MCP Configuration
Add to your MCP configuration:

```json
{
  "mcpServers": {
    "email-mcp": {
      "args": ["-m", "email_mcp.server"],
      "command": "python",
      "env": {
        "PYTHONPATH": "/path/to/email-mcp/src"
      }
    }
  }
}
```

## Usage Examples

### Basic Email Operations
```python
# Send an email
send_email(
    to="recipient@example.com",
    subject="Hello World",
    body="This is a test email",
    service="default"
)

# Check inbox
emails = check_inbox(service="default", limit=10)
for email in emails:
    print(f"Subject: {email['subject']}")
    print(f"From: {email['from']}")
```

### AI Email Management
```python
# AI-powered email cleanup
weed_trash(
    criteria="spam,marketing",
    dry_run=True
)

# Smart inbox summaries
summaries = email_summarizer(
    group_by="sender",
    time_range="1w"
)
```

## Supported Services

### Email Providers
- **Gmail**: SMTP/IMAP with App Passwords
- **Outlook/Hotmail**: Full SMTP/IMAP support
- **Yahoo Mail**: SMTP/IMAP
- **iCloud Mail**: SMTP/IMAP
- **ProtonMail**: SMTP/IMAP (special setup requirements - see ProtonMail section)

### Transactional APIs
- **SendGrid**: Enterprise email delivery
- **Mailgun**: Developer-friendly API
- **Resend**: Modern email API
- **Amazon SES**: AWS integration
- **Postmark**: Reliable delivery

### Local Testing
- **MailHog**: Web UI testing
- **Mailpit**: Modern testing
- **MailCatcher**: Simple testing
- **Inbucket**: Lightweight testing

### Webhook Services
- **Slack**: Channel notifications
- **Discord**: Channel/webhook integration
- **Telegram**: Bot integration
- **GitHub**: Issue/PR notifications

## Header Decoding Fix (v0.2.2)

Email MCP now automatically decodes encoded email headers:

**Before**: `=?UTF-8?B?VmVycGFzc2UgbmljaHQgdW5zZXIgMjDibMnDpHIgQW5nZWJvdA==?=`
**After**: `Verpasse nicht unser 2-fÃ¼r-1-Angebot`

This affects:
- Email subjects with special characters
- Sender names with non-ASCII characters
- Date headers with encoding
- All RFC 2047 encoded headers

## ProtonMail Setup

ProtonMail requires special configuration due to its security model:

### Free Accounts (ProtonMail Bridge)

**Requirements**: ProtonMail Bridge application

1. **Install Bridge**: Download from https://proton.me/mail/bridge
2. **Configure Account**: Set up your ProtonMail account in Bridge
3. **Local Servers**: Bridge creates local SMTP (port 1025) and IMAP (port 1143) servers

**Configuration**:
```bash
export SMTP_SERVER="127.0.0.1"
export SMTP_PORT="1025"
export IMAP_SERVER="127.0.0.1"
export IMAP_PORT="1143"
export SMTP_USER="your-username"
export SMTP_PASSWORD="your-password"
```

### Paid Accounts (Direct Access)

**Requirements**: ProtonMail paid plan

**Configuration**:
```bash
export SMTP_SERVER="mail.protonmail.com"
export SMTP_PORT="587"
export IMAP_SERVER="mail.protonmail.com"
export IMAP_PORT="993"
export SMTP_USER="your@protonmail.com"
export SMTP_PASSWORD="your-password"
```

**Setup Steps**:
1. Enable SMTP/IMAP in ProtonMail settings
2. Use your regular ProtonMail password
3. Configure Email MCP with the settings above

## Security Considerations

### Gmail App Passwords
Gmail requires App Passwords instead of regular passwords:
1. Enable 2-Step Verification
2. Generate App Password in Google Account settings
3. Use App Password as SMTP_PASSWORD

### API Key Security
- Store API keys securely (environment variables, secrets management)
- Rotate keys regularly
- Use least-privilege access

### Local Testing
- Use local testing services for development
- Never send real emails during testing
- Monitor local service logs

## Troubleshooting

### Connection Issues
```bash
# Test service connectivity
email_status(service="gmail")
```

### Header Encoding Problems
- Ensure UTF-8 encoding in email content
- Use proper character encoding for international content
- Check email client encoding settings

### API Rate Limits
- Monitor API usage and rate limits
- Implement retry logic for failed sends
- Use multiple service providers for redundancy

## Development

### Project Structure
```
email-mcp/
â”œâ”€â”€ src/email_mcp/
â”‚   â”œâ”€â”€ server.py          # Main MCP server
â”‚   â”œâ”€â”€ tools/             # Tool implementations
â”‚   â””â”€â”€ services/          # Email service handlers
â”œâ”€â”€ mcp-server/            # MCPB packaging
â”œâ”€â”€ monitoring/            # Health checks
â””â”€â”€ tests/                 # Test suite
```

### Standards Compliance
- âœ… MCPB Packaging (Claude Desktop ready)
- âœ… CI/CD Pipeline (GitHub Actions)
- âœ… Health Monitoring
- âœ… Comprehensive Testing
- âœ… Code Quality (Ruff, MyPy)

## FastMCP 3.1.1+.1 Server Communication

Email MCP leverages FastMCP 3.1.1+.1's server-to-server communication capabilities to collaborate with other MCP servers:

### Cross-Server Collaboration
- **Local LLM Integration**: Direct communication with local-llm-mcp for AI-powered email processing
- **Intelligent Composition**: AI-assisted email drafting and response generation
- **Content Analysis**: LLM-powered email categorization and prioritization
- **Automated Workflows**: Server compositing for complex email automation tasks

### Example Workflows
```python
# AI-assisted email composition
compose_email = await email_mcp.compose_with_ai(
    recipient="client@example.com",
    topic="project update",
    context="quarterly review"
)

# Intelligent email analysis
analysis = await email_mcp.analyze_with_llm(
    email_content=message,
    action="summarize,categorize,prioritize"
)
```

## Changelog

### v0.2.2 (2026-01-13)
- **Added**: FastMCP 3.1.1+.1 server-to-server communication capabilities
- **Added**: Direct collaboration with local-llm-mcp for AI email processing
- **Added**: Comprehensive ProtonMail setup documentation (Bridge vs Direct access)
- **Fixed**: Email header decoding for encoded subjects and sender names
- **Technical**: Added `decode_email_header()` function for RFC 2047 compliance

### v0.2.1 (2026-01-12)
- **Added**: AI Email Management Orchestrator
- **Added**: Server composition with local-llm-mcp
- **Added**: `weed_trash`, `email_summarizer`, `smart_email_filter` tools

### v0.2.0 (2026-01-12)
- **Added**: MCPB packaging support
- **Added**: CI/CD pipeline
- **Added**: Health monitoring
- **Added**: Comprehensive testing

### v0.1.0 (2026-01-01)
- **Added**: Multi-service email platform
- **Added**: SMTP/IMAP support
- **Added**: Basic service configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- **Documentation**: https://github.com/your-org/email-mcp
- **Issues**: https://github.com/your-org/email-mcp/issues
- **Discussions**: https://github.com/your-org/email-mcp/discussions

