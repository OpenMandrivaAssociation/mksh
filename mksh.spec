# Set with bin_sh to symlink mksh to /bin/sh
%bcond_with bin_sh

Summary:	A free Korn Shell implementation and successor to pdksh
Name:		mksh
Version:	R59c
Release:	5
License:	MirOS, BSD, ISC
Group:		Shells
URL:		https://www.mirbsd.org/mksh.htm
Source0:	https://www.mirbsd.org/MirOS/dist/mir/mksh/%{name}-%{version}.tgz
Source1:	https://www.mirbsd.org/TaC-mksh.txt
Source2:	https://www.mirbsd.org/pics/mksh.svg
Source3:	mkshrc
Source4:	dot-mkshrc
Patch0:		mksh-50e-no-tty-warning.patch
Patch1:		mksh-dont-barf-on-empty-HISTSIZE.patch
# For building docs
BuildRequires:	groff-base

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

CC="%{__cc}" CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}" sh Build.sh

%install
cp %{SOURCE1} .
install -D mksh %{buildroot}%{_bindir}/mksh
install -D mksh.1 %{buildroot}%{_mandir}/man1/mksh.1
install -D %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/mksh.svg
install -D -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/mkshrc
install -D -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/skel/.mkshrc

%if %{with bin_sh}
mkdir -p %{buildroot}/bin
ln -s %{_bindir}/mksh %{buildroot}/bin/sh
ln -s %{_bindir}/mksh %{buildroot}%{_bindir}/sh
%endif

# post is in lua so that we can run it without any external deps.  Helps
# for bootstrapping a new install.
# Jesse Keating 2009-01-29 (code from Ignacio Vazquez-Abrams)
# Roman Rakus 2011-11-07 (code from Sergey Romanov) #740611
%post -p <lua>
nl = '\n'
sh = '/bin/sh'..nl
bash = '/usr/bin/mksh'..nl
f = io.open('/etc/shells', 'a+')
if f then
    local shells = nl..f:read('*all')..nl
    if not shells:find(nl..sh) then f:write(sh) end
    if not shells:find(nl..bash) then f:write(bash) end
    f:close()
end

%postun -p <lua>
-- Run it only if we are uninstalling
if arg[2] == 0
then
    t={}
    for line in io.lines("/etc/shells")
    do
	if line ~= "/usr/bin/mksh" and line ~= "/bin/sh"
	then
	    table.insert(t,line)
	end
    end

    f = io.open("/etc/shells", "w+")
    for n,line in pairs(t)
    do
	f:write(line.."\n")
    end
    f:close()
end

%files
%doc dot.mkshrc TaC-mksh.txt
%config(noreplace) %{_sysconfdir}/mkshrc
%config(noreplace) %{_sysconfdir}/skel/.mkshrc
%{_bindir}/mksh
%if %{with bin_sh}
/bin/sh
%{_bindir}/sh
%endif
%doc %{_mandir}/man1/mksh.1*
%{_datadir}/pixmaps/mksh.svg
