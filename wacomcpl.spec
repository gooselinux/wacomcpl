Name:           wacomcpl
Version:        0.9.0
Release:        1%{?dist}
Summary:        Wacom driver configuration tool

Group:          User Interface/X
License:        GPLv2+
URL:            http://people.redhat.com/~phuttere/wacomcpl/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        http://people.redhat.com/~phuttere/wacomcpl/%{name}-%{version}.tar.bz2
Source1:        wacomcpl.desktop
Source2:        wacomcpl-icon.png

# wacom driver doesn't exist on those
ExcludeArch:    s390 s390x

BuildRequires:  automake libtool
BuildRequires:  libX11-devel libXext-devel libXi-devel
BuildRequires:  tcl-devel tk-devel desktop-file-utils

Requires:       xorg-x11-drv-wacom
Requires:       libX11 libXi libXext
Requires:       tcl tk
# for xdpyinfo
Requires:       xorg-x11-utils

%description
%{name} is a graphical configuration tool for Wacom devices. It wraps the
xsetwacom command and provides an interface to some configuration options of
the xorg-x11-drv-wacom driver.

%prep
%setup -q

%build
autoreconf -v --install || exit 1
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/TkXInput/libwacomxi.a %{buildroot}%{_libdir}/TkXInput/libwacomxi.la

install -d %{buildroot}%{_datadir}/wacomcpl
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/wacomcpl/wacomcpl.desktop
sed -i -e "s,DATADIR,%{_datadir}," %{buildroot}%{_datadir}/wacomcpl/wacomcpl.desktop

desktop-file-install --vendor gnome                             \
                --dir %{buildroot}%{_datadir}/applications      \
                --mode 0644                                     \
                --add-only-show-in GNOME                        \
                %{buildroot}%{_datadir}/wacomcpl/wacomcpl.desktop
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/wacomcpl/wacomcpl-icon.png

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/%{name}-exec
%doc GPL
%{_libdir}/TkXInput/libwacomxi.so*
%{_libdir}/TkXInput/pkgIndex.tcl
%{_sysconfdir}/X11/xinit/xinitrc.d/wacomcpl.sh
%{_datadir}/applications/gnome-wacomcpl.desktop
%{_datadir}/wacomcpl/wacomcpl.desktop
%{_datadir}/wacomcpl/wacomcpl-icon.png

%changelog
* Tue May 25 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.9.0-1
- Initial package.
