%global debug_package %{nil}
%undefine _debuginfo_subpackages
%undefine _debugsource_packages
%global __requires_exclude ^liblttng-ust\\.so\\..*$

Name:           v2rayN
Version:        7.24.8
Release:        1%{?dist}
Summary:        v2rayN (Avalonia) GUI client for Linux
License:        GPL-3.0-only
URL:            https://github.com/2dust/v2rayN
BugURL:         https://github.com/2dust/v2rayN/issues
ExclusiveArch: aarch64 x86_64 riscv64 ppc64le

Source0:        https://github.com/autorepobot/v2rayN-SIG/archive/refs/tags/%{version}.tar.gz
Source1:        https://github.com/2dust/GlobalHotKeys/archive/refs/heads/master.tar.gz
Source2:        https://github.com/autorepobot/v2rayN-SIG-Nuget/releases/download/%{version}/nuget-cache.tar.xz

%ifarch riscv64
Source3:        https://github.com/xujiegb/dotnet-riscv/releases/download/10.0.111/dotnet-sdk-10.0.111-linux-riscv64.tar.gz
%endif

Source4:        https://github.com/SagerNet/sing-box/releases/download/v1.13.19/sing-box-1.13.19-linux-amd64.tar.gz
Source5:        https://github.com/SagerNet/sing-box/releases/download/v1.13.19/sing-box-1.13.19-linux-arm64.tar.gz
Source6:        https://github.com/SagerNet/sing-box/releases/download/v1.13.19/sing-box-1.13.19-linux-riscv64.tar.gz
Source7:        https://github.com/SagerNet/sing-box/releases/download/v1.13.19/sing-box-1.13.19-linux-ppc64le.tar.gz

Source8:        https://github.com/Loyalsoldier/V2ray-rules-dat/releases/latest/download/geosite.dat
Source9:        https://github.com/Loyalsoldier/V2ray-rules-dat/releases/latest/download/geoip.dat
Source10:       https://raw.githubusercontent.com/Loyalsoldier/geoip/release/geoip-only-cn-private.dat
Source11:       https://raw.githubusercontent.com/Loyalsoldier/geoip/release/Country.mmdb
Source12:       https://github.com/MetaCubeX/meta-rules-dat/releases/latest/download/geoip.metadb

Source13:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-private.srs
Source14:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-cn.srs
Source15:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-facebook.srs
Source16:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-fastly.srs
Source17:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-google.srs
Source18:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-netflix.srs
Source19:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-telegram.srs
Source20:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-twitter.srs

Source21:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-cn.srs
Source22:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-gfw.srs
Source23:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-google.srs
Source24:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-greatfire.srs
Source25:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-geolocation-cn.srs
Source26:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-category-ads-all.srs
Source27:       https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-private.srs

%ifnarch riscv64
BuildRequires: dotnet-sdk-10.0
%endif
BuildRequires: tar
BuildRequires: unzip

Requires:      cairo, pango, openssl, mesa-libEGL, mesa-libGL
Requires:      glibc >= 2.39
Requires:      fontconfig >= 2.15.0
Requires:      desktop-file-utils >= 0.26
Requires:      xdg-utils >= 1.1.3
Requires:      coreutils >= 9.4
Requires:      bash >= 5.2.21
Requires:      freetype >= 2.13

%description
v2rayN Linux for Red Hat Enterprise Linux
Support vless / vmess / Trojan / http / socks / Anytls / Hysteria2 / Shadowsocks / tuic / WireGuard
Support Red Hat Enterprise Linux / Fedora Linux / Rocky Linux / AlmaLinux / CentOS
For more information, Please visit our website
https://github.com/2dust/v2rayN

%prep
%setup -q -n v2rayN-SIG-%{version}

tar -xzf %{SOURCE1} -C v2rayN/
rm -rf v2rayN/GlobalHotKeys
mv v2rayN/GlobalHotKeys-* v2rayN/GlobalHotKeys

tar -xJf %{SOURCE2}

%build
%ifarch x86_64
%global dotnet_rid linux-x64
%endif
%ifarch aarch64
%global dotnet_rid linux-arm64
%endif
%ifarch ppc64le
%global dotnet_rid linux-ppc64le
%endif
%ifarch riscv64
%global dotnet_rid linux-riscv64
mkdir -p %{_builddir}/dotnet_riscv
tar -C %{_builddir}/dotnet_riscv -xzf %{SOURCE3}
export PATH="%{_builddir}/dotnet_riscv:$PATH"
export DOTNET_ROOT="%{_builddir}/dotnet_riscv"
%endif

dotnet restore v2rayN/v2rayN.Desktop/v2rayN.Desktop.csproj \
    -r %{dotnet_rid} \
    --packages $PWD/nuget-cache \
    --source $PWD/nuget-cache \
    -p:EnableWindowsTargeting=true

dotnet publish v2rayN/v2rayN.Desktop/v2rayN.Desktop.csproj \
    -c Release \
    -r %{dotnet_rid} \
    --no-restore \
    --packages $PWD/nuget-cache \
    -p:PublishSingleFile=false \
    -p:SelfContained=true \
    -o %{_builddir}/publish_output

%install
install -dm0755 %{buildroot}/opt/v2rayN
cp -a %{_builddir}/publish_output/. %{buildroot}/opt/v2rayN/
install -m 0644 v2rayN/v2rayN.Desktop/v2rayN.png %{buildroot}/opt/v2rayN/v2rayn.png

find %{buildroot}/opt/v2rayN -type d -exec chmod 0755 {} +
find %{buildroot}/opt/v2rayN -type f -exec chmod 0644 {} +
[ -f %{buildroot}/opt/v2rayN/v2rayN ] && chmod 0755 %{buildroot}/opt/v2rayN/v2rayN || :

install -dm0755 %{buildroot}/opt/v2rayN/bin/sing_box
install -dm0755 %{buildroot}/opt/v2rayN/bin/srss


mkdir -p %{_builddir}/tmp_singbox
%ifarch x86_64
tar -xzf %{SOURCE4} -C %{_builddir}/tmp_singbox
%endif
%ifarch aarch64
tar -xzf %{SOURCE5} -C %{_builddir}/tmp_singbox
%endif
%ifarch riscv64
tar -xzf %{SOURCE6} -C %{_builddir}/tmp_singbox
%endif
%ifarch ppc64le
tar -xzf %{SOURCE7} -C %{_builddir}/tmp_singbox
%endif
SINGBOX_BIN=$(find %{_builddir}/tmp_singbox -type f -name 'sing-box' | head -n1)
install -m 0755 "$SINGBOX_BIN" %{buildroot}/opt/v2rayN/bin/sing_box/sing-box
CRONET_LIB=$(find %{_builddir}/tmp_singbox -type f -name 'libcronet*.so*' | head -n1 || true)
[ -n "$CRONET_LIB" ] && install -m 0644 "$CRONET_LIB" %{buildroot}/opt/v2rayN/bin/sing_box/libcronet.so || true

install -m 0644 %{SOURCE8} %{buildroot}/opt/v2rayN/bin/geosite.dat
install -m 0644 %{SOURCE9} %{buildroot}/opt/v2rayN/bin/geoip.dat
install -m 0644 %{SOURCE10} %{buildroot}/opt/v2rayN/bin/geoip-only-cn-private.dat
install -m 0644 %{SOURCE11} %{buildroot}/opt/v2rayN/bin/Country.mmdb
install -m 0644 %{SOURCE12} %{buildroot}/opt/v2rayN/bin/geoip.metadb

install -m 0644 %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE17} %{SOURCE18} %{SOURCE19} %{SOURCE20}\
                %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27}\
                %{buildroot}/opt/v2rayN/bin/srss/

install -dm0755 %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -m0644 v2rayN/v2rayN.Desktop/v2rayN.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/v2rayn.png

install -dm0755 %{buildroot}%{_bindir}
cat << 'EOF' > %{buildroot}%{_bindir}/v2rayn
#!/usr/bin/bash
set -euo pipefail
DIR="/opt/v2rayN"

if [[ -x "$DIR/v2rayN" ]]; then exec "$DIR/v2rayN" "$@"; fi

for dll in v2rayN.Desktop.dll v2rayN.dll; do
  if [[ -f "$DIR/$dll" ]]; then exec /usr/bin/dotnet "$DIR/$dll" "$@"; fi
done

echo "v2rayN launcher: no executable found in $DIR" >&2
ls -l "$DIR" >&2 || true
exit 1
EOF
chmod 0755 %{buildroot}%{_bindir}/v2rayn

install -dm0755 %{buildroot}%{_datadir}/applications
cat << 'EOF' > %{buildroot}%{_datadir}/applications/v2rayn.desktop
[Desktop Entry]
Type=Application
Name=v2rayN
Comment=v2rayN for Red Hat Enterprise Linux
Exec=v2rayn
Icon=v2rayn
Terminal=false
Categories=Network;
EOF
chmod 0644 %{buildroot}%{_datadir}/applications/v2rayn.desktop

%post
/usr/bin/update-desktop-database %{_datadir}/applications >/dev/null 2>&1 || true
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor >/dev/null 2>&1 || true

%postun
/usr/bin/update-desktop-database %{_datadir}/applications >/dev/null 2>&1 || true
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor >/dev/null 2>&1 || true

%files
%{_bindir}/v2rayn
/opt/v2rayN
%{_datadir}/applications/v2rayn.desktop
%{_datadir}/icons/hicolor/256x256/apps/v2rayn.png

%changelog
* Sun Aug 23 2026 Build Bot <repobot@local> - 7.24.8-1
- Add riscv64 architecture support and dotnet-sdk-10.0.111-linux-riscv64 source
