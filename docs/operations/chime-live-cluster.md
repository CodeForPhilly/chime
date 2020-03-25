# Operations: The `chime-live` Cluster

## Connecting with `kubectl`

1. [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
2. [Install Krew](https://krew.sigs.k8s.io/docs/user-guide/setup/install/):
3. [Install konfig](https://github.com/corneliusweig/konfig#via-krew):

    ```bash
    kubectl krew install konfig
    ```

4. Obtain `chime-live-kubeconfig.yaml` file from Code for Philly ops team
   - This file contains connection details and credentials for managing the cluster, treat its contents as top-secret!
5. Merge `chime-live-kubeconfig.yaml` into your local configuration:

    ```bash
    kubectl konfig import --save ~/Downloads/chime-live-kubeconfig.yaml
    ```

6. Switch to `lke_chime-live` context:

    ```bash
    kubectl config use-context lke_chime-live
    ```

7. Verify connection:

    ```bash
    kubectl get pod --all-namespaces
    ```

## Deploying a New CHIME Version

1. [Create a new release](release-process.md)
2. Wait for the `Docker` GitHub Actions workflow to complete
3. Verify the new version shows up at the top as "Latest version" here: https://github.com/CodeForPhilly/chime/packages/155340
4. Open a new issue on GitHub titled "Deploy chime $VERSION" (ex: https://github.com/CodeForPhilly/chime/issues/98)
  * Note the PR in which the release was approved
  * Confirm that the tag for the version was created
5. Create a local branch (based on "develop") to perform deploy time changed on, named "deploy/$VERSION"

    ```bash
    VERSION=1.2.3
    git rev-parse --abbrev-ref HEAD
    # develop
    git pull
    git checkout -b deploy/$VERSION
    ```

6. Update the app.yaml manifest file

    ```bash
    VERSION=1.2.3
    sed -Ei "s/(- image: .*):(.*)/\1:$VERSION/" k8s/app.yaml
    git add -A
    # verify changes are as expected
    git diff --staged
    git commit -m "Deploy chime $VERSION"
    ```

7. Push changes

    ```bash
    VERSION=1.2.3
    git push -u origin deploy/$VERSION
    ```

8. Open PR on GitHub to merge changes back into develop, ideally with
 the review of another DevOps admin whenever possible. Ensure to link
 to the PR in the deployment issue previously opened on GitHub.

9. Run:

    ```bash
    kubectl apply -f k8s/app.yaml
    ```

10. Watch rollout status:

    ```bash
    kubectl -n chime rollout status deployment.v1.apps/chime
    ```

11. Confirm the expected version is running

    ```bash
    kubectl -n chime get deployment chime -o yaml | grep image:
    #  - image: docker.pkg.github.com/codeforphilly/chime/penn-chime:$VERSION
    ```

12. Paste the output from steps 11 & 12 into the previously opened deployment issue
 to document the successful deployment and close the issue
13. $$$ PROFIT $$$

## Applying Changes to `k8s/` Manifests

After making changes to the manifests in `k8s/` that you want to apply, first review the diff for what you're about to change using an editor that wil color-code the output and make it easy to review:

```bash
kubectl diff -Rf k8s/ | code -
```

*Ignore any instances of `generation` being incremented*

Once you're satisfied with the results of the diff, you can apply a single manifest:

```bash
kubectl apply -f k8s/infra/ingress-nginx.yaml
```

Or the entire directory:

```bash
kubectl apply -Rf k8s/
```
