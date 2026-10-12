# Figma MCP config reference

The Figma MCP server is a remote streamable-HTTP server at `https://mcp.figma.com/mcp`. Every host adds MCP servers its own way (a config file, a settings UI, or a CLI command), so follow your host's MCP documentation for where the definition goes. Two auth options exist: the host's built-in OAuth flow (simplest, when the host supports it), or a bearer token read from your environment.

## Generic server definition

Many hosts accept an `mcpServers` JSON object like this. Key names (`type`, `url`/`httpUrl`, `headers`) and environment-variable expansion differ between hosts, so adapt it to your host's schema.

```json
{
  "mcpServers": {
    "figma": {
      "type": "http",
      "url": "https://mcp.figma.com/mcp"
    }
  }
}
```

For the bearer-token option, add an `Authorization: Bearer <token>` header and the region header, ideally referencing `FIGMA_OAUTH_TOKEN` from the environment rather than pasting the literal token into a file you may commit:

```json
{
  "mcpServers": {
    "figma": {
      "type": "http",
      "url": "https://mcp.figma.com/mcp",
      "headers": {
        "Authorization": "Bearer ${FIGMA_OAUTH_TOKEN}",
        "X-Figma-Region": "us-east-1"
      }
    }
  }
}
```

## Option A: OAuth (recommended where supported)

Register the URL with no token, then complete the browser sign-in the host offers for that server. The host stores and refreshes the OAuth credentials itself.

Example (Claude Code):

```bash
claude mcp add --transport http --scope user figma https://mcp.figma.com/mcp
```

then run `/mcp`, select `figma`, and finish the sign-in.

## Option B: bearer token from the environment

Keep the token in `FIGMA_OAUTH_TOKEN` and the region header aligned with your Figma region.

Example (Claude Code CLI; the shell expands the variable once, so the literal token is stored in the host's config):

```bash
claude mcp add --transport http --scope user figma https://mcp.figma.com/mcp \
  --header "Authorization: Bearer $FIGMA_OAUTH_TOKEN" \
  --header "X-Figma-Region: us-east-1"
```

Example (Codex, `~/.codex/config.toml`):

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
http_headers = { "X-Figma-Region" = "us-east-1" }
```

These are examples only; check your host's current MCP documentation for the exact syntax, and for a project-shared config prefer a form that reads the token from the environment.

## Notes and options
- Scope: most hosts distinguish a user-wide server from a project-only one. Choose deliberately; do not commit literal tokens.
- For Option B, the bearer token must be available as `FIGMA_OAUTH_TOKEN` in the environment that launches the host.
- Keep the region header aligned with your Figma region. If your org uses another region, update `X-Figma-Region` consistently.
- Timeouts and output caps are host settings. Large `get_design_context` results may hit the host's MCP output cap or tool timeout; consult the host's documentation to raise them, or fetch smaller nodes via `get_metadata`.

## Env var setup (if missing, Option B)
- One-time set for current shell: `export FIGMA_OAUTH_TOKEN="<token>"`
- Persist for future sessions: add the export line to your shell profile (e.g., `~/.zshrc` or `~/.bashrc`), then restart the shell or your IDE.
- Verify before launching the host: `echo $FIGMA_OAUTH_TOKEN` should print a non-empty token.

## Setup + verification checklist
- Add the server with one of the options above, then confirm it appears in the host's MCP server list.
- Restart or reload the host's MCP connections after updating config and env vars.
- Ask the agent to list the Figma tools or run a simple call (e.g. `whoami`) to confirm the server is reachable.

## Troubleshooting
- Token not picked up: export `FIGMA_OAUTH_TOKEN` in the same shell that launches the host, or add it to your shell profile and restart. If your host stored the literal token when you registered the server, remove and re-add the server after changing the token.
- OAuth errors: re-authenticate through the host's MCP UI (Option A), or verify the bearer token is valid (Option B). Tokens copied from Figma should not include surrounding quotes.
- Network/headers: keep the `X-Figma-Region` header; if your org uses another region, update the header consistently across config and requests.

## Usage reminders
- The server is link-based: copy the Figma frame or layer link, then ask the MCP client to implement that URL. The client will extract the node ID from the link (it does not browse the page).
- If output feels generic, restate the project-specific rules from the main skill and ensure you follow the required flow (get_design_context → get_metadata if needed → get_screenshot).
