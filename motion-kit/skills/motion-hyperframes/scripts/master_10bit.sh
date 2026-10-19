#!/usr/bin/env bash
# Master a lossless render (HyperFrames `render --format mov`, ProRes 4444) into a 10-bit H.264 delivery file
# with fine luma grain against banding, correct BT.709 tags and optional sound.
#
#   tools/master_10bit.sh master.mov film.mp4 [grain=0.35] [mix.wav]
#
# - Untagged input is treated as BT.601 (HyperFrames ProRes, issue #5380) and converted to BT.709; tagged input keeps its matrix.
# - Grain: zero-mean luma noise merged in 10 bit (0 = off, 0.35 = fine, 0.6 = visible film grain).
# - Warns when the MOV is transparent (background on <body> instead of the composition root -> black in MP4).
set -euo pipefail
in="${1:?master.mov}"; out="${2:?film.mp4}"; grain="${3:-0.35}"; audio="${4:-}"

alpha=$(ffmpeg -hide_banner -i "$in" -vf "alphaextract,format=gray,signalstats,metadata=print:key=lavfi.signalstats.YAVG" -frames:v 1 -f null - 2>&1 | sed -n 's/.*YAVG=\([0-9.]*\).*/\1/p' | head -1 || true)
if [ -n "$alpha" ] && awk "BEGIN{exit !($alpha < 250)}"; then
  echo "WARNUNG: erstes Bild ist teilweise transparent (Alpha-Mittel $alpha/255). Hintergrund auf das Root-Element [data-composition-id] legen, sonst wird es im MP4 schwarz. (Gewollte Overlays mit Alpha: MOV direkt liefern, nicht hiermit.)" >&2
fi

csp=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_space -of csv=p=0 "$in" | head -1)
case "$csp" in bt709) inm=bt709 ;; bt470bg|smpte170m|bt601) inm=bt601 ;; *) inm=bt601 ;; esac  # untagged = HyperFrames = BT.601
vf="[0:v]scale=in_color_matrix=$inm:out_color_matrix=bt709,format=yuv444p10le"
if awk "BEGIN{exit !($grain > 0)}"; then
  vf="$vf,split[a][b];[b]lutyuv=y=512:u=512:v=512,format=yuv420p,noise=c0s=14:c0f=t+u,format=yuv444p10le[n];[a][n]blend=c0_mode=grainmerge:c0_opacity=$grain:c1_mode=normal:c1_opacity=1:c2_mode=normal:c2_opacity=1"
fi
vf="$vf,format=yuv420p10le[v]"

args=(-v error -y -i "$in")
amap=(-map "0:a?")
if [ -n "$audio" ]; then args+=(-i "$audio"); amap=(-map 1:a:0 -shortest); fi
ffmpeg "${args[@]}" -filter_complex "$vf" -map "[v]" "${amap[@]}" \
  -c:v libx264 -preset slow -crf 14 -tune grain -profile:v high10 \
  -bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1 \
  -c:a aac -b:a 320k -movflags +faststart "$out"
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,color_space,r_frame_rate:format=duration -of compact "$out"
