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

1. Merge new version into `master` branch
2. Create a new release tag in the format `v1.2.3`, incrementing semantically
3. Wait for the `Docker` GitHub Actions workflow to complete
4. Verify the new version shows up at the top as "Latest version" here: https://github.com/CodeForPhilly/chime/packages/155340
5. Run:

    ```bash
    VERSION=1.2.3
    kubectl set image --record deployment/chime chime="docker.pkg.github.com/codeforphilly/chime/penn-chime:${VERSION}"
    ```

6. Watch rollout status:

    ```bash
    kubectl rollout status deployment.v1.apps/chime
    ```

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
kubectl diff -Rf k8s/
```
