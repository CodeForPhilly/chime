# Habitat Service Package for CHIME

This package can be used to run CHIME as a fully self-contained application.
See https://habitat.sh for more details.

## Examples

Quickstart With Docker "Shim" Container:

```bash
docker run -it -p 8000:8000 bixu/hab hab sup run "codeforphilly/chime" --channel="unstable"
```

Local Prototyping Example:

```bash
set -e
curl --silent "https://raw.githubusercontent.com/habitat-sh/habitat/master/components/hab/install.sh" | sudo bash -s
hab cli setup
direnv allow
hab studio enter
build
hab sup run $HAB_ORIGIN/chime --channel="unstable"
```

Complete `systemd` Bootstrap Example:

```bash
echo 'HAB_AUTH_TOKEN="<enter your token from https://bldr.habitat.sh/#/profile>"
HAB_LICENSE="accept"
HAB_NONINTERACTIVE="true"
' > supervisor.env

echo '[Unit]
Description=Habitat Supervisor
[Service]
EnvironmentFile=/etc/systemd/supervisor.env
ExecStartPre=/bin/bash -c "/bin/systemctl set-environment SSL_CERT_FILE=$(hab pkg path core/cacerts)/ssl/cert.pem"
ExecStart=/bin/hab sup run --no-color
ExecStop=/bin/hab sup term
KillMode=process
Restart=on-failure
[Install]
WantedBy=default.target
' > supervisor.service

curl --silent "https://raw.githubusercontent.com/habitat-sh/habitat/master/components/hab/install.sh" | sudo bash -s
sudo cp "supervisor.env" "/etc/systemd/supervisor.env"
sudo chown root "/etc/systemd/supervisor.env"
sudo chmod 400 "/etc/systemd/supervisor.env"
sudo mv supervisor.service "/etc/systemd/system/supervisor.service"
sudo --preserve-env hab pkg install "core/hab-sup"
sudo systemctl enable supervisor
sudo systemctl restart supervisor
sudo groupadd hab || true
sudo useradd --system --gid hab hab || true

sudo hab svc load "codeforphilly/chime" --channel="unstable"
```
