pkg_origin="codeforphilly"
pkg_name="chime"
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

pkg_exports=(
  [port]=streamlit.server.port
)

pkg_version() {
  if [ -n "${pkg_last_tag}" ]; then
    if [ ${pkg_last_tag_distance} -eq 0 ]; then
      echo "${pkg_last_version}"
    else
      echo "${pkg_last_version}-git+${pkg_last_tag_distance}.${pkg_commit}"
    fi
  else
    echo "${pkg_last_version}-git.${pkg_commit}"
  fi
}

do_before() {
  do_default_before

  # configure git repository
  export GIT_DIR="${PLAN_CONTEXT}/../.git"

  # load version information from git
  pkg_commit="$(git rev-parse --short HEAD)"
  pkg_last_tag="$(git describe --tags --abbrev=0 ${pkg_commit} || true 2>/dev/null)"

  if [ -n "${pkg_last_tag}" ]; then
    pkg_last_version=${pkg_last_tag#v}
    pkg_last_tag_distance="$(git rev-list ${pkg_last_tag}..${pkg_commit} --count)"
  else
    pkg_last_version="0.0.0"
  fi

  # initialize pkg_version
  update_pkg_version
}

do_prepare() {
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
