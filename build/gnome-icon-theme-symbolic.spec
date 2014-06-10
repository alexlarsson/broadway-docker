Summary: Symbolic GNOME icons
Name: gnome-icon-theme-symbolic
Version: 3.12.0
Release: 2%{?dist}
#VCS: git:git://git.gnome.org/gnome-icon-theme-symbolic
Source0: http://download.gnome.org/sources/gnome-icon-theme-symbolic/3.12/%{name}-%{version}.tar.xz
License: CC-BY-SA
BuildArch: noarch
Group: User Interface/Desktops
BuildRequires: icon-naming-utils >= 0.8.7
Requires: gnome-icon-theme >= 2.30.2.1-2

%description
This package contains symbolic icons for use by the GNOME desktop.

%prep
%setup -q

%build
# Avoid a BuildRequires on gtk2-devel
export ac_cv_path_GTK_UPDATE_ICON_CACHE=/bin/true

%configure

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/gnome &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/gnome &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :

%files
%doc COPYING AUTHORS
%{_datadir}/icons/gnome/*
%{_datadir}/pkgconfig/gnome-icon-theme-symbolic.pc

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 3.12.0-2
- import from f20

