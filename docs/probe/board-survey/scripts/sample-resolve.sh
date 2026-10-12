#!/bin/sh
export LC_ALL=C
printf 'SAMPLE	bash	/usr/bin/bash
'
readlink -f /usr/bin/bash
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/bash
printf 'SAMPLE	systemctl	/usr/bin/systemctl
'
readlink -f /usr/bin/systemctl
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/systemctl
printf 'SAMPLE	dbus_daemon	/usr/bin/dbus-daemon
'
readlink -f /usr/bin/dbus-daemon
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/dbus-daemon
printf 'SAMPLE	connmand	/usr/bin/connmand
'
readlink -f /usr/bin/connmand
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/connmand
printf 'SAMPLE	dlogutil	/usr/bin/dlogutil
'
readlink -f /usr/bin/dlogutil
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/dlogutil
printf 'SAMPLE	cynara	/usr/bin/cynara
'
readlink -f /usr/bin/cynara
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/cynara
printf 'SAMPLE	security_manager	/usr/bin/security-manager
'
readlink -f /usr/bin/security-manager
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/security-manager
printf 'SAMPLE	pkgmgr_server	/usr/bin/pkgmgr-server
'
readlink -f /usr/bin/pkgmgr-server
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/pkgmgr-server
printf 'SAMPLE	vconftool	/usr/bin/vconftool
'
readlink -f /usr/bin/vconftool
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/vconftool
printf 'SAMPLE	sqlite3	/usr/bin/sqlite3
'
readlink -f /usr/bin/sqlite3
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/sqlite3
printf 'SAMPLE	rpm	/usr/bin/rpm
'
readlink -f /usr/bin/rpm
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/rpm
printf 'SAMPLE	find	/usr/bin/find
'
readlink -f /usr/bin/find
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/bin/find
printf 'SAMPLE	libc_so_6	/usr/lib/libc.so.6
'
readlink -f /usr/lib/libc.so.6
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libc.so.6
printf 'SAMPLE	libstdc++_so_6	/usr/lib/libstdc++.so.6
'
readlink -f /usr/lib/libstdc++.so.6
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libstdc++.so.6
printf 'SAMPLE	libsystemd_so_0	/usr/lib/libsystemd.so.0
'
readlink -f /usr/lib/libsystemd.so.0
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libsystemd.so.0
printf 'SAMPLE	libglib_2_0_so_0	/usr/lib/libglib-2.0.so.0
'
readlink -f /usr/lib/libglib-2.0.so.0
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libglib-2.0.so.0
printf 'SAMPLE	libdbus_1_so_3	/usr/lib/libdbus-1.so.3
'
readlink -f /usr/lib/libdbus-1.so.3
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libdbus-1.so.3
printf 'SAMPLE	libcrypto_so_3	/usr/lib/libcrypto.so.3
'
readlink -f /usr/lib/libcrypto.so.3
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libcrypto.so.3
printf 'SAMPLE	libssl_so_3	/usr/lib/libssl.so.3
'
readlink -f /usr/lib/libssl.so.3
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libssl.so.3
printf 'SAMPLE	libsqlite3_so_0	/usr/lib/libsqlite3.so.0
'
readlink -f /usr/lib/libsqlite3.so.0
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libsqlite3.so.0
printf 'SAMPLE	libdlog_so_0	/usr/lib/libdlog.so.0
'
readlink -f /usr/lib/libdlog.so.0
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libdlog.so.0
printf 'SAMPLE	libcynara_client_so_0	/usr/lib/libcynara-client.so.0
'
readlink -f /usr/lib/libcynara-client.so.0
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libcynara-client.so.0
printf 'SAMPLE	libcynara_admin_so_0	/usr/lib/libcynara-admin.so.0
'
readlink -f /usr/lib/libcynara-admin.so.0
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libcynara-admin.so.0
printf 'SAMPLE	libsecurity_manager_client_so_3	/usr/lib/libsecurity-manager-client.so.3
'
readlink -f /usr/lib/libsecurity-manager-client.so.3
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libsecurity-manager-client.so.3
printf 'SAMPLE	libnetwork_so_0	/usr/lib/libnetwork.so.0
'
readlink -f /usr/lib/libnetwork.so.0
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libnetwork.so.0
printf 'SAMPLE	libpkgmgr_client_so_0	/usr/lib/libpkgmgr-client.so.0
'
readlink -f /usr/lib/libpkgmgr-client.so.0
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libpkgmgr-client.so.0
printf 'SAMPLE	libpkgmgr_info_so_0	/usr/lib/libpkgmgr-info.so.0
'
readlink -f /usr/lib/libpkgmgr-info.so.0
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libpkgmgr-info.so.0
printf 'SAMPLE	libvconf_so_0	/usr/lib/libvconf.so.0
'
readlink -f /usr/lib/libvconf.so.0
stat -Lc 'device=%d inode=%i bytes=%s mode=%a type=%F' /usr/lib/libvconf.so.0
