%global debug_package %{nil}
%global __strip /bin/true
%global __requires_exclude_from /opt/Freelens/.*

Name:           freelens2
Version:        2.0.0
Release:        1%{?dist}
Summary:        FreeLens 2 Kubernetes IDE
License:        MIT
URL:            https://freelens.app
Source0:        https://github.com/freelensapp/freelens/releases/download/v%{version}/Freelens-%{version}-linux-amd64.rpm
ExclusiveArch:  x86_64

BuildRequires:  cpio
BuildRequires:  desktop-file-utils
BuildRequires:  rpm

Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       gtk3
Requires:       libdrm
Requires:       libnotify
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       mesa-libgbm
Requires:       nss
Requires:       xdg-utils

# Upstream v1 and v2 both own /opt/Freelens and the desktop integration files.
Conflicts:      freelens

%description
FreeLens 2 is a free and open source IDE for Kubernetes. It is repackaged
from the official upstream RPM. FreeLens v1 extensions must be updated and
reinstalled for v2.

%prep
echo "b4d80f5dccbc0aa93cce44b34f064f3190cc88d61e7c7fe368488878412626d2  %{SOURCE0}" | sha256sum --check
rpm -qp --qf '%%{NAME} %%{VERSION}\n' %{SOURCE0} | grep -Fx 'freelens %{version}'

%install
rpm2cpio %{SOURCE0} | cpio --extract --make-directories --quiet --directory %{buildroot}
install -d %{buildroot}%{_bindir}
ln -s /opt/Freelens/freelens %{buildroot}%{_bindir}/freelens
ln -s /opt/Freelens/freelens %{buildroot}%{_bindir}/freelens2

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/freelens.desktop

%files
%license /opt/Freelens/LICENSE.electron.txt
%license /opt/Freelens/LICENSES.chromium.html
/opt/Freelens
%{_bindir}/freelens
%{_bindir}/freelens2
%{_datadir}/applications/freelens.desktop
%{_datadir}/icons/hicolor/*/apps/freelens.png
%{_metainfodir}/app.freelens.Freelens.metainfo.xml

%changelog
* Tue Nov 10 2026 OK <4374115+kappa8219@users.noreply.github.com> - 2.0.0-1
- Package the official FreeLens 2.0.0 RPM separately from FreeLens v1
