%define perlvendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)

Name:	lintian  
Group:	Development/Languages  
Version:	2.4.3
Release:	%mkrel 2
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
Provides: perl(Read_pkglists)
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
mkdir -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT/%{_sysconfdir} $RPM_BUILD_ROOT%{perlvendorlib} $RPM_BUILD_ROOT/%{_datadir}/%{name} $RPM_BUILD_ROOT/%{_mandir}/man1
sed 's/<VERSION>/%{version}/' frontend/%{name} > $RPM_BUILD_ROOT%{_bindir}/%{name}
sed 's/<VERSION>/%{version}/' frontend/%{name}-info > $RPM_BUILD_ROOT%{_bindir}/%{name}-info
chmod 755 $RPM_BUILD_ROOT%{_bindir}/%{name}*
install -m 644 doc/lintianrc.example $RPM_BUILD_ROOT%{_sysconfdir}/lintianrc
cp -a lib/* $RPM_BUILD_ROOT%{perlvendorlib}
cp -a checks collection data unpack $RPM_BUILD_ROOT/%{_datadir}/%{name}
cp -a man/* $RPM_BUILD_ROOT/%{_mandir}/man1
  
%files
%defattr (-,root,root)
%doc doc/*
%{_sysconfdir}/*
%{_bindir}/*
%{perlvendorlib}/*
%{_mandir}/man1/*
%{_datadir}/%{name}

%clean  
rm -rf $RPM_BUILD_ROOT  
  
%changelog  
