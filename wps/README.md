不想在系统里安装微软雅黑、宋体等俗套的 Windows 字体，否则很多在 CSS 中写死了此类字体的网页会展示对应的俗套字体，而不是跟随系统字体，然而，用 WPS 打开文档时还需要用到宋体、雅黑等，故诞生此需求。

### wps_wrapper.sh

源码。

在 /usr/share/fonts/ms 中放置 Windows 俗套字体，程序启动时会用 bwrap 建立沙盒，在 ~/.fonts/ms-tmp 建立 tmpfs 并把字体放置其中，只对 WPS 程序生效。之后，启动真正的 WPS（/usr/bin/wps.bak）。

### wps.hook

pacman hook。

把 wps wpp et wpspdf 全部重命名加上 .bak 后缀，然后用上文 wrapper 脚本取代之。

应该有更好的解决方案，但这个够用。

### wps-no-cloudsvr.hook

扬了 EverythingDaemon 和 wpscloudsvr。

我不使用 WPS 云服务，驻留进程实再碍眼，故诞生此需求。