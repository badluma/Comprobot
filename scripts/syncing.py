#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys
import tomllib

DEB_MAP = {
    "requests": "python3-requests",
    "appdirs": "python3-appdirs",
    "python-dotenv": "python3-dotenv",
    "httpx": "python3-httpx",
    "tomlkit": "python3-tomlkit",
}


def load_pyproject():
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"], data["project"]["dependencies"]


def desired_pkgbuild(current, version, deps):
    out = re.sub(r"^pkgver=.*$", f"pkgver={version}", current, flags=re.MULTILINE)
    pip_line = '    pip install --root="$pkgdir" --prefix=/usr ' + " ".join(deps) + "\n"
    return re.sub(
        r'    pip install --root="\$pkgdir" --prefix=/usr (?!--no-deps).*\n',
        pip_line,
        out,
    )


def desired_control(current, deps):
    deb_deps = ["${python3:Depends}", "python3-pip"]
    for dep in deps:
        base = re.sub(r"\[.*?\]", "", dep).strip().lower()
        base = re.split(r"[>=<!;\s]", base)[0].strip()
        if base in DEB_MAP:
            deb_deps.append(DEB_MAP[base])
    return re.sub(
        r"^Depends:.*$",
        "Depends: " + ", ".join(deb_deps),
        current,
        flags=re.MULTILINE,
    )


def changelog_in_sync(version):
    with open("debian/changelog") as f:
        return f.readline().startswith(f"comprobot ({version})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--check", action="store_true", help="report drift, change nothing"
    )
    args = ap.parse_args()

    version, deps = load_pyproject()

    with open("aur/PKGBUILD") as f:
        pkgbuild = f.read()
    new_pkgbuild = desired_pkgbuild(pkgbuild, version, deps)

    with open("debian/control") as f:
        control = f.read()
    new_control = desired_control(control, deps)

    drift = []
    if new_pkgbuild != pkgbuild:
        drift.append("aur/PKGBUILD")
    if new_control != control:
        drift.append("debian/control")
    if not changelog_in_sync(version):
        drift.append("debian/changelog")

    if args.check:
        if drift:
            print(
                f"::error::Packaging files out of sync with pyproject.toml: "
                f"{', '.join(drift)}. Push to main so 'Sync Dependencies' runs, "
                f"then re-tag.",
                file=sys.stderr,
            )
            return 1
        print("Packaging files in sync.")
        return 0

    if new_pkgbuild != pkgbuild:
        with open("aur/PKGBUILD", "w") as f:
            f.write(new_pkgbuild)
    if new_control != control:
        with open("debian/control", "w") as f:
            f.write(new_control)
    if not changelog_in_sync(version):
        subprocess.run(
            ["dch", "--newversion", version, "--distribution", "noble", f"Release {version}."],
            env={**os.environ, "DEBEMAIL": "macumba-51sandbar@icloud.com", "DEBFULLNAME": "badluma"},
            check=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
