Summary:	Library for reading and writing sound files
Name:		libsndfile
Version:	1.2.2
Release:	1.20241203222528837886.master%{?dist}
License:	LGPL-2.1-or-later AND GPL-2.0-or-later AND BSD-3-Clause
URL:		http://libsndfile.github.io/libsndfile/
Source0:        libsndfile-1.2.2.tar.gz
Patch0:		libsndfile-1.0.25-system-gsm.patch
%if %{undefined rhel}
# used to regenerate test .c sources from .def files
BuildRequires:  autogen
%endif
BuildRequires:  gcc-c++
BuildRequires:	alsa-lib-devel
BuildRequires:	flac-devel
BuildRequires:	gcc
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
BuildRequires:	sqlite-devel
BuildRequires:	gsm-devel
BuildRequires:	libtool
BuildRequires:	make
BuildRequires:	python3
BuildRequires:  opus-devel
BuildRequires:  lame-devel
BuildRequires:  mpg123-devel


%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface. It can
currently read/write 8, 16, 24 and 32-bit PCM files as well as 32 and
64-bit floating point WAV files and a number of compressed formats. It
compiles and runs on *nix, MacOS, and Win32.


%package devel
Summary:	Development files for libsndfile
Requires:	%{name}%{?_isa} = %{version}-%{release} pkgconfig


%description devel
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface.
This package contains files needed to develop with libsndfile.


%package utils
Summary:	Command Line Utilities for libsndfile
Requires:	%{name} = %{version}-%{release}


%description utils
libsndfile is a C library for reading and writing sound files such as
AIFF, AU, WAV, and others through one standard interface.
This package contains command line utilities for libsndfile.


%prep
%setup -q -n libsndfile-1.2.2
%patch -P0 -p1 -b .system-gsm
rm -r src/GSM610

%build
autoreconf -I M4 -fiv # for system-gsm patch
%configure \
	--disable-dependency-tracking \
	--enable-sqlite \
	--enable-alsa \
	--enable-largefile \
	--enable-mpeg \
	--disable-static

# Get rid of rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install
rm -rf __docs
mkdir __docs
cp -pR $RPM_BUILD_ROOT%{_docdir}/%{name}/* __docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}
find %{buildroot} -type f -name "*.la" -delete

# fix multilib issues
mv %{buildroot}%{_includedir}/sndfile.h \
   %{buildroot}%{_includedir}/sndfile-%{__isa_bits}.h

cat > %{buildroot}%{_includedir}/sndfile.h <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "sndfile-32.h"
#elif __WORDSIZE == 64
# include "sndfile-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif
EOF

%if 0%{?rhel} != 0
rm -f %{buildroot}%{_bindir}/sndfile-jackplay
%endif


%check
LD_LIBRARY_PATH=$PWD/src/.libs make check


%ldconfig_scriptlets


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
# NEWS files is missing in 1.1.0, check if it was re-added
%doc AUTHORS README
%{_libdir}/%{name}.so.1{,.*}

%files utils
%{_bindir}/sndfile-cmp
%{_bindir}/sndfile-concat
%{_bindir}/sndfile-convert
%{_bindir}/sndfile-deinterleave
%{_bindir}/sndfile-info
%{_bindir}/sndfile-interleave
%{_bindir}/sndfile-metadata-get
%{_bindir}/sndfile-metadata-set
%{_bindir}/sndfile-play
%{_bindir}/sndfile-salvage
%{_mandir}/man1/sndfile-cmp.1*
%{_mandir}/man1/sndfile-concat.1*
%{_mandir}/man1/sndfile-convert.1*
%{_mandir}/man1/sndfile-deinterleave.1*
%{_mandir}/man1/sndfile-info.1*
%{_mandir}/man1/sndfile-interleave.1*
%{_mandir}/man1/sndfile-metadata-get.1*
%{_mandir}/man1/sndfile-metadata-set.1*
%{_mandir}/man1/sndfile-play.1*
%{_mandir}/man1/sndfile-salvage.1*

%files devel
%doc __docs ChangeLog
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_includedir}/sndfile-%{__isa_bits}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/sndfile.pc


%changelog
* Tue Dec 3 2024 Michal Hlavinka <mhlavink@redhat.com> - 1.2.2-1.20241203222528837886.master
- Development snapshot (0d3f80b7)

* Tue Dec 3 2024 Michal Hlavinka <mhlavink@redhat.com> - 1.2.2-1.20241203221921481484.master
- Development snapshot (0d3f80b7)


