#!/usr/bin/env python3
"""Refresh the activity block in README.md from the GitHub API.

Counts private contributions as well as public ones, but publishes only
aggregate totals -- no private repository name ever reaches the README.

Deliberately does NOT use contributionsCollection's per-repository breakdown:
that endpoint collapses every private contribution into an opaque
`restrictedContributionsCount` unless "Include private contributions on my
profile" is enabled, which would silently under-report by ~2600 contributions.
The search endpoints honour the token's `repo` scope instead, so the numbers
are right either way.

Needs a classic PAT with the `repo` scope in ACTIVITY_TOKEN (or GH_TOKEN).
Standard library only.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

WINDOW_DAYS = 30
GRAPHQL = "https://api.github.com/graphql"
REST = "https://api.github.com"
README = "README.md"
START = "<!-- ACTIVITY:START -->"
END = "<!-- ACTIVITY:END -->"

# GitHub's search endpoints refuse to page past 1000 results.
PER_PAGE = 100
MAX_PAGES = 10

SEARCH_COUNT = """
query($q: String!) {
  search(query: $q, type: ISSUE) { issueCount }
}
"""


def _request(url, token, data=None, accept="application/vnd.github+json"):
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"bearer {token}",
            "Accept": accept,
            "Content-Type": "application/json",
            "User-Agent": "erfanhabibipanah-profile-activity",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        sys.exit(f"GitHub API returned HTTP {exc.code} for {url}: {exc.read().decode()[:400]}")


def graphql(token, query, variables):
    payload = _request(GRAPHQL, token, json.dumps({"query": query, "variables": variables}).encode())
    if "errors" in payload:
        sys.exit(f"GraphQL errors: {json.dumps(payload['errors'])[:400]}")
    return payload["data"]


def search_count(token, query):
    return graphql(token, SEARCH_COUNT, {"q": query})["search"]["issueCount"]


def commit_search(token, query):
    """Total commits plus the set of repositories they landed in.

    Returns (total, {repo_full_name: is_private}, truncated).
    Commit search only indexes default branches, which matches how GitHub
    counts contributions -- work parked on a feature branch is not counted
    here either, and will not be until it merges.
    """
    repos = {}
    total = None
    truncated = False

    for page in range(1, MAX_PAGES + 1):
        params = urllib.parse.urlencode({"q": query, "per_page": PER_PAGE, "page": page})
        payload = _request(f"{REST}/search/commits?{params}", token)
        if total is None:
            total = payload.get("total_count", 0)
        items = payload.get("items", [])
        for item in items:
            repo = item.get("repository") or {}
            if repo.get("full_name"):
                repos[repo["full_name"]] = bool(repo.get("private"))
        if len(items) < PER_PAGE:
            break
        if page == MAX_PAGES and total > MAX_PAGES * PER_PAGE:
            truncated = True

    return total or 0, repos, truncated


def plural(n, word):
    return word if n == 1 else f"{word}s"


def build_block(token):
    to = datetime.now(timezone.utc).replace(microsecond=0)
    frm = to - timedelta(days=WINDOW_DAYS)
    login = graphql(token, "{ viewer { login } }", {})["viewer"]["login"]

    span = f"{frm.date().isoformat()}..{to.date().isoformat()}"
    commits, repos, truncated = commit_search(
        token, f"author:{login} author-date:{span}"
    )
    merged = search_count(token, f"author:{login} is:pr is:merged merged:{span}")
    reviews = search_count(token, f"reviewed-by:{login} is:pr merged:{span}")

    total_repos = len(repos)
    private = sum(1 for is_private in repos.values() if is_private)

    if total_repos == 0:
        scope = "_nothing landed in this window_"
    else:
        noun = "repository" if total_repos == 1 else "repositories"
        count = f"{total_repos}+" if truncated else str(total_repos)
        scope = f"across **{count} {noun}**"
        if private:
            scope += f" ({private} private)"

    if truncated:
        print(
            f"note: commit search capped at {MAX_PAGES * PER_PAGE} of {commits} results; "
            "repository count is a lower bound and is marked with '+'",
            file=sys.stderr,
        )

    return "\n".join(
        [
            START,
            f"### Activity · last {WINDOW_DAYS} days",
            "",
            f"`{commits}` {plural(commits, 'commit')}  ·  "
            f"`{merged}` {plural(merged, 'PR')} merged  ·  "
            f"`{reviews}` {plural(reviews, 'review')}",
            scope,
            "",
            "<sub>public and private work, counted together · "
            f"updated {to.strftime('%Y-%m-%d')}</sub>",
            END,
        ]
    )


def main():
    token = os.environ.get("ACTIVITY_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        sys.exit(
            "No token. Set ACTIVITY_TOKEN to a classic PAT with the `repo` scope -- "
            "the Actions GITHUB_TOKEN cannot see private repositories."
        )

    with open(README, encoding="utf-8") as fh:
        readme = fh.read()

    if START not in readme or END not in readme:
        sys.exit(f"{README} is missing the activity markers; nothing was written.")

    block = build_block(token)
    updated = re.sub(
        re.escape(START) + r".*?" + re.escape(END), lambda _: block, readme, flags=re.S
    )

    if updated == readme:
        print("activity block unchanged")
        return

    with open(README, "w", encoding="utf-8") as fh:
        fh.write(updated)
    print("activity block updated")


if __name__ == "__main__":
    main()
