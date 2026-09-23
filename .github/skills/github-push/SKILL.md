---
name: github-push
description: "Use when publishing local files or commits to GitHub: initialize a repository, create or configure a remote, commit and push changes, verify the remote state, or recover from push/clone failures such as 502, CONNECT tunnel failed, and non-fast-forward."
argument-hint: "[repository or push goal]"
user-invocable: true
---

# GitHub Push

Safely publish a local project to a GitHub repository and verify the result.

## When to Use

- The user asks to push, upload, publish, commit, or sync local files to GitHub.
- The local directory has no Git repository yet.
- A remote repository must be created or configured.
- `git push` or `git clone` fails and needs diagnosis or recovery.

## Safety Rules

- Inspect the current directory, repository status, remotes, and branch before changing anything.
- Never print, paste, or commit access tokens, passwords, or credential-helper output.
- Do not force-push, overwrite remote history, delete a repository, or discard local changes without explicit approval.
- Preserve unrelated user changes and stop before resolving an ambiguous history conflict.
- Prefer the Git CLI. Use the GitHub REST Git Data API only when normal Git transport is unavailable and the user has authorized that fallback.

## Procedure

1. Identify the target directory, repository name, GitHub owner, target branch, visibility, and commit message. Ask only for missing information that cannot be inferred safely.
2. Inspect with `git status --short --branch`, `git remote -v`, and `git branch --show-current`. Confirm the directory is the intended project.
3. If `.git` is absent, initialize the repository, choose or create the target branch, stage only intended files, and make an initial commit. Do not add secrets or generated artifacts without checking them first.
4. If the remote is missing, add the GitHub remote. If the repository does not exist, create it through an authenticated GitHub mechanism available in the environment; never echo the credential.
5. Review the staged diff, then commit with a concise message when there are changes. If there is nothing to commit, continue to remote verification rather than creating an empty commit.
6. Push normally, using upstream tracking on the first push: `git push --set-upstream origin <branch>`.
7. Verify locally with `git status --short --branch` and `git log -1 --oneline`. Verify the remote tip through the GitHub UI or authenticated API without exposing credentials.
8. Classify failures before retrying:
   - Authentication or permission errors: check the remote URL and credential configuration; do not request or display the secret in chat.
   - `non-fast-forward`: fetch and inspect both histories. Reconcile explicitly; do not force-push by default.
   - `502`, `CONNECT tunnel failed`, or Git transport failure: use the Git Data API procedure in [api-push.md](./references/api-push.md) only if API access is available.
   - A suspiciously successful clone or push: verify that files exist and the expected commit is present.
9. Report the remote, branch, commit, verification result, and any remaining limitation.

## Completion Criteria

- The intended files are committed and the commit is reachable from the intended remote branch.
- No unrelated changes were overwritten.
- The final remote state was verified, or the exact blocker and next safe action were reported.