"""Capture and validate the actual standalone portfolio dashboard, never deploy."""
import csv
import hashlib
import json
import re
import subprocess
import tempfile
import threading
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/"docs/index.html"
ROUTES=("visao","setores","indicadores","movimentos","auditoria","fontes","relatorio")
ASSETS=ROOT/"assets"
URL="http://127.0.0.1:8765/"
def check(value,message):
    if not value: raise AssertionError(message)
def goto(page,route):
    page.goto(URL+"#"+route,wait_until="load")
    page.wait_for_selector("#screen h1")
    check(page.locator("#nav [data-go]").count()==7,"navigation")
    check(page.locator('#nav [data-go="'+route+'"][aria-current="page"]').count()==1,"active route")
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
def nav(page,route):
    if route in ("auditoria","fontes") and page.locator(".nav-accordion").get_attribute("open") is None:
        page.locator('summary[data-toggle="info"]').click()
    page.locator('#nav [data-go="'+route+'"]').click()
    check(page.locator('#nav [data-go="'+route+'"][aria-current="page"]').count()==1,"navigation click")
def no_external(route):
    if route.request.url.startswith(URL): route.continue_()
    else: route.abort()
def setup(ctx):
    ctx.route("**/*",no_external)
    page=ctx.new_page()
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    return page,errors

def main():
    text=HTML.read_text("utf-8")
    data=json.loads(re.search(r'<script id="udi-data" type="application/json">([\s\S]*?)</script>',text).group(1))
    check(len(data["metrics"])==25 and all(x["nivel"].startswith("P2_") for x in data["metrics"]),"P2 data")
    check(len(data["taxonomy"])==82 and len(data["events"])==38 and len(data["bulletins"])==29 and len(data["alerts"])==7 and data["finalAudit"]["series_setoriais_P4"]==0,"scope")
    check(not re.search(r'(?i)(?:gh[pousr]_[a-z0-9]{20,}|github_pat_[a-z0-9_]{20,}|sk-[a-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})',text),"sensitive pattern")
    for folder in ("screenshots","gifs","videos"):
        (ASSETS/folder).mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(("127.0.0.1",8765),partial(SimpleHTTPRequestHandler,directory=str(ROOT/"docs")))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    results=[]
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            for w,h,tag in [(1440,900,"desktop"),(390,844,"mobile"),(320,800,"compact")]:
                ctx=browser.new_context(viewport={"width":w,"height":h},has_touch=w<500,device_scale_factor=1,reduced_motion="reduce",accept_downloads=True)
                page,errors=setup(ctx)
                for route in ROUTES:
                    goto(page,route)
                    check(page.evaluate("document.documentElement.scrollWidth")<=w+1,f"overflow {w} {route}")
                    check(len(page.locator("#screen").inner_text())>200,f"empty {route}")
                    if tag!="compact":page.screenshot(path=str(ASSETS/"screenshots"/f"{tag}-{route}.png"),full_page=False,animations="disabled")
                    results.append({"width":w,"route":route,"status":"OK"})
                goto(page,"setores")
                page.locator("#filter-group").select_option(label="Saúde")
                page.locator("#filter-segment").select_option(label="Hospitais")
                check("CNES" in page.locator("#screen").inner_text(),"filter")
                goto(page,"movimentos")
                page.locator("#filter-eventPeriod").select_option(label="Só após set/2026")
                page.get_by_placeholder("Ex.: Ambev, investimento, saúde").fill("PlanejaUdi")
                check("1 registros encontrados" in page.locator("#screen").inner_text(),"search")
                goto(page,"indicadores")
                page.locator("[data-export=metrics]").evaluate("(el)=>el.scrollIntoView({block:'center',behavior:'instant'})")
                with page.expect_download() as dl: page.locator("[data-export=metrics]").click()
                with dl.value.path().open(encoding="utf-8-sig",newline="") as f: records=list(csv.DictReader(f))
                ids={x["id"]:x for x in records}
                check(len(records)==25 and ids["EMPREG-saldo_agro"]["valor"]=="-4" and ids["COMEX-2026-IMP-OUT"]["valor"]=="183.304529" and ids["COMEX-2026-EXP-OUT"]["valor"]=="1213.695882" and ids["COMEX-2026-SAL-OUT"]["valor"]=="1030.391353","export CSV")
                goto(page,"relatorio")
                page.locator("[data-export=reporthtml]").evaluate("(el)=>el.scrollIntoView({block:'center',behavior:'instant'})")
                with page.expect_download() as dl: page.locator("[data-export=reporthtml]").click()
                check(dl.value.suggested_filename.endswith(".html"),"report")
                check(not errors,str(errors))
                ctx.close()
            with tempfile.TemporaryDirectory() as tmp:
                ctx=browser.new_context(viewport={"width":1440,"height":900},device_scale_factor=1,record_video_dir=tmp,record_video_size={"width":1440,"height":900},reduced_motion="reduce")
                page,errors=setup(ctx)
                goto(page,"visao");page.wait_for_timeout(6000)
                page.mouse.move(1140,750);page.mouse.wheel(0,555);page.wait_for_timeout(5000)
                nav(page,"indicadores");page.wait_for_timeout(6000)
                page.mouse.move(1120,750);page.mouse.wheel(0,430);page.wait_for_timeout(5000)
                nav(page,"setores");page.wait_for_timeout(3000)
                page.locator("#filter-group").select_option(label="Saúde");page.wait_for_timeout(3000)
                page.locator("#filter-segment").select_option(label="Hospitais");page.wait_for_timeout(6000)
                nav(page,"movimentos");page.wait_for_timeout(3000)
                page.locator("#filter-eventPeriod").select_option(label="Só após set/2026");page.wait_for_timeout(3000)
                page.get_by_placeholder("Ex.: Ambev, investimento, saúde").fill("PlanejaUdi");page.wait_for_timeout(4000)
                nav(page,"auditoria");page.wait_for_timeout(6000)
                page.mouse.move(1140,750);page.mouse.wheel(0,550);page.wait_for_timeout(4000)
                nav(page,"fontes");page.wait_for_timeout(5000)
                nav(page,"relatorio");page.wait_for_timeout(6000)
                nav(page,"visao");page.wait_for_timeout(5000)
                check(not errors,str(errors))
                video=page.video;ctx.close()
                source=video.path()
                out=ASSETS/"videos"/"demonstracao-udi-beta.mp4"
                subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-t","85","-vf","scale=1280:800,fps=25","-c:v","libx264","-preset","fast","-crf","22","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],check=True)
                length=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(out)],text=True))
                check(60<=length<=90,f"duration {length}")
                gif=ASSETS/"gifs"/"navegacao-e-filtros.gif"
                subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss","24","-t","12","-i",str(out),"-filter_complex","fps=8,scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse","-loop","0",str(gif)],check=True)
                check(out.stat().st_size<95_000_000 and gif.stat().st_size<20_000_000,"media size")
            browser.close()
        result={"status":"OK","sha256_html":hashlib.sha256(HTML.read_bytes()).hexdigest(),"cenarios":len(results),"screenshots":14,"video_segundos":length,"video_bytes":out.stat().st_size,"gif_bytes":gif.stat().st_size,"checks":results,"limites":"Chromium automatizado; sem dispositivos físicos nem certificação WCAG; sem publicação"}
        (ROOT/"qa-media-result.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
        print(json.dumps(result,ensure_ascii=False))
    finally:
        server.shutdown()
if __name__=="__main__":main()
