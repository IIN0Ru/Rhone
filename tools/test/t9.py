import asyncio
from playwright.async_api import async_playwright
URL=''+__import__('pathlib').Path(__file__).resolve().parents[2].joinpath('prototype','index.html').as_uri()+''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width':1100,'height':690})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
        await pg.goto(URL); await pg.wait_for_timeout(800)
        await pg.evaluate("document.querySelector('[data-act=start]').click()"); await pg.wait_for_timeout(500); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300)
        await pg.evaluate("G.party.push(newMember('bark')); G.player.bhp=400; G.player.hp=400; G.party.forEach(m=>{m.bhp=400;m.hp=400})")
        await pg.evaluate("goScene('town',3768)"); await pg.wait_for_timeout(200); await pg.keyboard.press('Space'); await pg.wait_for_timeout(300)
        if await pg.evaluate('modalOpen'): await pg.keyboard.press('Enter')
        await pg.wait_for_timeout(900); await pg.screenshot(path='d_walk.png')
        shots={'d1':0,'d2':0,'d3':0}; knight=False
        for i in range(900):
            st = await pg.evaluate("({b:!!G.battle,l:G.lock,m:modalOpen,ph:G.phase,s:G.scene,x:G.player.x})")
            if st['ph']!='world': break
            if st['b'] and st['s'] in shots and shots[st['s']]<1 and not st['l']:
                await pg.wait_for_timeout(400); await pg.screenshot(path=f"d_{st['s']}_battle.png"); shots[st['s']]+=1
            if st['m']:
                t = await pg.evaluate("document.querySelector('#modalBox').innerText")
                if '쇠사슬' in t and not knight:
                    knight=True; await pg.screenshot(path='d_knight.png')
                await pg.keyboard.press('Enter'); await pg.wait_for_timeout(120); continue
            if st['b'] and not st['l']: await pg.keyboard.press('Space')
            if st['s']=='town' and i>30: break
            await pg.wait_for_timeout(90)
        print('end', await pg.evaluate("({scene:G.scene,phase:G.phase,ending:G.ending})"))
        print('ERRS', errs[:5]); await b.close()
asyncio.run(main())
