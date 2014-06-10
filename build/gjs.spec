%global gobject_introspection_version 1.39.3

Name:          gjs
Version:       1.40.1
Release:       2%{?dist}
Summary:       Javascript Bindings for GNOME

Group:         System Environment/Libraries
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:       MIT and (MPLv1.1 or GPLv2+ or LGPLv2+)
URL:           http://live.gnome.org/Gjs/
#VCS:          git://git.gnome.org/gjs
Source0:       http://download.gnome.org/sources/%{name}/1.40/%{name}-%{version}.tar.xz

BuildRequires: mozjs24-devel
BuildRequires: cairo-gobject-devel
BuildRequires: gobject-introspection-devel >= %{gobject_introspection_version}
BuildRequires: readline-devel
BuildRequires: dbus-glib-devel
BuildRequires: gtk3-devel
BuildRequires: intltool
BuildRequires: pkgconfig
# Bootstrap requirements
BuildRequires: gtk-doc gnome-common

Requires: gobject-introspection%{?_isa} >= %{gobject_introspection_version}

%description
Gjs allows using GNOME libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject introspection
framework.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with %{name}.

%prep
%setup -q

rm -f configure

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; fi;
 %configure --disable-static)

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%check
#make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING NEWS README
%{_bindir}/gjs
%{_bindir}/gjs-console
%{_libdir}/*.so.*
%{_libdir}/gjs

%files devel
%doc examples/*
%{_includedir}/gjs-1.0
%{_libdir}/pkgconfig/gjs-1.0.pc
%{_libdir}/pkgconfig/gjs-internals-1.0.pc
%{_libdir}/*.so

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 1.40.1-2
- import from f20

