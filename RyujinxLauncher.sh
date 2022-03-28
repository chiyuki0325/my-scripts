#!/bin/bash
#Ryujinx launcher script by YidaozhanYa
ryujinx_dir="/opt/ryujinx"
nvidia_tmp=$(lspci | grep VGA | grep NVIDIA)
intel_tmp=$(lspci | grep VGA | grep Intel)

common_prefix="env GDK_BACKEND=x11 "
gpu_prefix=""
optimus_prefix=""
gamemode_prefix=""

if [ -f "/usr/bin/gamemoderun" ];then
    gamemode_prefix="gamemoderun "
fi

if [[ $nvidia_tmp != "" ]] && [[ $intel_tmp != "" ]]; then
    #Optimus
    if [ -f "/usr/bin/prime-run" ];then
        optimus_prefix="prime-run "
        gpu_prefix="__GL_THREADED_OPTIMIZATIONS=0 __GL_SYNC_TO_VBLANK=0 "
    fi
elif [[ $nvidia_tmp != "" ]]; then
    #NVIDIA Only
    gpu_prefix="__GL_THREADED_OPTIMIZATIONS=0 __GL_SYNC_TO_VBLANK=0 "
else
    #Mesa
    gpu_prefix="AMD_DEBUG=w32ge,w32cs,nohyperz,nofmask glsl_zero_init=true radeonsi_clamp_div_by_zero=true force_integer_tex_nearest=true mesa_glthread=false vblank_mode=0 "
fi

if [ -d "$ryujinx_dir" ]; then
    if [ -f "$ryujinx_dir/Ryujinx.Ava" ];then
        executable_name="Ryujinx.Ava"
        ava_prefix="LANG=C LC_ALL=C "
    else
        executable_name="Ryujinx"
        ava_prefix=""
    fi
else
    if [[ -f "/usr/bin/ryujinx" ]];then
        ryujinx_dir="/usr/bin"
        executable_name="ryujinx"
    fi
    if [[ -f "/usr/bin/Ryujinx" ]];then
        ryujinx_dir="/usr/bin"
        executable_name="Ryujinx"
    fi
    ava_tmp=""
    ava_tmp=$(ls -l /usr/bin | grep Ryujinx.Ava)
    if [ "$ava_tmp" != "" ];then
        ava_prefix="LANG=C LC_ALL=C "
    else
        ava_prefix=""
    fi
fi

if [ ! -f "$HOME/.config/gamemode.ini" ];then
cat << EOF > "$HOME/.config/gamemode.ini"
[general]
reaper_freq=5
desiredgov=performance
igpu_desiredgov=performance
igpu_power_threshold=-1
softrealtime=off
renice=20
ioprio=0
inhibit_screensaver=1
[filter]
[gpu]
apply_gpu_optimisations=accept-responsibility
gpu_device=0
nv_powermizer_mode=1
;nv_core_clock_mhz_offset=200
;nv_mem_clock_mhz_offset=200
amd_performance_level=high
[supervisor]
[custom]
start=qdbus org.kde.KWin /Compositor org.kde.kwin.Compositing.suspend
end=qdbus org.kde.KWin /Compositor org.kde.kwin.Compositing.resume
EOF
echo "gamemode profile loaded!"
fi

final_command="${common_prefix}${ava_prefix}${gpu_prefix}${gamemode_prefix}${optimus_prefix}\"${ryujinx_dir}/${executable_name}\""
echo "$final_command"
eval "$final_command"
