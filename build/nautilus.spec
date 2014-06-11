%define glib2_version 2.35.3
%define gnome_desktop3_version 3.0.0
%define pango_version 1.28.3
%define gtk3_version 3.11.6
%define libxml2_version 2.7.8
%define libexif_version 0.6.20
%define exempi_version 2.1.0
%define gobject_introspection_version 0.9.5
%define gsettings_desktop_schemas_version 3.8.0

Name:           nautilus
Summary:        File manager for GNOME
Version:        3.12.2
Release:        1%{?dist}
License:        GPLv2+
Group:          User Interface/Desktops
Source:         http://download.gnome.org/sources/%{name}/3.13/%{name}-%{version}.tar.xz

Patch1:         nautilus-broadway.patch

URL:            https://wiki.gnome.org/Apps/Nautilus

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  pango-devel >= %{pango_version}
BuildRequires:  gtk3-devel >= %{gtk3_version}
BuildRequires:  libxml2-devel >= %{libxml2_version}
BuildRequires:  gnome-desktop3-devel >= %{gnome_desktop3_version}
BuildRequires:  intltool >= 0.40.6-2
BuildRequires:  desktop-file-utils
BuildRequires:  libtool
BuildRequires:  libexif-devel >= %{libexif_version}
BuildRequires:  exempi-devel >= %{exempi_version}
BuildRequires:  gettext
BuildRequires:  libselinux-devel
BuildRequires:  gobject-introspection-devel >= %{gobject_introspection_version}
BuildRequires:  gsettings-desktop-schemas-devel >= %{gsettings_desktop_schemas_version}
BuildRequires:  libnotify-devel

Requires:       glib2%{_isa} >= %{glib2_version}
Requires:       gsettings-desktop-schemas%{_isa} >= %{gsettings_desktop_schemas_version}
Requires:       gtk3%{_isa} >= %{gtk3_version}
Requires:       libexif%{_isa} >= %{libexif_version}
# the main binary links against libnautilus-extension.so
# don't depend on soname, rather on exact version
Requires:       nautilus-extensions = %{version}-%{release}
Requires:       gvfs

%description
Nautilus is the file manager and graphical shell for the GNOME desktop
that makes it easy to manage your files and the rest of your system.
It allows to browse directories on local and remote filesystems, preview
files and launch applications associated with them.
It is also responsible for handling the icons on the GNOME desktop.

%package extensions
Summary:        Nautilus extensions library
License:        LGPLv2+
Group:          Development/Libraries
Requires:       %{name}%{_isa} = %{version}-%{release}

%description extensions
This package provides the libraries used by nautilus extensions.

%package devel
Summary:        Support for developing nautilus extensions
License:        LGPLv2+
Group:          Development/Libraries
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       %{name}-extensions%{_isa} = %{version}-%{release}

%description devel
This package provides libraries and header files needed
for developing nautilus extensions.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .broadway

autoreconf -i -f

#%%patch4 -p1 -b .selinux

%build
CFLAGS="$RPM_OPT_FLAGS -g -DNAUTILUS_OMIT_SELF_CHECK" %configure --disable-more-warnings --disable-update-mimedb --disable-tracker

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

export tagname=CC
# disabled %{?_smp_mflags} due to racy intltool-merge
LANG=en_US make -j1 V=1

%install
export tagname=CC
LANG=en_US make install DESTDIR=$RPM_BUILD_ROOT LIBTOOL=/usr/bin/libtool

desktop-file-install --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --add-only-show-in GNOME                                  \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.la

%find_lang %name

%post
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null

%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :

%post extensions -p /sbin/ldconfig

%postun extensions -p /sbin/ldconfig

%files  -f %{name}.lang
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_datadir}/nautilus
%{_datadir}/appdata/
%{_datadir}/applications/*
%{_datadir}/mime/packages/nautilus.xml
%{_bindir}/*
%{_datadir}/dbus-1/services/org.gnome.Nautilus.service
%{_datadir}/dbus-1/services/org.freedesktop.FileManager1.service
%{_datadir}/gnome-shell/search-providers/nautilus-search-provider.ini
%{_mandir}/man1/nautilus-connect-server.1.gz
%{_mandir}/man1/nautilus.1.gz
%{_libexecdir}/nautilus-convert-metadata
%{_datadir}/GConf/gsettings/nautilus.convert
%{_datadir}/glib-2.0/schemas/org.gnome.nautilus.gschema.xml
%dir %{_libdir}/nautilus/extensions-3.0
%{_libdir}/nautilus/extensions-3.0/libnautilus-sendto.so
%{_sysconfdir}/xdg/autostart/nautilus-autostart.desktop
%{_datadir}/dbus-1/services/org.gnome.Nautilus.SearchProvider.service

%files extensions
%{_libdir}/libnautilus-extension.so.*
%{_libdir}/girepository-1.0/*.typelib
%dir %{_libdir}/nautilus

%files devel
%{_includedir}/nautilus
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/gir-1.0/*.gir
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%doc %{_datadir}/gtk-doc/html/libnautilus-extension/

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 3.13.1-2
- import from f20

