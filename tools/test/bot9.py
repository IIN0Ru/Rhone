import asyncio, random, json
from playwright.async_api import async_playwright
from common import URL, launch_args, shot
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(**launch_args())
        pg = await b.new_page(viewport={'width':1000,'height':900})
        errs=[]
        pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_timeout(400)
        endings={}; steps=0; scenes=set(); battles=0
        t0=asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time()-t0 < 170:
            steps+=1
            st = await pg.evaluate("({phase:G.phase, lock:G.lock, battle:!!G.battle, scene:G.scene, modal:modalOpen, day:G.day})")
            scenes.add(st['scene'])
            if st['modal']:
                bs = await pg.query_selector_all('#modal [data-mv]:not([disabled])')
                if bs: await random.choice(bs).evaluate('e=>e.click()')
                await pg.wait_for_timeout(60); continue
            if st['phase']=='intro':
                await pg.evaluate("document.querySelector('[data-act=start]').click()"); await pg.evaluate("G.fast=true"); continue
            if st['phase']=='ending':
                e = await pg.evaluate("G.ending"); endings[e]=endings.get(e,0)+1
                await pg.evaluate("document.querySelector('[data-act=restart]').click()"); await pg.wait_for_timeout(200); continue
            if st['lock']: await pg.wait_for_timeout(80); continue
            if st['battle']:
                battles+=1
                arg = 'attack' if random.random()<0.92 else 'retreat'
                btn = await pg.query_selector(f'[data-act=cmd][data-arg={arg}]:not([disabled])')
                if btn: await btn.evaluate('e=>e.click()')
                await pg.wait_for_timeout(60); continue
            if st['scene'].startswith('d'):
                if random.random()<0.03:
                    bt = await pg.query_selector('[data-act=goHome]:not([disabled])')
                    if bt: await bt.click()
                await pg.wait_for_timeout(150); continue
            # 랜덤 상호작용: 순간이동 후 Space
            its = await pg.evaluate("interactables().map(i=>i.x)")
            if not its: await pg.wait_for_timeout(100); continue
            if st['scene']=='town' and random.random()<0.25: its=[3768]
            x = random.choice(its)
            await pg.evaluate(f"G.player.x={x}")
            await pg.wait_for_timeout(30)
            await pg.keyboard.press('Space')
            await pg.wait_for_timeout(60)
        lod = await pg.evaluate('G.lodging')
        print(json.dumps({'lodging':lod,'endings':endings,'steps':steps,'scenes':sorted(scenes),'battleclicks':battles}, ensure_ascii=False))
        print('ERRS', len(errs), list(dict.fromkeys(errs))[:8])
        await b.close()
asyncio.run(main())
