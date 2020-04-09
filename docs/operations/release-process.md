# Operations: Release Process

## Full release

1. [Create a GitHub release](https://help.github.com/en/github/administering-a-repository/managing-releases-in-a-repository#creating-a-release)
  * Must be a full release, i.e., not tagged as a pre-release
2. Wait for CI to open a Pull Request titled "Deploy CHIME vX.X.X"
3. Have a release manager approve & merge the PR

## Release Candidate

1. [Create a GitHub release](https://help.github.com/en/github/administering-a-repository/managing-releases-in-a-repository#creating-a-release)
  * Must be marked as a pre-release
2. Wait for CI to build/deploy to pre-production environment

