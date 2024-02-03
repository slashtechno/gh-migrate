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
    # if args.migrate_all_repositories:
    if True:
        print("Migrating all repositories")
        repos, user = trio.run(get_repositories)
        migrated_repos = {
            "migrated_repos": trio.run(migrate_repositories, repos, user)
        }
        json.dump(migrated_repos, open("output.json", "w"))


async def migrate_repositories(repos: list[dict], user:str) -> None:
    """
    Migrate the repositories
    """
    migrated_repos = []
    async with httpx.AsyncClient() as client:
        for repo in repos:
            # Check if the repo is owned by the logied in user. This could be source of future bugs if this line is forgotten
            if repo["owner"]["login"] == user:
                repo_name = repo["name"]
                print(f"Migrating {repo['name']}")
                url = f"https://api.github.com/repos/{user}/{repo_name}/transfer"
                team_id = None if args.team_id == [] else args.team_id 
                data = {
                    "new_owner": args.new_owner,
                    "team_ids": team_id
                }
                headers = {
                    "Authorization": f"token {args.token}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "GH Migrate",
                    "X-GitHub-Api-Version": "2022-11-28"
                } 
                response = await client.post(url, headers=headers, data=json.dumps(data))
                if response.status_code == 422:
                    print(f"Error migrating {repo['name']} due to error 422. This is likely because the repository name is already taken by the new owner.")
                    print("Prepending \"transfered_\" to the repository name and trying again.")
                    data = {
                        "new_owner": args.new_owner,
                        "team_ids": team_id,
                        "new_name": f"transfered_{repo_name}"
                    }
                    response = await client.post(url, headers=headers, data=json.dumps(data))
                response.raise_for_status()
                migrated_repos.append(response.json()['id'])
                print(f"Successfully migrated {repo['name']}")

            else:
                print(f"{repo['full_name']} is not owned by {user}. Not migrating repository.")
    return migrated_repos

async def get_repositories() -> (list[dict], str):
    """
    Calculate the number of pages to iterate through and get the repositories
    """
    # Request the user's information to get the number of repositories
    url = "https://api.github.com/user"
    headers = {
        # Token should have repo and user:read scope
        "Authorization": f"token {args.token}",
        "Accept": "application/json",
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
    user = user["login"]

    repos = []

    try:
        async with httpx.AsyncClient() as client:
            # Start at page 1 and iterate through the pages
            # This usage of range is (start, stop) when generally it can be used as (stop)
            for page in range(1, pages + 1):
                url = f"https://api.github.com/user/repos?per_page={per_page}&page={page}"
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                instance_repos = response.json()
                repos.extend(instance_repos)
    except TypeError as e:
        if str(e) == "'NoneType' object is not iterable":
            print("No repos found")
            return repos, user
        else:
            raise e
    else:
        return repos, user


    

if __name__ == "__main__":
    main()
