"""Splice a Saturn FILM (.CPK) file: US visuals + JP audio.

Strategy: keep all US samples (video frames, keyframe-markers, structure) but for each
US AUDIO sample, replace its raw bytes with the matching JP AUDIO sample's bytes (matched
by their position in the audio-only sequence). Then recompute offsets and rebuild STAB.

If JP has fewer audio samples than US, the trailing US audio slots keep their US data
(silence trim or English ending). If JP has more, the surplus is dropped.
"""
import struct
import sys

def parse_film(path):
    with open(path, "rb") as f:
        raw = f.read()
    assert raw[:4] == b"FILM"
    file_len_field = struct.unpack(">I", raw[4:8])[0]
    version = raw[8:12]
    # Walk chunks at offset 16
    chunks = []
    off = 16
    while off < len(raw):
        cid = raw[off:off+4]
        if not cid: break
        csz = struct.unpack(">I", raw[off+4:off+8])[0]
        if csz == 0 or off + csz > len(raw): break
        chunks.append((cid, off, csz))
        if cid == b"STAB":
            break
        off += csz
    # Find STAB
    stab = next((c for c in chunks if c[0] == b"STAB"), None)
    assert stab, "no STAB chunk"
    stab_off, stab_size = stab[1], stab[2]
    framerate = struct.unpack(">I", raw[stab_off+8:stab_off+12])[0]
    n = struct.unpack(">I", raw[stab_off+12:stab_off+16])[0]
    samples = []
    for i in range(n):
        s = stab_off + 16 + i*16
        samples.append({
            "offset": struct.unpack(">I", raw[s:s+4])[0],
            "size":   struct.unpack(">I", raw[s+4:s+8])[0],
            "info":   struct.unpack(">I", raw[s+8:s+12])[0],
            "dur":    struct.unpack(">I", raw[s+12:s+16])[0],
        })
    data_start = stab_off + stab_size
    return {
        "raw": raw,
        "version": version,
        "fdsc_chunk": chunks[0],  # assumes FDSC is first
        "stab_offset": stab_off,
        "stab_size": stab_size,
        "framerate": framerate,
        "samples": samples,
        "data_start": data_start,
    }

def is_audio(s):
    # Saturn FILM container in MM8: audio chunks use info=0xffffffff (verified by
    # inspecting raw bytes — these contain 8-bit signed PCM-like waveforms; samples
    # with info=0x00xxxxxx or 0x80xxxxxx have valid Cinepak headers and are video).
    return s["info"] == 0xffffffff

def is_mark(s):
    return False  # no "mark" category in this format

def get_sample_bytes(film, s):
    start = film["data_start"] + s["offset"]
    return film["raw"][start:start + s["size"]]

def splice(us_path, jp_path, out_path, audio_shift=0):
    """audio_shift: number of US audio slots to skip at the start before placing JP audio.
    Use this to keep US's leading silence intro and align JP voice with the actual content."""
    us = parse_film(us_path)
    jp = parse_film(jp_path)

    # Extract JP audio sample data in order
    jp_audio_bytes = [get_sample_bytes(jp, s) for s in jp["samples"] if is_audio(s)]
    print(f"US samples: {len(us['samples'])}, JP samples: {len(jp['samples'])}")
    us_audio_count = sum(1 for s in us["samples"] if is_audio(s))
    jp_audio_count = len(jp_audio_bytes)
    print(f"US audio samples: {us_audio_count}, JP audio samples: {jp_audio_count}, shift: {audio_shift}")

    # Build new sample list
    new_samples = []
    audio_idx = 0  # counts which US audio slot we're at
    for s in us["samples"]:
        if is_audio(s):
            jp_idx = audio_idx - audio_shift
            if 0 <= jp_idx < jp_audio_count:
                new_data = jp_audio_bytes[jp_idx]
            else:
                # Slots before JP starts (the silence intro), or trailing slots beyond JP — keep US
                new_data = get_sample_bytes(us, s)
            new_samples.append({"info": s["info"], "dur": s["dur"], "data": new_data})
            audio_idx += 1
        else:
            new_samples.append({"info": s["info"], "dur": s["dur"], "data": get_sample_bytes(us, s)})

    # Compute new offsets (within data area)
    cur = 0
    for ns in new_samples:
        ns["offset"] = cur
        ns["size"] = len(ns["data"])
        cur += ns["size"]
    total_data = cur

    # Build output: FILM header + FDSC + STAB + data
    # FDSC: copy from US verbatim (codec/dimensions are identical between regions)
    fdsc_id, fdsc_off, fdsc_size = us["fdsc_chunk"]
    fdsc_bytes = us["raw"][fdsc_off:fdsc_off + fdsc_size]
    assert fdsc_id == b"FDSC"

    # STAB: build new sample table
    stab_content_size = 8 + 4 + 4 + len(new_samples) * 16  # header(8) + framerate(4) + nsamples(4) + samples
    stab_bytes = bytearray()
    stab_bytes += b"STAB"
    stab_bytes += struct.pack(">I", stab_content_size)
    stab_bytes += struct.pack(">I", us["framerate"])
    stab_bytes += struct.pack(">I", len(new_samples))
    for ns in new_samples:
        stab_bytes += struct.pack(">IIII", ns["offset"], ns["size"], ns["info"], ns["dur"])

    # FILM header: 16 bytes (magic + size + version + reserved)
    # The "size" field in the original was 0x6a90 = total STAB length+header bytes; better to
    # write the size of everything before the data area (FILM header + FDSC + STAB).
    pre_data_size = 16 + len(fdsc_bytes) + len(stab_bytes)
    film_header = bytearray()
    film_header += b"FILM"
    # Use US's version string (1.09) so executable/player treats it as US
    film_header += struct.pack(">I", pre_data_size)
    film_header += us["version"]  # keep US "1.09"
    film_header += b"\x00\x00\x00\x00"

    # Write out
    with open(out_path, "wb") as f:
        f.write(film_header)
        f.write(fdsc_bytes)
        f.write(stab_bytes)
        for ns in new_samples:
            f.write(ns["data"])

    import os
    out_sz = os.path.getsize(out_path)
    print(f"Wrote {out_path}: {out_sz} bytes (pre_data={pre_data_size}, data={total_data})")

if __name__ == "__main__":
    shift = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    splice(sys.argv[1], sys.argv[2], sys.argv[3], audio_shift=shift)
