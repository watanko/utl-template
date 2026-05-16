#!/usr/bin/env bash
set -euo pipefail

readonly ACTIONLINT_PACKAGE="github.com/rhysd/actionlint/cmd/actionlint@latest"
readonly GITLEAKS_PACKAGE="github.com/gitleaks/gitleaks/v8@latest"

sudo_if_needed() {
  if [ "$(id -u)" -eq 0 ]; then
    "$@"
  else
    sudo "$@"
  fi
}

install_macos_tools() {
  if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew is required on macOS. Install Homebrew first."
    exit 1
  fi

  brew bundle --file Brewfile
}

install_terraform_ubuntu() {
  wget -O- https://apt.releases.hashicorp.com/gpg \
    | gpg --dearmor \
    | sudo_if_needed tee /usr/share/keyrings/hashicorp-archive-keyring.gpg >/dev/null

  local codename
  codename="$(. /etc/os-release && printf "%s" "$VERSION_CODENAME")"

  echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com ${codename} main" \
    | sudo_if_needed tee /etc/apt/sources.list.d/hashicorp.list >/dev/null

  sudo_if_needed apt-get update
  sudo_if_needed apt-get install -y terraform
}

install_hadolint_linux() {
  local arch
  arch="$(uname -m)"

  case "$arch" in
    x86_64) arch="x86_64" ;;
    aarch64 | arm64) arch="arm64" ;;
    *)
      echo "Unsupported Linux architecture for hadolint: ${arch}"
      exit 1
      ;;
  esac

  curl -sSfL \
    -o /tmp/hadolint \
    "https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-${arch}"
  chmod +x /tmp/hadolint
  sudo_if_needed mv /tmp/hadolint /usr/local/bin/hadolint
}

install_tflint_linux() {
  curl -sSfL https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh \
    | sudo_if_needed bash
}

install_go_tools() {
  local bin_dir
  bin_dir="$(mktemp -d)"

  GOBIN="$bin_dir" go install "$ACTIONLINT_PACKAGE"
  GOBIN="$bin_dir" go install "$GITLEAKS_PACKAGE"

  sudo_if_needed mv "$bin_dir/actionlint" /usr/local/bin/actionlint
  sudo_if_needed mv "$bin_dir/gitleaks" /usr/local/bin/gitleaks
  rmdir "$bin_dir"
}

install_ubuntu_tools() {
  if [ ! -f /etc/os-release ]; then
    echo "Ubuntu installation requires /etc/os-release."
    exit 1
  fi

  local os_id
  os_id="$(. /etc/os-release && printf "%s" "$ID")"
  if [ "$os_id" != "ubuntu" ]; then
    echo "Only Ubuntu is supported for Linux tool installation. Detected: ${os_id}"
    exit 1
  fi

  sudo_if_needed apt-get update
  sudo_if_needed apt-get install -y ca-certificates curl gnupg golang-go wget
  install_terraform_ubuntu
  install_tflint_linux
  install_hadolint_linux
  install_go_tools
}

case "$(uname -s)" in
  Darwin)
    install_macos_tools
    ;;
  Linux)
    install_ubuntu_tools
    ;;
  *)
    echo "Unsupported OS: $(uname -s)"
    exit 1
    ;;
esac
