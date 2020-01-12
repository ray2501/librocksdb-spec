#
# spec file for package rocksdb
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define _toolsdir %{_libexecdir}/%{name}

%if 0%{?suse_version} >= 1510 || 0%{?sle_version} >= 150100
%bcond_without librados
%bcond_without gflags
%else
%bcond_with    librados
%bcond_with    gflags
%endif

Name:           rocksdb
Version:        6.5.3
Release:        0
Summary:        An embeddable, persistent key-value store for fast storage
License:        Apache-2.0 AND GPL-2.0-only
Group:          System/Libraries
URL:            http://rocksdb.org/
Source:         rocksdb-%{version}.tar.gz
Source99:       series
Patch1:         gtest-pthread.patch
Patch2:         build-db_bench.patch
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libnuma-devel
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  tbb-devel
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(jemalloc)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(zlib)
%if %{with gflags}
BuildRequires:  gflags-devel-static
BuildRequires:  pkgconfig(gflags)
%endif
%if %{with librados}
BuildRequires:  libradospp-devel
%endif
%if 0%{?suse_version} >= 1550
BuildRequires:  pkgconfig(snappy)
%else
BuildRequires:  snappy-devel
%endif

%description
RocksDB is a high performance embedded database for key-value data.
It is a fork of LevelDB which was then optimized to exploit many
central processing unit (CPU) cores, and make efficient use of fast
storage, such as solid-state drives (SSD), for input/output (I/O)
bound workloads. It is based on a log-structured merge-tree (LSM tree)
data structure.

%define lib_name librocksdb6

%package -n %{lib_name}
Summary:        Shared library from rocksdb
Group:          System/Libraries
Provides:       %{name} = %{version}
Obsoletes:      %{name} < %{version}

%description -n %{lib_name}
RocksDB is a high performance embedded database for key-value data.
It is a fork of LevelDB which was then optimized to exploit many
central processing unit (CPU) cores, and make efficient use of fast
storage, such as solid-state drives (SSD), for input/output (I/O)
bound workloads. It is based on a log-structured merge-tree (LSM tree)
data structure.

This package holds the shared library of rocksdb.

%package devel
Summary:        Development package for RocksDB
Group:          Development/Libraries/C and C++
Requires:       %{lib_name} = %{version}

%description devel
RocksDB is a high performance embedded database for key-value data.
It is a fork of LevelDB which was then optimized to exploit many
central processing unit (CPU) cores, and make efficient use of fast
storage, such as solid-state drives (SSD), for input/output (I/O)
bound workloads. It is based on a log-structured merge-tree (LSM tree)
data structure.

This package contains the files needed to compile programs that use
the RocksDB library.

%package devel-static
Summary:        Development files for statically link RocksDB
Group:          Development/Libraries/C and C++
Requires:       %{name}-devel = %{version}

%description devel-static
RocksDB is a high performance embedded database for key-value data.
It is a fork of LevelDB which was then optimized to exploit many
central processing unit (CPU) cores, and make efficient use of fast
storage, such as solid-state drives (SSD), for input/output (I/O)
bound workloads. It is based on a log-structured merge-tree (LSM tree)
data structure.

This package holds the development files for statically linking RocksDB.

%prep
%autosetup -n rocksdb-%{version} -p1

%build
%cmake                         \
 -DFAIL_ON_WARNINGS:BOOL=OFF   \
%if %{with asan}
 -DWITH_ASAN:BOOL=OFF          \
 -DWITH_TSAN:BOOL=OFF          \
 -DWITH_UBSAN:BOOL=OFF         \
%endif
 -DPORTABLE:BOOL=ON            \
 -DWITH_BZ2:BOOL=ON            \
 -DWITH_FALLOCATE:BOOL=ON      \
 %if %{with gflags}
 -DWITH_GFLAGS:BOOL=ON         \
 %endif
 -DWITH_JEMALLOC:BOOL=ON       \
 -DWITH_JNI:BOOL=OFF           \
 %if %{with librados}
 -DWITH_LIBRADOS:BOOL=ON       \
 %endif
 -DWITH_LZ4:BOOL=ON            \
 -DWITH_NUMA:BOOL=ON           \
 -DWITH_SNAPPY:BOOL=ON         \
 -DWITH_TBB:BOOL=ON            \
 -DWITH_TESTS:BOOL=OFF         \
 -DWITH_TOOLS:BOOL=ON          \
 -DWITH_ZLIB:BOOL=ON           \
 -DWITH_ZSTD:BOOL=ON

%make_jobs

%install
%cmake_install
pushd build/tools/
install -D -m 0755 -d %{buildroot}%{_toolsdir}
install -D -m 0755 \
    db_bench sst_dump rocksdb_undump rocksdb_dump ldb db_sanity_test write_stress db_repl_stress db_stress blob_dump \
  %{buildroot}%{_toolsdir}
popd

%post   -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files
%dir %{_toolsdir}
%{_toolsdir}/db_bench
%{_toolsdir}/db_repl_stress
%{_toolsdir}/db_sanity_test
%{_toolsdir}/db_stress
%{_toolsdir}/write_stress
%{_toolsdir}/ldb
%{_toolsdir}/sst_dump
%{_toolsdir}/rocksdb_dump
%{_toolsdir}/rocksdb_undump
%{_toolsdir}/blob_dump

%files -n %{lib_name}
%license COPYING LICENSE.Apache LICENSE.leveldb
%{_libdir}/librocksdb.so.*

%files devel
%license COPYING LICENSE.Apache LICENSE.leveldb
%doc README.md
%{_includedir}/rocksdb
%{_libdir}/librocksdb.so
%{_libdir}/cmake/rocksdb/

%files devel-static
%{_libdir}/librocksdb.a

%changelog

