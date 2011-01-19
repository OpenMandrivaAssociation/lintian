Name:	lintian  
Group:	Development/Languages  
Version:	2.4.3
Release:	%mkrel 1
License:	UNKNOWN  
Summary:	Debian package checker  
Source:		lintian_%{version}.tar.gz  
BuildRoot:	%{_tmppath}/%{name}-%{version}-build  
Requires:	perl
# build essentials  
BuildRequires:	ncurses-devel  
BuildRequires:	e2fsprogs  
BuildRequires:	fakeroot  
BuildRequires:	zlib-devel  
BuildRequires:	sed
BuildRequires:	dpkg
BuildRequires:	perl-IPC-Run, perl-Test-Pod, perl-AptPkg, perl-Parse-DebianChangelog
%description  
Lintian dissects Debian packages and reports bugs and policy  
violations. It contains automated checks for many aspects of Debian  
policy as well as some checks for common errors.  
  
It uses an archive directory, called laboratory, in which it stores  
information about the packages it examines.  It can keep this  
information between multiple invocations in order to avoid repeating  
expensive data-collection operations. This makes it possible to check the  
complete Debian archive for bugs, in a reasonable time.  
  
This package is useful for all people who want to check Debian  
packages for compliance with Debian policy. Every Debian maintainer  
should check packages with this tool before uploading them to the  
archive.  
  
%prep  
rm -rf %{name}-%{version}  

%setup -q
rm -rf doc/lintian.html/ doc/lintian.txt runtests doc/help.tmp doc/README
find -name "*.py?" -print0 | xargs -0r rm
  
%build
LINTIAN_ROOT="" ./frontend/lintian --help | tail -n +3 | perl -n -e 'print "  $_"' >doc/help.tmp
perl -p -e 'BEGIN { open(HELP,"doc/help.tmp") or die; local $/=undef; $h = <HELP> }; s/\%LINTIAN_HELP\%/$h/' doc/README.in >doc/README

%check
#LINTIAN_ROOT="" perl t/runtests -k t t/tests
#LINTIAN_ROOT="" perl testset/runtests -k testset t/tests
  
%install  
rm -rf $RPM_BUILD_ROOT  
mkdir -p $RPM_BUILD_ROOT%{_bindir}
sed 's/<VERSION>/%{version}/' frontend/lintian > $RPM_BUILD_ROOT%{_bindir}/lintian
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}
install -m 644 doc/lintianrc.example $RPM_BUILD_ROOT%{_sysconfdir}/lintianrc
  
%files
%{_sysconfdir}/*
%{_bindir}/*
  
%clean  
rm -rf $RPM_BUILD_ROOT  
  
%changelog  
