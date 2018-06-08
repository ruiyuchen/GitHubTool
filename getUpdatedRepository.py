import json
import requests
import sys

organization = sys.argv[1]
branch = sys.argv[2]
date = sys.argv[3]
username = sys.argv[4]
password = sys.argv[5]

session = requests.session()
session.auth = (username, password)

print("\n============================================================================")
print("Get '{}' organization '{}' branch repositories updated after '{}'".format(organization, branch, date))
print("Repository List")
print("============================================================================\n")

page = 1
while True:
    git_url = 'https://api.github.com/orgs/{}/repos?page={}'.format(organization, page)
    repository_data = session.get(git_url)
    json_repository_data = json.loads(repository_data.text)

    if json_repository_data:
        page += 1
    else:
        break

    for repository in json_repository_data:
        repository_name = repository['name']
        branch_url = 'https://api.github.com/repos/{}/{}/branches/{}'.format(organization, repository_name, branch)
        branch_data = session.get(branch_url)
        json_branch_data = json.loads(branch_data.text)

        try:
            repository_update_time = json_branch_data['commit']['commit']['committer']['date']
            if repository_update_time > date:
                print("{}: {}".format(repository_name, repository_update_time))
        except:
            pass

print("\n")
