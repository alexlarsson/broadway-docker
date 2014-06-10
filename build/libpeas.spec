
Name:		libpeas
Version:	1.10.0
Release:	3%{?dist}
Summary:	Plug-ins implementation convenience library

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://ftp.acc.umu.se/pub/GNOME/sources/libpeas/
Source0:	http://ftp.acc.umu.se/pub/GNOME/sources/%{name}/1.10/%{name}-%{version}.tar.xz

BuildRequires:	chrpath
BuildRequires:	gtk3-devel >= 3.0.0
BuildRequires:	python-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	gtk-doc

# For the girepository-1.0 directory
Requires:	gobject-introspection

BuildRequires:	autoconf automake gnome-common

%description
libpeas is a convenience library making adding plug-ins support
to GTK+ and glib-based applications.

%package devel
Summary:	Development files for libpeas
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development libraries and header files
that are needed to write applications that use libpeas.

%prep
%setup -q

%build
%configure --disable-seed

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT/%{_libdir}/lib*.la

# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/peas-demo
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libpeas-gtk-1.0.so

%find_lang libpeas

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%files -f libpeas.lang
%doc AUTHORS
%{_libdir}/libpeas*-1.0.so.*
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/icons/hicolor/*/actions/libpeas-plugin.*

%files devel
%{_bindir}/peas-demo
%{_includedir}/libpeas-1.0/
%{_libdir}/peas-demo/
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%{_datadir}/gtk-doc/html/libpeas/
%{_libdir}/libpeas*-1.0.so
%{_datadir}/gir-1.0/*.gir
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 1.10.0-3
- import from f20

