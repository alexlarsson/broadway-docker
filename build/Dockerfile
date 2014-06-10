FROM fedora:20
MAINTAINER Alexander Larsson <alexl@redhat.com>
EXPOSE 8080
VOLUME ["/rpms"]
RUN yum update -y
RUN yum install -y yum-utils rpm-build pixman-devel libpng-devel libxml2-devel freetype-devel fontconfig-devel gtk-doc gnome-common intltool libjpeg-devel libtiff-devel hicolor-icon-theme make abattis-cantarell-fonts liberation-mono-fonts liberation-sans-fonts liberation-serif-fonts flex bison python-mako
RUN yum-builddep -y glib2

RUN mkdir -p /rpmbuild/SOURCES

ADD glib2.spec  /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/glib/2.40/glib-2.40.0.tar.xz  /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/glib2.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/glib2-2.*.x86_64.rpm /rpmbuild/RPMS/x86_64/glib2-devel*.x86_64.rpm

ADD cairo.spec /rpmbuild/SOURCES/
ADD http://pkgs.fedoraproject.org/repo/pkgs/cairo/cairo-1.13.1-337ab1f.tar.xz/f44d8e5c7e57b1b47968747817e7e11c/cairo-1.13.1-337ab1f.tar.xz /rpmbuild/SOURCES/
ADD cairo-multilib.patch /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/cairo.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/cairo-1.*.x86_64.rpm /rpmbuild/RPMS/x86_64/cairo-devel-1.*.x86_64.rpm /rpmbuild/RPMS/x86_64/cairo-gobject-1.*.x86_64.rpm /rpmbuild/RPMS/x86_64/cairo-gobject-devel-1.*.x86_64.rpm

ADD gobject-introspection.spec  /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gobject-introspection/1.40/gobject-introspection-1.40.0.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gobject-introspection.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/gobject-introspection-1.*.x86_64.rpm /rpmbuild/RPMS/x86_64/gobject-introspection-devel*.x86_64.rpm

ADD pango.spec  /rpmbuild/SOURCES/
ADD http://ftp.gnome.org/pub/gnome/sources/pango/1.36/pango-1.36.3.tar.xz  /rpmbuild/SOURCES/
RUN yum install -y harfbuzz-devel libthai-devel
RUN rpmbuild -ba /rpmbuild/SOURCES/pango.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/pango-1.*.x86_64.rpm /rpmbuild/RPMS/x86_64/pango-devel-1.*.x86_64.rpm

ADD gdk-pixbuf2.spec /rpmbuild/SOURCES/
ADD http://ftp.gnome.org/pub/gnome/sources/gdk-pixbuf/2.30/gdk-pixbuf-2.30.8.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gdk-pixbuf2.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/gdk-pixbuf2-2.*.x86_64.rpm /rpmbuild/RPMS/x86_64/gdk-pixbuf2-devel-2.*.x86_64.rpm

RUN yum install -y gnome-doc-utils

ADD atk.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/atk/2.12/atk-2.12.0.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/atk.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/atk-2.*.x86_64.rpm /rpmbuild/RPMS/x86_64/atk-devel-*.x86_64.rpm

ADD gtk3.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gtk+/3.12/gtk+-3.12.2.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gtk3.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/gtk3-3.*.x86_64.rpm /rpmbuild/RPMS/x86_64/gtk3-devel-3.*.x86_64.rpm

RUN yum install -y icon-naming-utils
RUN yum install -y librsvg2-devel

ADD gnome-icon-theme.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gnome-icon-theme/3.12/gnome-icon-theme-3.12.0.tar.xz  /rpmbuild/SOURCES/
ADD legacy-icon-mapping.xml /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gnome-icon-theme.spec
RUN rpm -Uvh /rpmbuild/RPMS/noarch/gnome-icon-theme*.rpm

ADD gnome-icon-theme-symbolic.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gnome-icon-theme-symbolic/3.12/gnome-icon-theme-symbolic-3.12.0.tar.xz  /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gnome-icon-theme-symbolic.spec
RUN rpm -Uvh /rpmbuild/RPMS/noarch/gnome-icon-theme-symbolic-3.*.rpm

ADD gnome-themes-standard.spec /rpmbuild/SOURCES/
ADD http://ftp.gnome.org/pub/gnome/sources/gnome-themes-standard/3.12/gnome-themes-standard-3.12.0.tar.xz /rpmbuild/SOURCES/
ADD settings.ini /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gnome-themes-standard.spec
RUN rpm -Uvh /rpmbuild/RPMS/noarch/adwaita*.noarch.rpm /rpmbuild/RPMS/x86_64/adwaita*.x86_64.rpm /rpmbuild/RPMS/x86_64/gnome-themes-standard-*.x86_64.rpm

RUN yum install -y ncurses-devel

ADD vte3.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/vte/0.36/vte-0.36.2.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/vte3.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/vte3-0.*.x86_64.rpm /rpmbuild/RPMS/x86_64/vte3-devel*.x86_64.rpm

RUN yum install -y dbus-devel
RUN yum install -y vala-devel

ADD dconf.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/dconf/0.20/dconf-0.20.0.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/dconf.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/dconf-0.*.x86_64.rpm /rpmbuild/RPMS/x86_64/dconf-devel*.x86_64.rpm

ADD gsettings-desktop-schemas.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gsettings-desktop-schemas/3.12/gsettings-desktop-schemas-3.12.2.tar.xz  /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gsettings-desktop-schemas.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/gsettings-desktop*.rpm

RUN yum install -y desktop-file-utils libuuid-devel appdata-tools

ADD gnome-terminal.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gnome-terminal/3.12/gnome-terminal-3.12.2.tar.xz  /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gnome-terminal.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/gnome-terminal-3.*.rpm

ADD gtksourceview3.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gtksourceview/3.12/gtksourceview-3.12.2.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gtksourceview3.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/gtksourceview3-3.*.rpm /rpmbuild/RPMS/x86_64/gtksourceview3-devel*.rpm

# libpeas

ADD libpeas.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/libpeas/1.10/libpeas-1.10.0.tar.xz /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/libpeas.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/libpeas-1.*.rpm /rpmbuild/RPMS/x86_64/libpeas-devel*.rpm

RUN yum install -y enchant-devel iso-codes-devel

ADD gedit.spec /rpmbuild/SOURCES/
ADD http://ftp.acc.umu.se/pub/gnome/sources/gedit/3.12/gedit-3.12.2.tar.xz /rpmbuild/SOURCES/
ADD gedit-broadway.patch /rpmbuild/SOURCES/
RUN rpmbuild -ba /rpmbuild/SOURCES/gedit.spec
RUN rpm -Uvh /rpmbuild/RPMS/x86_64/gedit-3.*.rpm

#nautilus
#gjs
# script that wraps dbus + broadwayd + HOME, etc
# simple launcher
# Minimal runtime container
