Summary:	ZENIRC IRC Client
Summary(pl):	ZENIRC - klient IRC
Name:		xemacs-zenirc-pkg
%define		srcname	zenirc
Version:	2.112
Release:	1
License:	GPL
Group:		Applications/Editors/Emacs
Group(de):	Applikationen/Editors/Emacs
Group(pl):	Aplikacje/Edytory/Emacs
Source0:	ftp://ftp.splode.com/pub/zenirc/zenirc-%{version}.tar.gz
#Patch0:		xemacs-zenirc-pkg-info.patch
URL:		http://www.xemacs.org/
BuildArch:	noarch
Conflicts:	xemacs-sumo
Requires:	xemacs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ZENIRC IRC Client.

%description -l pl
ZENIRC - klient IRC.

%prep
%setup -q -n zenirc-%{version}
#%patch0 -p1
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

gzip -9nf BUGS README NEWS

%clean
rm -fr $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc *.gz doc *example*
%{_datadir}/xemacs-packages/lisp/*
%{_infodir}/*
