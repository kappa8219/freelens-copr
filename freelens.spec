%global debug_package %{nil}
%global __strip /bin/true
%global __requires_exclude_from /opt/Freelens/.*

Name:           freelens
Version:        1.10.2
Release:        2%{?dist}
Summary:        Free IDE for Kubernetes
License:        MIT
URL:            https://freelens.app
Source0:        https://github.com/freelensapp/freelens/releases/download/v%{version}/Freelens-%{version}-linux-amd64.rpm

BuildRequires:  cpio
BuildRequires:  desktop-file-utils
BuildRequires:  rpm

Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       gtk3
Requires:       libnotify
Requires:       libXScrnSaver
Requires:       mesa-libgbm
Requires:       nss
Requires:       xdg-utils

%description
Freelens is a free and open source IDE for Kubernetes.

%prep
echo "4f20ec36892c0402c80d0ba1f78c94ffbc279d0b7d9a17998e5ee9bdb19fbd6c  %{SOURCE0}" | sha256sum --check

%install
rpm2cpio %{SOURCE0} | cpio --extract --make-directories --quiet --directory %{buildroot}
install -d %{buildroot}%{_bindir}
ln -s /opt/Freelens/freelens %{buildroot}%{_bindir}/freelens

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/freelens.desktop

%files
%license /opt/Freelens/LICENSE.electron.txt
%license /opt/Freelens/LICENSES.chromium.html
/opt/Freelens
%{_bindir}/freelens
%{_datadir}/applications/freelens.desktop
%{_datadir}/icons/hicolor/*/apps/freelens.png
%{_metainfodir}/app.freelens.Freelens.metainfo.xml

%changelog
* Mon Aug 17 2026 kappa8219 <4374115+kappa8219@users.noreply.github.com> - 1.10.2-2
- Package Freelens 1.10.2

* Fri Jul 31 2026 OK <o.kraievyi@quadient.com> - 1.10.3-2
- Package the upstream Freelens RPM for COPR
