# Pokémon Card Collection — permanent inventory

`index.html` is a **fully self-contained** inventory of the collection: all CSS is inline,
there are **no images, scripts, fonts, or network requests of any kind**. Open it in any
web browser (now or decades from now) and it renders offline. HTML is chosen deliberately
as the most backward-compatible renderable format available.

## Integrity
- **SHA-256 of `index.html`:** `61c85770959b3a05fc241974f08dd526b9891650d941b1db1159f7f2d75f381a`
- To verify the file is intact and untampered:
  - PowerShell: `Get-FileHash index.html -Algorithm SHA256`
  - Bash: `sha256sum index.html`
  - The digest must match the value above.

## Durability model (LOCKSS — *Lots Of Copies Keep Stuff Safe*)
This GitHub Pages copy is **one** mirror, not the only one. The file also lives in:
- personal offline backups (multiple drives + a USB in a fireproof box),
- a printed color copy,
- (optionally) a laser-etched metal plaque of the recovery card.

If this repository ever disappears, any copy above reproduces the exact file — verify it
by the SHA-256. The QR code on the recovery card is only a convenience pointer to this URL.

_Last updated: 2026-07-11._
