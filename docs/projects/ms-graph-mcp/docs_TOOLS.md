# Tool reference

All tools are FastMCP portmanteaus: one function per domain with an
`operation` discriminator. Every tool returns
`{"success": bool, "message": str, "data": ...}`; failures add `error`,
`error_type` and `suggestions`.

**Auth first:** every data tool fails with `error_type: "auth_required"`
until `auth_ops(operation="login")` completes.

## auth_ops

Sign-in lifecycle (MSAL device code).

| operation | Behavior |
|-----------|----------|
| `status` | Returns auth state; also completes a pending login once the user signed in |
| `login` | Starts the device flow: returns `user_code` + `verification_uri` |
| `logout` | Clears the stored token |

## calendar_ops

Outlook calendar of the signed-in account.

| operation | Args | Behavior |
|-----------|------|----------|
| `list_week` | `start_date` (optional anchor) | Events for the current week, sorted |
| `list_range` | `start_date`, `end_date` | Events in the date range |
| `create` | `subject`, `start`, `end`, `body`?, `location`? | Creates an event |
| `update` | `event_id` + any field | Patches an event |
| `cancel` | `event_id` | Deletes an event |
| `find_free_slots` | `start_date`, `end_date`, `duration_min` | Gaps in Mon-Fri 09:00-17:00 (max 20) |

## todo_ops

Microsoft To-Do.

| operation | Args | Behavior |
|-----------|------|----------|
| `list_lists` | - | All task lists |
| `list_tasks` | `list_id`, `limit` | Tasks in a list (newest first) |
| `add` | `list_id`, `title`, `due`? | Adds a task |
| `complete` | `list_id`, `task_id` | Marks completed |
| `delete` | `list_id`, `task_id` | Removes a task |

## contacts_ops

Outlook contacts.

| operation | Args | Behavior |
|-----------|------|----------|
| `list` | `limit` | Contacts sorted by display name |
| `search` | `query`, `limit` | Free-text search (`$search`) |
| `create` | `given_name`/`surname`/`email`/`phone`/`company` | Creates a contact |
| `update` | `contact_id` + fields | Patches a contact |
| `delete` | `contact_id` | Removes a contact |

## onedrive_ops

OneDrive files.

| operation | Args | Behavior |
|-----------|------|----------|
| `list` | `path` ('' = root), `limit` | Folder/file listing with sizes |
| `read_text` | `path` | Returns file content as text |
| `upload` | `path`, `filename`, `content` | Creates/overwrites a text file |
| `download` | `path` | Saves to `%LOCALAPPDATA%\ms-graph-mcp\downloads\`, returns local path |
| `create_share_link` | `path` | Anonymous view link |

Paths use Graph syntax: `Documents/notes.txt` (no leading slash).

## profile_ops

| operation | Behavior |
|-----------|----------|
| `me` | Profile card (name, mail, job title, company, city, country) |
| `photo` | Profile photo as a data URL |

## ms_graph_health / show_health_prefab

Health: auth state, version, uptime, optional live Graph probe.
`show_health_prefab` renders the same as a chat card (PrefabApp).

## Error types

| error_type | Meaning | Recovery |
|------------|---------|----------|
| `auth_required` | No valid token | Run `auth_ops(login)` |
| `auth_pending` | User has not finished sign-in | Complete it, retry |
| `auth_declined` / `auth_invalid_grant` | Consent denied / refresh revoked | Re-run login |
| `auth_bad_client` | `MSG_CLIENT_ID` invalid | Fix config |
| `rate_limit` | Graph throttling (~10k req/10 min) | Wait 60s, shrink range |
| `not_found` | Bad id/path | Verify the id/path |
| `forbidden` | Scope missing | Re-consent with MSG_SCOPES |
