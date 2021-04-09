#!/usr/bin/tclsh

set arch "x86_64"
set base "rocksdb-6.16.4"
set fileurl "https://github.com/facebook/rocksdb/archive/v6.16.4.tar.gz"

set var [list wget $fileurl -O $base.tar.gz]
exec >@stdout 2>@stderr {*}$var

if {[file exists build]} {
    file delete -force build
}

file mkdir build/BUILD build/RPMS build/SOURCES build/SPECS build/SRPMS
file copy -force $base.tar.gz build/SOURCES
file copy -force build-db_bench.patch build/SOURCES
file copy -force gtest-pthread.patch build/SOURCES
file copy -force CMakeLists.txt.patch build/SOURCES

set buildit [list rpmbuild --target $arch --define "_topdir [pwd]/build" -bb rocksdb.spec]
exec >@stdout 2>@stderr {*}$buildit

# Remove our source code
file delete $base.tar.gz
