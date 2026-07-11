#!/usr/bin/env python3
"""Generate a self-contained, printable 'recovery card': a high-error-correction QR
pointing at the collection URL, plus the human-readable URL, SHA-256, and date —
so the archive is recoverable even if the QR is damaged or a link dies.

QR encoding is 100% offline (segno). Nothing is sent anywhere.

Usage:
  python gen-recovery.py --url https://USER.github.io/pokemon-cards/ \
      --file index.html --title "Pokémon Collection" --date 2026-07-11
"""
import argparse, hashlib, io, pathlib
import segno

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="URL the QR points to (the GitHub Pages URL)")
    ap.add_argument("--file", default="index.html", help="file to hash for the integrity line")
    ap.add_argument("--title", default="Pokémon Card Collection")
    ap.add_argument("--date", default="")
    ap.add_argument("--out", default="recovery-card.html")
    args = ap.parse_args()

    digest = hashlib.sha256(pathlib.Path(args.file).read_bytes()).hexdigest()

    # Error correction level H (30%) — maximum damage tolerance for a decades-long print.
    qr = segno.make(args.url, error="h")
    buf = io.StringIO()
    # inline SVG, no external refs; scale gives crisp large modules; dark on white for print
    qr.save(buf, kind="svg", scale=10, border=4, dark="#000000", light="#ffffff",
            svgclass=None, lineclass=None, xmldecl=False, svgns=True)
    qr_svg = buf.getvalue()

    # split hash into readable groups
    grouped = " ".join(digest[i:i+8] for i in range(0, len(digest), 8))

    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>{args.title} — recovery card</title>
<style>
  * {{ box-sizing:border-box; }}
  html {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
  body {{ font:13px/1.45 -apple-system,"Segoe UI",Roboto,Arial,sans-serif; color:#111; margin:0;
         display:flex; justify-content:center; padding:24px; }}
  .card {{ width:3.5in; border:2px solid #111; border-radius:10px; padding:18px 18px 14px; }}
  h1 {{ font-size:15px; margin:0 0 2px; letter-spacing:.2px; }}
  .sub {{ font-size:10.5px; color:#666; margin:0 0 12px; }}
  .qrwrap {{ display:flex; justify-content:center; margin:2px 0 12px; }}
  .qrwrap svg {{ width:2.3in; height:2.3in; }}
  .lab {{ font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:.6px; color:#999; margin:10px 0 2px; }}
  .url {{ font:12px/1.35 ui-monospace,"Cascadia Mono",Consolas,monospace; word-break:break-all; }}
  .hash {{ font:9.5px/1.5 ui-monospace,"Cascadia Mono",Consolas,monospace; word-break:break-all; color:#333; }}
  .foot {{ margin-top:12px; padding-top:8px; border-top:1px solid #ccc; font-size:9.5px; color:#777; }}
  @page {{ size:auto; margin:0.4in; }}
  @media print {{ body{{ padding:0; }} }}
</style></head><body>
<div class="card">
  <h1>{args.title}</h1>
  <p class="sub">Permanent inventory · scan to open (works offline once loaded)</p>
  <div class="qrwrap">{qr_svg}</div>
  <div class="lab">If the QR won't scan, type this</div>
  <div class="url">{args.url}</div>
  <div class="lab">File integrity — SHA-256 of index.html</div>
  <div class="hash">{grouped}</div>
  <div class="foot">Verify: <code>sha256sum index.html</code> must equal the digest above.
  Kept in multiple backups + print (LOCKSS). Created {args.date or "____-__-__"}.</div>
</div>
</body></html>"""
    pathlib.Path(args.out).write_text(html, encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"  url : {args.url}")
    print(f"  sha : {digest}")
    print(f"  QR  : segno, error-correction H (30%), {qr.version}-{qr.error}")

if __name__ == "__main__":
    main()
