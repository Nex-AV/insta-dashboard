# MNYC Instagram TV signage

Office TV screen for @mountingnyc, shown on Zoom Digital Signage.

- Live page: https://nex-av.github.io/insta-dashboard/
- Follower counts: `data/snapshots.json`. Add a row (date, followers, posts, following) to update the screen. The first row is the starting point (383 followers, Nov 5 2026).
- The screen checks for new numbers every minute and plays a "+1 New follower" moment when the count goes up.
- Preview the animation: add `#demo` to the URL.
- Source of truth for the page: Nex-AV/Skills, `plugins/mnyc/skills/social-media-dashboard/dashboard/signage.html`.
