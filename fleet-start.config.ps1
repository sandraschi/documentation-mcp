# Per-repo fleet start config for documentation-mcp
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'documentation-mcp'
    BackendPort  = 11033
    FrontendPort = 11032
    HealthPath   = '/api/settings'
    WebRoot      = 'D:\Dev\repos\documentation-mcp\web_sota'
    Backend = @{
        Kind          = 'uvicorn'
        UvicornTarget = 'docs_mcp.server:app'
        SyncExtras    = @('dev')
        Env           = @{ WEB_PORT = '11033' }
    }
    Frontend = @{
        Kind           = 'vite-npm'
        PackageManager = 'npm'
        PortEnvVar     = 'VITE_PORT'
        ApiTargetEnv   = 'VITE_API_TARGET'
    }
}
