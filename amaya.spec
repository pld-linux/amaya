#
# Conditional build:
%bcond_with	gtk1	# GTK+ 1.x instead of WX
#
Summary:	Web Browser/Editor from the World Wide Web Consortium
Summary(pl.UTF-8):	Przeglądarka/edytor stron WWW z World Wide Web Consortium
Name:		amaya
Version:	9.54
Release:	1.1
License:	Copyright 1995-2002 (MIT) (INRIA), (L)GPL compatible
Group:		X11/Applications/Networking
Source0:	ftp://ftp.w3.org/pub/amaya/%{name}-src-%{version}.tgz
# Source0-md5:	b8fa2655e026091835a9bb7c59e3db83
Patch0:		%{name}-opt.patch
Patch1:		%{name}-system-libwww.patch
URL:		http://www.w3.org/Amaya/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake
BuildRequires:	dos2unix
BuildRequires:	expat-devel
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.0
BuildRequires:	redland-devel >= 0.9.16
BuildRequires:	w3c-libwww-devel >= 5.4.0-8
BuildRequires:	zlib-devel
BuildRequires:	libraptor
BuildRequires:	libraptor-devel
BuildRequires:	libtool >= 2:1.4d-3
%if %{with gtk1}
BuildRequires:	gtk+-devel
BuildRequires:	imlib-devel
%else
BuildRequires:	wxGTK2-unicode-devel
BuildRequires:	wxGTK2-unicode-gl-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/%{_lib}
%define		_bindir		/usr/bin

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
%setup -q -n Amaya
%patch0 -p1

# AC_SUBST_FILE doesn't work with CR+LF
dos2unix amaya/Makefile.in

%patch1 -p1

%build
export LDFLAGS="-lraptor"
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
mkdir Linux
cd Linux
../%configure \
	WXCONFIG=/usr/bin/wx-gtk2-unicode-config \
	--enable-system-redland \
	--enable-system-wx \
	--without-graphiclibs \
	--with-dav \
	%{?with_gtk1:--with-gtk} \
	%{!?with_gtk1:--with-wx --with-gl}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_prefix}}

%{__make} -C Linux install \
	DESTDIR=$RPM_BUILD_ROOT

%if  %{with gtk1}
rm -f $RPM_BUILD_ROOT%{_bindir}/amaya-gtk
ln -sf %{_prefix}/Amaya-%{version}/gtk/bin/amaya $RPM_BUILD_ROOT%{_bindir}/amaya
%else
rm -f $RPM_BUILD_ROOT%{_bindir}/amaya-wx
ln -sf %{_prefix}/Amaya-%{version}/wx/bin/amaya $RPM_BUILD_ROOT%{_bindir}/amaya
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc amaya/COPYRIGHT README README.amaya README.gl README.wx
%attr(755,root,root) %{_bindir}/amaya*
%dir %{_prefix}/Amaya*
%{_prefix}/Amaya*/amaya
%{_prefix}/Amaya*/annotlib
%{_prefix}/Amaya*/config
%{_prefix}/Amaya*/dicopar
%{_prefix}/Amaya*/doc
%{_prefix}/Amaya*/fonts
%{_prefix}/Amaya*/resources
%if  %{with gtk1}
%dir %{_prefix}/Amaya*/gtk
%dir %{_prefix}/Amaya*/gtk/bin
%attr(755,root,root) %{_prefix}/Amaya*/gtk/bin/amaya
%attr(755,root,root) %{_prefix}/Amaya*/gtk/bin/print
%else
%dir %{_prefix}/Amaya*/wx
%dir %{_prefix}/Amaya*/wx/bin
%attr(755,root,root) %{_prefix}/Amaya*/wx/bin/amaya
%attr(755,root,root) %{_prefix}/Amaya*/wx/bin/print
%endif
