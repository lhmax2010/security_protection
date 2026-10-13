export LC_ALL=C
command -v ffmpeg
ls -l /usr/bin/ffmpeg /usr/lib/libav*.so* /usr/lib/gstreamer-1.0/*libav* 2>&1
find /usr/lib -maxdepth 3 \( -iname "*avcodec*" -o -iname "*avformat*" -o -iname "*avutil*" -o -iname "*ffmpeg*" -o -iname "*gstlibav*" \) -print
rpm -qa | grep -Ei "ffmpeg|libav|gstreamer.*(ffmpeg|libav)"
