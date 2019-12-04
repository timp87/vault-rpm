# https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Name:		vault
Version:	1.3.0
Release:	1%{?dist}
Summary:	Vault is a tool for securely accessing secrets
License:	MPLv2.0
Source0:	https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source1:	server.hcl
Source2:	agent.hcl
Source3:	%{name}-server.sysconfig
Source4:	%{name}-agent.sysconfig
Source5:	%{name}@.service

BuildRequires:	systemd-units
Requires(pre):	shadow-utils
Requires(post):	systemd libcap
Requires(preun):	systemd
Requires(postun):	systemd
URL:		https://www.vaultproject.io/

%define debug_package %{nil}

%description
Vault secures, stores, and tightly controls access to tokens, passwords,
certificates, API keys, and other secrets in modern computing. Vault handles
leasing, key revocation, key rolling, and auditing. Through a unified API, users
can access an encrypted Key/Value store and network encryption-as-a-service, or
generate AWS IAM/STS credentials, SQL/NoSQL databases, X.509 certificates, SSH
credentials, and more.

%prep
%autosetup -c %{name}-%{version}

%build

%install

mkdir -p %{buildroot}%{_bindir}/
cp -p %{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp -p %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/server.hcl
cp -p %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/agent.hcl

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp -p %{SOURCE3} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}-server
cp -p %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}-agent

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

mkdir -p %{buildroot}%{_unitdir}
cp -p %{SOURCE5} %{buildroot}%{_unitdir}

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

%files
%defattr(644,root,root,755)
%caps(cap_ipc_lock=+ep) %attr(755, -, -) %{_bindir}/%{name}

%dir %attr(-, %{name}, %{name}) %{_sysconfdir}/%{name}
%config(noreplace) %attr(750, %{name}, %{name}) %{_sysconfdir}/%{name}/server.hcl
%config(noreplace) %attr(750, %{name}, %{name}) %{_sysconfdir}/%{name}/agent.hcl

%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-server
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-agent

%dir %attr(750,%{name},%{name}) %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}@.service

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || \
    useradd -r -d %{_sharedstatedir}/%{name} -g %{name} \
    -s /sbin/nologin -c "Vault secret management tool" %{name}
exit 0

%post
%systemd_post %{name}@server.service
%systemd_post %{name}@agent.service

%preun
%systemd_preun %{name}@server.service
%systemd_preun %{name}@agent.service

%postun
%systemd_postun_with_restart %{name}@server.service
%systemd_postun_with_restart %{name}@agent.service

%changelog
* Wed Dec 04 2019 Pavel Timofeev <timp87@gmail.com> - 1.3.0-1
- Update to 1.3.0
- Rework package to support both vault server and agent

* Thu Oct 17 2019 Pavel Timofeev <timp87@gmail.com> - 1.2.3-1
- Update to 1.2.3

* Wed Apr 03 2019 Pavel Timofeev <timp87@gmail.com> - 1.1.0-1
- Update to 1.1.0

* Thu Mar 14 2019 Pavel Timofeev <timp87@gmail.com> - 1.0.3-1
- Update to 1.0.3

* Wed Jan 09 2019 Pavel Timofeev <timp87@gmail.com> - 1.0.1-1
- Update to 1.0.1

* Wed Nov 21 2018 Pavel Timofeev <timp87@gmail.com> - 0.11.5-1
- Update to 0.11.5

* Fri Nov 02 2018 Pavel Timofeev <timp87@gmail.com> - 0.11.4-1
- Update to 0.11.4

* Fri Sep 21 2018 Pavel Timofeev <timp87@gmail.com> - 0.11.1-1
- Update to 0.11.1

* Fri Jun 29 2018 Pavel Timofeev <timp87@gmail.com> - 0.10.3-1
- Update to 0.10.3

* Tue Feb 27 2018 Pavel Timofeev <timp87@gmail.com> - 0.9.5-1
- Update to 0.9.5

* Mon Jan 29 2018 Pavel Timofeev <timp87@gmail.com> - 0.9.3-1
- Update to 0.9.3

* Sun Jan 28 2018 Pavel Timofeev <timp87@gmail.com> - 0.9.2-1
- Update to 0.9.2
- Change vault config file extension from hcl to conf

* Wed Dec 27 2017 Pavel Timofeev <timp87@gmail.com> - 0.9.1-1
- Update to 0.9.1

* Mon Nov 27 2017 Pavel Timofeev <timp87@gmail.com> - 0.9.0-1
- Update to 0.9.0

* Fri Jun 23 2017 Pavel Timofeev <timp87@gmail.com> - 0.7.3-1
- Update to 0.7.3

* Thu May 11 2017 Pavel Timofeev <timp87@gmail.com> - 0.7.2-1
- Update to 0.7.2

* Tue Apr 04 2017 Pavel Timofeev <timp87@gmail.com> - 0.7.0-1
- Update to 0.7.0

* Fri Feb 17 2017 Pavel Timofeev <timp87@gmail.com> - 0.6.5-1
- Update to 0.6.5

* Wed Jan 04 2017 Pavel Timofeev <timp87@gmail.com> - 0.6.4-1
- Initial package
