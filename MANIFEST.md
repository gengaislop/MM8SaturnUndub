# Patch Manifest — v1.1.0

This file documents *exactly* which game data the v1.1.0 undub patch substitutes, so the patch can be independently reviewed, reproduced, and verified.

The patch does not include any of Capcom's data itself. Reproducing the build requires that you legitimately own a dump of both the USA and the JP discs, extract their data layers (ISO 9660 file trees), perform the substitutions listed below, and re-pack to a Mode 1 / 2352 BIN.

## Base disc

- USA disc (`Mega Man 8 (USA)`, Redump-matched) — provides the executable, all graphics, all text, the title-screen logo, all UI/menu data, and the original Track 2 redbook audio.

## Substitutions

### Full file swaps (USA disc file ← JP disc file)

All **46** of these are byte-for-byte copies of the JP disc's same-named file, overwriting the USA disc's version:

```
ASCII.DOT
BLS00.PAC   BLS01.PAC
BS01B.PAC   BS01C.PAC
BS02B.PAC   BS02C.PAC
BS03B.PAC   BS03C.PAC
BS04B.PAC   BS04C.PAC
BS05B.PAC   BS05C.PAC
BS06B.PAC   BS06C.PAC
BS07B.PAC   BS07C.PAC
BS08B.PAC   BS08C.PAC
BS10B.PAC   BS10C.PAC
CLR00.PAC   CLR01.PAC   CLR02.PAC   CLR03.PAC
CLR04.PAC   CLR05.PAC   CLR06.PAC   CLR07.PAC
COMMON.PAC
CUT1.PAC    CUT2.PAC
DUO00.PAC   DUO01.PAC
FORTE1.PAC  FORTE2.PAC
LABO_.PAC
ST00A.PAC   ST00C.PAC
ST01A.PAC
ST03A.PAC
ST09A.PAC
ST10A.PAC
STBOS.PAC
STSEL.PAC
TITLE_.PAC
WILY1.PAC   WILY2B.PAC  WILY3B.PAC
WOOD1.PAC   WOOD2.PAC
```

### Surgical FMV transformations

- **`ROCK8_0.CPK`** (opening cinematic): not a full swap. The USA file is parsed as a Sega FILM/Cinepak container, and the FILM's audio samples (and only the audio samples) are replaced by those from the JP version, with a 3-slot audio offset to compensate for the silence intro on the USA reel. The result keeps USA visuals byte-for-byte and adds JP voice. The exact algorithm is in the included `splice_film_audio_only.py`.

- **`ROCK8_1.CPK`, `ROCK8_2.CPK`, `ROCK8_3.CPK`, `ROCK8_4.CPK`** (in-game cinematics): built fresh from the JP source video with **English subtitles burned into the Cinepak frames**. The translation text is from [Hondoori](https://hondoori.wordpress.com/), provided in ASS format. The audio is byte-identical to the JP source — re-spliced after the video re-encode so no audio quality is lost. See the "FMV subtitle pipeline" section below for the full reproduction procedure.

### USA files explicitly kept (not swapped)

These files were deliberately retained from the USA disc because they hold UI, text-rendering, animation, or executable data that the USA build expects:

```
1STREAD.PRG   2NDREAD.PRG          (Saturn executables)
LABO.PAC      SLABO.PAC            (title-screen logo, menus, Bonus Mode UI)
STAGE00.PAC                        (in-game dialogue text pointer tables)
GETDEMO.PAC                        (weapon-get screen UI/animation data)
WARNING1.BG   WARNING2.BG          (boot warnings)
WARNING3.BG   WARNING4.BG
GETDEMO.PAC                        (weapon-get screen — fixed in v1.0.1, kept US to fix small logo glitch)
All BG / map / palette files not listed in the swap set above.
```

## FMV subtitle pipeline

For each `ROCK8_N.CPK` (N = 1, 2, 3, 4):

1. Render uncompressed AVI with subtitles burned in via ffmpeg + libass:
   `ffmpeg -i jp_cpk/ROCK8_N.CPK -vf "subtitles=ROCK8_N.ass:force_style='FontName=Arial,Bold=1,FontSize=18,Outline=2'" -c:v rawvideo -pix_fmt bgr24 -r 15 -c:a pcm_s16le -ar 22050 -ac 1 ROCK8_N_subtitled.avi`

2. Apply Cinepak compression in **VirtualDub2** (32-bit) running on Windows with the **1995 Radius `iccvid.dll`** codec installed. Settings: Cinepak Codec by Radius, Quality 100, target data rate 200 KB/s, force keyframes every 8 frames, audio direct stream copy, video full processing mode. Output as new AVI.

3. Remux AVI → MOV with ffmpeg (no re-encode):
   `ffmpeg -i ROCK8_N_cinepak.avi -c copy -movflags +faststart -f mov ROCK8_N_cinepak.mov`

4. Convert MOV → Saturn FILM via `MovieToSaturn` from TrekkiesUnite118's [SegaSaturnFilmTools](https://github.com/TrekkiesUnite118/SegaSaturnFilmMuxer) 3.0.1, with byte-identical audio swap from the original JP CPK:
   `java -cp SegaSaturnFilmTools.jar MakeFilm ROCK8_N_cinepak.mov jp_ROCK8_N.CPK ROCK8_N_final.CPK`

5. Normalize the FILM header to JP-Saturn-compatible timing: version `1.06`, framerate `30`, video frame duration `2`, timestamp increment `2` per frame.

6. Patch the FDSC chunk (audio format declaration) byte-identical to the JP source's, so the audio chunks we spliced in are correctly described to the decoder.

7. Pad to JP-original byte size with trailing zeros so subsequent files on the disc don't shift LBA.

The technical reason this exact pipeline is required (not simpler ones): MM8's Saturn decoder rejects FFmpeg-generated Cinepak. The Windows-side VirtualDub2 + Radius codec is the only encoder that produces byte sequences MM8 will accept, and FILM Tools is the only muxer that writes a STAB chunk MM8 will accept. See the project's reference documentation for the full investigation log if interested.

## Reproducing the patch from scratch

1. Extract the ISO 9660 file system from both `Mega Man 8 (USA) (Track 1).bin` and `Rockman 8 - Metal Heroes (Japan) (Track 1).bin` (each is MODE1/2352; strip the 16-byte sync header and 288-byte ECC trailer from every sector to get the 2048-byte payload).
2. Start from the USA file tree.
3. Overwrite each file listed under **Full file swaps** with the same-named file from the JP tree.
4. Run `splice_film_audio_only.py us_ROCK8_0.CPK jp_ROCK8_0.CPK ROCK8_0.CPK 3` and place the result at `ROCK8_0.CPK`.
5. For each `ROCK8_N.CPK` (N = 1, 2, 3, 4), run the **FMV subtitle pipeline** above using the appropriate subtitles.
6. Re-pack as ISO 9660 (`genisoimage -no-pad -iso-level 1 -sysid "SEGA SEGASATURN" -V MEGA_MAN_8`), splice the original USA IP.BIN (first 32 KB) back over the head of the ISO, then re-encode as MODE1/2352 with proper EDC/ECC bytes per sector.
7. Diff the result against the original USA Track 1 with `xdelta3 -e -9 -B 536870912` to produce the distributable patch.

## Verification

Anyone who applies the patch can re-extract the resulting `.bin`'s ISO contents and confirm that the files listed above match the JP disc bytes (full swaps), that `ROCK8_0.CPK` matches the splice tool's deterministic output, that `ROCK8_1`–`ROCK8_4` decode to videos with the documented Arial Bold 18 / 2-px outline subtitles overlaid (using the provided ASS files), and that every other byte of the data layer matches the USA disc.
