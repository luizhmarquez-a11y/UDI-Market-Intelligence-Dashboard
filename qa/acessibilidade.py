import json,hashlib,threading
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/"docs/index.html"
ROUTES=("visao","setores","indicadores","movimentos","auditoria","fontes","relatorio")
URL="http://127.0.0.1:8765/"
EXPECTED="7598e5cc21e8d897906acef26ba391da5050b8bb21418a6e6d949736937dd239"
assert hashlib.sha256(HTML.read_bytes()).hexdigest()==EXPECTED
server=ThreadingHTTPServer(("127.0.0.1",8765),partial(SimpleHTTPRequestHandler,directory=str(ROOT/"docs")))
threading.Thread(target=server.serve_forever,daemon=True).start()
rows=[]
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for w,h in [(1440,900),(390,844)]:
            ctx=browser.new_context(viewport={"width":w,"height":h},reduced_motion="reduce",has_touch=w<500)
            ctx.route("**/*",lambda r:r.continue_() if r.request.url.startswith(URL) else r.abort())
            page=ctx.new_page()
            for route in ROUTES:
                page.goto(URL+"#"+route,wait_until="load")
                page.wait_for_selector("#screen h1")
                page.add_script_tag(path=str(ROOT/"node_modules/axe-core/axe.min.js"))
                result=page.evaluate("""async () => await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}})""")
                def compact(items):
                    return [{"id":x["id"],"impact":x.get("impact"),"nodes":[{"target":n["target"],"summary":n.get("failureSummary","")} for n in x["nodes"]]} for x in items]
                row={"width":w,"route":route,"passes":len(result["passes"]),"violations":compact(result["violations"]),"incomplete":compact(result["incomplete"]),"overflow":page.evaluate("document.documentElement.scrollWidth>window.innerWidth+1")}
                rows.append(row)
                print(json.dumps({"width":w,"route":route,"violation_ids":[i["id"] for i in row["violations"]],"incomplete_ids":[i["id"] for i in row["incomplete"]],"overflow":row["overflow"]}),flush=True)
            ctx.close()
        ctx=browser.new_context(viewport={"width":1440,"height":900},reduced_motion="reduce")
        page=ctx.new_page()
        page.goto(URL+"#visao")
        page.wait_for_selector("#screen h1")
        keyboard=[]
        # Tab navigation from initial document and Enter activation of a focusable nav control.
        page.keyboard.press("Tab")
        keyboard.append({"first_focus":page.evaluate("document.activeElement.outerHTML.slice(0,250)")})
        target=page.locator('#nav [data-go="setores"]')
        target.focus()
        page.keyboard.press("Enter")
        assert page.locator('#nav [data-go="setores"][aria-current="page"]').count()==1
        assert page.evaluate("document.activeElement.id")=="screen"
        keyboard.append({"desktop_navigation_enter":True,"focus_after_navigation":"screen"})
        select=page.locator("#filter-group")
        select.focus()
        page.keyboard.press("Home")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        keyboard.append({"filter_keyboard_focus":page.evaluate("document.activeElement.id"),"filter_value":page.locator("#filter-group").input_value()})
        ctx.close()
        browser.close()
    out={"sha256_html":EXPECTED,"axe_version":"4.10.3","routes":len(rows),"confirmed_violations":sum(len(x["violations"]) for x in rows),"incomplete_rule_instances":sum(len(x["incomplete"]) for x in rows),"keyboard":keyboard,"details":rows,"limitations":"Automated axe and targeted keyboard checks only; manual contrast, screen readers, physical devices and full WCAG conformance not certified."}
    (ROOT/"acessibilidade-qa.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in out.items() if k!="details"},ensure_ascii=False),flush=True)
finally:
    server.shutdown()
