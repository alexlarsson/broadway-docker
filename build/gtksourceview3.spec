%define gtk_version 3.11.0

%define po_package gtksourceview-3.0

Summary: A library for viewing source files
Name: gtksourceview3
Version: 3.12.2
Release: 2%{?dist}
License: LGPLv2+ and GPLv2+
# the library itself is LGPL, some .lang files are GPL
Group: System Environment/Libraries
URL: http://gtksourceview.sourceforge.net/
#VCS: git:git://git.gnome.org/gtksourceview
Source0: http://download.gnome.org/sources/gtksourceview/3.12/gtksourceview-%{version}.tar.xz
BuildRequires: libxml2-devel
BuildRequires: gtk3-devel >= %{gtk_version}
BuildRequires: intltool >= 0.35
BuildRequires: gettext
BuildRequires: gobject-introspection-devel

Requires: gtk3%{?_isa} >= %{gtk_version}

%description
GtkSourceView is a text widget that extends the standard GTK+
GtkTextView widget. It improves GtkTextView by implementing
syntax highlighting and other features typical of a source code editor.

This package contains version 3 of GtkSourceView. The older version
2 is contains in the gtksourceview2 package.

%package devel
Summary: Files to compile applications that use gtksourceview3
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
gtksourceview3-devel contains the files required to compile
applications which use GtkSourceView 3.

%prep
%setup -q -n gtksourceview-%{version}

%build
%configure --disable-gtk-doc --disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# remove unwanted files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_datadir}/gtksourceview-3.0/language-specs/check.sh
rm -f $RPM_BUILD_ROOT%{_datadir}/gtksourceview-3.0/language-specs/convert.py

%find_lang %{po_package}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%doc README AUTHORS COPYING NEWS MAINTAINERS
%{_datadir}/gtksourceview-3.0
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GtkSource-3.0.typelib

%files devel
%{_includedir}/gtksourceview-3.0
%{_datadir}/gtk-doc/html/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/GtkSource-3.0.gir

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 3.12.2-2
- import from f20

