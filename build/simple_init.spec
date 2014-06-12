Name:           simple_init
Version:        0.1
Release:        1%{?dist}
Summary:        Simple init

License:        GPL
URL:            http://lwn.net/Articles/533493/
Source0:        simple_init.c

%description
A super simple init

%prep


%build
gcc $RPM_SOURCE_DIR/simple_init.c -o  simple_init

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install simple_init $RPM_BUILD_ROOT%{_bindir}

%files
%{_bindir}/simple_init

%changelog
* Thu Jun 12 2014 Alexander Larsson <alexl@redhat.com>
- Initial version
