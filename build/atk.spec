%define glib2_version 2.31.2
%define gobject_introspection_version 0.9.6

Summary: Interfaces for accessibility support
Name: atk
Version: 2.12.0
Release: 1%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
#VCS: git:git://git.gnome.org/atk
Source: http://download.gnome.org/sources/atk/2.13/atk-%{version}.tar.xz
URL: http://developer.gnome.org/platform-overview/stable/atk
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gnome-doc-utils
BuildRequires: gettext
BuildRequires: gobject-introspection-devel >= %{gobject_introspection_version}
# Bootstrap requirements
BuildRequires: gnome-common gtk-doc

%description
The ATK library provides a set of interfaces for adding accessibility
support to applications and graphical user interface toolkits. By
supporting the ATK interfaces, an application or toolkit can be used
with tools such as screen readers, magnifiers, and alternative input
devices.

%package devel
Summary: Development files for the ATK accessibility toolkit
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package includes libraries, header files, and developer documentation
needed for development of applications or toolkits which use ATK.

%prep
%setup -q

%build
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS)
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang atk10

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f atk10.lang
%doc README AUTHORS COPYING NEWS
%{_libdir}/libatk-1.0.so.*
%{_libdir}/girepository-1.0

%files devel
%{_libdir}/libatk-1.0.so
%{_includedir}/atk-1.0
%{_libdir}/pkgconfig/atk.pc
%{_datadir}/gtk-doc/html/atk
%{_datadir}/gir-1.0

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 2.12.0-1
- import from f20

