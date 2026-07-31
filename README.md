# Freelens COPR packaging

This repository repackages the official Freelens RPM for Fedora COPR. It does
not build Freelens from source. The spec downloads the exact upstream release
asset and verifies its SHA-256 checksum before extracting its payload.

## Update procedure

1. Obtain the current x86_64 RPM's version, download URL, and SHA-256 digest
   from [Freelens releases](https://github.com/freelensapp/freelens/releases).
2. Update `Version`, `Release`, the `Source0` URL if its naming changes, and
   the checksum in `freelens.spec`.
3. Build from SCM in COPR for the desired Fedora chroots.

Install the resulting package with:

```bash
sudo dnf copr enable ok8219/Freelens
sudo dnf install freelens
```
