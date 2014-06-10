%define glib2_version 2.33.12
%define pkgconfig_version 0.12
%define freetype_version 2.1.5
%define fontconfig_version 2.10.91
%define cairo_version 1.7.6
%define libthai_version 0.1.9
%define harfbuzz_version 0.9.9
%define bin_version 1.8.0

Summary: System for layout and rendering of internationalized text
Name: pango
Version: 1.36.3
Release: 1broadway%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
#VCS: git:git://git.gnome.org/pango
Source: http://download.gnome.org/sources/pango/1.34/pango-%{version}.tar.xz
URL: http://www.pango.org

Requires: glib2 >= %{glib2_version}
Requires: freetype >= %{freetype_version}
Requires: freetype >= %{freetype_version}
Requires: cairo >= %{cairo_version}
Requires: libthai >= %{libthai_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pkgconfig >= %{pkgconfig_version}
BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: libthai-devel >= %{libthai_version}
BuildRequires: harfbuzz-devel >= %{harfbuzz_version}
BuildRequires: gobject-introspection-devel
BuildRequires: cairo-gobject-devel
# Bootstrap requirements
BuildRequires: gnome-common intltool gtk-doc

%description
Pango is a library for laying out and rendering of text, with an emphasis
on internationalization. Pango can be used anywhere that text layout is needed,
though most of the work on Pango so far has been done in the context of the
GTK+ widget toolkit. Pango forms the core of text and font handling for GTK+.

Pango is designed to be modular; the core Pango layout engine can be used
with different font backends.

The integration of Pango with Cairo provides a complete solution with high
quality text handling and graphics rendering.

%package devel
Summary: Development files for pango
Group: Development/Libraries
Requires: pango%{?_isa} = %{version}-%{release}
Requires: glib2-devel >= %{glib2_version}
Requires: freetype-devel >= %{freetype_version}
Requires: fontconfig-devel >= %{fontconfig_version}
Requires: cairo-devel >= %{cairo_version}

%description devel
The pango-devel package includes the header files and developer documentation
for the pango package.

%prep
%setup -q -n pango-%{version}

%build

# We try hard to not link to libstdc++
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
          --enable-doc-cross-references \
          --with-included-modules=basic-fc )
make %{?_smp_mflags}


%install

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Remove files that should not be packaged
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/pango/*/modules/*.la

# We need to have separate 32-bit and 64-bit pango-querymodules binaries
# for places where we have two copies of the Pango libraries installed.
# (we might have x86_64 and i686 packages on the same system, for example.)
mv $RPM_BUILD_ROOT%{_bindir}/pango-querymodules $RPM_BUILD_ROOT%{_bindir}/pango-querymodules-%{__isa_bits}

# and add a man page too
echo ".so man1/pango-querymodules.1" > $RPM_BUILD_ROOT%{_mandir}/man1/pango-querymodules-%{__isa_bits}.1

touch $RPM_BUILD_ROOT%{_libdir}/pango/%{bin_version}/modules.cache

%post
/sbin/ldconfig
/usr/bin/pango-querymodules-%{__isa_bits} --update-cache || :

%postun
/sbin/ldconfig
if test $1 -gt 0; then
  /usr/bin/pango-querymodules-%{__isa_bits} --update-cache || :
fi

%files
%doc README AUTHORS COPYING NEWS
%doc pango-view/HELLO.txt
%{_libdir}/libpango*-*.so.*
%{_bindir}/pango-querymodules*
%{_bindir}/pango-view
%{_mandir}/man1/pango-view.1.gz
%{_mandir}/man1/pango-querymodules*
%{_libdir}/pango
%ghost %{_libdir}/pango/%{bin_version}/modules.cache
%{_libdir}/girepository-1.0/Pango-1.0.typelib
%{_libdir}/girepository-1.0/PangoCairo-1.0.typelib
%{_libdir}/girepository-1.0/PangoFT2-1.0.typelib


%files devel
%{_libdir}/libpango*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%doc %{_datadir}/gtk-doc/html/pango
%{_datadir}/gir-1.0/Pango-1.0.gir
%{_datadir}/gir-1.0/PangoCairo-1.0.gir
%{_datadir}/gir-1.0/PangoFT2-1.0.gir


%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 1.36.1-3broadway
- Import f20 spec

