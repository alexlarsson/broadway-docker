FROM fedora:20
MAINTAINER Alexander Larsson <alexl@redhat.com>
EXPOSE 8080
ADD broadway.repo /etc/yum.repos.d/

RUN yum install -y freetype fontconfig pixman libpng exempi libjpeg-turbo libthai abattis-cantarell-fonts hicolor-icon-theme libexif libtiff harfbuzz desktop-file-utils enchant mozjs24 liberation-mono-fonts liberation-sans-fonts liberation-serif-fonts avahi-glib libsecret gnutls libproxy && yum clean all

RUN yum -y --disablerepo=* --enablerepo=broadway install glib2 gtk3 && yum clean all
RUN yum -y install librsvg2 && yum clean all
RUN yum -y --disablerepo=*  --enablerepo=broadway install gnome-icon-theme gnome-icon-theme-symbolic gnome-themes-standard vte3 dconf gsettings-desktop-schemas gnome-terminal gedit nautilus gjs && yum clean all

RUN adduser user -c User -d /home/user -m -s /bin/bash -u 1000 -U

ADD init.sh /
ADD panel.js /

CMD ["/init.sh"]
USER 1000
WORKDIR /home/user
