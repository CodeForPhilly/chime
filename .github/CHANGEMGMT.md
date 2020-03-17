## Overview
Developers need to be working on a similar code base to avoid merge conflicts between their branch and the master branch. To ensure that this doesn't happen, we adhere to the following practices.

### Individual Branch 
When an individual is working on an issue, their branch will contain changes relevant to that issue (and that issue alone).  When the developer is done with that issue, they will create a pull request to merge that branch to the feature branch. To create a new branch, the developer starts with the most current version of the feature branch (`git fetch && git checkout <feature-branch> && git pull --rebase origin <feature-branch>`), then checks out a new branch `git checkout -b <branch name>`.  Individual branches should only be created off of the feature branch. 

To ensure that the branch is consistent with the working environment, the developer checks the status of their local repo with their git branch by running `git status`. Developers should commit changes to their branch once they are made. 
#### Committing to the Individual Branch
`git status`

`git add <file path or '.'>`

`git commit -m "<commit message>"`

`git push origin <branch name>`

### Feature Branch
The develop branch is the the working branch for the feature.  
#### Creating New Branch from Feature
When a developer starts a new issue, they will do a `git fetch`, then checkout feature branch (`git checkout <feature-branch>`).  They then need to ensure that the feature branch's code base is consistent with master by running `git pull --rebase origin master`.
#### Maintaining Individual Branch
It is possible that changes can be made to the feature branch as the developer is working on their individual branch.  Before generating a PR, developers need to fetch changes to the feature branch `git fetch`, ensure that the rest of their repo is consistent with the feature branch (`git pull --rebase origin <feature-branch>`) and then merge the develop changes to their branch `git merge <feature-branch>`. 

### Master Branch
The master branch is the deploy-able copy of the project. Once enough work has been vetted and added to the develop branch, the develop branch is merged with the master branch.  

## Pull Requests
Once an issue is completed, the developer creates a PR with the issue number and description as the title.  They assign at least one other developer from the same group (front end or back end) to check the PR.  Code must pass tests to be merged with the feature branch.  

### Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update the README.md with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.

