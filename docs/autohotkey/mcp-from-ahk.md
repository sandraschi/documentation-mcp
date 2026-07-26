# Calling MCP Servers from AHK

AHK scripts can call any MCP server that exposes **streamable HTTP** transport. Most fleet servers do.

## Prerequisites

No libraries needed — uses the WinHTTP COM object built into Windows.

## Basic JSON-RPC Call

```autohotkey
; Call any MCP tool via HTTP
CallMCP(host, toolName, args*) {
    whr := ComObject("WinHttp.WinHttpRequest.5.1")
    whr.Open("POST", host . "/mcp", false)
    whr.SetRequestHeader("Content-Type", "application/json")
    
    body := '{ "jsonrpc": "2.0", "id": 1, "method": "tools/call", '
          . '"params": { "name": "' toolName '", "arguments": {'
    
    for k, v in args
        body .= '"' k '": "' v '",'
    
    body := RTrim(body, ",") . '} } }'
    
    whr.Send(body)
    return whr.ResponseText
}

; Usage
result := CallMCP("http://127.0.0.1:10746", "list_scriptlets")
MsgBox(result)
```

## Fleet MCP Servers

| Server | Port | MCP Endpoint | Tools Available |
|--------|------|-------------|-----------------|
| autohotkey-mcp | 10746 | `/mcp` | list_scriptlets, run_scriptlet, stop_scriptlet, generate_scriptlet, help |
| arxiv-mcp | 10770 | `/mcp` | search_papers, get_paper_details, fetch_full_text, run_codehunt_scan |
| leanforge-mcp | 10855 | `/mcp` | submit_theorem, get_proof_status, validate_lean, list_jobs |
| games-mcp | 10987 | `/mcp` | chess analysis, tool listing, system status |
| aiwatcher-mcp | 64800 | stdio only | No HTTP — use claude desktop only |
| filesystem-mcp | — | stdio only | No HTTP |
| pywinauto-mcp | — | stdio only | No HTTP |

## Examples

### List available AHK scriptlets

```autohotkey
response := CallMCP("http://127.0.0.1:10746", "list_scriptlets")
MsgBox(response)
```

### Search arXiv papers

```autohotkey
response := CallMCP("http://127.0.0.1:10770", "search_papers", "query", "machine learning", "limit", "5")
MsgBox(response)
```

### Run an AHK scriptlet

```autohotkey
response := CallMCP("http://127.0.0.1:10746", "run_scriptlet", "script_id", "classic_pong.ahk")
MsgBox(response)
```

### Validate a Lean theorem

```autohotkey
response := CallMCP("http://127.0.0.1:10855", "validate_lean", "lean_source", "theorem add_comm (a b : Nat) : a + b = b + a := by { omega }")
MsgBox(response)
```

### List MCP tools from a server

```autohotkey
whr := ComObject("WinHttp.WinHttpRequest.5.1")
whr.Open("POST", "http://127.0.0.1:10746/mcp", false)
whr.SetRequestHeader("Content-Type", "application/json")
whr.Send('{ "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {} }')
MsgBox(whr.ResponseText)
```

## AHK as an MCP Server

You can also run an MCP server **from** AHK using the fleet's `HttpServer` library:

```autohotkey
#Include %A_ScriptDir%\lib\HttpServer.ahk

; Handle JSON-RPC calls
HandleRequest(data) {
    ; Parse JSON-RPC request, dispatch to tools
    return '{ "jsonrpc": "2.0", "id": 1, "result": { "tools": [] } }'
}

; Start HTTP server
server := HttpServer()
server.AddRoute("POST", "/mcp", HandleRequest)
server.Start(10800)
MsgBox("AHK MCP server running on port 10800")
```

## Caveats

- Servers using **stdio transport only** (aiwatcher, filesystem, pywinauto) cannot be reached via HTTP
- MCP tools are async — long-running tools may timeout
- Use `false` (synchronous) in `whr.Open()` to keep AHK's single-threaded model happy
- For concurrent calls, use `WinHttpRequest.enableRequestEvents()` with the Promise library
