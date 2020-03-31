# Operations: Deploy with Chef Habitat

CHIME can be quickly deployed to any Linux system with [Chef Habitat](https://habitat.sh):

```bash
hab svc load codeforphilly/chime
```

This will download the latest CHIME build from [bldr.habitat.sh](bldr.habitat.sh) and start it as a service, serving the interface on the default port of [`8000`](http://localhost:8000)

## Enable HTTPS access

Providing HTTPS access can be easily done by making use of [Caddy](https://caddyserver.com/) and its built-in automatic HTTPS.

First, start the `jarvus/caddy-proxy` service with your CHIME service instance bound to the `backend` slot:

```bash
hab svc load jarvus/caddy-proxy --bind backend:chime.default
```

This will open an HTTP interface on port `80` that proxies to the CHIME service on port `8000`.

To enable the HTTPS interface, configure an email address and at least one publicly-resolvable hostname so that Caddy can use [Let's Encrypt](https://letsencrypt.org/) to automatically obtain a free SSL certificate:

```bash
mkdir -p /hab/user/caddy-proxy/config

# use the editor of your choice:
vim /hab/user/caddy-proxy/config/user.toml
```

```toml
hostnames = [
    "mydomain.org"
]

[tls]
email = "hello@example.org"
```

After you save `user.toml`, the Habitat supervisor will automatically detect the change and apply it. CHIME should now be available via HTTPS, with the HTTP port automatically redirecting.
