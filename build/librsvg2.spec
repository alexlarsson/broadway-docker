Name:           librsvg2
Summary:        An SVG library based on cairo
Version:        2.40.2
Release:        2%{?dist}

License:        LGPLv2+
Group:          System Environment/Libraries
#VCS:           git:git://git.gnome.org/librsvg
Source:         http://download.gnome.org/sources/librsvg/2.40/librsvg-%{version}.tar.xz

# build with vala 0.18
Patch0: librsvg-vala.patch

Requires(post):   gdk-pixbuf2
Requires(postun): gdk-pixbuf2
BuildRequires:  libpng-devel
BuildRequires:  glib2-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  gtk3-devel
BuildRequires:  pango-devel
BuildRequires:  libxml2-devel
BuildRequires:  freetype-devel
BuildRequires:  cairo-devel
BuildRequires:  cairo-gobject-devel
BuildRequires:  libcroco-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  vala-devel
BuildRequires:  vala-tools
# grr, librsvg does not install api docs if --disable-gtk-doc
BuildRequires:  gtk-doc
BuildRequires:  automake
BuildRequires:  autoconf

Provides:       librsvg3 = %{name}.%{version}-%{release}

%description
An SVG library based on cairo.


%package devel
Summary:        Libraries and include files for developing with librsvg
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

Provides:       librsvg3-devel = %{name}.%{version}-%{release}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.


%package tools
Summary:        Extra tools for librsvg
Requires:       %{name} = %{version}-%{release}

%description tools
This package provides extra utilities based on the librsvg library.


%prep
%setup -q -n librsvg-%{version}
%patch0 -p1 -b .vala

autoreconf -i -f

%build
GDK_PIXBUF_QUERYLOADERS=/usr/bin/gdk-pixbuf-query-loaders-%{__isa_bits}
export GDK_PIXBUF_QUERYLOADERS
# work around an ordering problem in configure
enable_pixbuf_loader=yes
export enable_pixbuf_loader
%configure --disable-static  \
        --disable-gtk-doc \
        --disable-gtk-theme \
        --enable-introspection
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders
rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/svg-viewer.svg

%post
/sbin/ldconfig
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :

%postun
/sbin/ldconfig
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :


%files
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_libdir}/librsvg-2.so.*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader-svg.so
%{_libdir}/girepository-1.0/*

%files devel
%{_libdir}/librsvg-2.so
%{_includedir}/librsvg-2.0
%{_libdir}/pkgconfig/librsvg-2.0.pc
%{_datadir}/gir-1.0/*
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/librsvg-2.0.vapi
%doc %{_datadir}/gtk-doc/html/rsvg-2.0

%files tools
%{_bindir}/rsvg-convert
%{_bindir}/rsvg-view-3
%{_mandir}/man1/rsvg-convert.1*


%changelog
* Thu Jun 12 2014 Alexander Larsson <alexl@redhat.com> - 2.40.2-2
- import from fedora

