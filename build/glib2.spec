%global _changelog_trimtime %(date +%s -d "1 year ago")

Summary: A library of handy utility functions
Name: glib2
Version: 2.40.0
Release: 1%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.gtk.org
#VCS: git:git://git.gnome.org/glib
Source: http://download.gnome.org/sources/glib/2.40/glib-%{version}.tar.xz

BuildRequires: pkgconfig
BuildRequires: gettext
BuildRequires: libattr-devel
BuildRequires: libselinux-devel
# for sys/inotify.h
BuildRequires: glibc-devel
BuildRequires: zlib-devel
# for sys/sdt.h
BuildRequires: systemtap-sdt-devel
# Bootstrap build requirements
BuildRequires: automake autoconf libtool
BuildRequires: gtk-doc
BuildRequires: python-devel
BuildRequires: libffi-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: chrpath

# required for GIO content-type support
Requires: shared-mime-info

%description
GLib is the low-level core library that forms the basis for projects
such as GTK+ and GNOME. It provides data structure handling for C,
portability wrappers, and interfaces for such runtime functionality
as an event loop, threads, dynamic loading, and an object system.


%package devel
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: glib2-static < 2.32.1-2

%description devel
The glib2-devel package includes the header files for the GLib library.

%package doc
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
The glib2-doc package includes documentation for the GLib library.

%package fam
Summary: FAM monitoring module for GIO
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: gamin-devel

%description fam
The glib2-fam package contains the FAM (File Alteration Monitor) module for GIO.

%package tests
Summary: Tests for the glib2 package
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The glib2-tests package contains tests that can be used to verify
the functionality of the installed glib2 package.

%prep
%setup -q -n glib-%{version}

# Workaround wrong gtk-doc.make timestamp
# https://bugzilla.gnome.org/show_bug.cgi?id=700350
touch -r Makefile.am gtk-doc.make

%build
# Support builds of both git snapshots and tarballs packed with autogoo
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
           --enable-systemtap \
           --disable-static \
           --enable-installed-tests
)

make %{?_smp_mflags}

%install
# Use -p to preserve timestamps on .py files to ensure
# they're not recompiled with different timestamps
# to help multilib: https://bugzilla.redhat.com/show_bug.cgi?id=718404
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p -c"
# Also since this is a generated .py file, set it to a known timestamp,
# otherwise it will vary by build time, and thus break multilib -devel
# installs.
touch -r gio/gdbus-2.0/codegen/config.py.in $RPM_BUILD_ROOT/%{_datadir}/glib-2.0/codegen/config.py
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so
chrpath --delete $RPM_BUILD_ROOT%{_libexecdir}/installed-tests/glib/gdbus-peer

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/gdb/*.{pyc,pyo}
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/codegen/*.{pyc,pyo}

# Multilib fixes for systemtap tapsets; see
# https://bugzilla.redhat.com/718404
for f in $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/*.stp; do
    (dn=$(dirname ${f}); bn=$(basename ${f});
     mv ${f} ${dn}/%{__isa_bits}-${bn})
done

mv  $RPM_BUILD_ROOT%{_bindir}/gio-querymodules $RPM_BUILD_ROOT%{_bindir}/gio-querymodules-%{__isa_bits}

touch $RPM_BUILD_ROOT%{_libdir}/gio/modules/giomodule.cache

# bash-completion scripts need not be executable
chmod 644 $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/*

%find_lang glib20


%post
/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules


%postun
/sbin/ldconfig
[ ! -x %{_bindir}/gio-querymodules-%{__isa_bits} ] || \
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules


%files -f glib20.lang
%doc AUTHORS COPYING NEWS README
%{_libdir}/libglib-2.0.so.*
%{_libdir}/libgthread-2.0.so.*
%{_libdir}/libgmodule-2.0.so.*
%{_libdir}/libgobject-2.0.so.*
%{_libdir}/libgio-2.0.so.*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/gdbus
%{_datadir}/bash-completion/completions/gsettings
%{_datadir}/bash-completion/completions/gapplication
%dir %{_datadir}/glib-2.0
%dir %{_datadir}/glib-2.0/schemas
%dir %{_libdir}/gio
%dir %{_libdir}/gio/modules
%ghost %{_libdir}/gio/modules/giomodule.cache
%{_bindir}/gio-querymodules*
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_bindir}/gdbus
%{_bindir}/gapplication
%doc %{_mandir}/man1/gio-querymodules.1.gz
%doc %{_mandir}/man1/glib-compile-schemas.1.gz
%doc %{_mandir}/man1/gsettings.1.gz
%doc %{_mandir}/man1/gdbus.1.gz
%doc %{_mandir}/man1/gapplication.1.gz

%files devel
%{_libdir}/lib*.so
%{_libdir}/glib-2.0
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_datadir}/glib-2.0/gdb
%{_datadir}/glib-2.0/gettext
%{_datadir}/glib-2.0/schemas/gschema.dtd
%{_datadir}/bash-completion/completions/gresource
%{_bindir}/glib-genmarshal
%{_bindir}/glib-gettextize
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query
%{_bindir}/gtester
%{_bindir}/gdbus-codegen
%{_bindir}/glib-compile-resources
%{_bindir}/gresource
%{_datadir}/glib-2.0/codegen
%attr (0755, root, root) %{_bindir}/gtester-report
%doc %{_mandir}/man1/glib-genmarshal.1.gz
%doc %{_mandir}/man1/glib-gettextize.1.gz
%doc %{_mandir}/man1/glib-mkenums.1.gz
%doc %{_mandir}/man1/gobject-query.1.gz
%doc %{_mandir}/man1/gtester-report.1.gz
%doc %{_mandir}/man1/gtester.1.gz
%doc %{_mandir}/man1/gdbus-codegen.1.gz
%doc %{_mandir}/man1/glib-compile-resources.1.gz
%doc %{_mandir}/man1/gresource.1.gz
%{_datadir}/gdb/auto-load%{_libdir}/libglib-2.0.so.*-gdb.py*
%{_datadir}/gdb/auto-load%{_libdir}/libgobject-2.0.so.*-gdb.py*
%{_datadir}/systemtap/tapset/*.stp

%files doc
%doc %{_datadir}/gtk-doc/html/*

%files fam
%{_libdir}/gio/modules/libgiofam.so

%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 2.40.0-1
- import from f20

