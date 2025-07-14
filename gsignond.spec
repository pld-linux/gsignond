#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
%bcond_without	ostro		# Ostro extension (trousers+ecryptfs)
%bcond_without	tizen		# Tizen extension (smack+ecryptfs)

Summary:	Single-sign-on daemon
Summary(pl.UTF-8):	Demon wspólnego logowania (single-sign-on)
Name:		gsignond
Version:	1.0.6
Release:	1
License:	LGPL v2.1+
Group:		Daemons
#Source0Download: https://gitlab.com/accounts-sso/gsignond/tags
Source0:	https://gitlab.com/accounts-sso/gsignond/repository/archive.tar.bz2?ref=%{version}&fake_out=/%{name}-%{version}.tar.bz2
# Source0-md5:	6cc5286f83ca8e398347c735557e2f4a
Patch0:		%{name}-update.patch
URL:		https://gitlab.com/accounts-sso/gsignond
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
BuildRequires:	check-devel >= 0.9.4
BuildRequires:	dbus-devel
%if %{with ostro} || %{with tizen}
BuildRequires:	ecryptfs-utils-devel >= 96
%endif
BuildRequires:	glib2-devel >= 1:2.30
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk-doc >= 1.18
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
%{?with_tizen:BuildRequires:	smack-devel >= 1.0}
BuildRequires:	sqlite3-devel >= 3
%{?with_ostro:BuildRequires:	trousers-devel}
BuildRequires:	vala
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Single-sign-on daemon.

%description -l pl.UTF-8
Demon wspólnego logowania (single-sign-on).

%package extension-ostro
Summary:	Ostro extension for gsignond
Summary(pl.UTF-8):	Rozszerzenie Ostro dla gsignond
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ecryptfs-utils >= 96

%description extension-ostro
Ostro extension for gsignond.

%description extension-ostro -l pl.UTF-8
Rozszerzenie Ostro dla gsignond.

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

%package -n vala-gsignond
Summary:	Vala API for gsignond library
Summary(pl.UTF-8):	API języka Vala do biblioteki gsignond
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala

%description -n vala-gsignond
Vala API for gsignond library.

%description -n vala-gsignond -l pl.UTF-8
API języka Vala do biblioteki gsignond.

%package apidocs
Summary:	API documentation for gsignond
Summary(pl.UTF-8):	Dokumentacja API gsidnond
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for gsignond.

%description apidocs -l pl.UTF-8
Dokumentacja API gsidnond.

%prep
%setup -q -n %{name}-%{version}-3214aef8e7c84a9918d8b18fb258247d81be12e2
%patch -P0 -p1

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

%if %{with ostro}
%files extension-ostro
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gsignond/extensions/libextension-ostro.so
%endif

%if %{with tizen}
%files extension-tizen
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gsignond/extensions/libextension-tizen.so
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgsignond-common.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgsignond-common.so.0
%{_libdir}/girepository-1.0/gSignond-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgsignond-common.so
%{_includedir}/gsignond
%{_datadir}/dbus-1/interfaces/com.google.code.AccountsSSO.gSingleSignOn.*.xml
%{_datadir}/gir-1.0/gSignond-1.0.gir
%{_pkgconfigdir}/gsignond.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgsignond-common.a
%endif

%files -n vala-gsignond
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gsignond.deps
%{_datadir}/vala/vapi/gsignond.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gsignond
%endif
