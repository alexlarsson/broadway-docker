FROM fedora:20
MAINTAINER Alexander Larsson <alexl@redhat.com>
EXPOSE 8080

RUN yum install -y yum-utils rpm-build pixman-devel libpng-devel libxml2-devel freetype-devel fontconfig-devel gtk-doc gnome-common intltool libjpeg-devel libtiff-devel hicolor-icon-theme make abattis-cantarell-fonts liberation-mono-fonts liberation-sans-fonts liberation-serif-fonts flex bison python-mako ncurses-devel icon-naming-utils dbus-devel desktop-file-utils libuuid-devel appdata-tools  iso-codes-devel mozjs24-devel readline-devel dbus-glib-devel gcc-c++  createrepo lighttpd  gnome-doc-utils vala-devel vala-tools libxslt-devel fuse-devel libarchive-devel libcroco-devel
RUN yum-builddep -y glib2

RUN mkdir -p /rpmbuild/SOURCES

ADD glib2.spec  /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/glib/2.40/glib-2.40.0.tar.xz  /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/glib2.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/glib2-2.*.x86_64.rpm /rpmbuild/RPMS/x86_64/glib2-devel*.x86_64.rpm

ADD cairo.spec /rpmbuild/SOURCES/
ADD http://pkgs.fedoraproject.org/repo/pkgs/cairo/cairo-1.13.1-337ab1f.tar.xz/f44d8e5c7e57b1b47968747817e7e11c/cairo-1.13.1-337ab1f.tar.xz /rpmbuild/SOURCES/
ADD cairo-multilib.patch /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/cairo.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/cairo-1.*.x86_64.rpm /rpmbuild/RPMS/x86_64/cairo-devel-1.*.x86_64.rpm /rpmbuild/RPMS/x86_64/cairo-gobject-1.*.x86_64.rpm /rpmbuild/RPMS/x86_64/cairo-gobject-devel-1.*.x86_64.rpm

ADD gobject-introspection.spec  /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gobject-introspection/1.40/gobject-introspection-1.40.0.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gobject-introspection.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/gobject-introspection-1.*.x86_64.rpm /rpmbuild/RPMS/x86_64/gobject-introspection-devel*.x86_64.rpm

RUN yum install -y harfbuzz-devel libthai-devel
ADD pango.spec  /rpmbuild/SOURCES/
ADD http://ftp.gnome.org/pub/gnome/sources/pango/1.36/pango-1.36.3.tar.xz  /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/pango.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/pango-1.*.x86_64.rpm /rpmbuild/RPMS/x86_64/pango-devel-1.*.x86_64.rpm

ADD gdk-pixbuf2.spec /rpmbuild/SOURCES/
ADD http://ftp.gnome.org/pub/gnome/sources/gdk-pixbuf/2.30/gdk-pixbuf-2.30.8.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gdk-pixbuf2.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/gdk-pixbuf2-2.*.x86_64.rpm /rpmbuild/RPMS/x86_64/gdk-pixbuf2-devel-2.*.x86_64.rpm

ADD atk.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/atk/2.12/atk-2.12.0.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/atk.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/atk-2.*.x86_64.rpm /rpmbuild/RPMS/x86_64/atk-devel-*.x86_64.rpm

ADD gtk3.spec /rpmbuild/SOURCES/
ADD librsvg-vala.patch /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gtk+/3.12/gtk+-3.12.2.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gtk3.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/gtk3-3.*.x86_64.rpm /rpmbuild/RPMS/x86_64/gtk3-devel-3.*.x86_64.rpm

ADD librsvg2.spec /rpmbuild/SOURCES/
ADD http://ftp.gnome.org/pub/gnome/sources/librsvg/2.40/librsvg-2.40.2.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/librsvg2.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/librsvg2-2.*.x86_64.rpm /rpmbuild/RPMS/x86_64/librsvg2-devel-2.*.x86_64.rpm

ADD gnome-icon-theme.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gnome-icon-theme/3.12/gnome-icon-theme-3.12.0.tar.xz  /rpmbuild/SOURCES/
ADD legacy-icon-mapping.xml /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gnome-icon-theme.spec && rpm -Uvh /rpmbuild/RPMS/noarch/gnome-icon-theme*.rpm

ADD gnome-icon-theme-symbolic.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gnome-icon-theme-symbolic/3.12/gnome-icon-theme-symbolic-3.12.0.tar.xz  /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gnome-icon-theme-symbolic.spec && rpm -Uvh /rpmbuild/RPMS/noarch/gnome-icon-theme-symbolic-3.*.rpm

ADD gnome-themes-standard.spec /rpmbuild/SOURCES/
ADD http://ftp.gnome.org/pub/gnome/sources/gnome-themes-standard/3.12/gnome-themes-standard-3.12.0.tar.xz /rpmbuild/SOURCES/
ADD settings.ini /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gnome-themes-standard.spec && rpm -Uvh /rpmbuild/RPMS/noarch/adwaita*.noarch.rpm /rpmbuild/RPMS/x86_64/adwaita*.x86_64.rpm /rpmbuild/RPMS/x86_64/gnome-themes-standard-*.x86_64.rpm

ADD vte3.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/vte/0.36/vte-0.36.2.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/vte3.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/vte3-0.*.x86_64.rpm /rpmbuild/RPMS/x86_64/vte3-devel*.x86_64.rpm

ADD dconf.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/dconf/0.20/dconf-0.20.0.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/dconf.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/dconf-0.*.x86_64.rpm /rpmbuild/RPMS/x86_64/dconf-devel*.x86_64.rpm

ADD gsettings-desktop-schemas.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gsettings-desktop-schemas/3.12/gsettings-desktop-schemas-3.12.2.tar.xz  /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gsettings-desktop-schemas.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/gsettings-desktop*.rpm

ADD libpeas.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/libpeas/1.10/libpeas-1.10.0.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/libpeas.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/libpeas-1.*.rpm /rpmbuild/RPMS/x86_64/libpeas-devel*.rpm

ADD gjs.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gjs/1.40/gjs-1.40.1.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gjs.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/gjs-1.*.rpm /rpmbuild/RPMS/x86_64/gjs-devel*.rpm

ADD gnome-desktop3.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gnome-desktop/3.12/gnome-desktop-3.12.2.tar.xz /rpmbuild/SOURCES/
ADD gnome-desktop-broadway.patch /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gnome-desktop3.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/gnome-desktop3-3.*.x86_64.rpm /rpmbuild/RPMS/x86_64/gnome-desktop3-devel-3.*.x86_64.rpm

RUN yum install -y libexif-devel exempi-devel

ADD libnotify.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/libnotify/0.7/libnotify-0.7.6.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/libnotify.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/libnotify-0.*.x86_64.rpm /rpmbuild/RPMS/x86_64/libnotify-devel*.x86_64.rpm

RUN yum install -y libproxy-devel gnutls-devel

ADD glib-networking.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/glib-networking/2.40/glib-networking-2.40.1.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/glib-networking.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/glib-networking-2.*.x86_64.rpm

RUN yum install -y sqlite-devel

ADD libsoup.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/libsoup/2.46/libsoup-2.46.0.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/libsoup.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/libsoup-2.*.x86_64.rpm /rpmbuild/RPMS/x86_64/libsoup-devel*.x86_64.rpm

RUN yum install -y avahi-devel avahi-glib-devel libsecret-devel

ADD gvfs.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gvfs/1.20/gvfs-1.20.2.tar.xz /rpmbuild/SOURCES/
ADD gvfs-archive-integration.patch /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gvfs.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/gvfs-1.*.x86_64.rpm /rpmbuild/RPMS/x86_64/gvfs-devel*.x86_64.rpm

ADD gtksourceview3.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gtksourceview/3.12/gtksourceview-3.12.2.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gtksourceview3.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/gtksourceview3-3.*.rpm /rpmbuild/RPMS/x86_64/gtksourceview3-devel*.rpm

ADD gnome-terminal.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gnome-terminal/3.12/gnome-terminal-3.12.2.tar.xz  /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gnome-terminal.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/gnome-terminal-3.*.rpm

RUN yum install -y enchant-devel

ADD gedit.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gedit/3.12/gedit-3.12.2.tar.xz /rpmbuild/SOURCES/
ADD gedit-broadway.patch /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gedit.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/gedit-3.*.rpm

ADD nautilus.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/nautilus/3.12/nautilus-3.12.2.tar.xz /rpmbuild/SOURCES/
ADD nautilus-broadway.patch /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/nautilus.spec && rpm -Uvh /rpmbuild/RPMS/x86_64/nautilus-3.*.x86_64.rpm /rpmbuild/RPMS/x86_64/nautilus-extensions*.x86_64.rpm /rpmbuild/RPMS/x86_64/nautilus-devel-3.*.x86_64.rpm

ADD simple_init.spec /rpmbuild/SOURCES/
ADD simple_init.c /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/simple_init.spec

RUN mkdir -p /repo && cp /rpmbuild/RPMS/noarch/* /rpmbuild/RPMS/x86_64/* /repo &&  createrepo /repo

ADD http.conf /
EXPOSE 80

CMD ["/usr/sbin/lighttpd","-D","-f", "/http.conf"]
