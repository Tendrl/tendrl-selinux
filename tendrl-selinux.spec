# defining macros needed by SELinux
%global selinuxtype        targeted
%global selinux_policyver  3.13.1-166
%global moduletype         services
%global modulenames        tendrl carbon grafana collectd

# Usage: _format var format
#   Expand 'modulenames' into various formats as needed
#   Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;

Name:           tendrl-selinux
Version:        1.5.3
Release:        1%{?dist}
Summary:        SELinux policies for Tendrl

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
SELinux policy modules for Tendrl.

%prep
%setup -q

%build
make SHAREDIR="%{_datadir}" TARGETS="%{modulenames}"

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
# TODO: is it possible to loop over %{modulenames} variable?
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/tendrl
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/carbon
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/grafana
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/collectd

%postun
if [ $1 -eq 0 ]; then
    # TODO: is it possible to loop over %{modulenames} variable?
    %selinux_modules_uninstall -s %{selinuxtype} tendrl
    %selinux_modules_uninstall -s %{selinuxtype} carbon
    %selinux_modules_uninstall -s %{selinuxtype} grafana
    %selinux_modules_uninstall -s %{selinuxtype} collectd
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%files
%defattr(-,root,root,0755)
%attr(0644,root,root) %{_datadir}/selinux/packages/*.pp.bz2
%attr(0644,root,root) %{_datadir}/selinux/devel/include/%{moduletype}/*.if
# readme and license files
%doc      %{_pkgdocdir}/README.md
%license  %{_pkgdocdir}/LICENSE

%changelog
* Wed Oct 11 2017 Martin Bukatovič <mbukatov@redhat.com> - 1.5.3-1
- First Build
