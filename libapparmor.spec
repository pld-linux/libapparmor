%include	/usr/lib/rpm/macros.perl
Summary:	Library to provide key AppArmor symbols
Summary(pl.UTF-8):	Biblioteka udostępniająca kluczowe symbole AppArmor
Name:		libapparmor
Version:	2.6.0
Release:	1
Epoch:		1
License:	LGPL
Group:		Libraries
Source0:	http://launchpad.net/apparmor/2.6/%{version}/+download/apparmor-%{version}.tar.gz
# Source0-md5:	3b4fb4186ac6440a03d8f2dcf188d4b4
URL:		http://apparmor.wiki.kernel.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	perl-devel
BuildRequires:	perl-tools-pod
BuildRequires:	python-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-perl
BuildRequires:	swig-python
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
%prep
%setup -q -n apparmor-%{version}

%build
cd libraries/libapparmor
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--with-python \
	--with-perl \
	--without-ruby

%{__make} -j1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C libraries/libapparmor install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/aalogparse
%{_includedir}/sys/*.h
%{_mandir}/man2/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files -n python-apparmor
%defattr(644,root,root,755)
%dir %{py_sitedir}/LibAppArmor
%attr(755,root,root) %{py_sitedir}/LibAppArmor/*.so
%{py_sitedir}/LibAppArmor/*.py[co]
%{py_sitedir}/*.egg-info

%files -n perl-apparmor
%defattr(644,root,root,755)
%{perl_vendorarch}/*.pm
%dir %{perl_vendorarch}/auto/LibAppArmor
%attr(755,root,root) %{perl_vendorarch}/auto/LibAppArmor/*.so
