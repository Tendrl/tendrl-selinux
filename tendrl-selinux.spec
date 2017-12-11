# defining macros needed by SELinux
%global selinuxtype        targeted
%global selinux_policyver  3.13.1-166
%global moduletype         services
%global modulenames        tendrl carbon collectd grafana

# Usage: _format var format
#   Expand 'modulenames' into various formats as needed
#   Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;

Name:           tendrl-selinux
Version:        1.5.4
Release:        2%{?dist}
Summary:        SELinux policy for Tendrl

License:        LGPLv2.1
Url:            https://github.com/Tendrl/tendrl-selinux
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       selinux-policy >= %{selinux_policyver}
BuildRequires:  git
BuildRequires:  bzip2
BuildRequires:  pkgconfig(systemd)
BuildRequires:  selinux-policy
BuildRequires:  selinux-policy-devel
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): libselinux-utils
Requires(post): policycoreutils
Requires(post): policycoreutils-python

%description
SELinux policy module for Tendrl.

%package -n carbon-selinux
Summary:        SELinux policy for Carbon
Requires:       selinux-policy >= %{selinux_policyver}
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): libselinux-utils
Requires(post): policycoreutils
Requires(post): policycoreutils-python

%description -n carbon-selinux
SELinux policy module for Carbon.

%package -n tendrl-collectd-selinux
Summary:        SELinux policy for Tendrl Collectd
Requires:       selinux-policy >= %{selinux_policyver}
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): libselinux-utils
Requires(post): policycoreutils
Requires(post): policycoreutils-python

%description -n tendrl-collectd-selinux
SELinux policy module for Tendrl Collectd.

%package -n tendrl-grafana-selinux
Summary:        SELinux policy for Tendrl Grafana
Requires:       selinux-policy >= %{selinux_policyver}
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): libselinux-utils
Requires(post): policycoreutils
Requires(post): policycoreutils-python

%description -n tendrl-grafana-selinux
SELinux policy module for Tendrl Grafana.

%prep
%setup -q

%build
make DATADIR="%{_datadir}" TARGETS="%{modulenames}" modules

%pre
%selinux_relabel_pre -s %{selinuxtype}

%install
# Create directories where SELinux polies will be installed
install -d %{buildroot}%{_datadir}/selinux/packages
install -d -p %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -d -p %{buildroot}%{_pkgdocdir}/

# Install SELinux interfaces
%_format INTERFACES $x.if
install -p -m 644 $INTERFACES %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}

# Install policy modules
%_format MODULES $x.pp.bz2
install -m 0644 $MODULES %{buildroot}%{_datadir}/selinux/packages

# Install readme and license files
install -p -m 644 README.md    %{buildroot}%{_pkgdocdir}/README.md
install -p -m 644 LICENSE      %{buildroot}%{_pkgdocdir}/LICENSE

%check

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/tendrl.pp.bz2

%post -n carbon-selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/carbon.pp.bz2

%post -n tendrl-collectd-selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/collectd.pp.bz2

%post -n tendrl-grafana-selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/grafana.pp.bz2

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} tendrl
fi

%postun -n carbon-selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} carbon
fi

%postun -n tendrl-collectd-selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} collectd
fi

%postun -n tendrl-grafana-selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} grafana
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%files
%defattr(-,root,root,0755)
%attr(0644,root,root) %{_datadir}/selinux/packages/tendrl.pp.bz2
%attr(0644,root,root) %{_datadir}/selinux/devel/include/%{moduletype}/tendrl.if
# readme and license files
%doc      %{_pkgdocdir}/README.md
%license  %{_pkgdocdir}/LICENSE

%files -n carbon-selinux
%attr(0644,root,root) %{_datadir}/selinux/packages/carbon.pp.bz2
%attr(0644,root,root) %{_datadir}/selinux/devel/include/%{moduletype}/carbon.if

%files -n tendrl-collectd-selinux
%attr(0644,root,root) %{_datadir}/selinux/packages/collectd.pp.bz2
%attr(0644,root,root) %{_datadir}/selinux/devel/include/%{moduletype}/collectd.if

%files -n tendrl-grafana-selinux
%attr(0644,root,root) %{_datadir}/selinux/packages/grafana.pp.bz2
%attr(0644,root,root) %{_datadir}/selinux/devel/include/%{moduletype}/grafana.if

%changelog
* Mon Dec 11 2017 Rohan Kanade <rkanade@redhat.com> - 1.5.4-2
- Fix /var/log/tendrl/* perms

* Fri Nov 24 2017 Rohan Kanade <rkanade@redhat.com> - 1.5.4-1
- tendrl-selinux 1.5.4

* Thu Oct 12 2017 Martin Bukatovič <mbukatov@redhat.com> - 1.5.3-1
- First build of Tendrl SELinux policies
