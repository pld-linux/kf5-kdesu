%define		kdeframever	5.80
%define		qtver		5.9.0
%define		kfname		kdesu

Summary:	User interface for running shell commands with root privileges
Name:		kf5-%{kfname}
Version:	5.80.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	9b44251d2c577e6594ec786ea82ec05b
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kconfig-devel >= %{version}
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	kf5-kdbusaddons-devel >= %{version}
BuildRequires:	kf5-ki18n-devel >= %{version}
BuildRequires:	kf5-kpty-devel >= %{version}
BuildRequires:	kf5-kservice-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KDESU provides functionality for building GUI front ends for (password
asking) console mode programs. For example, kdesu and kdessh use it to
interface with su and ssh respectively.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5 --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_prefix}/libexec/kf5/kdesu_stub
%attr(755,root,root) %{_prefix}/libexec/kf5/kdesud
%ghost %{_libdir}/libKF5Su.so.5
%attr(755,root,root) %{_libdir}/libKF5Su.so.*.*
%{_datadir}/qlogging-categories5/ksu.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KDESu
%{_includedir}/KF5/kdesu_version.h
%{_libdir}/cmake/KF5Su
%{_libdir}/libKF5Su.so
%{qt5dir}/mkspecs/modules/qt_KDESu.pri
