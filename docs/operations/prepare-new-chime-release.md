# Operations: Prepare New Chime Release

At the end of following this process you will have deployed a new CHIME version to https://penn-chime.phl.io

## Start Here

## Prepare Chime on the Develop Branch

1. Open a new issue on GitHub titled "Deploy chime $VERSION" (ex: https://github.com/CodeForPhilly/chime/issues/98)
  * Note the PR in which the release was approved
  * Confirm that the tag for the version was created
2. Create a local branch (based on "develop") to perform deploy time changed on, named "deploy/$VERSION"

    ```bash
    export VERSION=x.x.x #set this to the release version you are releasing. (export VERSION=1.1.1 for version 1.1.1)
    git checkout develop
    git pull
    git checkout -b deploy/$VERSION # this will ultimately create a branch deploy/1.1.1 (from the reference above)
    ```

3. Update the app.yaml manifest file using an editor. You will need to change the line that has: ```- image: docker.pkg.github.com/codeforphilly/chime/penn-chime:<insert versions here>```
    * After that is complete, update your branch.

    ```bash
    git add k8s/app.yml
    git diff --staged
    git commit -m "Deploy chime $VERSION"
    ```

4. Push changes

    ```bash
    git push -u origin deploy/$VERSION
    ```

5. [Open PR on GitHub](https://github.com/CodeForPhilly/chime/compare) to merge changes back into develop, ideally with
 the review of another DevOps admin whenever possible. Ensure to link
 to the PR in the deployment issue previously opened on GitHub.

6. One approved you will need to [create a release to auto deploy](release-process.md)