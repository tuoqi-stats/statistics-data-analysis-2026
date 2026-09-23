#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub Git Data API 推送工具。

用途：在 `git push` 走不通（沙箱 502 / CONNECT tunnel failed）时，
绕过 git 协议，直接用 REST API 把本地文件推送到远程分支。
也可用于只想推送部分文件、不产生本地 commit 的场景。

只依赖 Python 标准库，无需 pip 安装。

用法示例：

  # 1) 预演：只列出将推送的文件 + 查询远程 HEAD，不产生任何写入
  python api_push.py --repo tuoqi-stats/my-repo --all --dry-run

  # 2) 推送指定文件
  python api_push.py --repo tuoqi-stats/my-repo --paths README.md src/main.py -m "更新说明"

  # 3) 推送整个目录（目录名前缀匹配，递归）
  python api_push.py --repo tuoqi-stats/my-repo --paths docs/ -m "同步文档"

  # 4) 推送所有未被 .gitignore 排除的文件（tracked + untracked）
  python api_push.py --repo tuoqi-stats/my-repo --all -m "同步"

  # 5) 同时删除远程文件
  python api_push.py --repo tuoqi-stats/my-repo --paths x.md --delete old.md -m "整理"

  # 6) 推送后把本地 git 对齐到远程（会 git reset --hard）
  python api_push.py --repo tuoqi-stats/my-repo --all -m "..." --sync-local

退出码：0 成功；1 失败；2 参数/安全检查不通过。
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
BLOCK_SIZE = 100 * 1024 * 1024   # GitHub 单文件硬上限
WARN_SIZE = 50 * 1024 * 1024     # 超过则告警

# 疑似凭据文件：命中则拒绝推送，除非显式加 --allow-secrets
SECRET_PATTERNS = [
    r"(^|/)\.env(\.|$)", r"\.pem$", r"\.key$", r"\.pfx$", r"\.p12$",
    r"(^|/)id_rsa", r"(^|/)id_ed25519", r"credential", r"secret",
    r"(^|/)\.npmrc$", r"(^|/)\.netrc$", r"token\.json$",
]


def log(msg: str) -> None:
    print(msg, flush=True)


def die(msg: str, code: int = 1) -> None:
    print(f"[错误] {msg}", file=sys.stderr, flush=True)
    sys.exit(code)


# --------------------------------------------------------------------------
# token / HTTP
# --------------------------------------------------------------------------

def get_token() -> str:
    """优先取环境变量 GITHUB_TOKEN，否则从 git 凭据管理器拿。绝不回显 token。"""
    env = os.environ.get("GITHUB_TOKEN")
    if env:
        return env.strip()
    try:
        out = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=30,
        ).stdout or ""
    except Exception as exc:  # noqa: BLE001
        die(f"调用 git credential fill 失败：{exc}")
    for line in out.splitlines():
        if line.startswith("password="):
            return line[len("password="):].strip()
    die("未能从 git 凭据管理器取到 token。请先配置 GitHub 凭据，或设置环境变量 GITHUB_TOKEN。")
    return ""  # unreachable


def api(token: str, method: str, path: str, body=None, timeout: int = 60):
    """调用 api.github.com。失败时抛出带响应正文的 RuntimeError。"""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        API + path, data=data, method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "workbuddy-github-push-skill",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {method} {path}\n{detail[:800]}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f"网络不可达 {method} {path}：{exc.reason}") from None


# --------------------------------------------------------------------------
# 文件收集与安全检查
# --------------------------------------------------------------------------

def git_out(args: list[str]) -> str:
    try:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=60,
        ).stdout or ""
    except Exception:  # noqa: BLE001
        return ""


def collect_all_files() -> list[str]:
    """collect all files: git ls-files -co --exclude-standard (respects .gitignore)."""
    out = git_out(["ls-files", "-co", "--exclude-standard"])
    files = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if files:
        return files
    # 非 git 仓库时的兜底：遍历目录，排除 .git
    result = []
    for root, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in names:
            result.append(os.path.relpath(os.path.join(root, name), ".").replace("\\", "/"))
    return result


def expand_paths(patterns: list[str]) -> list[str]:
    """展开 --paths：支持文件与目录前缀。"""
    found: list[str] = []
    for pat in patterns:
        pat = pat.replace("\\", "/").rstrip("/")
        if os.path.isfile(pat):
            found.append(pat)
        elif os.path.isdir(pat):
            for root, dirs, names in os.walk(pat):
                dirs[:] = [d for d in dirs if d != ".git"]
                for name in names:
                    found.append(os.path.join(root, name).replace("\\", "/"))
        else:
            die(f"--paths 指定的路径不存在：{pat}", 2)
    return found


def check_secrets(files: list[str], allow: bool) -> list[str]:
    hits = [f for f in files if any(re.search(p, f, re.I) for p in SECRET_PATTERNS)]
    if hits and not allow:
        print("[阻断] 以下文件疑似凭据/密钥，已停止推送：", file=sys.stderr)
        for f in hits:
            print(f"  - {f}", file=sys.stderr)
        print("如确认要推送（危险，会进入 git 历史且难以彻底删除），加 --allow-secrets。",
              file=sys.stderr)
        sys.exit(2)
    return hits


def describe(files: list[str]) -> tuple[list[str], list[str]]:
    """返回 (文本文件, 二进制文件)，顺便做体积检查。"""
    text, binary = [], []
    for f in files:
        size = os.path.getsize(f)
        if size > BLOCK_SIZE:
            die(f"文件超过 GitHub 100MB 上限，需改用 Git LFS 或 Releases：{f}（{size/1048576:.1f}MB）", 2)
        if size > WARN_SIZE:
            log(f"  [提示] 大文件 {f}（{size/1048576:.1f}MB），推送可能较慢")
        with open(f, "rb") as fh:
            head = fh.read(8000)
        (binary if b"\x00" in head else text).append(f)
    return text, binary


def read_blob_content(path: str, is_binary: bool) -> bytes:
    with open(path, "rb") as fh:
        raw = fh.read()
    if is_binary:
        return raw
    # 关键：统一 LF，避免与 git 正常提交（LF）的 blob SHA 分叉
    return raw.replace(b"\r\n", b"\n")


# --------------------------------------------------------------------------
# 推送主流程
# --------------------------------------------------------------------------

def get_ref(token: str, repo: str, branch: str):
    """返回 parent commit sha；空仓库返回 None。"""
    try:
        return api(token, "GET", f"/repos/{repo}/git/ref/heads/{branch}")["object"]["sha"]
    except RuntimeError as exc:
        if "HTTP 404" in str(exc):
            return None
        raise


def push(token: str, repo: str, branch: str, files: list[str],
         deletes: list[str], message: str, sync_local: bool) -> str:
    parent = get_ref(token, repo, branch)
    if parent:
        base_tree = api(token, "GET", f"/repos/{repo}/git/commits/{parent}")["tree"]["sha"]
        log(f"远程 {branch} 当前 HEAD：{parent[:10]}")
    else:
        base_tree = None
        log(f"远程 {branch} 为空仓库（无 parent）")

    text_files, binary_files = describe(files)
    binary_set = set(binary_files)

    tree_entries = []
    for path in files:
        content = read_blob_content(path, path in binary_set)
        blob = api(token, "POST", f"/repos/{repo}/git/blobs",
                   {"content": base64.b64encode(content).decode("ascii"), "encoding": "base64"})
        mode = index_mode(path)
        tree_entries.append({"path": path, "mode": mode, "type": "blob", "sha": blob["sha"]})
        log(f"  blob {path}  ->  {blob['sha'][:10]}")

    for path in deletes:
        tree_entries.append({"path": path, "mode": "100644", "type": "blob", "sha": None})
        log(f"  删除 {path}")

    tree_body = {"tree": tree_entries}
    if base_tree:
        tree_body["base_tree"] = base_tree
    new_tree = api(token, "POST", f"/repos/{repo}/git/trees", tree_body)["sha"]

    commit_body = {"message": message, "tree": new_tree}
    if parent:
        commit_body["parents"] = [parent]
    commit = api(token, "POST", f"/repos/{repo}/git/commits", commit_body)["sha"]
    log(f"新 commit：{commit[:10]}  ({message})")

    if parent:
        api(token, "PATCH", f"/repos/{repo}/git/refs/heads/{branch}",
            {"sha": commit, "force": False})
    else:
        api(token, "POST", f"/repos/{repo}/git/refs",
            {"ref": f"refs/heads/{branch}", "sha": commit})

    verify(token, repo, branch, commit, files)

    if sync_local:
        sync(token, repo, commit)
    return commit


def index_mode(path: str) -> str:
    """沿用 git 索引里的文件模式（保留可执行位），取不到则 100644。"""
    out = git_out(["ls-files", "-s", "--", path]).strip()
    if out:
        mode = out.split()[0]
        if mode in ("100644", "100755"):
            return mode
    return "100644"


def verify(token: str, repo: str, branch: str, commit: str, files: list[str]) -> None:
    head = api(token, "GET", f"/repos/{repo}/git/ref/heads/{branch}")["object"]["sha"]
    ok_ref = head == commit
    log(f"[校验] 远程 ref {'已更新' if ok_ref else '未更新'}：{head[:10]}")
    for path in files[:5]:
        try:
            info = api(token, "GET", f"/repos/{repo}/contents/{urllib.parse.quote(path)}?ref={branch}")
            log(f"[校验] {path} 已存在于远程（{info.get('size', '?')} bytes）")
        except RuntimeError:
            log(f"[校验] {path} 未取到，请人工确认")
    if not ok_ref:
        die("远程分支引用未指向新 commit，请复查上方输出", 1)


def sync(token: str, repo: str, commit: str) -> None:
    """把本地 git 对齐到 API 创建的 commit（需要先能拉到该对象）。"""
    url = f"https://github.com/{repo}.git"
    log("同步本地：git fetch <sha> + git reset --hard")
    fetch = subprocess.run(["git", "fetch", "--no-tags", url, commit],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
    if fetch.returncode != 0:
        log("[警告] 带 SHA 的 fetch 失败，本地未同步。可稍后网络恢复再执行。")
        log((fetch.stderr or "")[:400])
        return
    reset = subprocess.run(["git", "reset", "--hard", commit],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
    if reset.returncode == 0:
        log("[同步] 本地 HEAD 已对齐到远程 commit。")
        log("[提示] 若 git status 仍显示 ahead/behind，检查 origin/main 跟踪引用是否卡住（见 SKILL.md）。")
    else:
        log("[警告] git reset --hard 失败：\n" + (reset.stderr or "")[:400])


def main() -> None:
    p = argparse.ArgumentParser(description="用 GitHub Git Data API 推送本地文件到远程分支")
    p.add_argument("--repo", required=True, help="owner/repo，如 tuoqi-stats/my-repo")
    p.add_argument("--branch", default="main")
    p.add_argument("--paths", nargs="*", default=[], help="要推送的文件或目录，可多个")
    p.add_argument("--all", action="store_true", help="推送所有未被 .gitignore 排除的文件")
    p.add_argument("--delete", nargs="*", default=[], help="要删除的远程文件路径")
    p.add_argument("-m", "--message", default="Update from local workspace")
    p.add_argument("--dry-run", action="store_true", help="只预演，不写入远程")
    p.add_argument("--allow-secrets", action="store_true", help="允许推送疑似凭据文件（危险）")
    p.add_argument("--sync-local", action="store_true", help="推送后 fetch+reset 对齐本地（会 reset --hard）")
    args = p.parse_args()

    if not args.paths and not args.all and not args.delete:
        die("请至少指定 --paths / --all / --delete 之一", 2)
    if "/" not in args.repo:
        die("--repo 需为 owner/repo 形式", 2)

    files = (collect_all_files() if args.all else []) + (expand_paths(args.paths) if args.paths else [])
    files = sorted({f for f in files if os.path.isfile(f)})
    deletes = [d.replace("\\", "/") for d in args.delete]

    check_secrets(files, args.allow_secrets)

    log(f"目标：{args.repo} @ {args.branch}")
    log(f"待推送 {len(files)} 个文件，待删除 {len(deletes)} 个：")
    total = 0
    for f in files:
        size = os.path.getsize(f)
        total += size
        log(f"  - {f}  ({size} bytes)")
    for d in deletes:
        log(f"  - [删除] {d}")
    log(f"合计 {total/1024:.1f} KB")

    if args.dry_run:
        token = get_token()
        parent = get_ref(token, args.repo, args.branch)
        log(f"[预演] 远程 {args.branch} HEAD：{parent or '（空仓库）'}")
        log("[预演] 未写入任何内容。去掉 --dry-run 即正式推送。")
        return

    token = get_token()
    commit = push(token, args.repo, args.branch, files, deletes, args.message, args.sync_local)
    log("推送完成。")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        die(str(exc), 1)
