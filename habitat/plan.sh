pkg_origin="codeforphilly"
pkg_name="chime"
pkg_version="0.1.0"
pkg_maintainer="Code for Philly <hello@codeforphilly.org>"
pkg_license=('MIT')
pkg_deps=(
  "core/python"
  "core/sudo"
  "core/dbus"
)
pkg_build_deps=(
  "core/make"
  "core/git"
)
pkg_bin_dirs=(
  "bin"
)
pkg_svc_user="root"

do_prepare() {
  if ! ls "/etc/sudoers" &> "/dev/null"
  then
    echo "root ALL=(ALL)  ALL" >> "/etc/sudoers"
  fi
  python -m venv "${pkg_prefix}"
  source "${pkg_prefix}/bin/activate"
  pip install --upgrade --force-reinstall "pip" "wheel" "setuptools"
  return $?
}

do_build() {
  pip install ${PLAN_CONTEXT}/../
  return $?
}

do_install() {
  cp -pr ${PLAN_CONTEXT}/../src/* "${pkg_prefix}/"
  return $?
}

do_check() {
  return 0
}

do_strip() {
  return 0
}
