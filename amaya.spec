Summary:	Web Browser/Editor from the World Wide Web Consortium
Summary(pl.UTF-8):	Przeglądarka/edytor stron WWW z World Wide Web Consortium
Name:		amaya
Version:	11.4.4
Release:	0.1
License:	Copyright 1995-2002 (MIT) (INRIA), (L)GPL compatible
Group:		X11/Applications/Networking
Source0:	ftp://ftp.w3.org/pub/amaya/%{name}-sources-%{version}.tgz
# Source0-md5:	e8072c7b1d06b983951c56e9f51fbacf
Patch0:		%{name}-opt.patch
URL:		http://www.w3.org/Amaya/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake
BuildRequires:	expat-devel
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.0
BuildRequires:	libraptor
BuildRequires:	libraptor-devel
BuildRequires:	libtool >= 2:1.4d-3
BuildRequires:	redland-devel >= 0.9.16
BuildRequires:	w3c-libwww-devel >= 5.4.0-8
BuildRequires:	zlib-devel
BuildRequires:	wxGTK2-unicode-devel
BuildRequires:	wxGTK2-unicode-gl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# ../.././thotlib/base/batchmessage.c:29:25: error: format not a string literal and no format arguments [-Werror=format-security]
# ../.././thotlib/base/batchmessage.c:37:25: error: format not a string literal and no format arguments [-Werror=format-security]
%define		filterout_cxx	-Werror=format-security

%description
Amaya is a complete web browsing and authoring environment and comes
equipped with a WYSIWYG style of interface, similar to that of the
most popular commercial browsers. With such an interface, users do not
need to know the HTML or CSS languages.

%description -l pl.UTF-8
Amaya jest kompletną przeglądarką WWW i środowiskiem tworzenia stron
WWW, wyposażona jest w interfejs WYSIWYG podobny do stosowanego w
najbardziej popularnych komercyjnych przeglądarkach. Z takim
interfejsem użytkownicy nie muszą wiedzieć co to jest HTML czy CSS.

%prep
%setup -q -n Amaya%{version}
install -d sys-libs
mv Mesa freetype libwww redland wxWidgets sys-libs
cd Amaya
%patch0 -p1

%build
cd Amaya
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
install -d Linux
cd Linux
../%configure \
	WXCONFIG=/usr/bin/wx-gtk2-unicode-config \
	--prefix=%{_libdir} \
	--enable-system-libwww \
	--enable-system-wx \
	--with-dav \
	--with-gl

%{__make} -j1 \
	AMAYA_LIBWWW_SRC= \
	AMAYA_LIBWWW_INCLUDES="$(libwww-config --cflags)" \
	AMAYA_LIBWWW_LIBS="$(libwww-config --libs)" \
	IMGLIBS="-lpng -ljpeg" \
	EXPAT_LIBRARIES="-lpng -ljpeg"

#  EXPAT_LIBRARIES/IMGLIBS is fake, just convient place to add LIBS

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_prefix}}
%{__make} -C Amaya/Linux install \
	AMAYA_LIBWWW_SRC= \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf %{_libdir}/Amaya/wx/bin/amaya $RPM_BUILD_ROOT%{_bindir}/amaya

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Amaya/{amaya/COPYRIGHT,README,README.wx}
%attr(755,root,root) %{_bindir}/amaya
%dir %{_libdir}/Amaya
%{_libdir}/Amaya/amaya
%{_libdir}/Amaya/annotlib
%{_libdir}/Amaya/config
%{_libdir}/Amaya/dicopar
%{_libdir}/Amaya/doc
%{_libdir}/Amaya/fonts
%{_libdir}/Amaya/resources
%dir %{_libdir}/Amaya/wx
%dir %{_libdir}/Amaya/wx/bin
%attr(755,root,root) %{_libdir}/Amaya/wx/bin/amaya
%attr(755,root,root) %{_libdir}/Amaya/wx/bin/amaya_bin
%attr(755,root,root) %{_libdir}/Amaya/wx/bin/print
