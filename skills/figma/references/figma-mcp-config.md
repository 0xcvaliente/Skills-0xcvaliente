# Figma MCP config reference

Register the remote Figma MCP server (`https://mcp.figma.com/mcp`) with Claude Code as a streamable HTTP server. Two auth options: Claude Code's built-in OAuth flow (simplest), or a bearer token pulled from your environment.

## Option A: OAuth (recommended)

```bash
claude mcp add --transport http --scope user figma https://mcp.figma.com/mcp
```

Then, inside Claude Code, run `/mcp`, select `figma`, and complete the browser sign-in. Claude Code stores and refreshes the OAuth credentials itself.

## Option B: bearer token from the environment

Keep the token in `FIGMA_OAUTH_TOKEN` and the region header aligned with your Figma region. With the CLI (the shell expands the variable once, so the literal token is stored in your Claude Code config):

```bash
claude mcp add --transport http --scope user figma https://mcp.figma.com/mcp \
  --header "Authorization: Bearer $FIGMA_OAUTH_TOKEN" \
  --header "X-Figma-Region: us-east-1"
```

Or, to keep the token out of the config and share the setup with a project, add a project-scoped `.mcp.json` at the repo root. Claude Code expands `${VAR}` at launch, so the token is read from the environment each time:

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

## Notes and options
- `--scope user` makes the server available in every project; omit it (local scope, this project only) or use `--scope project` (writes `.mcp.json`) as needed.
- For Option B, the bearer token must be available as `FIGMA_OAUTH_TOKEN` in the environment that launches Claude Code.
- Keep the region header aligned with your Figma region. If your org uses another region, update `X-Figma-Region` consistently.
- Optional timeouts: Claude Code reads `MCP_TIMEOUT` (server startup, in ms) and `MCP_TOOL_TIMEOUT` (tool calls, in ms) from the environment, e.g. `MCP_TIMEOUT=10000 claude`. Large `get_design_context` results may also hit the MCP output cap; raise `MAX_MCP_OUTPUT_TOKENS` or fetch smaller nodes via `get_metadata`.

## Env var setup (if missing, Option B)
- One-time set for current shell: `export FIGMA_OAUTH_TOKEN="<token>"`
- Persist for future sessions: add the export line to your shell profile (e.g., `~/.zshrc` or `~/.bashrc`), then restart the shell or your IDE.
- Verify before launching Claude Code: `echo $FIGMA_OAUTH_TOKEN` should print a non-empty token.

## Setup + verification checklist
- Add the server with one of the options above. `claude mcp list` (or `claude mcp get figma`) should show it.
- Restart Claude Code after updating config and env vars (or run `/mcp` to check the server's status and reconnect).
- Ask Claude to list the Figma tools or run a simple call (e.g. `whoami`) to confirm the server is reachable.

## Troubleshooting
- Token not picked up: Export `FIGMA_OAUTH_TOKEN` in the same shell that launches Claude Code, or add it to your shell profile and restart. If you used the CLI form of Option B, re-run `claude mcp add` after changing the token (`claude mcp remove figma` first), because the old value was stored literally.
- OAuth errors: Re-run `/mcp` and re-authenticate (Option A), or verify the bearer token is valid (Option B). Tokens copied from Figma should not include surrounding quotes.
- Network/headers: Keep the `X-Figma-Region` header; if your org uses another region, update the header consistently across config and requests.

## Usage reminders
- The server is link-based: copy the Figma frame or layer link, then ask the MCP client to implement that URL. The client will extract the node ID from the link (it does not browse the page).
- If output feels generic, restate the project-specific rules from the main skill and ensure you follow the required flow (get_design_context → get_metadata if needed → get_screenshot).
