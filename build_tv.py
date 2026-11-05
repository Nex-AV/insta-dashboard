"""Builds tv.html: a static, old-browser-safe version of the signage for Zoom.
Numbers are baked in from data/snapshots.json. Run: python3 build_tv.py
"""
import json, datetime, html, base64

d = json.load(open("data/snapshots.json"))
snaps = d["snapshots"]
first, last = snaps[0], snaps[-1]
gain = last["followers"] - first["followers"]
today = datetime.date.fromisoformat(last["date"])
monday = today - datetime.timedelta(days=today.weekday())
def base(cut):
    before = [s for s in snaps if s["date"] < cut.isoformat()]
    return before[-1] if before else None
def grow(cut):
    b = base(cut)
    if not b:
        return "+0", "since " + today.strftime("%b %-d")
    g = last["followers"] - b["followers"]
    return ("+" if g >= 0 else "-") + str(abs(g)), ""
t_today, _ = grow(today)
t_week, _ = grow(monday)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
plan = d.get("post_days", [])
tp = d["talking_points"][today.toordinal() % len(d["talking_points"])]
delta = ("Starting point, " + datetime.date.fromisoformat(first["date"]).strftime("%b %-d, %Y")) if gain == 0 else \
    '<b>%s%d</b> since %s (%d)' % ("+" if gain > 0 else "-", abs(gain), first["date"], first["followers"])
dayhtml = "".join('<td class="day%s%s">%s</td>' % (" post" if x in plan else "", " today" if days.index(x) == today.weekday() else "", x) for x in days)

page = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>MountingNYC Instagram</title>
<style>
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%%; background: #001D35; color: #FFFEF2; font-family: Helvetica, Arial, sans-serif; overflow: hidden; }
.top { height: 7vh; }
.bar { background: #1F5F7A; height: 9vh; border-bottom: 0.6vh solid #E1306C; padding: 0 4vh; white-space: nowrap; overflow: hidden; }
.bar table { height: 100%%; border-collapse: collapse; }
.bar td { vertical-align: middle; padding: 0; }
.logo { height: 5vh; vertical-align: middle; margin-right: 2vh; }
.word { font-size: 3.6vh; font-weight: bold; vertical-align: middle; }
.pill { display: inline-block; margin-left: 2.4vh; padding: 0.8vh 1.8vh; border-radius: 4vh; background: #E1306C; color: #fff; font-size: 2vh; font-weight: bold; letter-spacing: 0.3vh; vertical-align: middle; }
.main { width: 100%%; height: 70vh; border-collapse: collapse; table-layout: fixed; }
.mcell { vertical-align: middle; padding: 0 4vh; }
.eyebrow { font-size: 2.4vh; font-weight: bold; letter-spacing: 0.5vh; color: #E1306C; }
.handle { font-size: 3vh; color: #A3B2BA; margin-top: 0.8vh; font-family: "Courier New", monospace; }
.big { font-family: Georgia, "Times New Roman", serif; font-size: 24vh; line-height: 1; margin: 1vh 0; }
.delta { font-size: 2.8vh; color: #A3B2BA; }
.delta b { color: #E1306C; }
.tiles { width: 100%%; table-layout: fixed; border-collapse: separate; border-spacing: 0.3vh; background: #0b3350; }
.tile { background: #032844; padding: 2.4vh 2.4vh; width: 50%%; vertical-align: top; }
.k { font-size: 1.9vh; font-weight: bold; letter-spacing: 0.3vh; color: #A3B2BA; white-space: nowrap; }
.v { font-family: Georgia, "Times New Roman", serif; font-size: 8vh; line-height: 1.1; }
.v.up { color: #E1306C; }
.s { font-size: 2vh; color: #A3B2BA; }
.week { width: 100%%; table-layout: fixed; border-collapse: separate; border-spacing: 0.5vh 0; margin-top: 1vh; }
.day { text-align: center; padding: 1.1vh 0; font-size: 2.1vh; font-weight: bold; color: #74858F; background: #0a2e49; border: 0.25vh solid #0a2e49; }
.day.post { color: #FFFEF2; background: #154A61; border-color: #154A61; }
.day.today { border-color: #E1306C; }
.foot { height: 14vh; border-top: 0.2vh solid #0b3350; padding: 0 4vh; }
.foot table { width: 100%%; height: 100%%; border-collapse: collapse; }
.foot td { vertical-align: middle; padding: 0; }
.chip { display: inline-block; background: #1F5F7A; color: #fff; padding: 1vh 1.4vh; font-size: 1.9vh; font-weight: bold; letter-spacing: 0.3vh; margin-right: 2.4vh; white-space: nowrap; }
.tp { font-family: Georgia, "Times New Roman", serif; font-size: 3.4vh; line-height: 1.2; }
.src { text-align: right; font-size: 1.6vh; color: #A3B2BA; white-space: nowrap; padding-left: 2vh !important; }
</style></head>
<body>
<div class="top"></div>
<div class="bar"><table><tr>
<td><span class="word">MountingNYC</span><span class="pill">INSTAGRAM</span></td>
</tr></table></div>
<table class="main"><tr>
<td class="mcell" style="width:46%%">
<div class="eyebrow">FOLLOWERS</div>
<div class="handle">@%(account)s</div>
<div class="big">%(followers)s</div>
<div class="delta">%(delta)s</div>
</td>
<td class="mcell" style="width:54%%">
<table class="tiles">
<tr><td class="tile"><div class="k">TODAY</div><div class="v%(today_up)s">%(t_today)s</div><div class="s">new followers</div></td>
<td class="tile"><div class="k">THIS WEEK</div><div class="v%(week_up)s">%(t_week)s</div><div class="s">new followers</div></td></tr>
<tr><td class="tile"><div class="k">POSTS</div><div class="v">%(posts)s</div><div class="s">on the grid</div></td>
<td class="tile"><div class="k">FOLLOWING</div><div class="v">%(following)s</div><div class="s">accounts</div></td></tr>
<tr><td class="tile" colspan="2"><div class="k">POSTING PLAN THIS WEEK</div><table class="week"><tr>%(dayhtml)s</tr></table></td></tr>
</table>
</td></tr></table>
<div class="foot"><table><tr>
<td style="width:1%%"><span class="chip">%(tp_kind)s</span></td>
<td class="tp">%(tp_text)s</td>
<td class="src">Updated %(asof)s</td>
</tr></table></div>
</body></html>
""" % {
    "account": html.escape(d.get("account", "mountingnyc")),
    "followers": "{:,}".format(last["followers"]),
    "delta": delta,
    "t_today": t_today, "t_week": t_week,
    "today_up": " up" if t_today.startswith("+") and t_today != "+0" else "",
    "week_up": " up" if t_week.startswith("+") and t_week != "+0" else "",
    "posts": last["posts"], "following": last["following"],
    "dayhtml": dayhtml,
    "tp_kind": html.escape(tp["kind"].upper()), "tp_text": html.escape(tp["text"]),
    "asof": today.strftime("%b %-d, %Y"),
    "logo": "data:image/png;base64," + base64.b64encode(open("assets/mnyc-logo-white.png", "rb").read()).decode(),
}
open("tv.html", "w").write(page)
print("tv.html built:", last["followers"], "followers")
