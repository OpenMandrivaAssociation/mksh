%define debug_package %{nil}

Name: mksh
Version: R50e
Release: 1
Summary: A free Korn Shell implementation and successor to pdksh
License: MirOS, BSD, ISC
Group: Shells
URL: https://www.mirbsd.org/mksh.htm
Source0: https://www.mirbsd.org/MirOS/dist/mir/mksh/%{name}-%{version}.tgz
Source1: https://www.mirbsd.org/TaC-mksh.txt
Source2: https://www.mirbsd.org/pics/mksh.svg
Source3: mkshrc
# For building docs
BuildRequires: groff-base

%description
mksh is the MirBSD enhanced version of the Public Domain Korn shell (pdksh),
a bourne-compatible shell which is largely similar to the original AT&T Korn
shell. It includes bug fixes and feature improvements in order to produce a
modern, robust shell good for interactive and especially script use.

mksh is a direct descendant from the OpenBSD /bin/ksh and contains most of
its bug fixes and enhancements. mksh implements many, but by far not all,
ksh93 features, and most ksh88 features. mksh can do many things GNU bash
can't, and is much faster and smaller.

%prep
%setup -qn %{name}
# Packagers/vendors adding patches that make mksh deviate from the default
# behavior should append a space plus a vendor-defined string so they can
# be distinguished. 
%define product %{product_vendor} %{product_version}
sed -i '/^\t@(#)MIRBSD KSH/s/$/ %{product}/' check.t
sed -i '/^#define MKSH_VERSION/s/"$/ %{product}"/' sh.h
sed -i -e 's|-O2|%{optflags}|g' Build.sh

%build
sh Build.sh
./test.sh

%install
cp %SOURCE1 .
install -D mksh %{buildroot}/bin/mksh
install -D mksh.1 %{buildroot}%{_mandir}/man1/mksh.1
install -D %SOURCE2 %{buildroot}%{_datadir}/pixmaps/mksh.svg
install -D %SOURCE3 %{buildroot}%{_sysconfdir}/mkshrc

%post
/usr/share/rpm-helper/add-shell %{name} $1 /bin/mksh

%postun
/usr/share/rpm-helper/del-shell %{name} $1 /bin/mksh

%files
%doc dot.mkshrc TaC-mksh.txt
%config(noreplace) %{_sysconfdir}/mkshrc
/bin/mksh
%{_mandir}/man1/mksh.1*
%{_datadir}/pixmaps/mksh.svg
