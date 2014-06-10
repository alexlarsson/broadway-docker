%global _changelog_trimtime %(date +%s -d "1 year ago")

%if 0%{?fedora} > 12
%global with_zeitgeist 1
%global with_python3 1
%else
%global with_zeitgeist 0
%global with_python3 0
%endif

%if %{with_python3}
%global __python %{__python3}
%endif

%define glib2_version 2.39.5
%define gtk3_version 3.11.6
%define pygo_version 3.0.0
%define desktop_file_utils_version 0.9
%define gtksourceview_version 3.11.2
%define enchant_version 1.2.0
%define isocodes_version 0.35
%define libpeas_version 1.7.0
%define zeitgeist_version 0.9.12

Summary:	Text editor for the GNOME desktop
Name:		gedit
Epoch:		2
Version:	3.12.2
Release:	2%{?dist}
License:	GPLv2+ and GFDL
Group:		Applications/Editors
#VCS: git:git://git.gnome.org/gedit
Source0:	http://download.gnome.org/sources/gedit/3.12/gedit-%{version}.tar.xz

URL:		http://projects.gnome.org/gedit/

Requires(post):         desktop-file-utils >= %{desktop_file_utils_version}
Requires(postun):       desktop-file-utils >= %{desktop_file_utils_version}

Patch4: gedit-disable-python3.patch

BuildRequires: gnome-common
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: enchant-devel >= %{enchant_version}
BuildRequires: iso-codes-devel >= %{isocodes_version}
BuildRequires: libattr-devel
BuildRequires: gtksourceview3-devel >= %{gtksourceview_version}
BuildRequires: gettext
BuildRequires: pygobject3-devel
BuildRequires: libpeas-devel >= %{libpeas_version}
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: which
BuildRequires: autoconf, automake, libtool
BuildRequires: intltool
BuildRequires: gobject-introspection-devel
BuildRequires: yelp-tools
BuildRequires: itstool
BuildRequires: vala-tools
%if %{with_python3}
BuildRequires: python3-devel
BuildRequires: python3-gobject >= %{pygo_version}
%else
BuildRequires: python-devel
%endif

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: gtksourceview3%{?_isa} >= %{gtksourceview_version}
%if %{with_python3}
Requires: python3-gobject >= %{pygo_version}
%endif
# the run-command plugin uses zenity
Requires: zenity
Requires: gsettings-desktop-schemas
Requires: gvfs

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

%if %{with_zeitgeist}
%package zeitgeist
Summary: Zeitgeist plugin for gedit
Group: Applications/Editors
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: zeitgeist >= %{zeitgeist_version}
BuildRequires: zeitgeist-devel >= %{zeitgeist_version}

%description zeitgeist
This packages brings the Zeitgeist dataprovider - a plugin that logs
access and leave event for documents used with gedit.
%endif

%prep
%setup -q

%if !%{with_python3}
%patch4 -p1 -b .disable-python
%endif

autoreconf -i -f
intltoolize -f

%build
%configure \
	--disable-gtk-doc \
	--enable-introspection=yes \
%if %{with_python3}
	--enable-python=yes \
%else
	--enable-python=no \
%endif
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
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :

%files -f %{name}.lang
%doc README COPYING AUTHORS
%{_datadir}/gedit
%{_datadir}/applications/gedit.desktop
%{_mandir}/man1/*
%if %{with_python3}
%{python3_sitearch}/gi/overrides/Gedit.py*
%{python3_sitearch}/gi/overrides/__pycache__
%endif
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
%if %{with_python3}
%{_libdir}/gedit/plugins/externaltools.plugin
%{_libdir}/gedit/plugins/externaltools
%{_libdir}/gedit/plugins/pythonconsole.plugin
%{_libdir}/gedit/plugins/pythonconsole
%{_libdir}/gedit/plugins/quickopen.plugin
%{_libdir}/gedit/plugins/quickopen
%{_libdir}/gedit/plugins/snippets.plugin
%{_libdir}/gedit/plugins/snippets
%endif
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
%if %{with_python3}
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.externaltools.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.pythonconsole.gschema.xml
%endif
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.enums.xml
%{_datadir}/dbus-1/services/org.gnome.gedit.service


%files devel
%{_includedir}/gedit-3.12
%{_libdir}/pkgconfig/gedit.pc
%{_datadir}/gtk-doc
%{_datadir}/vala/

%if %{with_zeitgeist}
%files zeitgeist
%{_libdir}/gedit/plugins/zeitgeist.plugin
%{_libdir}/gedit/plugins/libzeitgeist.so
%endif

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 2:3.12.2-2
- import from f20

