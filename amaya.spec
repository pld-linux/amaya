Summary:	Web Browser/Editor from the World Wide Web Consortium
Summary(pl):	Przegl±darka/edytor stron www z World Wide Web Consortium
Name:		amaya
Version:	7.1
Release:	1
License:	Copyright 1995-2002 (MIT) (INRIA), (L)GPL compatible
Group:		X11/Applications/Networking
URL:		http://www.w3.org/Amaya/
Source0:	ftp://ftp.w3.org/pub/amaya/%{name}-src-%{version}.tgz
#Source1:	ftp://ftp.w3.org/pub/amaya/Dutch.tgz
#Source2:	ftp://ftp.w3.org/pub/amaya/Spanish.tgz
#Source3:	ftp://ftp.w3.org/pub/amaya/Italian.tgz
#Source4:	ftp://ftp.w3.org/pub/amaya/Swedish.tgz
#Source5:	ftp://ftp.w3.org/pub/amaya/German.tgz
Patch0:		%{name}-ac-gtkglarea.patch
Patch1:		%{name}-install.patch
BuildRequires:	autoconf
BuildRequires:	expat-devel
BuildRequires:	gtk+-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	zlib-devel
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description

Amaya is a complete web browsing and authoring environment and comes
equipped with a WYSIWYG style of interface, similar to that of the
most popular commercial browsers. With such an interface, users do not
need to know the HTML or CSS languages.

Authors:
--------- Irene.Vatton@w3.org, Jose.Kahan@w3.org,
  Vincent.Quint@w3.org, Laurent.Carcone@w3.org

%description -l pl

Amaya jest kompletn± przegl±dark± www i ¶rodowiskiem tworzenia stron
www, wyposa¿ona jest w interfejs WYSIWYG podobny do stosowanego w
najbardziej popularnych komercyjnych przegl±darkach. Z takim
interfejsem u¿ytkownicy nie musz± wiedzieæ co to jest HTML czy CSS.

Autorzy:
--------- Irene.Vatton@w3.org, Jose.Kahan@w3.org,
  Vincent.Quint@w3.org, Laurent.Carcone@w3.org

%prep
%setup -q -n Amaya
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
cp -f /usr/share/automake/{config.,missing}* .
mkdir Linux
cd Linux
../%configure \
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--without-graphic-libs \
	--with-dav \
	--with-x
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}/bin
cd Linux
%{__make} install
ln -sf %{_prefix}/Amaya/applis/bin/%{name} $RPM_BUILD_ROOT%{_prefix}/bin/%{name} 

%files
%defattr(644,root,root,755)
%doc amaya/COPYRIGHT README README.amaya README.gl
%attr(755,root,root) %{_bindir}/amaya
%dir %{_prefix}/Amaya
%{_prefix}/Amaya/amaya
%{_prefix}/Amaya/annotlib
%{_prefix}/Amaya/[cdf]*
%attr(755,root,root) %{_prefix}/Amaya/applis/bin/*

%clean
rm -rf $RPM_BUILD_ROOT
