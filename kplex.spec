Name: kplex
Summary: A multiplexer for various NMEA-0183 interfaces
Version: 1.3.4
Release: 1%{?dist}
License: GPLv3+
Source0: http://www.stripydog.com/download/kplex-%{version}.tgz
Source1: kplex.service

%{?systemd_ordering}
BuildRequires: systemd

Requires(pre): shadow-utils

%description
A multiplexer for various NMEA-0183 interfaces

%prep
%setup0
sed -ie 's/-g $(INSTGROUP) -o root//' Makefile

%build
%make_build CFLAGS="%{optflags}" LDFLAGS="%{__global_ldflags}"

%install
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
%make_install
cp -a kplex.conf.ex %{buildroot}%{_sysconfdir}/kplex.conf
cp %{SOURCE1} %{buildroot}%{_unitdir}/kplex.service

%pre
getent group kplex >/dev/null || groupadd -r GROUPNAME
getent passwd kplex >/dev/null || \
    useradd -r -g kplex -d  -s /sbin/nologin \
	    -c "NMEA-0183 multiplexer" kplex
usermod -a -G dialout kplex
exit 0

%post
%systemd_post kplex.service

%preun
%systemd_preun kplex.service

%postun
%systemd_postun_with_restart kplex.service

%files
%doc README CHANGELOG COPYING kplex.conf.ex
%config(noreplace) %attr(644,kplex,kplex) %{_sysconfdir}/kplex.conf
%{_unitdir}/kplex.service
%{_bindir}/kplex
