#
# Conditional build:
%bcond_without	ruby		# build without Ruby bindings
%bcond_with	python3		# build for Python3

%include	/usr/lib/rpm/macros.perl
Summary:	Library to provide key AppArmor symbols
Summary(pl.UTF-8):	Biblioteka udostępniająca kluczowe symbole AppArmor
Name:		libapparmor
Version:	2.11.0
Release:	3
Epoch:		1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://launchpad.net/apparmor/2.11/2.11/+download/apparmor-%{version}.tar.gz
# Source0-md5:	899fd834dc5c8ebf2d52b97e4a174af7
Patch0:		%{name}-private.patch
URL:		http://wiki.apparmor.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.4
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gcc >= 5:3.2
BuildRequires:	libtool
BuildRequires:	perl-devel
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
%if %{with python3}
BuildRequires:	python3-devel
%else
BuildRequires:	python-devel
%endif
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

%package -n perl-LibAppArmor
Summary:	AppArmor Perl bindings
Summary(pl.UTF-8):	Dowiązania do AppArmor dla Perla
Summary(pt_BR.UTF-8):	Módulos Perl para acessar os recursos do AppArmor
Group:		Development/Languages/Perl
Obsoletes:	perl-apparmor
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n perl-LibAppArmor
AppArmor Perl bindings.

%description -n perl-LibAppArmor -l pl.UTF-8
Dowiązania do AppArmor dla Perla.

%description -n perl-LibAppArmor -l pt_BR.UTF-8
Módulos Perl para acessar os recursos do AppArmor.

%package -n python-LibAppArmor
Summary:	AppArmor Python bindings
Summary(pl.UTF-8):	Dowiązania do AppArmor dla Pythona
Summary(pt_BR.UTF-8):	Módulos Python para acessar os recursos do AppArmor
Group:		Development/Languages/Python
%pyrequires_eq  python
Obsoletes:	python-apparmor
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n python-LibAppArmor
AppArmor Python bindings.

%description -n python-LibAppArmor -l pl.UTF-8
Dowiązania do AppArmor dla Pythona.

%description -n python-LibAppArmor -l pt_BR.UTF-8
Módulos Python para acessar os recursos do AppArmor.

%package -n python3-LibAppArmor
Summary:	AppArmor Python bindings
Summary(pl.UTF-8):	Dowiązania do AppArmor dla Pythona
Summary(pt_BR.UTF-8):	Módulos Python para acessar os recursos do AppArmor
Group:		Development/Languages/Python
%pyrequires_eq  python3
Obsoletes:	python3-apparmor
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n python3-LibAppArmor
AppArmor Python bindings.

%description -n python3-LibAppArmor -l pl.UTF-8
Dowiązania do AppArmor dla Pythona.

%description -n python3-LibAppArmor -l pt_BR.UTF-8
Módulos Python para acessar os recursos do AppArmor.

%package -n ruby-LibAppArmor
Summary:	AppArmor Ruby bindings
Summary(pl.UTF-8):	Dowiązania do AppArmor dla języka Ruby
Group:		Development/Languages
Obsoletes:	ruby-apparmor
Requires:	%{name} = %{epoch}:%{version}-%{release}
%{?ruby_mod_ver_requires_eq}

%description -n ruby-LibAppArmor
AppArmor Ruby bindings.

%description -n ruby-LibAppArmor -l pl.UTF-8
Dowiązania do AppArmor dla języka Ruby.

%prep
%setup -q -n apparmor-%{version}
%patch0 -p1

%build
cd libraries/libapparmor
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
%if %{with python3}
	PYTHON="%{__python3}" \
%endif
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
%{_includedir}/sys/apparmor_private.h
%{_pkgconfigdir}/libapparmor.pc
%{_mandir}/man2/aa_change_hat.2*
%{_mandir}/man2/aa_change_profile.2*
%{_mandir}/man2/aa_find_mountpoint.2*
%{_mandir}/man2/aa_getcon.2*
%{_mandir}/man2/aa_query_label.2*
%{_mandir}/man2/aa_stack_profile.2*
%{_mandir}/man3/aa_features.3*
%{_mandir}/man3/aa_kernel_interface.3*
%{_mandir}/man3/aa_policy_cache.3*
%{_mandir}/man3/aa_splitcon.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libapparmor.a

%files -n perl-LibAppArmor
%defattr(644,root,root,755)
%{perl_vendorarch}/LibAppArmor.pm
%dir %{perl_vendorarch}/auto/LibAppArmor
%attr(755,root,root) %{perl_vendorarch}/auto/LibAppArmor/LibAppArmor.so

%if %{with python3}
%files -n python3-LibAppArmor
%defattr(644,root,root,755)
%dir %{py3_sitedir}/LibAppArmor
%attr(755,root,root) %{py3_sitedir}/LibAppArmor/_LibAppArmor.*.so
%{py3_sitedir}/LibAppArmor/__pycache__
%{py3_sitedir}/LibAppArmor/__init__.py
%{py3_sitedir}/LibAppArmor-*.egg-info
%else
%files -n python-LibAppArmor
%defattr(644,root,root,755)
%dir %{py_sitedir}/LibAppArmor
%attr(755,root,root) %{py_sitedir}/LibAppArmor/_LibAppArmor.so
%{py_sitedir}/LibAppArmor/__init__.py[co]
%{py_sitedir}/LibAppArmor/LibAppArmor.py[co]
%{py_sitedir}/LibAppArmor-*.egg-info
%endif

%if %{with ruby}
%files -n ruby-LibAppArmor
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/LibAppArmor.so
%endif
