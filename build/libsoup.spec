%define glib2_version 2.38.0

### Abstract ###

Name: libsoup
Version: 2.46.0
Release: 3%{?dist}
License: LGPLv2
Group: Development/Libraries
Summary: Soup, an HTTP library implementation
URL: http://live.gnome.org/LibSoup
#VCS: git:git://git.gnome.org/libsoup
Source: http://download.gnome.org/sources/libsoup/2.46/libsoup-%{version}.tar.xz
Requires: glib-networking >= %{glib2_version}

### Build Dependencies ###

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: glib-networking
BuildRequires: gobject-introspection-devel
BuildRequires: intltool
BuildRequires: libxml2-devel
BuildRequires: sqlite-devel

%description
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it).

%package devel
Summary: Header files for the Soup library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel >= %{glib2_version}
Requires: gnutls-devel
Requires: libxml2-devel

%description devel
Libsoup is an HTTP library implementation in C. This package allows
you to develop applications that use the libsoup library.

%prep
%setup -q

%build
%configure --disable-static

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%find_lang libsoup

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libsoup.lang
%doc README COPYING NEWS AUTHORS
%{_libdir}/lib*.so.*
%{_libdir}/girepository-1.0/Soup*2.4.typelib

%files devel
%{_includedir}/%{name}-2.4
%{_includedir}/%{name}-gnome-2.4
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Soup*2.4.gir
%{_datadir}/gtk-doc/html/%{name}-2.4

%changelog
* Wed Jun 11 2014 Alexander Larsson <alexl@redhat.com> - 2.46.0-3
- import from fedora

