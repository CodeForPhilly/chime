# Operations: The `chime-live` Cluster

At the end of following this process you will have deployed a new CHIME version to https://penn-chime.phl.io

## Start Here

## Deploying a New CHIME Version

1. [Create a new release](release-process.md)
2. Wait for the `Docker` GitHub Actions workflow to complete
3. Verify the new version shows up at the top as "Latest version" here: https://github.com/CodeForPhilly/chime/packages/155340
4. Open a new issue on GitHub titled "Deploy chime $VERSION" (ex: https://github.com/CodeForPhilly/chime/issues/98)
  * Note the PR in which the release was approved
  * Confirm that the tag for the version was created
5. Create a local branch (based on "develop") to perform deploy time changed on, named "deploy/$VERSION"

    ```bash
    export VERSION=x.x.x #set this to the release version you are releasing. (export VERSION=1.1.1 for version 1.1.1)
    git checkout develop
    git pull
    git checkout -b deploy/$VERSION # this will ultimately create a branch deploy/1.1.1 (from the reference above)
    ```

6. Update the app.yaml manifest file using an editor. You will need to change the line that has: ```- image: docker.pkg.github.com/codeforphilly/chime/penn-chime:<insert versions here>```

    ```bash
    git add k8s/app.yml
    git diff --staged
    git commit -m "Deploy chime $VERSION"
    ```

7. Push changes

    ```bash
    git push -u origin deploy/$VERSION
    ```

8. [Open PR on GitHub](https://github.com/CodeForPhilly/chime/compare) to merge changes back into develop, ideally with
 the review of another DevOps admin whenever possible. Ensure to link
 to the PR in the deployment issue previously opened on GitHub.

9. One approved you will need to [create a release to auto deploy](release-process.md)