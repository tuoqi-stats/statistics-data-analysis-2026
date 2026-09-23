# GitHub Git Data API Fallback

Use this only when normal Git transport fails with a network/proxy error such as `502` or `CONNECT tunnel failed`, and authenticated requests to `api.github.com` are available.

## Preconditions

- Confirm the repository owner, name, branch, and intended files.
- Obtain an access token through the configured credential manager or another approved secret store. Keep it in a protected environment variable; never print it or place it in a command transcript.
- Do not use this fallback to bypass a history conflict or to overwrite remote work without explicit approval.

## Workflow

1. Read the current remote branch reference. For a non-empty branch, use its commit SHA as the parent. For an empty repository, omit `parents` when creating the first commit.
2. Create one blob per intended file. Normalize text files to LF before base64 encoding if the local Git configuration stores LF; treat binary files as opaque bytes.
3. Create a tree containing the blob SHAs. Preserve the repository-relative paths and appropriate modes (`100644` for ordinary files, `100755` for executable files).
4. Create a commit with the tree, parent commit when present, and the requested message.
5. Move the existing branch reference with a non-force update. For an empty repository, create `refs/heads/<branch>`.
6. Query the branch or latest commit endpoint and verify that the returned SHA matches the created commit.
7. When normal Git transport becomes available, reconcile the local and remote histories before pushing again. A force push requires explicit approval and a reviewed reason.

## Line Ending Warning

If API blobs are created directly from Windows CRLF content while local Git commits use LF, the resulting blob SHAs and histories can diverge. Normalize text content consistently before encoding, then verify the resulting commit rather than assuming the HTTP request succeeded.

## Failure Handling

- `401` or `403`: stop and report an authentication or permission issue without exposing the token.
- `404`: verify the owner, repository, branch, and token visibility.
- `409`: treat as a concurrent update or history conflict; re-read the remote tip and inspect before retrying.
- Any response that is not valid JSON for the expected endpoint: report the HTTP status and stop rather than constructing the next request from an error page.