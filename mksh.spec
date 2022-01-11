# Set with bin_sh to symlink mksh to /bin/sh
%bcond_with bin_sh

Name: mksh
Version: R59c
Release: 3
Summary: A free Korn Shell implementation and successor to pdksh
License: MirOS, BSD, ISC
Group: Shells
URL: https://www.mirbsd.org/mksh.htm
Source0: https://www.mirbsd.org/MirOS/dist/mir/mksh/%{name}-%{version}.tgz
Source1: https://www.mirbsd.org/TaC-mksh.txt
Source2: https://www.mirbsd.org/pics/mksh.svg
Source3: mkshrc
Source4: dot-mkshrc
Patch0: mksh-50e-no-tty-warning.patch
Patch1: mksh-dont-barf-on-empty-HISTSIZE.patch
# For building docs
BuildRequires: groff-base
Requires(post,postun): rpm-helper

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
%autosetup -n %{name} -p1

# Packagers/vendors adding patches that make mksh deviate from the default
# behavior should append a space plus a vendor-defined string so they can
# be distinguished.
%define product %{product_vendor} %{product_version}
sed -i '/^\t@(#)MIRBSD KSH/s/$/ %{product}/' check.t
sed -i '/^#define MKSH_VERSION/s/"$/ %{product}"/' sh.h
sed -i -e 's|-O2|%{optflags}|g' Build.sh

%build
%set_build_flags

CC="%{__cc}" CFLAGS="%{optflags}" LDFLAGS="%{ldflags}" sh Build.sh

%install
cp %{SOURCE1} .
install -D mksh %{buildroot}/bin/mksh
install -D mksh.1 %{buildroot}%{_mandir}/man1/mksh.1
install -D %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/mksh.svg
install -D -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/mkshrc
install -D -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/skel/.mkshrc

%if %{with bin_sh}
ln -s mksh %{buildroot}/bin/sh
%endif

%post
%_add_shell_helper %{name} $1 /bin/mksh

%postun
%_del_shell_helper %{name} $1 /bin/mksh

%files
%doc dot.mkshrc TaC-mksh.txt
%config(noreplace) %{_sysconfdir}/mkshrc
%config(noreplace) %{_sysconfdir}/skel/.mkshrc
/bin/mksh
%if %{with bin_sh}
/bin/sh
%endif
%{_mandir}/man1/mksh.1*
%{_datadir}/pixmaps/mksh.svg
