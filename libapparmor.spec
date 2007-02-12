%define		_ver 2.0
%define		_svnrel 132
Summary:	Library to provide key AppArmor symbols
Summary(pl.UTF-8):   Biblioteka udostępniająca kluczowe symbole AppArmor
Name:		libapparmor
Version:	%{_ver}.%{_svnrel}
Release:	0.8
License:	LGPL
Group:		Libraries
Source0:	http://forgeftp.novell.com/apparmor/Development%20-%20September%20snapshot/%{name}-%{_ver}-%{_svnrel}.tar.gz
# Source0-md5:	2253abf77f478fc1d02ad8e870bf7228
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
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
Summary(pl.UTF-8):   Pliki nagłówkowe biblioteki libapparmor
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for libapparmor
library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki libapparmor.

%package static
Summary:	Static libapparmor library
Summary(pl.UTF-8):   Statyczna biblioteka libapparmor
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libapparmor library.

%description static -l pl.UTF-8
Statyczna biblioteka libapparmor.

%prep
%setup -q -n %{name}-%{_ver}

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIB=%{_lib} \
	VERSION=%{version} \
	RELEASE=%{release}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/sys/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
