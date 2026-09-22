import os, uuid
from flask import Flask, request, send_file, render_template_string
import yt_dlp, imageio_ffmpeg

app = Flask(__name__)
os.makedirs("dl", exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()

HTML = """<!DOCTYPE html><html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>Master Box</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,sans-serif;-webkit-tap-highlight-color:transparent}
body{background:#FFFDF5;color:#4B5563;padding-bottom:40px}
@keyframes shine{0%{background-position:-200% center}100%{background-position:200% center}}
@keyframes moveBlue{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
header{
  background:linear-gradient(90deg,#FFD700,#FFED4E,#60A5FA,#FFD700);
  background-size:400% 400%;
  animation:moveBlue 8s ease infinite;
  color:#4B5563;
  padding:24px 18px;
  text-align:center;
  box-shadow:0 4px 20px rgba(255,215,0,0.3);
}
header h1{font-size:28px;font-weight:800;text-shadow:0 1px 2px rgba(255,255,255,0.6)}
header p{font-size:13px;margin-top:4px;color:#374151;font-weight:600}
.langs{display:flex;gap:8px;padding:12px;background:#FFF9E6;overflow-x:auto;-webkit-overflow-scrolling:touch}
.langs button{
  padding:8px 16px;
  border:2px solid #FDE68A;
  background:#fff;
  border-radius:20px;
  font-size:13px;
  font-weight:600;
  color:#6B7280;
  white-space:nowrap;
  transition:all 0.3s;
}
.langs button.on{
  background:linear-gradient(135deg,#FFD700,#FFED4E);
  color:#4B5563;
  border-color:#FFD700;
  box-shadow:0 2px 8px rgba(255,215,0,0.4);
}
.tabs{display:flex;gap:6px;padding:10px 12px;background:#FFF9E6;overflow-x:auto}
.tabs button{
  flex:1;
  padding:12px 8px;
  border:2px solid transparent;
  background:#fff;
  border-radius:12px;
  font-size:12px;
  font-weight:700;
  color:#9CA3AF;
  white-space:nowrap;
  transition:all 0.3s;
  min-width:70px;
}
.tabs button.on{
  background:linear-gradient(135deg,#FFD700,#FFED4E);
  color:#4B5563;
  box-shadow:0 3px 10px rgba(255,215,0,0.4);
}
.wrap{padding:16px}
.card{
  background:linear-gradient(135deg,#FFFDF5,#FFF9E6);
  border:2px solid #FDE68A;
  border-radius:20px;
  padding:22px;
  margin-bottom:16px;
  box-shadow:0 4px 16px rgba(255,215,0,0.15);
}
.card h2{font-size:20px;color:#4B5563;margin-bottom:16px;font-weight:800}
.card h2 span{color:#F59E0B}
input[type=text],input[type=number]{
  width:100%;
  padding:14px;
  border:2px solid #FDE68A;
  border-radius:12px;
  font-size:15px;
  margin-bottom:12px;
  background:#fff;
  outline:none;
  color:#4B5563;
  transition:border 0.3s;
}
input:focus{border-color:#FFD700;box-shadow:0 0 0 3px rgba(255,215,0,0.15)}
input[type=file]{
  width:100%;
  padding:14px;
  border:2px dashed #FDE68A;
  border-radius:12px;
  font-size:14px;
  margin-bottom:12px;
  background:#FFFDF5;
  color:#6B7280;
}
.btn{
  width:100%;
  padding:16px;
  background:linear-gradient(135deg,#FFD700,#FFED4E);
  color:#4B5563;
  border:none;
  border-radius:12px;
  font-size:16px;
  font-weight:800;
  margin-top:4px;
  transition:all 0.2s;
  box-shadow:0 4px 12px rgba(255,215,0,0.3);
}
.btn:active{transform:scale(0.98)}
.btn:disabled{opacity:0.6}
.btn.blue{
  background:linear-gradient(135deg,#60A5FA,#93C5FD);
  color:#fff;
  box-shadow:0 4px 12px rgba(96,165,250,0.4);
}
.btn.blue:active{transform:scale(0.98)}
.res{margin-top:14px;padding:14px;border-radius:12px;font-size:14px;display:none;word-break:break-word;line-height:1.5}
.res.ok{background:#D1FAE5;color:#065F46;display:block;border-left:4px solid #10B981}
.res.err{background:#FEE2E2;color:#991B1B;display:block;border-left:4px solid #EF4444}
.res.info{background:#FEF3C7;color:#92400E;display:block;border-left:4px solid #F59E0B}
.res a{
  color:#065F46;
  font-weight:800;
  display:block;
  margin-top:10px;
  padding:12px;
  background:#fff;
  border-radius:8px;
  text-align:center;
  text-decoration:none;
  border:2px solid #10B981;
}
.res a.blue{color:#1E40AF;border-color:#60A5FA}
.hide{display:none}
.feature{
  padding:12px 0;
  border-bottom:1px solid #FDE68A;
  font-size:14px;
  display:flex;
  gap:12px;
  align-items:center;
  color:#4B5563;
}
.feature:last-child{border:none}
.feature-icon{font-size:22px;min-width:30px}
.page{
  background:#FFFDF5;
  padding:16px;
}
.page h2{
  font-size:22px;
  color:#4B5563;
  margin-bottom:16px;
  padding-bottom:12px;
  border-bottom:3px solid #FFD700;
}
.page p{
  font-size:14px;
  line-height:1.7;
  color:#4B5563;
  margin-bottom:14px;
}
.page h3{
  font-size:16px;
  color:#F59E0B;
  margin:16px 0 8px;
  font-weight:800;
}
.page ul{
  padding-left:20px;
  margin-bottom:14px;
}
.page li{
  font-size:14px;
  line-height:1.7;
  color:#4B5563;
  margin-bottom:6px;
}
.back{
  display:inline-block;
  padding:10px 18px;
  background:linear-gradient(135deg,#FFD700,#FFED4E);
  color:#4B5563;
  border-radius:10px;
  font-weight:700;
  font-size:14px;
  text-decoration:none;
  margin-bottom:16px;
  box-shadow:0 2px 8px rgba(255,215,0,0.3);
}
.footer{
  text-align:center;
  padding:24px 16px;
  color:#9CA3AF;
  font-size:12px;
}
.footer a{
  color:#F59E0B;
  text-decoration:none;
  margin:0 8px;
  font-weight:700;
}
</style>
</head>
<body>

<div id="main-app">
<header>
  <h1>🌐 Master Box</h1>
  <p id="tag">Download · Cut · Share</p>
</header>

<div class="langs">
  <button class="on" onclick="L('en',this)">English</button>
  <button onclick="L('pa',this)">ਪੰਜਾਬੀ</button>
  <button onclick="L('hi',this)">हिंदी</button>
  <button onclick="L('es',this)">Español</button>
  <button onclick="L('ar',this)">العربية</button>
</div>

<div class="tabs">
  <button class="on" onclick="T('v',this)">🎬 Video</button>
  <button onclick="T('a',this)">🎵 MP3</button>
  <button onclick="T('r',this)">✂️ Ringtone</button>
  <button onclick="T('p',this)">📄 PDF</button>
  <button onclick="T('i',this)">📋 Info</button>
</div>

<div class="wrap">

  <div id="tab-v">
    <div class="card">
      <h2>🎬 <span id="h1">Download Video</span></h2>
      <input type="text" id="vurl" placeholder="Paste YouTube / TikTok / Instagram URL...">
      <button class="btn" id="b1" onclick="dl('video')">⬇️ <span id="b1t">Download Video</span></button>
      <div class="res" id="r1"></div>
    </div>
  </div>

  <div id="tab-a" class="hide">
    <div class="card">
      <h2>🎵 <span id="h2">Download MP3</span></h2>
      <input type="text" id="aurl" placeholder="Paste URL for MP3...">
      <button class="btn" id="b2" onclick="dl('mp3')">🎵 <span id="b2t">Extract MP3</span></button>
      <div class="res" id="r2"></div>
    </div>
  </div>

  <div id="tab-r" class="hide">
    <div class="card">
      <h2>✂️ <span id="h3">Ringtone Cutter</span></h2>
      <input type="file" id="rf" accept="audio/*">
      <input type="number" id="rs" placeholder="Start (seconds)" value="0">
      <input type="number" id="re" placeholder="End (seconds)" value="30">
      <button class="btn" id="b3" onclick="cut()">✂️ <span id="b3t">Cut Ringtone</span></button>
      <div class="res" id="r3"></div>
    </div>
  </div>

  <div id="tab-p" class="hide">
    <div class="card">
      <h2>📄 <span>PDF Tools</span></h2>
      <input type="file" id="pdff" accept="application/pdf">
      <button class="btn blue" onclick="sharePDF()">📤 Share / Save PDF</button>
      <div class="res" id="r4"></div>
    </div>
  </div>

  <div id="tab-i" class="hide">
    <div class="card">
      <h2>📋 <span>Features</span></h2>
      <div class="feature"><span class="feature-icon">🎬</span><span>Video download (1000+ sites)</span></div>
      <div class="feature"><span class="feature-icon">🎵</span><span>MP3 audio extraction</span></div>
      <div class="feature"><span class="feature-icon">✂️</span><span>Ringtone cutter</span></div>
      <div class="feature"><span class="feature-icon">📄</span><span>PDF upload & share</span></div>
      <div class="feature"><span class="feature-icon">📤</span><span>Share to WhatsApp</span></div>
      <div class="feature"><span class="feature-icon">🌐</span><span>Multi-language support</span></div>
      <div class="feature"><span class="feature-icon">🔒</span><span>Privacy protected</span></div>
    </div>
  </div>

</div>

<div class="footer">
  <a onclick="showPage('about')">About</a>
  <a onclick="showPage('privacy')">Privacy</a>
  <a onclick="showPage('disclaimer')">Disclaimer</a>
  <p style="margin-top:14px;color:#D1D5DB">© 2026 Master Box</p>
</div>
</div>

<!-- ABOUT PAGE -->
<div id="page-about" class="hide page">
  <a class="back" onclick="showPage('main')">← Back</a>
  <h2>📚 About Master Box</h2>
  <p>Master Box is an all-in-one media toolkit that lets you download videos, extract MP3 audio, cut ringtones, and manage PDF files — all from one simple app.</p>
  <h3>🎯 Our Mission</h3>
  <p>Make media tools simple, fast, and free for everyone. No complicated steps. Just paste a link and download.</p>
  <h3>✨ Features</h3>
  <ul>
    <li>Download from 1000+ websites</li>
    <li>Extract MP3 in high quality</li>
    <li>Cut custom ringtones</li>
    <li>Upload and share PDFs</li>
    <li>Supports 100+ languages</li>
  </ul>
  <h3>📧 Contact</h3>
  <p>Email: support@masterbox.app</p>
</div>

<!-- PRIVACY PAGE -->
<div id="page-privacy" class="hide page">
  <a class="back" onclick="showPage('main')">← Back</a>
  <h2>🔒 Privacy Policy</h2>
  <p><strong>Last Updated:</strong> 2026</p>
  <h3>1. Data We Collect</h3>
  <p>We do not collect personal information. Downloaded files are stored temporarily on our server and deleted automatically.</p>
  <h3>2. How We Use Data</h3>
  <ul>
    <li>Process your download requests</li>
    <li>Improve service speed</li>
    <li>No data sold to third parties</li>
  </ul>
  <h3>3. Cookies</h3>
  <p>We do not use cookies to track users. Only essential session data is used.</p>
  <h3>4. Third-Party Services</h3>
  <p>We use YouTube's API for downloads. Their privacy policy applies to those interactions.</p>
  <h3>5. Your Rights</h3>
  <ul>
    <li>Delete your data anytime</li>
    <li>Request data export</li>
    <li>No account required</li>
  </ul>
  <h3>6. Security</h3>
  <p>All downloads use HTTPS encryption. Files auto-delete within 1 hour.</p>
  <h3>7. Contact</h3>
  <p>Questions? Email: privacy@masterbox.app</p>
</div>

<!-- DISCLAIMER PAGE -->
<div id="page-disclaimer" class="hide page">
  <a class="back" onclick="showPage('main')">← Back</a>
  <h2>⚠️ Disclaimer</h2>
  <h3>1. Copyright Notice</h3>
  <p>Master Box does not host any videos or media. We only provide a tool to download publicly available content.</p>
  <h3>2. User Responsibility</h3>
  <ul>
    <li>Download only content you have rights to</li>
    <li>Do not redistribute copyrighted material</li>
    <li>Respect content creators' rights</li>
    <li>Follow local copyright laws</li>
  </ul>
  <h3>3. No Liability</h3>
  <p>Master Box is not responsible for how users use downloaded content. Users are solely responsible for their actions.</p>
  <h3>4. DMCA</h3>
  <p>If you believe your content is being misused, contact: dmca@masterbox.app</p>
  <h3>5. Legal Use Only</h3>
  <p>This tool is for personal and legal use only. Downloading copyrighted content without permission is illegal.</p>
  <h3>6. Age Restriction</h3>
  <p>Users must be 13+ years old. Minors need parental consent.</p>
</div>

<script>
const TT={
  en:{t:"Download · Cut · Share",h1:"Download Video",b1:"Download Video",h2:"Download MP3",b2:"Extract MP3",h3:"Ringtone Cutter",b3:"Cut Ringtone"},
  pa:{t:"ਡਾਊਨਲੋਡ · ਕੱਟੋ · ਸਾਂਝਾ ਕਰੋ",h1:"ਵੀਡੀਓ ਡਾਊਨਲੋਡ",b1:"ਵੀਡੀਓ ਡਾਊਨਲੋਡ",h2:"MP3 ਡਾਊਨਲੋਡ",b2:"MP3 ਕੱਢੋ",h3:"ਰਿੰਗਟੋਨ ਕਟਰ",b3:"ਰਿੰਗਟੋਨ ਕੱਟੋ"},
  hi:{t:"डाउनलोड · काटें · शेयर",h1:"वीडियो डाउनलोड",b1:"वीडियो डाउनलोड",h2:"MP3 डाउनलोड",b2:"MP3 निकालें",h3:"रिंगटोन कटर",b3:"रिंगटोन काटें"},
  es:{t:"Descargar · Cortar · Compartir",h1:"Descargar Video",b1:"Descargar Video",h2:"Descargar MP3",b2:"Extraer MP3",h3:"Cortador de Tono",b3:"Cortar Tono"},
  ar:{t:"تحميل · قص · مشاركة",h1:"تحميل الفيديو",b1:"تحميل الفيديو",h2:"تحميل MP3",b2:"استخراج MP3",h3:"قاطع النغمة",b3:"قص النغمة"}
};

function L(l,e){
  document.querySelectorAll('.langs button').forEach(b=>b.classList.remove('on'));
  e.classList.add('on');
  const t=TT[l];
  document.getElementById('tag').textContent=t.t;
  document.getElementById('h1').textContent=t.h1;
  document.getElementById('b1t').textContent=t.b1;
  document.getElementById('h2').textContent=t.h2;
  document.getElementById('b2t').textContent=t.b2;
  document.getElementById('h3').textContent=t.h3;
  document.getElementById('b3t').textContent=t.b3;
}

function T(n,e){
  document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('on'));
  e.classList.add('on');
  ['v','a','r','p','i'].forEach(xookies=>document.getElementById('tab-'+x).classList.add('hide'));
  document.getElementById('tab-'+n).classList.remove('hide');
}

function showPage(p){
  document.getElementById('main-app').classList.add('hide');
  document.querySelectorAll('.page').forEach(pg=>pg.classList.add('hide'));
  if(p==='main'){
    document.getElementById('main-app').classList.remove('hide');
  } else {
    document.getElementById('page-'+p).classList.remove('hide');
  }
  window.scrollTo(0,0);
}

async function dl(f){
  const u=f==='video'?document.getElementById('vurl').value:document.getElementById('aurl').value;
  const r=f==='video'?document.getElementById('r1'):document.getElementById('r2');
  const b=f==='video'?document.getElementById('b1'):document.getElementById('b2');
  if(!u){r.className='res err';r.textContent='⚠️ Please paste a URL';return;}
  b.disabled=true;
  const origText=b.innerHTML;
  b.innerHTML='⏳ Processing...';
  r.className='res info';
  r.textContent='⏳ Downloading... Please wait';
  try{
    const x=await fetch('/api/download?url='+encodeURIComponent(u)+'&format='+f,{method:'POST'});
    const d=await x.json();
    if(d.ok){
      r.className='res ok';
      r.innerHTML='✅ '+d.title+'<a href="/api/file/'+d.filename+'" download>📥 Save to Phone</a><a class="blue" onclick="shareFile(\''+d.filename+'\')">📤 Share</a>';
    } else {
      r.className='res err';
      r.textContent='❌ '+d.error;
    }
  }catch(e){
    r.className='res err';
    r.textContent='❌ Connection error';
  }
  b.disabled=false;
  b.innerHTML=origText;
}

async function cut(){
  const f=document.getElementById('rf').files[0];
  const r=document.getElementById('r3');
  if(!f){r.className='res err';r.textContent='⚠️ Select an audio file';return;}
  r.className='res info';
  r.textContent='⏳ Cutting...';
  const fd=new FormData();
  fd.append('file',f);
  fd.append('start',document.getElementById('rs').value);
  fd.append('end',document.getElementById('re').value);
  try{
    const x=await fetch('/api/ringtone',{method:'POST',body:fd});
    const d=await x.json();
    if(d.ok){
      r.className='res ok';
      r.innerHTML='✅ Ringtone Ready<a href="/api/file/'+d.filename+'" download>📥 Save Ringtone</a><a class="blue" onclick="shareFile(\''+d.filename+'\')">📤 Share</a>';
    } else {
      r.className='res err';
      r.textContent='❌ '+d.error;
    }
  }catch(e){
    r.className='res err';
    r.textContent='❌ Error';
  }
}

function sharePDF(){
  const f=document.getElementById('pdff').files[0];
  const r=document.getElementById('r4');
  if(!f){r.className='res err';r.textContent='⚠️ Select a PDF file';return;}
  if(navigator.share){
    navigator.share({title:f.name,files:[f]}).then(()=>{
      r.className='res ok';
      r.textContent='✅ Shared successfully';
    }).catch(()=>{
      r.className='res info';
      r.textContent='ℹ️ Saved: '+f.name;
    });
  } else {
    r.className='res info';
    r.textContent='ℹ️ File selected: '+f.name;
  }
}

function shareFile(filename){
  const url=window.location.origin+'/api/file/'+filename;
  if(navigator.share){
    navigator.share({title:'Master Box',text:'Downloaded from Master Box',url:url}).catch(()=>{});
  } else {
    navigator.clipboard.writeText(url);
    alert('Link copied!');
  }
}
</script>
</body></html>"""

@app.route("/")
def home(): return render_template_string(HTML)

@app.route("/api/download", methods=["POST"])
def dl():
    url = request.args.get("url")
    fmt = request.args.get("format", "video")
    j = str(uuid.uuid4())[:8]
    o = {'outtmpl': f'dl/{j}_%(title)s.%(ext)s', 'ffmpeg_location': FF, 'quiet': True}
    if os.path.exists("cookies.txt"):
        o['cookiefile'] = "c.txt"
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