yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' -o 'video/clip.%(ext)s' https://www.youtube.com/watch?v=xECx-42Wlho

ffmpeg -i video/clip.mp4 -c:v libx264 -preset fast -pix_fmt yuv420p -r 30 -c:a aac -b:a 128k -movflags +faststart video/clean_clip.mp4
