from decouple import config
from github import Github
import os


github_username = config('username')
github_password = config('password')

github_api = Github(github_username, github_password).get_user()

os.system('clear')
print("Cria repositório no Github.\n")

while True:
    nome_repo = input("Nome do repositório e da pasta a serem criados: ")
    if nome_repo in [repo.name for repo in github_api.get_repos()] or os.path.exists(nome_repo):
        print("Esse repositório (e|ou) a pasta já existe(m). Escolha outro nome.\n")
    else:
        criando_repo = github_api.create_repo(nome_repo)
        os.mkdir(nome_repo)
        if nome_repo in [repo.name for repo in github_api.get_repos()] and os.path.exists(nome_repo):
            print("Repositório e pasta criados com sucesso!\n")
        break

local = os.path.abspath(nome_repo)
os.chdir(local)
with open('.gitignore', 'w') as arquivo:
    arquivo.write('.env\n.gitignore')
os.system('echo "# {}" >> README.md'.format(nome_repo))
os.system('git init')
os.system('git add .')
os.system('git commit -m "first commit"')
os.system('git remote add origin git@github.com:{}/{}.git'.format(github_username, nome_repo))
os.system('git push -u origin master')
