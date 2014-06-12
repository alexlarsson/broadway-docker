%global glib2_version 2.37.0

Summary: Backends for the gio framework in GLib
Name: gvfs
Version: 1.20.2
Release: 3%{?dist}
License: GPLv3 and LGPLv2+ and BSD and MPLv1.1
Group: System Environment/Libraries
URL: http://www.gtk.org

Source: http://download.gnome.org/sources/gvfs/1.21/gvfs-%{version}.tar.xz
BuildRequires: pkgconfig
BuildRequires: glib2-devel >= %{glib2_version}
# for post-install update-gio-modules and overall functionality
Requires: glib2%{?_isa} >= %{glib2_version}
BuildRequires: dbus-glib-devel
BuildRequires: /usr/bin/ssh
BuildRequires: libsoup-devel >= 2.34.0
BuildRequires: pkgconfig(avahi-client) pkgconfig(avahi-glib)
BuildRequires: libsecret-devel
BuildRequires: intltool
BuildRequires: gettext-devel
BuildRequires: expat-devel
BuildRequires: libxslt-devel
BuildRequires: gtk3-devel
BuildRequires: docbook-style-xsl

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

# The patch touches Makefile.am files:
BuildRequires: automake autoconf
BuildRequires: libtool

# http://bugzilla.gnome.org/show_bug.cgi?id=567235
Patch0: gvfs-archive-integration.patch

%description
The gvfs package provides backend implementations for the gio
framework in GLib. It includes ftp, sftp, cifs.

%package devel
Summary: Development files for gvfs
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The gvfs-devel package contains headers and other files that are
required to develop applications using gvfs.


%package fuse
Summary: FUSE support for gvfs
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: fuse-devel
Requires: fuse

%description fuse
This package provides support for applications not using gio
to access the gvfs filesystems.


%package archive
Summary: Archiving support for gvfs
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libarchive-devel >= 2.7.1-1

%description archive
This package provides support for accessing files inside Zip and Tar archives,
as well as ISO images, to applications using gvfs.

%package afp
Summary: AFP support for gvfs
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
BuildRequires: libgcrypt-devel >= 1.2.2
# this should ensure having this new subpackage installed on upgrade from older versions
Obsoletes: %{name} < 1.9.4-1

%description afp
This package provides support for reading and writing files on
Mac OS X and original Mac OS network shares via Apple Filing Protocol
to applications using gvfs.


%prep
%setup -q
%patch0 -p1 -b .archive-integration

# Needed for gvfs-0.2.1-archive-integration.patch
libtoolize --force  || :
aclocal  || :
autoheader  || :
automake  || :
autoconf  || :

%build
%configure \
        --disable-hal \
        --disable-gdu \
        --disable-obexftp \
        --enable-udisks2 \
        --enable-keyring
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/gvfs/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.la

# trashlib is GPLv3, include the license
cp -p daemon/trashlib/COPYING COPYING.GPL3

%find_lang gvfs

%post
/sbin/ldconfig
# Reload .mount files:
killall -USR1 gvfsd >&/dev/null || :
update-desktop-database &> /dev/null || :
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%postun
/sbin/ldconfig
update-desktop-database &> /dev/null ||:
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%post archive
update-desktop-database >&/dev/null || :
killall -USR1 gvfsd >&/dev/null || :

%postun archive
update-desktop-database >&/dev/null || :

%files -f gvfs.lang
%doc AUTHORS COPYING COPYING.GPL3 NEWS README
%dir %{_datadir}/gvfs
%dir %{_datadir}/gvfs/mounts
%{_datadir}/gvfs/mounts/sftp.mount
%{_datadir}/gvfs/mounts/trash.mount
%{_datadir}/gvfs/mounts/computer.mount
%{_datadir}/gvfs/mounts/dav.mount
%{_datadir}/gvfs/mounts/dav+sd.mount
%{_datadir}/gvfs/mounts/http.mount
%{_datadir}/gvfs/mounts/localtest.mount
%{_datadir}/gvfs/mounts/burn.mount
%{_datadir}/gvfs/mounts/dns-sd.mount
%{_datadir}/gvfs/mounts/network.mount
%{_datadir}/gvfs/mounts/ftp.mount
%{_datadir}/gvfs/mounts/recent.mount
%{_datadir}/dbus-1/services/gvfs-daemon.service
%{_datadir}/dbus-1/services/gvfs-metadata.service
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.xml
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/gvfs
%{_libdir}/gvfs/libgvfscommon.so
%{_libdir}/gvfs/libgvfsdaemon.so
%dir %{_datadir}/gvfs/remote-volume-monitors
%{_libdir}/gio/modules/libgioremote-volume-monitor.so
%{_libdir}/gio/modules/libgvfsdbus.so
%{_libexecdir}/gvfsd
%{_libexecdir}/gvfsd-ftp
%{_libexecdir}/gvfsd-sftp
%{_libexecdir}/gvfsd-trash
%{_libexecdir}/gvfsd-computer
%{_libexecdir}/gvfsd-dav
%{_libexecdir}/gvfsd-http
%{_libexecdir}/gvfsd-localtest
%{_libexecdir}/gvfsd-burn
%{_libexecdir}/gvfsd-dnssd
%{_libexecdir}/gvfsd-network
%{_libexecdir}/gvfsd-metadata
%{_libexecdir}/gvfsd-recent
%{_bindir}/gvfs-cat
%{_bindir}/gvfs-copy
%{_bindir}/gvfs-info
%{_bindir}/gvfs-less
%{_bindir}/gvfs-ls
%{_bindir}/gvfs-mime
%{_bindir}/gvfs-mkdir
%{_bindir}/gvfs-monitor-dir
%{_bindir}/gvfs-monitor-file
%{_bindir}/gvfs-mount
%{_bindir}/gvfs-move
%{_bindir}/gvfs-open
%{_bindir}/gvfs-rename
%{_bindir}/gvfs-rm
%{_bindir}/gvfs-save
%{_bindir}/gvfs-trash
%{_bindir}/gvfs-tree
%{_bindir}/gvfs-set-attribute
%doc %{_mandir}/man1/gvfs-*
%doc %{_mandir}/man1/gvfsd.1.gz
%doc %{_mandir}/man1/gvfsd-metadata.1.gz
%doc %{_mandir}/man7/gvfs.7.gz

%files devel
%dir %{_includedir}/gvfs-client
%dir %{_includedir}/gvfs-client/gvfs
%{_includedir}/gvfs-client/gvfs/gvfsurimapper.h
%{_includedir}/gvfs-client/gvfs/gvfsuriutils.h


%files fuse
%{_libexecdir}/gvfsd-fuse
%doc %{_mandir}/man1/gvfsd-fuse.1.gz

%files archive
%{_datadir}/applications/mount-archive.desktop
%{_libexecdir}/gvfsd-archive
%{_datadir}/gvfs/mounts/archive.mount

%files afp
%{_libexecdir}/gvfsd-afp
%{_libexecdir}/gvfsd-afp-browse
%{_datadir}/gvfs/mounts/afp.mount
%{_datadir}/gvfs/mounts/afp-browse.mount

%changelog
* Wed Jun 11 2014 Alexander Larsson <alexl@redhat.com> - 1.20.2-3
- import from fedora

