# MNYC Instagram TV signage

Office TV screen for @mountingnyc, shown on Zoom Digital Signage.

- Live page: https://nex-av.github.io/insta-dashboard/
- Follower counts: `data/snapshots.json`. Add a row (date, followers, posts, following) to update the screen. The first row is the starting point (383 followers, Nov 5 2026).
- The screen checks for new numbers every minute and plays a "+1 New follower" moment when the count goes up.
- Preview the animation: add `#demo` to the URL.
- Source of truth for the page: Nex-AV/Skills, `plugins/mnyc/skills/social-media-dashboard/dashboard/signage.html`.

## Zoom version (/tv)
`tv.html` is a static, old-browser-safe copy for Zoom Digital Signage: no web fonts, no data loading, numbers baked in.
After editing `data/snapshots.json`, run `python3 build_tv.py` and commit `tv.html`. It reloads itself every 15 minutes.
Zoom URL: https://nex-av.github.io/insta-dashboard/tv
