Name:           wacomcpl
Version:        0.9.0
Release:        1%{?dist}.2
Summary:        Wacom driver configuration tool

Group:          User Interface/X
License:        GPLv2+
URL:            http://people.redhat.com/~phuttere/wacomcpl/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        http://people.redhat.com/~phuttere/wacomcpl/%{name}-%{version}.tar.bz2
Source1:        wacomcpl.desktop
Source2:        wacomcpl-icon.png

# Bug 624560 - wacom control panel functions are not working
# applies to Patch001 through to Patch016
Patch001:       0001-Fix-typo-mode-should-be-mode.patch
Patch002:       0002-Fix-typo-don-t-use-variablename-when-setting-a-varia.patch
Patch003:       0003-Change-TwinView-settings-to-names-instead-of-numbers.patch
Patch004:       0004-TwinView-returns-strings-not-numbers.patch
Patch005:       0005-Purge-Xinerama-option-the-driver-doesn-t-handle-it.patch
Patch006:       0006-Interpret-screen-number-of-255-as-1.patch
Patch007:       0007-Handle-NumScreen-in-a-separate-function.patch
Patch008:       0008-Hack-up-TwinView-settings.patch
Patch009:       0009-Set-the-device-s-screen-number-after-selecting-a-cal.patch
Patch010:       0010-Work-around-xsetwacom-xydefault-bug-by-supplying-dum.patch
Patch011:       0011-Remove-blinking-animation-on-messageWindow.patch
Patch012:       0012-If-TVResolution-isn-t-set-show-an-error-and-exit.patch
Patch013:       0013-Change-to-use-TVResolution-instead-of-TVResolution0-.patch
Patch014:       0014-Show-an-error-window-if-the-device-wasn-t-found.patch
Patch015:       0001-If-TwinView-is-selected-try-to-guess-the-TVResolutio.patch
Patch016:       0001-Append-not-prepend-wacomcplrc-commands.patch

# Bug 624560 - wacom control panel functions are not working, Comment 36
# https://bugzilla.redhat.com/show_bug.cgi?id=624560#c36
Patch017:       0001-Fix-invalid-parsing-of-mode.patch
Patch018:       0002-Change-button-mapping-from-Button-2-to-simply-2.patch
Patch019:       0003-Use-case-insensitive-type-comparison.patch
Patch020:       0004-Fix-parsing-of-TPCButton.patch
Patch021:       0005-Parse-key-and-button-as-special-configurations.patch
Patch022:       0006-Button-Ignore-should-mean-button-0.patch
Patch023:       0007-Hack-in-ignorebutton-handling.patch
Patch024:       0008-Disallow-doubleclick-use-button-1-1-instead.patch
Patch025:       0009-Purge-screen-toggle-this-isn-t-supported-by-the-driv.patch
Patch026:       0010-Fix-reset-handling-for-displaytoggle-modetoggle-and-.patch

Patch027:       0001-update-the-screen-number-when-calibrating.patch

# wacom driver doesn't exist on those
ExcludeArch:    s390 s390x

BuildRequires:  automake libtool
BuildRequires:  libX11-devel libXext-devel libXi-devel
BuildRequires:  tcl-devel tk-devel desktop-file-utils

Requires:       xorg-x11-drv-wacom >= 0.10.5-6%{?dist}.2
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
%patch001 -p1 
%patch002 -p1 
%patch003 -p1 
%patch004 -p1 
%patch005 -p1 
%patch006 -p1 
%patch007 -p1 
%patch008 -p1 
%patch009 -p1 
%patch010 -p1 
%patch011 -p1 
%patch012 -p1 
%patch013 -p1 
%patch014 -p1 
%patch015 -p1 
%patch016 -p1 
%patch017 -p1 
%patch018 -p1 
%patch019 -p1 
%patch020 -p1 
%patch021 -p1 
%patch022 -p1 
%patch023 -p1 
%patch024 -p1 
%patch025 -p1 
%patch026 -p1 
%patch027 -p1 

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
* Thu Feb 03 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.9.0-1.2
- Multiple patches to address button mapping issues (#624560, z-stream #642915).
- update the screen number when updating
- requires updated xorg-x11-drv-wacom for the matching fixes to xsetwacom
  and the driver.

* Fri Oct 15 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.9.0-1.1
- Multiple patches to address issues with TwinView calibration and setting
  (#624560)
- requires xorg-x11-drv-wacom-0.10.5-7 for TwinView fixes.

* Tue May 25 2010 Peter Hutterer <peter.hutterer@redhat.com> 0.9.0-1
- Initial package.
