#!/usr/bin/env python3
"""Build single-file standalone HTML for publishing."""
import base64
import re
from pathlib import Path

ROOT = Path(__file__).parent
MAIN = ROOT / "-泡泡宇宙-信息茧房互动体验.html"
GAME = ROOT / "-信息茧房体验馆.html"
IMG = ROOT / "ChatGPT Image Jun 14, 2026, 10_13_42 PM.png"
OUT = ROOT / "index.html"

main = MAIN.read_text(encoding="utf-8")
game_b64 = base64.b64encode(GAME.read_bytes()).decode("ascii")
img_b64 = base64.b64encode(IMG.read_bytes()).decode("ascii")
img_data = f"data:image/png;base64,{img_b64}"

main = main.replace(
    "ChatGPT Image Jun 14, 2026, 10_13_42 PM.png",
    img_data,
)

main = main.replace(
    '<iframe id="gameFrame" src="-信息茧房体验馆.html?lang=cn" title="茧房迷宫互动游戏"></iframe>',
    '<iframe id="gameFrame" title="茧房迷宫互动游戏"></iframe>',
)

embed_script = f"""
<script id="bubble-game-b64" type="application/json">{game_b64}</script>
<script>
var gameBlobUrl=null;
function getGameBlobUrl(){{
  if(gameBlobUrl)return gameBlobUrl;
  var b64=document.getElementById('bubble-game-b64').textContent;
  var bin=atob(b64);
  var bytes=new Uint8Array(bin.length);
  for(var i=0;i<bin.length;i++)bytes[i]=bin.charCodeAt(i);
  gameBlobUrl=URL.createObjectURL(new Blob([bytes],{{type:'text/html;charset=utf-8'}}));
  return gameBlobUrl;
}}
function loadGameFrame(lang){{
  var f=document.getElementById('gameFrame');
  if(!f)return;
  if(f.getAttribute('data-loaded')!=='1'){{
    f.src=getGameBlobUrl();
    f.setAttribute('data-loaded','1');
    f.onload=function(){{try{{syncGameLang(lang)}}catch(e){{}}}};
  }}else{{try{{syncGameLang(lang)}}catch(e){{}}}}
}}
</script>
"""

main = main.replace("<script>", embed_script + "<script>", 1)

main = re.sub(
    r"if\(f\)f\.src='-信息茧房体验馆\.html\?lang='\+lang;",
    "loadGameFrame(lang);",
    main,
)

main = main.replace(
    "function setLang(l){\n"
    "  document.body.className='lang-'+l;\n"
    "  document.getElementById('btnCn').classList.toggle('on',l==='cn');\n"
    "  document.getElementById('btnEn').classList.toggle('on',l==='en');\n"
    "  if(currentView==='game') syncGameLang(l);\n"
    "  else{\n"
    "    var f=document.getElementById('gameFrame');\n"
    "    if(f)f.src='-信息茧房体验馆.html?lang='+l;\n"
    "  }\n"
    "}",
    "function setLang(l){\n"
    "  document.body.className='lang-'+l;\n"
    "  document.getElementById('btnCn').classList.toggle('on',l==='cn');\n"
    "  document.getElementById('btnEn').classList.toggle('on',l==='en');\n"
    "  if(currentView==='game') syncGameLang(l);\n"
    "}",
)

OUT.write_text(main, encoding="utf-8")
size_mb = OUT.stat().st_size / (1024 * 1024)
print(f"Written: {OUT.name} ({size_mb:.2f} MB)")
