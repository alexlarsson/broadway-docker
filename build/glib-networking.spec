%define glib2_version 2.39.1

Name:           glib-networking
Version:        2.40.1
Release:        2%{?dist}
Summary:        Networking support for GLib

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.gnome.org
Source:         http://download.gnome.org/sources/glib-networking/2.40/%{name}-%{version}.tar.xz

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  libproxy-devel
BuildRequires:  gnutls-devel
BuildRequires:  intltool
BuildRequires:  ca-certificates
BuildRequires:  gsettings-desktop-schemas-devel

Requires:       ca-certificates
Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       gsettings-desktop-schemas

%description
This package contains modules that extend the networking support in
GIO. In particular, it contains libproxy- and GSettings-based
GProxyResolver implementations and a gnutls-based GTlsConnection
implementation.

%prep
%setup -q


%build
%configure --disable-static --with-libproxy

make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.la

%find_lang %{name}

%post
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules

%postun
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules

%files -f %{name}.lang
%doc COPYING NEWS README
%{_libdir}/gio/modules/libgiolibproxy.so
%{_libdir}/gio/modules/libgiognomeproxy.so
%{_libdir}/gio/modules/libgiognutls.so
%{_libexecdir}/glib-pacrunner
%{_datadir}/dbus-1/services/org.gtk.GLib.PACRunner.service


%changelog
* Wed Jun 11 2014 Alexander Larsson <alexl@redhat.com> - 2.40.1-2
- import from fedora

