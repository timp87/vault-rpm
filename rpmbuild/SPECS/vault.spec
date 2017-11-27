# https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Name:		vault
Version:	0.9.0
Release:	1%{?dist}
Summary:	Vault is a tool for securely accessing secrets
License:	MPLv2.0
Source0:	https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source1:	%{name}.hcl
Source2:	%{name}.service
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
cp -p %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/%{name}.hcl

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

mkdir -p %{buildroot}%{_unitdir}
cp -p %{SOURCE2} %{buildroot}%{_unitdir}

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/*

%files
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.hcl
%attr(0750,%{name},%{name}) %dir %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || \
    useradd -r -d %{_sharedstatedir}/%{name} -g %{name} \
    -s /sbin/nologin -c "Vault secret management tool" %{name}
exit 0

%post
%systemd_post %{name}.service
/sbin/setcap cap_ipc_lock=+ep %{_bindir}/%{name}

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Mon Nov 27 2017 Pavel Timofeev <timp87@gmail.com> - 0.9.0-1
- Update to 0.9.0

* Wed Jun 23 2017 Pavel Timofeev <timp87@gmail.com> - 0.7.3-1
- Update to 0.7.3

* Wed May 11 2017 Pavel Timofeev <timp87@gmail.com> - 0.7.2-1
- Update to 0.7.2

* Wed Apr 04 2017 Pavel Timofeev <timp87@gmail.com> - 0.7.0-1
- Update to 0.7.0

* Wed Feb 17 2017 Pavel Timofeev <timp87@gmail.com> - 0.6.5-1
- Update to 0.6.5

* Wed Jan 04 2016 Pavel Timofeev <timp87@gmail.com> - 0.6.4-1
- Initial package
