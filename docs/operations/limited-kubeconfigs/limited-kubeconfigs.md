# Creating Kubeconfigs with Limited Permissions

## Create a Role

Kubernetes has two primary resources which represent a set of permissions,
Roles and ClusterRoles. ClusterRoles apply to resources in all namespaces,
whereas Roles are limited to a specific namespace. Let's create a Role in the
chime namespace which will allow read/write access to Deployments and
read-only access to Pods.

deployer.yaml:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployer
  namespace: chime
rules:
- apiGroups:
    - apps
  resources:
    - deployments
  verbs:
    # we are _not_ including 'create' and 'delete'
    - get
    - list
    - watch
    - update
    - patch
- apiGroups:
    - ""
  resources:
    - pods
  verbs:
    # so that we can observe our pods getting created
    - get
    - list
    - watch
```

## Create a ServiceAccount

One of the subjects which can take on a Role is a ServiceAccount. Let's
create a ServiceAccount called penn-deployer in the chime namespace:

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: penn-deployer
  namespace: chime
```

## Create a RoleBinding

We can now give the ServiceAccount the Role that we created earlier using a
RoleBinding in the chime namespace.

```
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: penn-deployer:deployer
  namespace: chime
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: deployer
subjects:
  - kind: ServiceAccount
    name: penn-deployer
    namespace: chime
```

## Grabbing the token for the ServiceAccount

Every ServiceAccount gets a token, lets grab it.

```
k get secrets -n chime
```

Look for `penn-deployer-token-<hash>`

```
k get secrets -n chime penn-deployer-token-<hash>
```

Grab the "token:" base64 encoded token.

*base64 decode this token, which will produce base64*

## Creating a token-based kubeconfig

Now take a look at the Kubeconfig that you are currently using. Does it use a
token? If so, you can construct a Kubeconfig for this ServiceAccount by copying
your kubeconfig and replacing the token and user name with this decoded token
and the user name "penn-deployer".

It will look something like this:

```
apiVersion: v1
kind: Config
preferences: {}

clusters:
- name: chime-cluster
  cluster:
    certificate-authority-data: <ca-cert-base64, same as existing>
    server: https://<server-hostname>:<server-port>

users:
- name: penn-deployer
  user:
    as-user-extra: {}
    token: <ServiceAccount token! Be very sure that this is the ServiceAccount token!>

contexts:
- name: penn-deployer-chime
  context:
    cluster: chime-cluster
    user: penn-deployer
    namespace: chime

current-context: penn-deployer-chime
```

## Test out your token-based Kubeconfig

You can now use this ServiceAccount to modify Deployments, and view Pods, but do nothing else.

```
$ k get pods -A
Error from server (Forbidden): pods is forbidden: User "system:serviceaccount:chime:penn-deployer" cannot list resource "pods" in API group "" at the cluster scope
```

```
$ export KUBECONFIG=new-kubeconfig.yaml
$ k get pods -n chime
$ k get deployments -n chime
# deploy version 0.5.0
$ k set image deployment/chime -n chime chime=docker.pkg.github.com/codeforphilly/chime/penn-chime:0.5.0 --record
# observe status of deployment
$ k get pods -n chime
```
