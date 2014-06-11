%global gtk2_version 2.24.15
%global gtk3_version 3.9.3

Name: gnome-themes-standard
Version: 3.12.0
Release: 1%{?dist}
Summary: Standard themes for GNOME applications

Group: User Interface/Desktops
License: LGPLv2+
URL: http://git.gnome.org/browse/gnome-themes-standard
Source0: http://download.gnome.org/sources/%{name}/3.10/%{name}-%{version}.tar.xz
Source1: settings.ini

Obsoletes: fedora-gnome-theme <= 15.0-1.fc15
Provides: fedora-gnome-theme = 1:%{version}-%{release}

Obsoletes: gnome-background-standard < 3.0.0-2
Provides: gnome-background-standard = %{version}-%{release}

BuildRequires: gtk3-devel >= %{gtk3_version}
BuildRequires: librsvg2-devel
BuildRequires: intltool gettext autoconf automake libtool
Requires: gnome-icon-theme
Requires: abattis-cantarell-fonts
Requires: adwaita-cursor-theme = %{version}-%{release}
Requires: adwaita-gtk3-theme = %{version}-%{release}

%description
The gnome-themes-standard package contains the standard theme for the GNOME
desktop, which provides default appearance for cursors, desktop background,
window borders and GTK+ applications.

%package -n adwaita-cursor-theme
Summary: Adwaita cursor theme
Group: User Interface/Desktops
BuildArch: noarch

%description -n adwaita-cursor-theme
The adwaita-cursor-theme package contains a modern set of cursors originally
designed for the GNOME desktop.

%package -n adwaita-gtk3-theme
Summary: Adwaita gtk3 theme
Group: User Interface/Desktops
Requires: gtk3%{_isa} >= %{gtk3_version}

%description -n adwaita-gtk3-theme
The adwaita-gtk3-theme package contains a gtk3 theme for rendering widgets
with a GNOME look and feel.

%prep
%setup -q

%build
%configure --disable-gtk2-engine
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

for t in HighContrast; do
  rm -f $RPM_BUILD_ROOT%{_datadir}/icons/$t/icon-theme.cache
  touch $RPM_BUILD_ROOT%{_datadir}/icons/$t/icon-theme.cache
done

rm $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/3.0.0/theming-engines/libadwaita.la

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gtk-3.0
cp $RPM_SOURCE_DIR/settings.ini $RPM_BUILD_ROOT%{_datadir}/gtk-3.0/settings.ini

%post
for t in HighContrast; do
  touch --no-create %{_datadir}/icons/$t &>/dev/null || :
done

%posttrans
for t in HighContrast; do
  gtk-update-icon-cache -i %{_datadir}/icons/$t &>/dev/null || :
done

%files
%doc COPYING NEWS

# Background and WM
%{_datadir}/themes/Adwaita
%exclude %{_datadir}/themes/Adwaita/gtk-3.0

# Background
%{_datadir}/gnome-background-properties/*

# A11y themes
%ghost %{_datadir}/icons/HighContrast/icon-theme.cache
%{_datadir}/icons/HighContrast
%{_datadir}/themes/HighContrast

%files -n adwaita-cursor-theme
# Cursors
%{_datadir}/icons/Adwaita

%files -n adwaita-gtk3-theme
# gtk3 Theme and engine
%{_libdir}/gtk-3.0/3.0.0/theming-engines/libadwaita.so
%{_datadir}/themes/Adwaita/gtk-3.0
# Default gtk3 settings
%{_datadir}/gtk-3.0/settings.ini


%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 3.10.0-2
- import from f20

