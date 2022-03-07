# GIT RESEARCH
Git is like a versioned file system. Git object model contains commit, tree, blobs and annotated tag.
There are different topologies in version control systems like Centralized, Hierarchical and Distributed.

Git is a kind of DVCS(Distributed Version Control System). 
- Distributed: Developers push their changes to their own repository and maintainers will pull these changes into the official repository
if they are deemed valuable. For example in Github, if you want to contribute changes, you can fork the main repository, make
your changes and then issue a pull request to the upstream project maintainer. 

- Upstream means, we can connect our local cloned repository to the original remote branch and then we can pull changes to our local from original remote. We cannot push directly to upstream, so we can send a message to upstream and ask them to pull our changes. This is called pull request

## Installation & Initialization
For loading Git on Debian/Ubuntu distros type: "apt-get install git-core"

- All database is stored in .git folder.

- git --version: Get current git version

- git init: Turn empty directory into a local Git repository. Creates .git directory which contains the repository and all its metadata.

- Git configuration: For getting Git configuration,   
  - git config --global --list  or cat ~/.gitconfig or 
- Git configuration for current repository: 
  - cat .git/config
    
- For doing global configuration: 
  - git config --global user.name "Fatih Cirakoglu"
  - git config --global user.email "fatih.cirakoglu@boun.edu.tr"

- To configure editor: 
    - git config --global core.editor vim

## Useful Git commands
  ### Simple Git sequence : 
 - git clone my_repository_link: Clone your repository to local. 
 - git branch: Observe the current branch and lets say it is master.
 - git pull: Get latest of the master branch 
 - git branch my_private_branch : Create a private branch rebasing from master branch
 - git checkout my_private_branch: Checkout to private branch 
 - touch README.txt : Create a simple text file
 - echo "Hello Git" :  README.txt: Enter a text into file
 - git status : Observe untracked files
 - git add README.txt : Add file to git repository
 - git status: Observe that file is new and staged to be added to the repository  
 - git commit "added README.txt": Submit file to the repository by entering commit message 
 - git log: Observe commit history
 - git push origin my_private_branch: Push your private branch to remote git server
 - Then go to git server and create a pull request against your master branch to let review and merge your changes

 ### Commit ID :  
 Git creates a commit ID for each commit, so this commit ID includes the state where this commit is executed. Each commit has its own tree and blobs, commits are also linked to each other. First commit doesnt have a parent. Other commits have parents. For each commit a different tree is created. References between commits are used to track history

 ### Observe differences between different commit IDs :
 - git diff dd68..a15e : Show differences between two Commit IDs.  
 - git diff HEAD~1..HEAD(firs commit): Show difference between last commit and previous one.

### Reset repositry changes :
- git reset --hard:  Undo all changes back that are staged
- git reset --soft HEAD~1 :  Undo latest changes that are committed
- git reset --hard HEAD~1 : Delete last commit and discard all the changes
- git clean -n : Clean files that are untracked
- git clean -f : Force to clean files directly that are untracked

### Ignore unwanted files with Gitignore :
- vi .gitignore : Specifiy files that you dont want to commit to your repository


### Observe history in graphical form :  
- git log --oneline --graph : Show different branch and merges in graphical form

### Handle history :
- git shortlog : It lists the authors and commit messages from each of them
- git show HEAD : Show last commit
- git show HAED~1 : Show what is reversed.
- git show "commitnumber": Show the specific commit ID's log 

### Handle branches :
- git remote -v : Show the fetch and push URL for that particular remote.
- git branch : Display all branches in this repository
- git branch -r : Display all remote branches in this repository
- git branch -d test: Delete the local branch 
- git push origin --delete test: Delete the remote branch 

### Observe Tags : 
- git tag : Show table points in your code base where you can often tag versions.
- git tag v1.0: Create a tag that is named as "v1.0"
- git push --tags: Push tags that are created locally to remote git server

### Delete last commit :
Revert last commit and delete from history.
- git reset --soft HEAD^: Delete last commit
- git push -f: Force push changes

### Change last commit :
To change the last commit use below commands:
- git commit --amend: Open editor to change commit
- git push -f: Force push commit change

### Checkout to a specific commit ID :
- git checkout SHA1: You can checkout to a commit

### Rebase your local repository : 
- git rebase master: It pulls the latest changes in this repository and put your local changes on top of latest commit. There can be conflicts such as merge conflicts, so you have to resolve them.

# WIKIDATA API

Wikidata supports restful API interface which is a web service that allows access to some wiki features like authentication, page operations, and search. It can provide meta information about the wiki and the logged-in user.

Here is an example API that gets the "centralauthtoken" parameter in json format.
- What is "centralauthtoken" ?
  - When accessing the API using a cross-domain AJAX request (CORS), use this to authenticate as the current SUL user. Use action=centralauthtoken on this wiki to retrieve the token, before making the CORS request. Each token may only be used once, and expires after 10 seconds. This should be included in any pre-flight request, and therefore should be included in the request URI (not the POST body).
- API Request:

https://www.wikidata.org/w/api.php?action=centralauthtoken&format=json

```
{
	"action": "centralauthtoken",
	"format": "json"
}
```

- Reply:
```
{
    "centralauthtoken": {
        "centralauthtoken": "1bc6480c4e70756f9d07d13ba48f21ca41ed983"
    }
}
```