Summary:    GNOME icon theme
Name:       gnome-icon-theme
Version:    3.12.0
License:    LGPLv3+
Group:      User Interface/Desktops
Release:    2%{?dist}
URL:        http://www.gnome.org

#VCS: git:git://git.gnome.org/gnome-icon-theme
Source0: http://download.gnome.org/sources/gnome-icon-theme/3.12/%{name}-%{version}.tar.xz
Source1: legacy-icon-mapping.xml

BuildRequires: icon-naming-utils >= 0.8.7
BuildRequires: intltool
BuildRequires: librsvg2
Requires: hicolor-icon-theme

BuildArch: noarch

%description
This package contains the default icon theme used by the GNOME desktop.

%package legacy
Summary: Old names for icons in gnome-icon-theme
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}

%description legacy
This package contains symlinks to make the icons in gnome-icon-theme
available under old names.

%package devel

Summary: Development files for gnome-icon-theme
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files for gnome-icon-theme

%prep
%setup -q

%build
%configure --enable-icon-mapping

%install
make install DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT%{_datadir}/icons/gnome/icon-theme.cache

cp %{SOURCE1} .
export INU_DATA_DIR=$PWD
(cd $RPM_BUILD_ROOT%{_datadir}/icons/gnome
for size in 8x8 16x16 22x22 24x24 32x32 48x48 256x256; do
        cd $size || continue;
        echo -e "Adding rtl variants for $size"
        for dir in `find . -type d`; do
                context="`echo $dir | cut -c 3-`"
                if [ $context ]; then
                        icon-name-mapping -c $context
                fi
        done
        cd ..
done
)

# Add scalable directories for symbolic icons
(cd $RPM_BUILD_ROOT%{_datadir}/icons/gnome

mkdir -p scalable/actions
mkdir -p scalable/apps
mkdir -p scalable/devices
mkdir -p scalable/emblems
mkdir -p scalable/mimetypes
mkdir -p scalable/places
mkdir -p scalable/status
)

touch files.txt

(cd $RPM_BUILD_ROOT%{_datadir}
 echo "%%defattr(-,root,root)"
 find icons/gnome \( -name *-rtl.png -or -name *-ltr.png -or -type f \) -printf "%%%%{_datadir}/%%p\n"
 find icons/gnome -type d -printf "%%%%dir %%%%{_datadir}/%%p\n"
) > files.txt

(cd $RPM_BUILD_ROOT%{_datadir}
 echo "%%defattr(-,root,root)"
 find icons/gnome \( -type l -and -not -name *-rtl.png -and -not -name *-ltr.png \) -printf "%%%%{_datadir}/%%p\n"
) > legacy.txt

%post
touch --no-create %{_datadir}/icons/gnome &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/gnome &>/dev/null
    gtk-update-icon-cache -i %{_datadir}/icons/gnome &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -i %{_datadir}/icons/gnome &>/dev/null || :

%post legacy
touch --no-create %{_datadir}/icons/gnome &>/dev/null || :

%postun legacy
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/gnome &>/dev/null
    gtk-update-icon-cache -i %{_datadir}/icons/gnome &>/dev/null || :
fi

%posttrans legacy
gtk-update-icon-cache -i %{_datadir}/icons/gnome &>/dev/null || :

%files -f files.txt
%doc COPYING AUTHORS
%ghost %{_datadir}/icons/gnome/icon-theme.cache

%files legacy -f legacy.txt

%files devel
%{_datadir}/pkgconfig/gnome-icon-theme.pc

%changelog
* Tue Jun 10 2014 Alexander Larsson <alexl@redhat.com> - 3.12.0-2
- import from f20

