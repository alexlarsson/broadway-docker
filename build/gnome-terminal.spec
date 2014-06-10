%define gettext_package gnome-terminal

%define glib2_version 2.40.0
%define gtk3_version 3.9.9
%define vte_version 0.36.0
%define desktop_file_utils_version 0.2.90

Summary: Terminal emulator for GNOME
Name: gnome-terminal
Version: 3.12.2
Release: 1%{?dist}
License: GPLv3+ and GFDL
Group: User Interface/Desktops
URL: http://www.gnome.org/
#VCS: git:git://git.gnome.org/gnome-terminal
Source0: http://download.gnome.org/sources/gnome-terminal/3.13/gnome-terminal-%{version}.tar.xz

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: vte3-devel >= %{vte_version}
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: gnome-common
BuildRequires: autoconf automake libtool
BuildRequires: itstool
BuildRequires: dconf-devel
BuildRequires: libuuid-devel
BuildRequires: appdata-tools
BuildRequires: vala

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gsettings-desktop-schemas
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: vte3%{?_isa} >= %{vte_version}

%description
gnome-terminal is a terminal emulator for GNOME. It features the ability to use
multiple terminals in a single window (tabs) and profiles support.

%prep
%setup -q

%build
%configure --disable-static --with-gtk=3.0 --disable-migration --disable-search-provider --without-nautilus-extension
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{gettext_package} --with-gnome

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/gnome-terminal.desktop

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{gettext_package}.lang
%doc AUTHORS COPYING NEWS

%{_bindir}/gnome-terminal
%{_datadir}/appdata/gnome-terminal.appdata.xml
%{_datadir}/applications/gnome-terminal.desktop
%{_libexecdir}/gnome-terminal-server
%{_datadir}/dbus-1/services/org.gnome.Terminal.service
%{_datadir}/glib-2.0/schemas/org.gnome.Terminal.gschema.xml

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 3.12.2-1
- import from f20

