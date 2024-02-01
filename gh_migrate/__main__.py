import math
import trio 
import httpx
import json

# from .utils import utils
from .utils.cli_args import argparser

args = None


def main():
    global args 
    args = argparser.parse_args()
    if args.migrate_all_repositories:
        print("Migrating all repositories")
        repos = trio.run(get_repositories)

async def get_repositories() -> list[dict]:
    """
    Calculate the number of pages to iterate through and get the repositories
    """
    # Request the user's information to get the number of repositories
    url = "https://api.github.com/user"
    headers = {
        "Authorization": f"token {args.token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GH Migrate",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    # This request is required before getting the repositories
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        user = response.json()
    total_repos = user["public_repos"] + user["owned_private_repos"]
    # Get the number of pages to iterate through
    per_page = 100
    pages = math.ceil(total_repos / per_page)
    

if __name__ == "__main__":
    main()
