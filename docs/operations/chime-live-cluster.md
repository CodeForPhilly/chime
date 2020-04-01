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