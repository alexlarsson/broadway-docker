Name:           gobject-introspection
Version:        1.40.0
Release:        3%{?dist}
Summary:        Introspection system for GObject-based libraries

Group:      Development/Libraries
License:        GPLv2+, LGPLv2+, MIT
URL:            http://live.gnome.org/GObjectIntrospection
#VCS:           git:git://git.gnome.org/gobject-introspection
Source0:        http://download.gnome.org/sources/gobject-introspection/1.40/%{name}-%{version}.tar.xz

Obsoletes:      gir-repository

BuildRequires:  glib2-devel
BuildRequires:  python-devel >= 2.5
BuildRequires:  gettext
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  libffi-devel
BuildRequires:  cairo-gobject-devel
BuildRequires:  libxml2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
# Bootstrap requirements
BuildRequires:  gnome-common
BuildRequires:  intltool
BuildRequires:  gtk-doc
# For doctool
BuildRequires:  python-mako

%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package devel
Summary: Libraries and headers for gobject-introspection
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
# Not always, but whatever, it's a tiny dep to pull in
Requires: libtool
# For g-ir-doctool
Requires: python-mako
Obsoletes: gir-repository-devel

%description devel
Libraries and headers for gobject-introspection

%prep
%setup -q

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; fi;)
%configure --enable-gtk-doc --enable-doctool

make V=1 %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Die libtool, die.
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING

%{_libdir}/lib*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_libdir}/lib*.so
%dir %{_libdir}/gobject-introspection
%{_libdir}/gobject-introspection/*
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/g-ir-*
%{_datadir}/gir-1.0
%dir %{_datadir}/gobject-introspection-1.0
%{_datadir}/gobject-introspection-1.0/*
%{_datadir}/aclocal/introspection.m4
%{_mandir}/man1/*.gz
%dir %{_datadir}/gtk-doc/html/gi
%{_datadir}/gtk-doc/html/gi/*

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 1.40.0-3
- import from f20

