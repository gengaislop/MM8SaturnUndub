# MM8 Saturn Undub

A fan-made undub patch that swaps the English dub in *Mega Man 8* (Sega Saturn, USA release) with the original Japanese audio from *Rockman 8: Metal Heroes*, and adds **English subtitles** to the four full-motion cinematics. The English menu text, graphics, and title logo are preserved from the USA release.

Distributed as an **xdelta3 binary diff**. No game data is included — you supply your own legitimately-acquired copy of the USA disc image and apply the patch yourself.

This project is open source. See `MANIFEST.md` for the exact list of files substituted and a step-by-step description of how the patch is built, and `splice_film_audio_only.py` for the source of the opening-cinematic audio splice. Released under [The Unlicense](LICENSE) — public domain, do anything with it.

## Credits

- **FMV translations: [Hondoori](https://hondoori.wordpress.com/).** Hondoori graciously provided the English translations for every line of dialogue in the four FMVs.
- **TrekkiesUnite118** for the [SegaSaturnFilmTools / FILM Muxer](https://github.com/TrekkiesUnite118/SegaSaturnFilmMuxer) — the only working tool for muxing Cinepak video into Saturn-compliant FILM containers with correct STAB chunks.
- **The Radius Cinepak codec** (now hosted on the [Internet Archive](https://archive.org/details/cinepakcodec1.10.0.11_20231027)) — the 1995 Windows codec is the only one that produces Saturn-compatible Cinepak encoding.

---

## Required source files

Your USA disc dump must match these checksums (Redump-indexed dump of "Mega Man 8 (USA)"):

| File | MD5 | SHA-1 |
|------|-----|-------|
| `Mega Man 8 (USA) (Track 1).bin` | `a4d575cd681b7d7c88b45d639ed7ffb7` | `047182c8f4f5ace8b4a87d6f55d24a4a44460630` |
| `Mega Man 8 (USA) (Track 2).bin` | `a2201327867523e4e31de62c445e2996` | `e959c797d94c8b18feb067301ef838c2a06aed72` |

Track 1 must be in **MODE1/2352** format. If your dump's checksums don't match, the patch will not apply.

---

## Installing xdelta3 / a patcher

The patch is an xdelta3 binary diff. You can apply it from the command line on Linux / macOS / Windows, or use a cross-platform GUI patcher.

**Linux command line:**
- Debian / Ubuntu: `sudo apt install xdelta3`
- Fedora / Red Hat: `sudo dnf install xdelta3`
- Arch: `sudo pacman -S xdelta3`

**macOS GUI:** MultiPatch — <https://www.romhacking.net/utilities/746/>

**Windows GUI:** xdelta UI — <https://www.romhacking.net/utilities/598/>

**Cross-platform GUI (Linux flatpak / Windows / macOS):** DeltaPatcher — <https://github.com/marco-calautti/DeltaPatcher>

---

## Applying the patch

From the folder containing your USA `.bin` and this patch, run this single command:

```bash
xdelta3 -d -B 536870912 -s "Mega Man 8 (USA) (Track 1).bin" "Mega Man 8 (USA) [Undub v1.1.0].xdelta" "Mega Man 8 (USA) [Undub v1.1.0] (Track 1).bin"
```

That produces `Mega Man 8 (USA) [Undub v1.1.0] (Track 1).bin`.

For Track 2, copy your unmodified USA Track 2 alongside it and rename to `Mega Man 8 (USA) [Undub v1.1.0] (Track 2).bin`. The audio track is byte-identical to the USA release — the patch doesn't touch it.

Use the included `Mega Man 8 (USA) [Undub v1.1.0].cue` (it already references those filenames).

---

## What's patched

- **All in-game voices** — every voice line spoken during gameplay (Mega Man, Robot Masters, Auto, Roll, Bass, Duo, Wily, announcers, etc.) is the original Japanese cast.
- **Opening cinematic (`ROCK8_0.CPK`)** — surgical splice: US visuals preserved byte-for-byte, FILM audio samples replaced with the JP versions (audio offset by 3 slots so the voice lines up with the US reel's silent intro). See `splice_film_audio_only.py` for the exact algorithm.
- **Cinematics 1–4 (`ROCK8_1` to `ROCK8_4`)** — the full Japanese versions (visuals + audio), now with **English subtitles burned into the video** thanks to Hondoori's translations. Subtitles are part of the encoded Cinepak frames, not a runtime overlay.

## Tested on

v1.1.0 has been validated on the **Saturn** core for MiSTer FPGA, **Beetle Saturn** core in RetroArch and on **standalone Mednafen** (Saturn module). It has *not* yet been tested on real hardware, nor on SSF / Yabause / Kronos for the full play-through. Behavior on real Saturn consoles or other emulators is unverified — reports welcome.


## Legal

This release contains no game data, code, or assets. The xdelta patch is a pure binary diff that requires a user-supplied USA disc image to produce any usable output.

The included `.cue` file is plain-text metadata (sector layout / track type) that contains no game content; cue sheets are routinely distributed alongside fan patches and are not subject to copyright.

The project's own code, build scripts, and documentation are released into the public domain under [The Unlicense](LICENSE).

*Mega Man 8* and *Rockman 8: Metal Heroes* are © Capcom Co., Ltd. — this is an unofficial fan modification with no affiliation to or endorsement from Capcom. You must own a legitimate copy of the USA release to use this patch.
