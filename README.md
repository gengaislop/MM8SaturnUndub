# Mega Man 8 (Sega Saturn) Japanese-Voice Undub

A fan-made undub patch that swaps the English dub in *Mega Man 8* (Sega Saturn, USA release) with the original Japanese audio from *Rockman 8: Metal Heroes*, while preserving the English menu text, graphics, and title logo.

Distributed as an **xdelta3 binary diff**. No game data is included — you supply your own legitimately-acquired copy of the USA disc image and apply the patch yourself.

This project is open source: see `MANIFEST.md` for the exact list of files substituted and a step-by-step description of how the patch is built, and `splice_film_audio_only.py` for the source of the only non-trivial transformation (the opening cinematic's audio splice). Released under [The Unlicense](LICENSE) — public domain, do anything with it.

---

## Required source files

Your USA disc dump must match these checksums (Redump-indexed dump of "Mega Man 8 (USA)"):

| File | MD5 | SHA-1 |
|------|-----|-------|
| `Mega Man 8 (USA) (Track 1).bin` | `a4d575cd681b7d7c88b45d639ed7ffb7` | `047182c8f4f5ace8b4a87d6f55d24a4a44460630` |
| `Mega Man 8 (USA) (Track 2).bin` | `a2201327867523e4e31de62c445e2996` | `e959c797d94c8b18feb067301ef838c2a06aed72` |

Track 1 must be in **MODE1/2352** format. If your dump's checksums don't match, the patch will not apply.

You also need `xdelta3` installed (Linux: `apt install xdelta3` / `dnf install xdelta`; macOS: `brew install xdelta`; Windows: prebuilt binary at <https://xdelta.org/>).

---

## Applying the patch

From the folder containing your USA `.bin` and this patch:

```bash
xdelta3 -d -B 536870912 \
  -s "Mega Man 8 (USA) (Track 1).bin" \
  "Mega Man 8 (Undub v1.0.1).xdelta" \
  "Mega Man 8 (Undub v1.0.1) (Track 1).bin"
```

That produces `Mega Man 8 (Undub v1.0.1) (Track 1).bin`. For Track 2, copy your unmodified USA Track 2 alongside it and rename it `Mega Man 8 (Undub v1.0.1) (Track 2).bin` — the audio track is byte-identical to the USA release, so the patch doesn't need to modify it.

---

## What was patched

- **All in-game voices** — every voice line spoken during gameplay (Mega Man, Robot Masters, Auto, Roll, Bass, Duo, Wily, announcers, etc.) is the original Japanese cast.
- **Opening cinematic (`ROCK8_0.CPK`)** — a surgical splice: the US visuals are preserved byte-for-byte and only the FILM/Cinepak audio samples are replaced with the JP versions (audio offset by 3 slots so the voice lines up with the US reel's intro). See `splice_film_audio_only.py` for the exact algorithm.
- **Cinematics 1–4 (`ROCK8_1.CPK` through `ROCK8_4.CPK`)** — the full Japanese versions (both visuals and audio are Japanese). Adding English subtitles into these is being investigated for a future release; v1 ships without subtitles for these cutscenes.

## Tested on

So far v1 has only been validated on the **Beetle Saturn** core in RetroArch. It has *not* yet been tested on real hardware, nor on standalone emulators like SSF, Mednafen, Yabause, or Kronos. Behavior on real Saturn consoles or other emulators is unverified — reports welcome.

## Legal

This release contains no game data, code, or assets. The xdelta patch is a pure binary diff that requires a user-supplied USA disc image to produce any usable output.

The included `.cue` file is plain-text metadata (sector layout / track type) that contains no game content; cue sheets are routinely distributed alongside fan patches and are not subject to copyright.

The project's own code, build scripts, and documentation are released into the public domain under [The Unlicense](LICENSE). *Mega Man 8* and *Rockman 8: Metal Heroes* are © Capcom Co., Ltd. — this is an unofficial fan modification with no affiliation to or endorsement from Capcom. You must own a legitimate copy of the USA release to use this patch.
