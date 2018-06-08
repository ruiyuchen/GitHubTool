import json
import sys
import subprocess

organization = sys.argv[1]
date = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
credential = '{}:{}'.format(username, password)

print("\n============================================================================")
print("Get '{}' organization repositories updated after '{}'".format(organization, date))
print("Repository List")
print("============================================================================\n")

page = 1
while True:
    git_url = 'https://{}@api.github.com/orgs/{}/repos?page={}'.format(credential, organization, page)
    repository_data = subprocess.check_output(["curl", git_url, "-X", "GET", "-sS"])
    json_repository_data = json.loads(repository_data)

    if json_repository_data:
        page += 1
    else:
        break

    for repository in json_repository_data:
        repository_name = repository['name']
        branch_url = 'https://{}@api.github.com/repos/{}/{}/branches/master'.format(credential, organization, repository_name)
        branch_data = subprocess.check_output(["curl", branch_url, "-X", "GET", "-sS"])
        json_branch_data = json.loads(branch_data)
        repository_update_time = json_branch_data['commit']['commit']['committer']['date']

        try:
            has_update = json_branch_data['commit']['commit']['committer']['date'] > date
            if has_update:
                print("{}: {}".format(repository_name, json_branch_data['commit']['commit']['committer']['date']))
        except:
            pass

print("\n")
