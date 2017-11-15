from decouple import config
from github import Github
import os
import webbrowser
import argparse
import sys


parser = argparse.ArgumentParser(description='Opções de repositórios no Github.')
parser.add_argument('-p', '--pasta', action='store_true',
                    help='Ignora a criação da pasta e cria somente o repositório no Github.')

args = parser.parse_args()

github_username = config('username')
github_password = config('password')

github_api = Github(github_username, github_password).get_user()

os.system('clear')
print("Esse script cria uma pasta(opcional) e um repositório no Github.\n")

nome_repo = os.path.basename(os.getcwd())
local = os.path.abspath(os.getcwd())

if args.pasta:
    while True:
        descricao = input("Descrição do repositório no Github (opcional): ")
        if nome_repo in [repo.name for repo in github_api.get_repos()]:
            print("\nEsse repositório (e|ou) a pasta já existe(m). O repositório não será criado.\n")
            sys.exit()
        else:
            criando_repo = github_api.create_repo(nome_repo)
            github_api.get_repo(nome_repo).edit(description=descricao)
            if nome_repo in [repo.name for repo in github_api.get_repos()]:
                print("\nRepositório criado com sucesso!\n")
            else:
                print("\nO repositório não foi criado.")
            break

else:
    while True:
        nome_repo = input("Nome do repositório e da pasta(opcional) a serem criados: ")
        descricao = input("Descrição do repositório no Github (opcional): ")
        if nome_repo in [repo.name for repo in github_api.get_repos()] or os.path.exists(nome_repo):
            print("\nEsse repositório (e|ou) a pasta já existe(m). Escolha outro nome.\n")
        else:
            criando_repo = github_api.create_repo(nome_repo)
            github_api.get_repo(nome_repo).edit(description=descricao)
            os.mkdir(nome_repo)
            if nome_repo in [repo.name for repo in github_api.get_repos()] and os.path.exists(nome_repo):
                print("\nRepositório e pasta criados com sucesso!\n")
            break

# local = os.path.abspath(nome_repo)
# print(local)
os.chdir(local)
with open('.gitignore', 'w') as arquivo:
    arquivo.write('.env\n.venv\n.gitignore\n.idea\ndb.sqlite3\n*pyc\n__pycache__\n')
os.system('echo "# {}" >> README.md'.format(nome_repo))
os.system('git init')
os.system('git add .')
os.system('git commit -m "first commit"')
os.system('git remote add origin git@github.com:{}/{}.git'.format(github_username, nome_repo))
os.system('git push -u origin master')

url_repo = github_api.get_repo(nome_repo).html_url
print("\nURL do repositório:", url_repo)

b = webbrowser.get('google-chrome')
b.open(url_repo)
