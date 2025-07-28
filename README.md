# streamweaver
This is a utility that takes a MP4 and loops it. Serves it up as a stream to be consumed. It is useful for simulating media content that needs to be consumed via service.


## Goals

This is intended to be an educational exploration of what [mediamtx](https://github.com/bluenviron/mediamtx) actually does more or less functionally already.

## Open VLC

You can download Open VLC via this link [here](https://get.videolan.org/vlc/3.0.21/win32/vlc-3.0.21-win32.exe).


## Download Video

```
 yt-dlp -f 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/mp4'   -o kung_fu_clean.mp4 https://www.youtube.com/watch?v=xECx-42Wlho
 ```


## Running ffmpeg

```
ffmpeg -re -stream_loop -1 -i video/kung_fu_clean.mp4   -c copy -f rtsp rtsp://localhost:8554/stream
```

## Mediamtx

Install the server:
`make install-mediamtx`

```
paths:
  all:
    source: publisher
    sourceProtocol: tcp
```

Next, we run the server as follows:
`src/streamweaver/thirdparty/mediamtx/mediamtx src/streamweaver/thirdparty/mediamtx/mediamtx.yml`

## Run Program

The following is the default as follows: 

`/opt/streamweaver/venv/bin/python /opt/streamweaver/src/streamweaver/entrypoint.py`

The following is running a custom video: 

```
/opt/streamweaver/venv/bin/python /opt/streamweaver/src/streamweaver/entrypoint.py \
  --path /opt/streamweaver/video/dancing_space_seals.mp4 \
  --fps 25 \
  --width 1920 \
  --height 1080 \
  --rtsp-url rtsp://127.0.0.1:8554/custom-ai
```




## Creating debian package

First, make sure there are no build artifacts as follows:
```
rm -rf debian/streamweaver
rm -rf debian/.debhelper
rm -f debian/files debian/debhelper-build-stamp
```

Second, you can do the following:
```
dpkg-buildpackage -us -uc
```

Third, you can confirm it is running with the following command:
```
 sudo systemctl status streamweaver-mediamtx.service
```

## Install debian package

```
sudo dpkg -i streamweaver_1.0.0_all.deb 

```

## Uninstall debian package

The manual uninstallation process is rather straight forward:

```
sudo dpkg -r streamweaver
sudo dpkg --purge streamweaver
rm -rf debian/streamweaver debian/.debhelper debian/files debian/debhelper-build-stamp
```

## Debugging the service file 

Please navigate here: 
`/usr/lib/systemd/system/streamweaver.service`

Make changes to this file and then run: 

```
sudo systemctl daemon-reload
sudo systemctl restart streamweaver
sudo systemctl status streamweaver
```

## Run the video for simulation 
/opt/streamweaver/venv/bin/python /opt/streamweaver/src/streamweaver/entrypoint.py



Finally,

## TO DO


```
#!/bin/bash
echo "Restarting streamweaver service..."
sudo systemctl restart streamweaver
echo "Service status:"
sudo systemctl status --no-pager --full streamweaver
echo "Recent logs:"
sudo journalctl -u streamweaver --no-pager -n 30#!/bin/bash
echo "Restarting streamweaver service..."
sudo systemctl restart streamweaver
echo "Service status:"
sudo systemctl status --no-pager --full streamweaver
echo "Recent logs:"
sudo journalctl -u streamweaver --no-pager -n 30
```

- Remove ability to stand up mtx automatically in debian
- Spin up mtx (if it doesn't already existt) with ffmpeg and be able to set the port

## Reference

- [Writing gstream plugin](https://medium.com/@jasonlife/writing-gstreamer-plugin-with-python-b98627cd24c1)
- [RTSP Loop](https://stackoverflow.com/questions/25648337/using-vlc-to-host-a-stream-of-an-infinite-video-loop)
- [RTSP Loop II](https://stackoverflow.com/questions/63129603/making-gstreamer-video-audio-in-python-smooth-and-loop)
- [RTSP Loop III](https://stackoverflow.com/questions/53747278/seamless-video-loop-in-gstreamer?rq=3)


## Technical References 
- [Packaing Tutorial](https://www.debian.org/doc/manuals/packaging-tutorial/packaging-tutorial)
- [Ultimate Packaging Tutorial](https://dario.griffo.io/posts/ultimate-guide-debian-packaging/)
- []