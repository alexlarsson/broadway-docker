Name: vte3
Version: 0.36.2
Release: 1%{?dist}
Summary: A terminal emulator
License: LGPLv2+
Group: User Interface/X
#VCS: git:git://git.gnome.org/vte
Source: http://download.gnome.org/sources/vte/0.36/vte-%{version}.tar.xz

BuildRequires: gtk3-devel >= 3.0.0
BuildRequires: ncurses-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: gobject-introspection-devel

# initscripts creates the utmp group
Requires: initscripts

%description
VTE is a terminal emulator widget for use with GTK+.

%package devel
Summary: Files needed for developing applications which use vte
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: ncurses-devel

%description devel
The vte-devel package includes the header files and developer docs
for the vte package.

Install vte-devel if you want to develop programs which will use
vte.

%prep
%setup -q -n vte-%{version}

%build
CFLAGS="%optflags -fPIE -DPIE" \
CXXFLAGS="$CFLAGS" \
LDFLAGS="$LDFLAGS -Wl,-z,relro -Wl,-z,now -pie" \
%configure \
        --enable-shared \
        --disable-static \
        --with-gtk=3.0 \
        --libexecdir=%{_libdir}/vte-2.90 \
        --without-glX \
        --disable-gtk-doc \
        --enable-introspection
make V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang vte-2.90

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f vte-2.90.lang
%doc COPYING HACKING NEWS README
%doc src/iso2022.txt
%doc doc/utmpwtmp.txt doc/boxes.txt doc/openi18n/UTF-8.txt doc/openi18n/wrap.txt
%{_sysconfdir}/profile.d/vte.sh
%{_libdir}/*.so.*
%dir %{_libdir}/vte-2.90
%attr(2711,root,utmp) %{_libdir}/vte-2.90/gnome-pty-helper
%{_libdir}/girepository-1.0

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_bindir}/vte2_90
%doc %{_datadir}/gtk-doc/html/vte-2.90
%{_datadir}/gir-1.0


%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 0.34.9-3
- import from f20

