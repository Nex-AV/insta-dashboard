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
.bar { background: #1F5F7A; height: 10vh; border-bottom: 0.6vh solid #E1306C; }
.bar table { width: 100%%; height: 100%%; border-collapse: collapse; }
.bar > table > tbody > tr > td { padding: 0 3.3vw; vertical-align: middle; white-space: nowrap; }
.logo { height: 5.4vh; vertical-align: middle; }
.word { font-size: 3.4vh; font-weight: bold; margin-left: 1.5vw; vertical-align: middle; }
.pill { display: inline-block; margin-left: 2vw; padding: 0.7vh 1.2vw; border-radius: 4vh; background: #E1306C; color: #fff; font-size: 2vh; font-weight: bold; letter-spacing: 0.3vh; vertical-align: middle; }
.clock { text-align: right; font-size: 3.6vh; }
.main { width: 100%%; height: 74vh; border-collapse: collapse; table-layout: fixed; }
.mcell { vertical-align: middle; padding: 0 3.3vw; }
.eyebrow { font-size: 2.3vh; font-weight: bold; letter-spacing: 0.5vh; color: #E1306C; }
.handle { font-size: 3.2vh; color: #A3B2BA; margin-top: 1vh; font-family: "Courier New", monospace; }
.big { font-family: Georgia, "Times New Roman", serif; font-size: 30vh; line-height: 1; margin: 1vh 0; }
.delta { font-size: 3.2vh; color: #A3B2BA; }
.delta b { color: #E1306C; }
.tiles { width: 100%%; table-layout: fixed; border-collapse: separate; border-spacing: 0.3vh; background: #0b3350; }
.tile { background: #032844; padding: 3vh 2vw; width: 50%%; }
.k { font-size: 2vh; font-weight: bold; letter-spacing: 0.3vh; color: #A3B2BA; }
.v { font-family: Georgia, "Times New Roman", serif; font-size: 9vh; line-height: 1.1; }
.v.up { color: #E1306C; }
.s { font-size: 2.2vh; color: #A3B2BA; }
.week { width: 100%%; table-layout: fixed; border-collapse: separate; border-spacing: 0.4vw 0; margin-top: 1vh; }
.day { text-align: center; padding: 1.3vh 0; font-size: 2.4vh; font-weight: bold; color: #74858F; background: #0a2e49; border: 0.25vh solid #0a2e49; }
.day.post { color: #FFFEF2; background: #154A61; border-color: #154A61; }
.day.today { border-color: #E1306C; }
.foot { height: 15.4vh; border-top: 0.2vh solid #0b3350; }
.foot table { width: 100%%; height: 100%%; border-collapse: collapse; }
.foot > table > tbody > tr > td { padding: 0 3.3vw; vertical-align: middle; }
.chip { display: inline-block; background: #1F5F7A; color: #fff; padding: 1vh 1vw; font-size: 2vh; font-weight: bold; letter-spacing: 0.3vh; }
.tp { font-family: Georgia, "Times New Roman", serif; font-size: 4.4vh; }
.src { text-align: right; font-size: 1.7vh; color: #A3B2BA; white-space: nowrap; }
</style></head>
<body>
<div class="bar"><table><tr>
<td><img class="logo" src="%(logo)s" alt=""><span class="word">MountingNYC</span><span class="pill">INSTAGRAM</span></td>
<td class="clock" id="clock"></td>
</tr></table></div>
<table class="main"><tr>
<td class="mcell" style="width:45%%">
<div class="eyebrow">FOLLOWERS</div>
<div class="handle">@%(account)s</div>
<div class="big">%(followers)s</div>
<div class="delta">%(delta)s</div>
</td>
<td class="mcell" style="width:55%%">
<table class="tiles">
<tr><td class="tile"><div class="k">TODAY</div><div class="v%(today_up)s">%(t_today)s</div><div class="s">new followers today</div></td>
<td class="tile"><div class="k">THIS WEEK</div><div class="v%(week_up)s">%(t_week)s</div><div class="s">new followers this week</div></td></tr>
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
<script>
function pad(n) { return n < 10 ? "0" + n : "" + n; }
function tick() {
  var d = new Date(), h = d.getHours(), ap = h >= 12 ? "PM" : "AM";
  h = h %% 12; if (h === 0) h = 12;
  var el = document.getElementById("clock");
  if (el) el.innerHTML = h + ":" + pad(d.getMinutes()) + " " + ap;
}
tick(); setInterval(tick, 10000);
setTimeout(function () { window.location.reload(); }, 900000);
</script>
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
