#!/usr/bin/env python3
"""通过 GitHub Git Data API 把本地 git 索引内容推送到远程分支。

用途：沙箱 / 受限网络下 `git push` 报 502、CONNECT tunnel failed 等传输层错误，
但 api.github.com 仍可达时，用 REST API 复刻一次快进式 `git push`。

原理：读取本地 git 索引 → 与远程 HEAD 的 tree 逐文件对比 → 为新增/修改文件建 blob
      → 基于远程 base_tree 建新 tree（含删除项）→ 以远程 HEAD 为 parent 建 commit
      → 更新分支 ref（force=false）→ 对齐本地 HEAD 与远程跟踪引用 → 调 API 验证。

用法：
    python push_via_api.py --repo "E:/repos/statistics-data-analysis-2026" \
        --branch main -m "新增：RAG 学习资料"

退出码：0 成功（含"已是最新"）；1 失败。
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
import urllib.request

API_VERSION = "2022-11-28"
USER_AGENT = "workbuddy-github-push"
MAX_BLOB_MB_DEFAULT = 50.0


# --------------------------------------------------------------------------- #
# 基础工具
# --------------------------------------------------------------------------- #
def log(msg: str = "") -> None:
    print(msg, flush=True)


def fail(msg: str) -> "NoReturn":  # type: ignore[valid-type]
    log(f"\n❌ {msg}")
    sys.exit(1)


def run_git(repo: str, args: list[str], check: bool = True, text: bool = True):
    proc = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=text
    )
    if check and proc.returncode != 0:
        err = proc.stderr if text else proc.stderr.decode(errors="replace")
        fail(f"git {' '.join(args)} 执行失败：\n{err.strip()}")
    return proc


# --------------------------------------------------------------------------- #
# 远程地址与凭据
# --------------------------------------------------------------------------- #
def parse_remote_url(url: str) -> tuple[str, str, str]:
    """从 remote URL 解析 (host, owner, repo)。"""
    url = url.strip()
    if url.endswith(".git"):
        url = url[:-4]
    patterns = [
        r"^https?://(?:[^@/]+@)?(?P<host>[^/]+)/(?P<owner>[^/]+)/(?P<repo>[^/]+)$",
        r"^ssh://(?:[^@/]+@)?(?P<host>[^/]+)/(?P<owner>[^/]+)/(?P<repo>[^/]+)$",
        r"^(?:[^@/]+@)?(?P<host>[^:/]+)[:/](?P<owner>[^/]+)/(?P<repo>[^/]+)$",
    ]
    for pat in patterns:
        m = re.match(pat, url)
        if m:
            host = m.group("host")
            if host in ("github.com", "www.github.com"):
                host = "github.com"
            return host, m.group("owner"), m.group("repo")
    fail(f"无法从 remote URL 解析出 owner/repo：{url}")


def get_token(host: str) -> tuple[str, str]:
    """按环境变量 → git credential 的顺序取 token，返回 (token, 来源说明)。"""
    for var in ("GITHUB_TOKEN", "GH_TOKEN"):
        val = os.environ.get(var)
        if val:
            return val.strip(), f"环境变量 {var}"

    proc = subprocess.run(
        ["git", "credential", "fill"],
        input=f"protocol=https\nhost={host}\n\n",
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        for line in proc.stdout.splitlines():
            if line.startswith("password=") and line[9:].strip():
                return line[9:].strip(), "git credential（系统凭据管理器）"

    fail(
        "未取到 GitHub 凭据。请确认已登录（git credential fill 能返回 password），"
        "或设置 GITHUB_TOKEN / GH_TOKEN 环境变量。"
    )


# --------------------------------------------------------------------------- #
# GitHub API
# --------------------------------------------------------------------------- #
def api(
    method: str,
    path: str,
    token: str,
    host: str = "github.com",
    body: dict | None = None,
):
    url = f"https://api.{host}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", API_VERSION)
    req.add_header("User-Agent", USER_AGENT)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(detail).get("message", detail)
        except json.JSONDecodeError:
            pass
        fail(f"GitHub API {method} {path} 失败（HTTP {exc.code}）：{detail}")
    except urllib.error.URLError as exc:
        fail(
            f"无法访问 api.{host}：{exc.reason}\n"
            "网络完全不通时本兜底方案不可用，请让用户检查网络后手动 push。"
        )


# --------------------------------------------------------------------------- #
# 索引与树对比
# --------------------------------------------------------------------------- #
def read_index(repo: str) -> dict[str, tuple[str, str]]:
    """读取 git 索引，返回 {path: (mode, blob_sha)}。"""
    out = run_git(repo, ["ls-files", "-s", "-z"]).stdout
    entries: dict[str, tuple[str, str]] = {}
    for rec in out.split("\0"):
        if not rec.strip():
            continue
        meta, _, path = rec.partition("\t")
        parts = meta.split()
        if len(parts) < 3 or parts[2] != "0":  # 跳过冲突/未合并条目
            continue
        entries[path] = (parts[0], parts[1])
    return entries


def read_remote_tree(owner: str, name: str, tree_sha: str, token: str, host: str):
    data = api(
        "GET",
        f"/repos/{owner}/{name}/git/trees/{tree_sha}?recursive=1",
        token,
        host,
    )
    if data.get("truncated"):
        fail("远程仓库文件过多，tree 响应被截断，本脚本不适用（请改用 git push）。")
    entries: dict[str, tuple[str, str]] = {}
    for item in data.get("tree", []):
        if item.get("type") == "blob":
            entries[item["path"]] = (item["mode"], item["sha"])
    return entries


# --------------------------------------------------------------------------- #
# 本地同步
# --------------------------------------------------------------------------- #
def sync_local(repo: str, remote: str, branch: str, new_sha: str) -> None:
    run_git(repo, ["fetch", remote], check=False)
    if run_git(repo, ["cat-file", "-e", f"{new_sha}^{{commit}}"], check=False).returncode:
        run_git(repo, ["fetch", remote, branch], check=False)
    if run_git(repo, ["cat-file", "-e", f"{new_sha}^{{commit}}"], check=False).returncode:
        log(f"⚠️  本地缺少对象 {new_sha[:8]}，跳过本地 HEAD 对齐（下次 git fetch 后可恢复）。")
        return

    run_git(repo, ["reset", "--hard", new_sha])

    # 修复 origin/<branch> 跟踪引用（可能困在 packed-refs 中读不到新值）
    tracking = f"refs/remotes/{remote}/{branch}"
    cur = run_git(repo, ["rev-parse", tracking], check=False).stdout.strip()
    if cur != new_sha:
        run_git(repo, ["update-ref", tracking, new_sha], check=False)
        cur = run_git(repo, ["rev-parse", tracking], check=False).stdout.strip()
    if cur != new_sha:
        git_dir = run_git(repo, ["rev-parse", "--absolute-git-dir"]).stdout.strip()
        loose = os.path.join(git_dir, "refs", "remotes", remote)
        os.makedirs(loose, exist_ok=True)
        with open(os.path.join(loose, branch), "w", encoding="ascii") as fh:
            fh.write(new_sha + "\n")
        run_git(repo, ["pack-refs", "--all"], check=False)
        cur = run_git(repo, ["rev-parse", tracking], check=False).stdout.strip()
    log(f"   本地 {tracking} → {cur[:8] if cur else '未知'}")


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(
        description="通过 GitHub Git Data API 推送本地索引内容到远程分支（git push 的兜底方案）"
    )
    parser.add_argument("--repo", default=".", help="本地仓库路径，默认当前目录")
    parser.add_argument("--branch", default=None, help="目标分支，默认当前分支")
    parser.add_argument("--remote", default="origin", help="remote 名称，默认 origin")
    parser.add_argument("-m", "--message", required=True, help="提交信息")
    parser.add_argument("--dry-run", action="store_true", help="只打印推送计划，不写入")
    parser.add_argument("--no-sync", action="store_true", help="跳过推送后的本地 HEAD 对齐")
    parser.add_argument(
        "--max-blob-mb",
        type=float,
        default=MAX_BLOB_MB_DEFAULT,
        help=f"单文件大小上限（MB），超过则中止，默认 {MAX_BLOB_MB_DEFAULT:g}",
    )
    args = parser.parse_args()

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(os.path.join(repo, ".git")):
        fail(f"{repo} 不是 git 仓库根目录（未找到 .git 目录）。")

    branch = args.branch or run_git(
        repo, ["rev-parse", "--abbrev-ref", "HEAD"]
    ).stdout.strip()
    if branch in ("HEAD", ""):
        fail("当前处于 detached HEAD，请先切换或创建分支（git switch -c <branch>）。")

    remote_url = run_git(repo, ["remote", "get-url", args.remote], check=False).stdout.strip()
    if not remote_url:
        fail(f"未找到 remote「{args.remote}」，请先 git remote add。")
    host, owner, name = parse_remote_url(remote_url)
    token, token_src = get_token(host)

    log(f"仓库信息：{owner}/{name}  分支：{branch}  remote：{args.remote}")
    log(f"凭据来源：{token_src}")

    staged = run_git(repo, ["diff", "--cached", "--name-only"]).stdout.strip()
    if staged:
        log(f"⚠️  索引中有 {len(staged.splitlines())} 个已暂存但未提交的文件，将一并推送到远程。")

    # 1. 本地索引
    local = read_index(repo)
    if not local:
        fail("git 索引为空，没有可推送的内容（先 git add 或确认是否在正确的仓库）。")
    log(f"\n本地索引：{len(local)} 个文件")

    # 2. 远程当前 HEAD / base tree
    ref = api("GET", f"/repos/{owner}/{name}/git/ref/heads/{branch}", token, host)
    remote_head = ref["object"]["sha"]
    commit_info = api(
        "GET", f"/repos/{owner}/{name}/git/commits/{remote_head}", token, host
    )
    base_tree = commit_info["tree"]["sha"]
    log(f"远程 HEAD：{remote_head[:8]}（分支 {branch}）")

    remote = read_remote_tree(owner, name, base_tree, token, host)
    log(f"远程 tree：{len(remote)} 个文件")

    # 3. 差异计算
    to_write = sorted(p for p, v in local.items() if remote.get(p) != v)
    to_delete = sorted(p for p in remote if p not in local)
    submodules = [p for p, (mode, _) in local.items() if mode == "160000"]

    if submodules:
        log(f"⚠️  跳过 {len(submodules)} 个子模块条目（API 无法提交 submodule）：{submodules}")
    if not to_write and not to_delete:
        log("\n✅ 本地内容与远程一致，无需推送。")
        return

    log(f"\n待推送计划：新增/修改 {len(to_write)} 个，删除 {len(to_delete)} 个")
    for p in to_write:
        log(f"   M {p}")
    for p in to_delete:
        log(f"   D {p}")

    if args.dry_run:
        log("\n（--dry-run，未写入远程。）")
        return

    # 4. 建 blob
    limit = int(args.max_blob_mb * 1024 * 1024)
    tree_entries: list[dict] = []
    for path in to_write:
        blob = run_git(repo, ["cat-file", "blob", local[path][1]], text=False).stdout
        if len(blob) > limit:
            fail(
                f"文件 {path} 大小 {len(blob) / 1024 / 1024:.1f} MB，超过 "
                f"{args.max_blob_mb:g} MB 阈值。请用 Git LFS 或 Releases，或调大 --max-blob-mb。"
            )
        created = api(
            "POST",
            f"/repos/{owner}/{name}/git/blobs",
            token,
            host,
            {
                "content": base64.b64encode(blob).decode("ascii"),
                "encoding": "base64",
            },
        )
        tree_entries.append(
            {
                "path": path,
                "mode": local[path][0],
                "type": "blob",
                "sha": created["sha"],
            }
        )
    log(f"\n已创建 {len(tree_entries)} 个 blob。")

    # 5. 建 tree（base_tree 上覆盖改动，删除项 sha 置 null）
    for path in to_delete:
        tree_entries.append(
            {"path": path, "mode": remote[path][0], "type": "blob", "sha": None}
        )
    new_tree = api(
        "POST",
        f"/repos/{owner}/{name}/git/trees",
        token,
        host,
        {"base_tree": base_tree, "tree": tree_entries},
    )

    # 6. 建 commit
    new_commit = api(
        "POST",
        f"/repos/{owner}/{name}/git/commits",
        token,
        host,
        {"message": args.message, "tree": new_tree["sha"], "parents": [remote_head]},
    )
    log(f"已创建 commit：{new_commit['sha'][:8]}")

    # 7. 更新分支 ref（force=false → 保证快进；远程已前进则 API 返回 422）
    api(
        "PATCH",
        f"/repos/{owner}/{name}/git/refs/heads/{branch}",
        token,
        host,
        {"sha": new_commit["sha"], "force": False},
    )
    log(f"已更新 refs/heads/{branch} → {new_commit['sha'][:8]}")

    # 8. 对齐本地
    if not args.no_sync:
        log("\n同步本地 git 状态：")
        sync_local(repo, args.remote, branch, new_commit["sha"])

    # 9. 验证
    verify = api("GET", f"/repos/{owner}/{name}/git/ref/heads/{branch}", token, host)
    remote_now = verify["object"]["sha"]
    ok = remote_now == new_commit["sha"]
    log("\n--- 推送结果 ---")
    log(f"远程 refs/heads/{branch}：{remote_now}")
    log(f"新 commit：{new_commit['sha']}")
    log(f"提交信息：{args.message.splitlines()[0]}")
    log(f"文件变更：新增/修改 {len(to_write)}，删除 {len(to_delete)}")
    log(f"验证：{'✅ 远程 SHA 已更新' if ok else '❌ 远程 SHA 与预期不一致'}")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
