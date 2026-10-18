# MM8 Saturn Undub

A fan-made undub patch that swaps the English dub in *Mega Man 8* (Sega Saturn, USA release) with the original Japanese audio from *Rockman 8: Metal Heroes*, adds **English subtitles** to the four full-motion cinematics, and restores the Japanese ending-credits song **"Brand New Way"**. The English menu text, graphics, and title logo are preserved from the USA release.

Distributed as an **xdelta3 binary diff**. No game data is included — you supply your own legitimately-acquired copy of the USA disc image and apply the patch yourself.

This project is open source. See `MANIFEST.md` for the exact list of files substituted and a step-by-step description of how the patch is built, and `splice_film_audio_only.py` for the source of the opening-cinematic audio splice. Released under [The Unlicense](LICENSE) — public domain, do anything with it.

## Screenshots

| | |
  |:-:|:-:|
  | ![](<screenshots/Mega_Man_8_(USA)_[Undub_v1.1.0]_1.png>) | ![](<screenshots/Mega_Man_8_(USA)_[Undub_v1.1.0]_2.png>) |
  | ![](<screenshots/Mega_Man_8_(USA)_[Undub_v1.1.0]_3.png>) | ![](<screenshots/Mega_Man_8_(USA)_[Undub_v1.1.0]_4.png>) |

## Credits

- **FMV translations: [Hondoori](https://hondoori.wordpress.com/).** Hondoori graciously provided the English translations for every line of dialogue in the four FMVs.
- **TrekkiesUnite118** for the [SegaSaturnFilmTools / FILM Muxer](https://github.com/TrekkiesUnite118/SegaSaturnFilmMuxer) — the only working tool for muxing Cinepak video into Saturn-compliant FILM containers with correct STAB chunks.
- **The Radius Cinepak codec** (now hosted on the [Internet Archive](https://archive.org/details/cinepakcodec1.10.0.11_20231027)) — the 1995 Windows codec is the only one that produces Saturn-compatible Cinepak encoding.

---

## What's new in v1.2.0

- **Ending credits now play the Japanese song "Brand New Way".** The USA release replaced it with a different credits track. The game plays its credits music from the disc's CD audio, so v1.2.0 now patches **Track 2** as well as Track 1. Track 1 is unchanged from v1.1.0.

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

v1.2.0 contains **two** patches — one for each track. From the folder containing your USA `.bin` files and the patches, run:

```bash
xdelta3 -d -B 536870912 -s "Mega Man 8 (USA) (Track 1).bin" "Mega Man 8 (USA) [Undub v1.2.0].xdelta" "Mega Man 8 (USA) [Undub v1.2.0] (Track 1).bin"
xdelta3 -d -B 536870912 -s "Mega Man 8 (USA) (Track 2).bin" "Mega Man 8 (USA) [Undub v1.2.0] (Track 2).xdelta" "Mega Man 8 (USA) [Undub v1.2.0] (Track 2).bin"
```

That produces `Mega Man 8 (USA) [Undub v1.2.0] (Track 1).bin` and `Mega Man 8 (USA) [Undub v1.2.0] (Track 2).bin`. With a GUI patcher, apply each `.xdelta` to its matching USA track the same way.

Use the included `Mega Man 8 (USA) [Undub v1.2.0].cue` (it already references those filenames).

**Upgrading from v1.1.0?** Track 1 is identical, so you only need the Track 2 patch. Rename your v1.1.0 Track 1 bin to the v1.2.0 name (or edit the cue).

Patched output checksums:

| File | MD5 | SHA-1 |
|------|-----|-------|
| `Mega Man 8 (USA) [Undub v1.2.0] (Track 1).bin` | `4b9c5e9e1dc5660f04a6d7f87b30bd68` | `d3e5eff83fc2016613044715cd85070a374579a8` |
| `Mega Man 8 (USA) [Undub v1.2.0] (Track 2).bin` | `814b6bddcfbebf5ee1699d7f9c3c06cc` | `d162771b0e955c45b08d56b09ad80c10722d6a6e` |

---

## What's patched

- **All in-game voices** — every voice line spoken during gameplay (Mega Man, Robot Masters, Auto, Roll, Bass, Duo, Wily, announcers, etc.) is the original Japanese cast.
- **Opening cinematic (`ROCK8_0.CPK`)** — surgical splice: US visuals preserved byte-for-byte, FILM audio samples replaced with the JP versions (audio offset by 3 slots so the voice lines up with the US reel's silent intro). See `splice_film_audio_only.py` for the exact algorithm.
- **Cinematics 1–4 (`ROCK8_1` to `ROCK8_4`)** — the full Japanese versions (visuals + audio), now with **English subtitles burned into the video** thanks to Hondoori's translations. Subtitles are part of the encoded Cinepak frames, not a runtime overlay.
- **Ending credits music (CD audio, Track 2)** — the Japanese credits song "Brand New Way", taken from the JP disc's CD audio tracks. See `MANIFEST.md` for details.

## Tested on

### Emulators
v1.2.0 has been tested by the maintainer. v1.1.0 was validated on the **Saturn** core for MiSTer FPGA, **Beetle Saturn** core in RetroArch and on **standalone Mednafen** (Saturn module). It has *not* yet been tested on real hardware, nor on SSF / Yabause / Kronos for the full play-through. Behavior on other emulators is unverified — reports welcome.

### Real Hardware
Sega Saturn VA0 + Fenrir ODE: Version 1.1.0 reported to work through a full playthrough, with no noticeable issues. [Source
](https://github.com/gengaislop/MM8SaturnUndub/issues/1#issue-5467743688)

Reports are welcome for real hardware.

## Legal

This release contains no game data, code, or assets. The xdelta patch is a pure binary diff that requires a user-supplied USA disc image to produce any usable output.

The included `.cue` file is plain-text metadata (sector layout / track type) that contains no game content; cue sheets are routinely distributed alongside fan patches and are not subject to copyright.

The project's own code, build scripts, and documentation are released into the public domain under [The Unlicense](LICENSE).

*Mega Man 8* and *Rockman 8: Metal Heroes* are © Capcom Co., Ltd. — this is an unofficial fan modification with no affiliation to or endorsement from Capcom. You must own a legitimate copy of the USA release to use this patch.
