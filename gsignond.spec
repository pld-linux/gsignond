#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
%bcond_without	tizen		# Tizen extension (smack+ecryptfs)
#
Summary:	Single-sign-on daemon
Summary(pl.UTF-8):	Demon wspólnego logowania (single-sign-on)
Name:		gsignond
Version:	1.0.1
Release:	1
License:	LGPL v2.1+
Group:		Daemons
#Source0Download: https://gitlab.com/accounts-sso/gsignond/tags
Source0:	https://gitlab.com/accounts-sso/gsignond/repository/archive.tar.bz2?ref=1.0.1&fake_out=/%{name}-%{version}.tar.bz2
# Source0-md5:	c5a85fb3e98ebf6668b6ed448ab5da5d
URL:		https://gitlab.com/accounts-sso/gsignond
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
BuildRequires:	check-devel >= 0.9.4
%{?with_tizen:BuildRequires:	ecryptfs-utils-devel >= 96}
BuildRequires:	glib2-devel >= 1:2.30
BuildRequires:	gtk-doc >= 1.18
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
%{?with_tizen:BuildRequires:	smack-devel >= 1.0}
BuildRequires:	sqlite3-devel >= 3
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Single-sign-on daemon.

%description -l pl.UTF-8
Demon wspólnego logowania (single-sign-on).

%package extension-tizen
Summary:	Tizen extension for gsignond
Summary(pl.UTF-8):	Rozszerzenie Tizen dla gsignond
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ecryptfs-utils >= 96
Requires:	smack-libs >= 1.0

%description extension-tizen
Tizen extension for gsignond.

%description extension-tizen -l pl.UTF-8
Rozszerzenie Tizen dla gsignond.

%package libs
Summary:	Single sign-on daemon library
Summary(pl.UTF-8):	Biblioteka demona wspólnego logowania
Group:		Libraries

%description libs
Single sign-on daemon library.

%description libs -l pl.UTF-8
Biblioteka demona wspólnego logowania.

%package devel
Summary:	Header files for gsignond library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gsignond
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.30
Requires:	sqlite3-devel >= 3

%description devel
Header files for gsignond library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gsignond.

%package static
Summary:	Static gsignond library
Summary(pl.UTF-8):	Statyczna biblioteka gsignond
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gsignond library.

%description static -l pl.UTF-8
Statyczna biblioteka gsignond.

%package apidocs
Summary:	API documentation for gsignond
Summary(pl.UTF-8):	Dokumentacja API gsidnond
Group:		Documentation

%description apidocs
API documentation for gsignond.

%description apidocs -l pl.UTF-8
Dokumentacja API gsidnond.

%prep
%setup -q -n %{name}-%{version}-61538c810dbe355e006e4e61a53271b3ce81a150

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# loadable modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gsignond/*/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gsignond/*/*.a
%endif
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gsignond.conf
%attr(755,root,root) %{_bindir}/gsignond
%dir %{_libdir}/gsignond
%dir %{_libdir}/gsignond/extensions
%attr(755,root,root) %{_libdir}/gsignond/extensions/libextension-test.so
%dir %{_libdir}/gsignond/gplugins
%attr(755,root,root) %{_libdir}/gsignond/gplugins/libdigest.so
%attr(755,root,root) %{_libdir}/gsignond/gplugins/libpassword.so
%attr(755,root,root) %{_libdir}/gsignond/gplugins/libssotest.so
%dir %{_libdir}/gsignond/pluginloaders
%attr(755,root,root) %{_libdir}/gsignond/pluginloaders/gsignond-plugind

%files extension-tizen
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gsignond/extensions/libextension-tizen.so

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgsignond-common.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgsignond-common.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgsignond-common.so
%{_includedir}/gsignond
%{_pkgconfigdir}/gsignond.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgsignond-common.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gsignond
%endif
