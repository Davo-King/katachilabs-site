from playwright.sync_api import sync_playwright
pages={"home":"/","labs":"/labs/","labs-bookmark-plus":"/labs/bookmark-plus/","privacy":"/bookmark-plus/privacy/","consultancy":"/consultancy/","contact":"/contact/","404":"/404.html","bookmark-plus":"/bookmark-plus/"}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
    for n,u in pages.items():
        for w,suf in((1280,"1280"),(390,"390")):
            pg=b.new_page(viewport={"width":w,"height":900})
            pg.goto("http://localhost:8765"+u);pg.wait_for_load_state("networkidle");pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,80))}window.scrollTo(0,0)}");pg.wait_for_load_state("networkidle");pg.wait_for_timeout(500)
            print(n,w,"imgs broken:",pg.evaluate("[...document.images].filter(i=>!i.complete||i.naturalWidth==0).length"))
            sw=pg.evaluate("document.documentElement.scrollWidth")
            print(n,w,"scrollWidth",sw,"OVERFLOW" if sw>w else "ok")
            pg.screenshot(path=f"_shots/{n}-{suf}.png",full_page=True);pg.close()
    b.close()
