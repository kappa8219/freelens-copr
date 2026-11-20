#!/usr/bin/env python3
"""Prepare update PRs for the latest stable FreeLens v1 and v2 releases."""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
API_URL = "https://api.github.com/repos/freelensapp/freelens/releases?per_page=100"
ASSET_BASE = "https://github.com/freelensapp/freelens/releases/download/"
CHANNELS = {
    1: ("freelens.spec", 1),
    2: ("freelens2.spec", 2),
}


def get(url):
    return urlopen(Request(url, headers={"User-Agent": "freelens-copr-release-check"}), timeout=180)


def version_tuple(version):
    if not re.fullmatch(r"\d+(?:\.\d+)+", version):
        raise ValueError(f"Unexpected release version: {version}")
    return tuple(int(part) for part in version.split("."))


def replace_once(text, pattern, replacement, label):
    result, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(f"Expected one {label}; found {count}")
    return result


def main():
    with get(API_URL) as response:
        releases = json.load(response)

    latest = {}
    for release in releases:
        if release.get("draft") or release.get("prerelease"):
            continue
        version = release.get("tag_name", "").removeprefix("v")
        try:
            key = version_tuple(version)
        except ValueError:
            continue
        major = key[0]
        if major not in CHANNELS:
            continue
        previous = latest.get(major)
        if previous is None or key > previous[0]:
            latest[major] = (key, version, release)

    if set(latest) != set(CHANNELS):
        raise ValueError("Could not find stable releases for both the v1 and v2 package channels")

    updates = []
    for major, (filename, _) in CHANNELS.items():
        spec_path = ROOT / filename
        spec = spec_path.read_text()
        match = re.search(r"^Version:\s+(\S+)$", spec, re.MULTILINE)
        if not match:
            raise ValueError(f"Could not read version from {filename}")
        current = match.group(1)
        _, version, release = latest[major]
        if version_tuple(version) <= version_tuple(current):
            continue

        name = f"Freelens-{version}-linux-amd64.rpm"
        assets = {asset.get("name"): asset.get("browser_download_url") for asset in release.get("assets", [])}
        url = assets.get(name)
        if not url or not url.startswith(ASSET_BASE):
            raise ValueError(f"Release {version} is missing expected asset {name}")
        digest = hashlib.sha256()
        with get(url) as response:
            while chunk := response.read(1024 * 1024):
                digest.update(chunk)

        spec = replace_once(spec, r"^(Version:\s+)\S+$", rf"\g<1>{version}", "Version")
        spec = replace_once(
            spec,
            r'^(echo ")[0-9a-f]{64}(  %\{SOURCE0\}" \| sha256sum --check)$',
            rf"\g<1>{digest.hexdigest()}\g<2>",
            "source checksum",
        )
        spec = replace_once(spec, r"^(Release:\s+)\S+$", r"\g<1>1%{?dist}", "Release")
        date = datetime.now(timezone.utc).strftime("%a %b %d %Y")
        package = "FreeLens" if major == 1 else "FreeLens 2"
        entry = f"* {date} OK <4374115+kappa8219@users.noreply.github.com> - {version}-1\n- Update {package} to {version}\n\n"
        spec = replace_once(spec, r"^%changelog[ \t]*\n", "%changelog\n" + entry, "changelog")
        spec_path.write_text(spec)
        updates.append(f"v{major}={version}")

    makefile_path = ROOT / ".copr/Makefile"
    makefile = makefile_path.read_text()
    v1 = latest[1][1]
    makefile = replace_once(makefile, r"^(version := )\S+$", rf"\g<1>{v1}", "v1 Makefile version")
    makefile_path.write_text(makefile)

    print(f"updated={'true' if updates else 'false'}")
    print(f"versions=v1-{latest[1][1]}-v2-{latest[2][1]}")
    print("release_url=https://github.com/freelensapp/freelens/releases")
    if updates:
        print(f"updated_channels={','.join(updates)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Release update failed: {error}", file=sys.stderr)
        sys.exit(1)
