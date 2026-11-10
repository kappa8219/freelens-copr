# Freelens COPR packaging

This repository repackages the official Freelens RPM for Fedora COPR. It does
not build Freelens from source. The spec downloads the exact upstream release
asset and verifies its SHA-256 checksum before extracting its payload.

## Update procedure

1. Obtain the current x86_64 RPM's version, download URL, and SHA-256 digest
   from [Freelens releases](https://github.com/freelensapp/freelens/releases).
2. Update `Version`, `Release`, the `Source0` URL, the checksum in
   `freelens.spec`, and `source_url` in `.copr/Makefile`.
3. Build from SCM in COPR for Fedora 43, 44, 45, and Rawhide.

Install the resulting package with:

```bash
sudo dnf copr enable ok8219/Freelens
sudo dnf install freelens
```

## FreeLens 2

`freelens2` is a separate COPR package built from the official FreeLens 2 RPM:

```bash
sudo dnf copr enable ok8219/freelens2
sudo dnf install freelens2
```

The v1 `freelens` and `freelens2` RPMs use the same application paths and
cannot be installed together. FreeLens 2 also has a breaking extension API:
v1 extensions must be updated and reinstalled; they are not migrated.
