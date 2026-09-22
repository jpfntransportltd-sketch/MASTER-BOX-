import os, uuid
from flask import Flask, request, send_file, render_template_string
import yt_dlp, imageio_ffmpeg

app = Flask(__name__)
os.makedirs("dl", exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()

HTML = """<!DOCTYPE html><html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Master Box</title><style>
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,sans-serif}
body{background:#fff;color:#1F2937}
header{background:linear-gradient(135deg,#4F46E5,#7C3AED);color:#fff;padding:22px}
header h1{font-size:26px}header p{font-size:13px;opacity:.9}
.langs{display:flex;gap:8px;padding:12px;background:#EEF2FF;overflow-x:auto}
.langs button{padding:8px 14px;border:1px solid #C7D2FE;background:#fff;border-radius:20px;font-size:13px}
.langs button.on{background:#4F46E5;color:#fff}
.tabs{display:flex;gap:6px;padding:10px;background:#F3F4F6}
.tabs button{flex:1;padding:11px;border:none;background:#fff;border-radius:10px;font-size:13px;font-weight:600;color:#6B7280}
.tabs button.on{background:#4F46E5;color:#fff}
.wrap{padding:16px}
.card{background:#FEF3C7;border:2px solid #FCD34D;border-radius:18px;padding:20px}
.card h2{font-size:19px;margin-bottom:14px}
input{width:100%;padding:13px;border:2px solid #A5B4FC;border-radius:12px;font-size:15px;margin-bottom:12px;background:#fff}
.btn{width:100%;padding:15px;background:#4F46E5;color:#fff;border:none;border-radius:12px;font-size:16px;font-weight:700}
.btn.g{background:#10B981}.btn.o{background:#F59E0B}.btn:disabled{opacity:.5}
.res{margin-top:14px;padding:13px;border-radius:12px;font-size:14px;display:none;word-break:break-word}
.res.ok{background:#D1FAE5;color:#065F46;display:block}
.res.err{background:#FEE2E2;color:#991B1B;display:block}
.res.info{background:#FEF3C7;color:#92400E;display:block}
.res a{color:#065F46;font-weight:700;display:block;margin-top:8px;padding:10px;background:#fff;border-radius:8px;text-align:center;text-decoration:none}
.hide{display:none}
</style></head><body>
<header><h1>🌐 Master Box</h1><p id="tag">Download · Cut · Share</p></header>
<div class="langs">
<button class="on" onclick="L('en',this)">English</button>
<button onclick="L('pa',this)">ਪੰਜਾਬੀ</button>
<button onclick="L('hi',this)">हिंदी</button>
<button onclick="L('es',this)">Español</button>
</div>
<div class="tabs">
<button class="on" onclick="T('v',this)">🎬 Video</button>
<button onclick="T('a',this)">🎵 MP3</button>
<button onclick="T('r',this)">✂️ Ringtone</button>
</div>
<div class="wrap">
<div id="tab-v"><div class="card">
<h2 id="h1">🎬 Download Video</h2>
<input id="vurl" placeholder="Paste URL...">
<button class="btn" id="b1" onclick="dl('video')">⬇️ Download</button>
<div class="res" id="r1"></div></div></div>
<div id="tab-a" class="hide"><div class="card">
<h2 id="h2">🎵 Download MP3</h2>
<input id="aurl" placeholder="Paste URL...">
<button class="btn g" id="b2" onclick="dl('mp3')">🎵 Extract</button>
<div class="res" id="r2"></div></div></div>
<div id="tab-r" class="hide"><div class="card">
<h2 id="h3">✂️ Ringtone Cutter</h2>
<input type="file" id="rf" accept="audio/*">
<input type="number" id="rs" placeholder="Start sec" value="0">
<input type="number" id="re" placeholder="End sec" value="30">
<button class="btn o" id="b3" onclick="cut()">✂️ Cut</button>
<div class="res" id="r3"></div></div></div>
</div>
<script>
const TT={en:{t:"Download · Cut · Share",h1:"🎬 Download Video",b1:"⬇️ Download",h2:"🎵 MP3",b2:"🎵 Extract",h3:"✂️ Ringtone",b3:"✂️ Cut"},
pa:{t:"ਡਾਊਨਲੋਡ · ਕੱਟੋ",h1:"🎬 ਵੀਡੀਓ ਡਾਊਨਲੋਡ",b1:"⬇️ ਡਾਊਨਲੋਡ",h2:"🎵 MP3",b2:"🎵 ਕੱਢੋ",h3:"✂️ ਰਿੰਗਟੋਨ",b3:"✂️ ਕੱਟੋ"},
hi:{t:"डाउनलोड · काटें",h1:"🎬 वीडियो",b1:"⬇️ डाउनलोड",h2:"🎵 MP3",b2:"🎵 निकालें",h3:"✂️ रिंगटोन",b3:"✂️ काटें"},
es:{t:"Descargar · Cortar",h1:"🎬 Video",b1:"⬇️ Descargar",h2:"🎵 MP3",b2:"🎵 Extraer",h3:"✂️ Tono",b3:"✂️ Cortar"}};
function L(l,e){document.querySelectorAll('.langs button').forEach(b=>b.classList.remove('on'));e.classList.add('on');const t=TT[l];
document.getElementById('tag').textContent=t.t;document.getElementById('h1').textContent=t.h1;document.getElementById('b1').textContent=t.b1;
document.getElementById('h2').textContent=t.h2;document.getElementById('b2').textContent=t.b2;document.getElementById('h3').textContent=t.h3;
document.getElementById('b3').textContent=t.b3;}
function T(n,e){document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('on'));e.classList.add('on');
['v','a','r'].forEach(x=>document.getElementById('tab-'+x).classList.add('hide'));document.getElementById('tab-'+n).classList.remove('hide');}
async function dl(f){const u=f==='video'?document.getElementById('vurl').value:document.getElementById('aurl').value;
const r=f==='video'?document.getElementById('r1'):document.getElementById('r2');
const b=f==='video'?document.getElementById('b1'):document.getElementById('b2');
if(!u){r.className='res err';r.textContent='⚠️ URL paste';return;}
b.disabled=true;b.textContent='⏳...';r.className='res info';r.textContent='⏳ Processing...';
try{const x=await fetch('/api/download?url='+encodeURIComponent(u)+'&format='+f,{method:'POST'});
const d=await x.json();
if(d.ok){r.className='res ok';r.innerHTML='✅ '+d.title+'<a href="/api/file/'+d.filename+'" download>📥 Save</a>';}
else{r.className='res err';r.textContent='❌ '+d.error;}}catch(e){r.className='res err';r.textContent='❌ Error';}
b.disabled=false;b.textContent=f==='video'?'⬇️ Download':'🎵 Extract';}
async function cut(){const f=document.getElementById('rf').files[0];const r=document.getElementById('r3');
if(!f){r.className='res err';r.textContent='⚠️ File select';return;}
r.className='res info';r.textContent='⏳ Cutting...';
const fd=new FormData();fd.append('file',f);fd.append('start',document.getElementById('rs').value);fd.append('end',document.getElementById('re').value);
try{const x=await fetch('/api/ringtone',{method:'POST',body:fd});const d=await x.json();
if(d.ok){r.className='res ok';r.innerHTML='✅ Ready<a href="/api/file/'+d.filename+'" download>📥 Save</a>';}
else{r.className='res err';r.textContent='❌ '+d.error;}}catch(e){r.className='res err';r.textContent='❌ Error';}}
</script></body></html>"""

@app.route("/")
def home(): return render_template_string(HTML)

@app.route("/api/download", methods=["POST"])
def dl():
    url = request.args.get("url")
    fmt = request.args.get("format", "video")
    j = str(uuid.uuid4())[:8]
    o = {'outtmpl': f'dl/{j}_%(title)s.%(ext)s', 'ffmpeg_location': FF, 'quiet': True}
    if fmt == "mp3":
        o['format'] = 'bestaudio/best'
        o['postprocessors'] = [{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192'}]
    else:
        o['format'] = 'best[ext=mp4]/best'
    try:
        with yt_dlp.YoutubeDL(o) as y:
            i = y.extract_info(url, download=True)
            fn = y.prepare_filename(i)
            if fmt == "mp3": fn = os.path.splitext(fn)[0] + ".mp3"
            return {"ok": True, "title": i.get('title','video'), "filename": os.path.basename(fn)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.route("/api/ringtone", methods=["POST"])
def ring():
    try:
        f = request.files["file"]
        start = float(request.form["start"])
        end = float(request.form["end"])
        j = str(uuid.uuid4())[:8]
        inp = f"dl/{j}_in"
        f.save(inp)
        out = f"{j}_ring.m4r"
        os.system(f'"{FF}" -y -i "{inp}" -ss {start} -t {end-start} -c copy "dl/{out}"')
        return {"ok": True, "filename": out}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.route("/api/file/<name>")
def gf(name): return send_file(os.path.join("dl", name), as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)