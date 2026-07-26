# Configuration Reference

## Table of Contents

- [Server Configuration](#server-configuration)
- [Backup Settings](#backup-settings)
- [Scheduling](#scheduling)
- [Security](#security)
- [Notifications](#notifications)
- [Logging](#logging)
- [Advanced](#advanced)

## Server Configuration

### Basic Settings

```yaml
server:
  # Server host (0.0.0.0 for all interfaces)
  host: 0.0.0.0

  # Server port
  port: 8000

  # Base URL for API endpoints
  base_url: /api/v1

  # Enable/disable debug mode (not recommended for production)
  debug: false
```

### Performance

```yaml
server:
  # Maximum number of concurrent backup jobs
  max_concurrent_jobs: 3

  # Maximum upload size in MB
  max_upload_size: 1024

  # Request timeout in seconds
  timeout: 300
```

## Backup Settings

### Defaults

```yaml
backup:
  # Default backup destination directory
  default_destination: /path/to/backups

  # Default retention policy in days
  retention_days: 30

  # Default compression level (none, fast, normal, high)
  compression: normal

  # Split backup into multiple files of this size (MB)
  split_size: 4096
```

### Advanced Backup Options

```yaml
backup:
  # Enable/disable file verification after backup
  verify: true

  # Enable/disable encryption
  encryption:
    enabled: true
    algorithm: AES-256
    # Path to encryption key file (leave empty to generate)
    key_file: /path/to/keyfile

  # File exclusions (glob patterns)
  exclude_patterns:
    - "**/node_modules/**"
    - "**/.git/**"
    - "**/temp/**"
    - "**/tmp/**"
    - "**/*.tmp"
    - "**/*.log"
```

## Scheduling

### Scheduler Settings

```yaml
scheduler:
  # Enable/disable the scheduler
  enabled: true

  # Timezone for scheduled jobs
  timezone: UTC

  # Maximum number of retry attempts for failed jobs
  max_retries: 3

  # Delay between retries in minutes
  retry_delay: 5
```

### Job History

```yaml
scheduler:
  # Maximum number of job history entries to keep
  max_history: 100

  # Clean up job history older than X days
  history_retention_days: 30
```

## Security

### Authentication

```yaml
security:
  # Enable/disable API key authentication
  require_auth: true

  # API key for authentication
  api_key: your_secure_api_key_here

  # Enable CORS (Cross-Origin Resource Sharing)
  enable_cors: false

  # Allowed CORS origins
  allowed_origins:
    - https://example.com
    - http://localhost:3000
```

### Rate Limiting

```yaml
security:
  rate_limiting:
    # Enable/disable rate limiting
    enabled: true

    # Maximum requests per minute per IP
    requests: 100

    # Time window in minutes
    window: 1

    # Maximum requests per day per API key
    daily_limit: 1000
```

## Notifications

### Email Notifications

```yaml
notifications:
  email:
    enabled: false
    smtp_server: smtp.example.com
    smtp_port: 587
    use_tls: true
    username: user@example.com
    password: your_password
    from: backup@example.com
    to:
      - admin@example.com

    # Events to notify about
    events:
      - backup_started
      - backup_completed
      - backup_failed
      - schedule_created
      - schedule_updated
      - schedule_deleted
```

### Webhook Notifications

```yaml
notifications:
  webhook:
    enabled: false
    url: https://example.com/webhook
    secret: your_webhook_secret

    # Events to send to webhook
    events:
      - backup_started
      - backup_completed
      - backup_failed
      - error_occurred
```

## Logging

### Log Configuration

```yaml
logging:
  # Log level (debug, info, warning, error, critical)
  level: info

  # Log file path
  file: logs/hasleo-backup-mcp.log

  # Maximum log file size in MB before rotation
  max_size: 10

  # Number of backup log files to keep
  backup_count: 5

  # Log format
  format: "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"

  # Date format in logs
  date_format: "%Y-%m-%d %H:%M:%S"
```

## Advanced

### Database

```yaml
database:
  # Database URL (sqlite, postgresql, mysql)
  url: sqlite:///data/hasleo-backup-mcp.db

  # Enable SQL query logging
  echo: false

  # Connection pool settings
  pool_size: 5
  max_overflow: 10
  pool_timeout: 30
  pool_recycle: 3600
```

### Maintenance

```yaml
maintenance:
  # Enable automatic database cleanup
  auto_cleanup: true

  # Run cleanup at this time (HH:MM)
  cleanup_time: "02:00"

  # Days to keep job history
  history_retention_days: 30

  # Days to keep log files
  log_retention_days: 7
```

### Environment Variables

All configuration options can be set using environment variables with the `HASLEO_` prefix:

```bash
# Example: Set server port
export HASLEO_SERVER_PORT=8080

# Example: Set API key
export HASLEO_SECURITY_API_KEY=your_key_here

# Example: Enable debug mode
export HASLEO_SERVER_DEBUG=true
```

### Configuration Precedence

1. Command-line arguments (highest priority)
2. Environment variables
3. Configuration file
4. Default values (lowest priority)
