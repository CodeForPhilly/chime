# Operations: Release Deployment

The release deployment is an automated process which tracks the following steps:

1. **human**: Create a GitHub Release
2. *bot*: Build a container image from the release
3. *bot*: Push container image to GitHub packages
4. *bot*: Generate manifest files to deploy release
5. *bot*: Publish manifest files to GitHub release
6. *bot*: Open Pull Request into `releases/v1` from `develop`
7. *bot*: Comment on PR showing changes to be applied by deployment
8. **human**: Approve/merge release
9. *bot*: Download manifest files from GitHub release
10. *bot*: Apply manifest files for release to cluster

The automated portions are implemented in .github/workflows/infra-release.yml and .github/workflows/infra-deploy.yml
