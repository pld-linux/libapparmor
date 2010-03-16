#
# TODO:
# - add subpackages: perl-apparmor, python-apparmor
#
Summary:	Library to provide key AppArmor symbols
Summary(pl.UTF-8):	Biblioteka udostępniająca kluczowe symbole AppArmor
Name:		libapparmor
Version:	2.5
Release:	1
Epoch:		1
License:	LGPL
Group:		Libraries
Source0:	http://kernel.org/pub/linux/security/apparmor/AppArmor-%{version}/AppArmor-%{version}.tgz
# Source0-md5:	4a747d1a1f85cb272d55b52c7e8a4a02
URL:		http://apparmor.wiki.kernel.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	perl-devel
BuildRequires:	perl-tools-pod
BuildRequires:	python-devel
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

%prep
%setup -q -n AppArmor-%{version}

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
