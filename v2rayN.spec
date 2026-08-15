%global debug_package %{nil}
%undefine _debuginfo_subpackages
%undefine _debugsource_packages
%global __requires_exclude ^liblttng-ust\\.so\\..*$

Name:           v2rayN
Version:        7.24.7
Release:        1%{?dist}
Summary:        v2rayN (Avalonia) GUI client for Linux
License:        GPL-3.0-only
URL:            https://github.com/2dust/v2rayN
BugURL:         https://github.com/2dust/v2rayN/issues
ExclusiveArch: aarch64 x86_64 riscv64

Source0:        https://github.com/autorepobot/v2rayN-SIG/archive/refs/tags/%{version}.tar.gz
Source1:        https://github.com/2dust/GlobalHotKeys/archive/refs/heads/master.tar.gz
Source2:        https://github.com/autorepobot/v2rayN-SIG-Nuget/releases/download/%{version}/nuget-cache.tar.gz

%ifarch riscv64
Source5:        https://github.com/xujiegb/dotnet-riscv/releases/download/10.0.111/dotnet-sdk-10.0.111-linux-riscv64.tar.gz
%endif

# Source10:      https://github.com/XTLS/Xray-core/releases/download/v26.7.28/Xray-linux-64.zip
# Source11:      https://github.com/XTLS/Xray-core/releases/download/v26.7.28/Xray-linux-arm64-v8a.zip
Source12:      https://github.com/SagerNet/sing-box/releases/download/v1.13.18/sing-box-1.13.18-linux-amd64.tar.gz
Source13:      https://github.com/SagerNet/sing-box/releases/download/v1.13.18/sing-box-1.13.18-linux-arm64.tar.gz
# Source14:      https://github.com/XTLS/Xray-core/releases/download/v26.7.28/Xray-linux-riscv64.zip
Source15:      https://github.com/SagerNet/sing-box/releases/download/v1.13.18/sing-box-1.13.18-linux-riscv64.tar.gz

Source20:      https://github.com/Loyalsoldier/V2ray-rules-dat/releases/latest/download/geosite.dat
Source21:      https://github.com/Loyalsoldier/V2ray-rules-dat/releases/latest/download/geoip.dat
Source22:      https://raw.githubusercontent.com/Loyalsoldier/geoip/release/geoip-only-cn-private.dat
Source23:      https://raw.githubusercontent.com/Loyalsoldier/geoip/release/Country.mmdb
Source24:      https://github.com/MetaCubeX/meta-rules-dat/releases/latest/download/geoip.metadb

Source30:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-private.srs
Source31:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-cn.srs
Source32:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-facebook.srs
Source33:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-fastly.srs
Source34:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-google.srs
Source35:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-netflix.srs
Source36:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-telegram.srs
Source37:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geoip/geoip-twitter.srs

Source40:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-cn.srs
Source41:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-gfw.srs
Source42:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-google.srs
Source43:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-greatfire.srs
Source44:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-geolocation-cn.srs
Source45:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-category-ads-all.srs
Source46:      https://raw.githubusercontent.com/2dust/sing-box-rules/refs/heads/rule-set-geosite/geosite-private.srs

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

tar -xzf %{SOURCE2}

%build
%ifarch x86_64
%global dotnet_rid linux-x64
%endif
%ifarch aarch64
%global dotnet_rid linux-arm64
%endif
%ifarch riscv64
%global dotnet_rid linux-riscv64
mkdir -p %{_builddir}/dotnet_riscv
tar -C %{_builddir}/dotnet_riscv -xzf %{SOURCE5}
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

find %{buildroot}/opt/v2rayN -type d -exec chmod 0755 {} +
find %{buildroot}/opt/v2rayN -type f -exec chmod 0644 {} +
[ -f %{buildroot}/opt/v2rayN/v2rayN ] && chmod 0755 %{buildroot}/opt/v2rayN/v2rayN || :

# install -dm0755 %{buildroot}/opt/v2rayN/bin/xray
install -dm0755 %{buildroot}/opt/v2rayN/bin/sing_box
install -dm0755 %{buildroot}/opt/v2rayN/bin/srss

# mkdir -p %{_builddir}/tmp_xray
# %ifarch x86_64
# unzip -q %{SOURCE10} -d %{_builddir}/tmp_xray
# %endif
# %ifarch aarch64
# unzip -q %{SOURCE11} -d %{_builddir}/tmp_xray
# %endif
# %ifarch riscv64
# unzip -q %{SOURCE14} -d %{_builddir}/tmp_xray
# %endif
# install -m 0755 %{_builddir}/tmp_xray/xray %{buildroot}/opt/v2rayN/bin/xray/xray

mkdir -p %{_builddir}/tmp_singbox
%ifarch x86_64
tar -xzf %{SOURCE12} -C %{_builddir}/tmp_singbox
%endif
%ifarch aarch64
tar -xzf %{SOURCE13} -C %{_builddir}/tmp_singbox
%endif
%ifarch riscv64
tar -xzf %{SOURCE15} -C %{_builddir}/tmp_singbox
%endif
SINGBOX_BIN=$(find %{_builddir}/tmp_singbox -type f -name 'sing-box' | head -n1)
install -m 0755 "$SINGBOX_BIN" %{buildroot}/opt/v2rayN/bin/sing_box/sing-box
CRONET_LIB=$(find %{_builddir}/tmp_singbox -type f -name 'libcronet*.so*' | head -n1 || true)
[ -n "$CRONET_LIB" ] && install -m 0644 "$CRONET_LIB" %{buildroot}/opt/v2rayN/bin/sing_box/libcronet.so || true

install -m 0644 %{SOURCE20} %{buildroot}/opt/v2rayN/bin/geosite.dat
install -m 0644 %{SOURCE21} %{buildroot}/opt/v2rayN/bin/geoip.dat
install -m 0644 %{SOURCE22} %{buildroot}/opt/v2rayN/bin/geoip-only-cn-private.dat
install -m 0644 %{SOURCE23} %{buildroot}/opt/v2rayN/bin/Country.mmdb
install -m 0644 %{SOURCE24} %{buildroot}/opt/v2rayN/bin/geoip.metadb

install -m 0644 %{SOURCE30} %{SOURCE31} %{SOURCE32} %{SOURCE33} %{SOURCE34} %{SOURCE35} %{SOURCE36} %{SOURCE37} \
                %{SOURCE40} %{SOURCE41} %{SOURCE42} %{SOURCE43} %{SOURCE44} %{SOURCE45} %{SOURCE46} \
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
* Sat Aug 15 2026 Build Bot <repobot@local> - 7.24.7-1
- Add riscv64 architecture support and dotnet-sdk-10.0.111-linux-riscv64 source
