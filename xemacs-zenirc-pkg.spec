Summary:	ZENIRC IRC Client
Summary(pl.UTF-8):	ZENIRC - klient IRC
%define		srcname	zenirc
Name:		xemacs-zenirc-pkg
Version:	2.112
Release:	2
License:	GPL
Group:		Applications/Editors/Emacs
Source0:	ftp://ftp.splode.com/pub/zenirc/zenirc-%{version}.tar.gz
# Source0-md5:	ad6e1bb57e6416deac171c870bce2830
#Patch0:		%{name}-info.patch
URL:		http://www.xemacs.org/
BuildRequires:	xemacs
Requires:	xemacs
Conflicts:	xemacs-sumo
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZENIRC IRC Client.

%description -l pl.UTF-8
ZENIRC - klient IRC.

%prep
%setup -q -n zenirc-%{version}
#%%patch0 -p1
cat <<EOF >src/auto-autoloads.el
(autoload 'zenirc "zenirc" nil t)
# no goodies!
#(autoload 'zenirc-color-mode "zenirc-color-mode" nil t)
#(autoload 'zenirc-complete "zenirc-complete" nil t)
EOF

%build
#(cd man/zenirc; awk '/^\\input texinfo/ {print FILENAME}' * | xargs makeinfo)
./configure
%{__make} EMACS=xemacs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/xemacs-packages/lisp/zenirc
install -d $RPM_BUILD_ROOT%{_infodir}

cp src/*example* .
# remove .el file if corresponding .elc exists
for i in src/*.el; do test ! -f ${i}c || rm -f $i ; done
install src/*.el* $RPM_BUILD_ROOT%{_datadir}/xemacs-packages/lisp/zenirc

install doc/*.info* $RPM_BUILD_ROOT%{_infodir}

rm -f doc/zenirc.{info,txt,texi}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc BUGS README NEWS doc *example*
%{_datadir}/xemacs-packages/lisp/*
%{_infodir}/*.info*
