%global _changelog_trimtime %(date +%s -d "1 year ago")

%define glib2_version 2.39.5
%define gtk3_version 3.11.6
%define pygo_version 3.0.0
%define desktop_file_utils_version 0.9
%define gtksourceview_version 3.11.2
%define enchant_version 1.2.0
%define isocodes_version 0.35
%define libpeas_version 1.7.0

Summary:	Text editor for the GNOME desktop
Name:		gedit
Epoch:		2
Version:	3.12.2
Release:	2%{?dist}
License:	GPLv2+ and GFDL
Group:		Applications/Editors
#VCS: git:git://git.gnome.org/gedit
Source0:	http://download.gnome.org/sources/gedit/3.12/gedit-%{version}.tar.xz

Patch1:         gedit-broadway.patch

URL:		http://projects.gnome.org/gedit/

Requires(post):         desktop-file-utils >= %{desktop_file_utils_version}
Requires(postun):       desktop-file-utils >= %{desktop_file_utils_version}

BuildRequires: gnome-common
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: enchant-devel >= %{enchant_version}
BuildRequires: iso-codes-devel >= %{isocodes_version}
BuildRequires: libattr-devel
BuildRequires: gtksourceview3-devel >= %{gtksourceview_version}
BuildRequires: gettext
BuildRequires: libpeas-devel >= %{libpeas_version}
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: which
BuildRequires: autoconf, automake, libtool
BuildRequires: intltool
BuildRequires: gobject-introspection-devel
BuildRequires: yelp-tools
BuildRequires: itstool

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: gtksourceview3%{?_isa} >= %{gtksourceview_version}
Requires: gsettings-desktop-schemas

%description
gedit is a small, but powerful text editor designed specifically for
the GNOME desktop. It has most standard text editor functions and fully
supports international text in Unicode. Advanced features include syntax
highlighting and automatic indentation of source code, printing and editing
of multiple documents in one window.

gedit is extensible through a plugin system, which currently includes
support for spell checking, comparing files, viewing CVS ChangeLogs, and
adjusting indentation levels. Further plugins can be found in the
gedit-plugins package.

%package devel
Summary: Support for developing plugins for the gedit text editor
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: gtksourceview3-devel >= %{gtksourceview_version}

%description devel
gedit is a small, but powerful text editor for the GNOME desktop.
This package allows you to develop plugins that add new functionality
to gedit.

Install gedit-devel if you want to write plugins for gedit.

%prep
%setup -q
%patch1 -p1 -b .broadway

autoreconf -i -f
intltoolize -f

%build
%configure \
	--disable-gtk-doc \
        --disable-vala \
	--enable-introspection=yes \
        --disable-python \
	--disable-updater \
	--enable-gvfs-metadata
make %{_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

## clean up all the static libs for plugins (workaround for no -module)
/bin/rm -f `find $RPM_BUILD_ROOT%{_libdir} -name "*.a"`
/bin/rm -f `find $RPM_BUILD_ROOT%{_libdir} -name "*.la"`

%find_lang %{name} --with-gnome

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/gedit.desktop

%post
update-desktop-database >&/dev/null || :
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
update-desktop-database >&/dev/null || :
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache -i %{_datadir}/icons/hicolor >&/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache -i %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :

%files -f %{name}.lang
%doc README COPYING AUTHORS
%{_datadir}/gedit
%{_datadir}/applications/gedit.desktop
%{_mandir}/man1/*
%{_libexecdir}/gedit
%{_libdir}/gedit/girepository-1.0
%dir %{_libdir}/gedit
%dir %{_libdir}/gedit/plugins
%{_libdir}/gedit/libgedit.so
%{_libdir}/gedit/plugins/docinfo.plugin
%{_libdir}/gedit/plugins/libdocinfo.so
%{_libdir}/gedit/plugins/filebrowser.plugin
%{_libdir}/gedit/plugins/libfilebrowser.so
%{_libdir}/gedit/plugins/modelines.plugin
%{_libdir}/gedit/plugins/libmodelines.so
%{_libdir}/gedit/plugins/sort.plugin
%{_libdir}/gedit/plugins/libsort.so
%{_libdir}/gedit/plugins/spell.plugin
%{_libdir}/gedit/plugins/libspell.so
%{_libdir}/gedit/plugins/time.plugin
%{_libdir}/gedit/plugins/libtime.so
%{_bindir}/*
%{_datadir}/appdata/
%{_datadir}/GConf/gsettings
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.enums.xml
%{_datadir}/dbus-1/services/org.gnome.gedit.service


%files devel
%{_includedir}/gedit-3.12
%{_libdir}/pkgconfig/gedit.pc
%{_datadir}/gtk-doc

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 2:3.12.2-2
- import from f20

