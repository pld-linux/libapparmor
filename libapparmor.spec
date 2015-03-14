# Conditional build:
%bcond_without	ruby			# build without Ruby bindings

%include	/usr/lib/rpm/macros.perl
Summary:	Library to provide key AppArmor symbols
Summary(pl.UTF-8):	Biblioteka udostępniająca kluczowe symbole AppArmor
Name:		libapparmor
Version:	2.9.1
Release:	1
Epoch:		1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://launchpad.net/apparmor/2.9/%{version}/+download/apparmor-%{version}.tar.gz
# Source0-md5:	0e036d69d7ebfb9cc113ed301b8a6c5d
URL:		http://apparmor.wiki.kernel.org/
BuildRequires:	autoconf
BuildRequires:	automake >= 1.4
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	perl-devel
BuildRequires:	perl-tools-pod
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.272
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	swig-perl
BuildRequires:	swig-python
%{?with_ruby:BuildRequires:	swig-ruby}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides the libapparmor library, which contains the
change_hat(2) symbol, used for sub-process confinement by AppArmor.
Applications that wish to make use of change_hat(2) need to link
against this library. This package is part of a suite of tools that
used to be named SubDomain.

%description -l pl.UTF-8
Ten pakiet udostępnia bibliotekę libapparmor, zawierającą symbol
change_hat(2), używany do więzienia podprocesów przez AppArmor.
Aplikacje chcące używać change_hat(2) muszą być linkowane z tą
biblioteką. Ten pakiet jest częścią zestawu narzędzi nazywanego
SubDomain.

%package devel
Summary:	Header files for libapparmor library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libapparmor
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
This is the package containing the header files for libapparmor
library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki libapparmor.

%package static
Summary:	Static libapparmor library
Summary(pl.UTF-8):	Statyczna biblioteka libapparmor
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static libapparmor library.

%description static -l pl.UTF-8
Statyczna biblioteka libapparmor.

%package -n perl-apparmor
Summary:	AppArmor Perl bindings
Summary(pl.UTF-8):	Dowiązania do AppArmor dla Perla
Summary(pt_BR.UTF-8):	Módulos Perl para acessar os recursos do AppArmor
Group:		Development/Languages/Perl
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n perl-apparmor
AppArmor Perl bindings.

%description -n perl-apparmor -l pl.UTF-8
Dowiązania do AppArmor dla Perla.

%description -n perl-apparmor -l pt_BR.UTF-8
Módulos Perl para acessar os recursos do AppArmor.

%package -n python-apparmor
Summary:	AppArmor Python bindings
Summary(pl.UTF-8):	Dowiązania do AppArmor dla Pythona
Summary(pt_BR.UTF-8):	Módulos Python para acessar os recursos do AppArmor
Group:		Development/Languages/Python
%pyrequires_eq  python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n python-apparmor
AppArmor Python bindings.

%description -n python-apparmor -l pl.UTF-8
Dowiązania do AppArmor dla Pythona.

%description -n python-apparmor -l pt_BR.UTF-8
Módulos Python para acessar os recursos do AppArmor.

%package -n ruby-apparmor
Summary:	AppArmor Ruby bindings
Summary(pl.UTF-8):	Dowiązania do AppArmor dla języka Ruby
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
%{?ruby_mod_ver_requires_eq}

%description -n ruby-apparmor
AppArmor Ruby bindings.

%description -n ruby-apparmor -l pl.UTF-8
Dowiązania do AppArmor dla języka Ruby.

%prep
%setup -q -n apparmor-%{version}

%build
cd libraries/libapparmor
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	%{?with_ruby:--with-ruby} \
	--with-python \
	--with-perl

%{__make} -j1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 -C libraries/libapparmor install \
	RUBYARCHDIR=$RPM_BUILD_ROOT%{ruby_vendorarchdir} \
	DESTDIR=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libapparmor.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libapparmor.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libapparmor.so
%{_libdir}/libapparmor.la
%{_includedir}/aalogparse
%{_includedir}/sys/apparmor.h
%{_pkgconfigdir}/libapparmor.pc
%{_mandir}/man2/aa_change_hat.2*
%{_mandir}/man2/aa_change_profile.2*
%{_mandir}/man2/aa_find_mountpoint.2*
%{_mandir}/man2/aa_getcon.2*

%files static
%defattr(644,root,root,755)
%{_libdir}/libapparmor.a

%files -n perl-apparmor
%defattr(644,root,root,755)
%{perl_vendorarch}/LibAppArmor.pm
%dir %{perl_vendorarch}/auto/LibAppArmor
%attr(755,root,root) %{perl_vendorarch}/auto/LibAppArmor/LibAppArmor.so

%files -n python-apparmor
%defattr(644,root,root,755)
%dir %{py_sitedir}/LibAppArmor
%attr(755,root,root) %{py_sitedir}/LibAppArmor/_LibAppArmor.so
%{py_sitedir}/LibAppArmor/__init__.py[co]
%{py_sitedir}/LibAppArmor-*.egg-info

%if %{with ruby}
%files -n ruby-apparmor
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/LibAppArmor.so
%endif
