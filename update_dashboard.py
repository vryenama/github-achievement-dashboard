import os
import requests
from datetime import datetime, timezone

# 1. Fetch environment variables provided by GitHub Actions
GITHUB_USERNAME = os.getenv("GITHUB_REPOSITORY_OWNER")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def fetch_github_stats():
    if not GITHUB_USERNAME:
        print("Error: GITHUB_REPOSITORY_OWNER is not set.")
        return None

    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

    response = requests.get(url, headers=headers, params={"per_page": 100}, timeout=30)
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        print(response.text)
        return None

    return response.json()


def generate_markdown(repos_data):
    total_repos = len(repos_data)
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
    total_forks = sum(repo.get("forks_count", 0) for repo in repos_data)
    has_issues_enabled = sum(1 for repo in repos_data if repo.get("has_issues"))

    # Determine custom milestone tiers based on your metrics
    if total_repos < 10:
        repo_tier = "🥉 Bronze Developer"
    elif total_repos < 25:
        repo_tier = "🥈 Silver Architect"
    else:
        repo_tier = "🥇 Gold Master"

    if total_stars > 0:
        star_tier = "⭐ Rising Star"
    else:
        star_tier = "💤 Lurking Dev"

    updated_at = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")

    markdown_content = f"""# 📊 My Developer Achievement Dashboard

Generated automatically using a custom Python automated pipeline.

### 🏆 Custom Milestone Tiers
* **Project Volume Rank:** {repo_tier}
* **Community Engagement Rank:** {star_tier}

### 📈 Live Repository Metrics
* 📁 **Total Public Repositories:** {total_repos}
* ⭐ **Total Stars Received:** {total_stars}
* 🍴 **Total Times Forked:** {total_forks}
* 🛠️ **Repos tracking Active Issues:** {has_issues_enabled}

*Last Updated on: {updated_at}*
"""
    return markdown_content


def main():
    print(f"Starting stats update for user: {GITHUB_USERNAME}")
    repos_data = fetch_github_stats()

    if repos_data:
        content = generate_markdown(repos_data)
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)
        print("README.md updated successfully!")


if __name__ == "__main__":
    main()
