"""Local v3 browser interaction test; test evidence, not user observation data."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).parent
EVIDENCE=ROOT/'evidence'

def run():
    html=(ROOT/'index.html').read_text(encoding='utf-8')
    errors=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':1440,'height':980},device_scale_factor=1)
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.evaluate("""() => { const data={}; Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return Object.prototype.hasOwnProperty.call(data,k)?data[k]:null},setItem(k,v){data[k]=String(v)},removeItem(k){delete data[k]},clear(){Object.keys(data).forEach(k=>delete data[k])}}}) }""")
        page.set_content(html)
        assert page.locator('#page-prepare').is_visible()
        page.screenshot(path=str(EVIDENCE/'01_prepare_v3.png'),full_page=True)
        page.locator('#load-example').click()
        assert '4 terms' in page.locator('#glossary-status').inner_text()
        page.locator('#go-live').click()
        assert page.locator('#page-live').is_visible()
        bounds=page.evaluate("""() => {let a=document.querySelector('#original-slide-heading').closest('.panel').getBoundingClientRect();let b=document.querySelector('.cn-card').getBoundingClientRect();return {english:a.width,chinese:b.width,ratio:a.width/b.width}}""")
        assert bounds['ratio'] > 2.15,bounds
        page.screenshot(path=str(EVIDENCE/'02_live_wide_slide.png'),full_page=True)
        # Select arbitrary text in the slide. The script handles the same browser Selection API as a drag/highlight.
        page.evaluate("""() => { const li=document.querySelector('#english-points li:nth-child(2)'); const text=li.firstChild; const pos=text.textContent.indexOf('standard deviation'); const sel=window.getSelection(); const r=document.createRange(); r.setStart(text,pos); r.setEnd(text,pos+'standard deviation'.length); sel.removeAllRanges();sel.addRange(r);document.querySelector('#slide-content').dispatchEvent(new MouseEvent('mouseup',{bubbles:true})) }""")
        assert 'standard deviation' in page.locator('#selected-preview').inner_text()
        page.locator('#add-selection').click()
        expect(page.locator('#word-term')).to_have_value('standard deviation')
        expect(page.locator('#word-translation')).to_have_value('标准差')
        page.locator('#word-note').fill('Review before the next statistics lecture.')
        page.screenshot(path=str(EVIDENCE/'03_word_editor_open.png'),full_page=True)
        page.locator('#save-selected-word').click()
        expect(page.locator('#word-feedback')).to_contain_text('added to Review')
        expect(page.locator('#nav-count')).to_contain_text('1')
        page.screenshot(path=str(EVIDENCE/'03_selected_term_saved.png'),full_page=True)
        # Manually add any term, including vocabulary not in sample glossary.
        page.locator('#add-selection').click()
        page.locator('#word-term').fill('likelihood')
        page.locator('#word-translation').fill('似然')
        page.locator('#word-note').fill('A term to revisit after class.')
        page.locator('#save-selected-word').click()
        expect(page.locator('#nav-count')).to_contain_text('2')
        # Duplication should be handled cleanly.
        page.locator('#add-selection').click()
        page.locator('#word-term').fill('likelihood')
        page.locator('#save-selected-word').click()
        expect(page.locator('#word-feedback')).to_contain_text('already')
        page.locator('#cancel-selected-word').click()
        page.locator('[data-page="review"]').click()
        expect(page.locator('#saved-total')).to_have_text('2')
        assert page.locator('.reviewcard').count()==2
        assert page.get_by_text('standard deviation',exact=True).count()>=1
        page.screenshot(path=str(EVIDENCE/'04_review_vocab.png'),full_page=True)
        page.locator('.reviewcard').first.get_by_role('button',name='Reveal explanation').click()
        expect(page.locator('.reviewcard').first).to_contain_text('似然')
        page.locator('.reviewcard').first.get_by_role('button',name='Mark as understood').click()
        expect(page.locator('#known-total')).to_have_text('1')
        # Existing captions and decisions still work.
        page.locator('[data-page="live"]').click()
        page.locator('#slide-selector').select_option('gradient')
        page.locator('#correction-panel summary').first.click()
        page.locator('#check-evidence').click()
        page.locator('#accept-correction').click()
        assert '上升最快' in page.locator('#chinese-caption').inner_text()
        page.locator('#restart-example').click()
        assert '下降最快' in page.locator('#chinese-caption').inner_text()
        page.locator('#slide-selector').select_option('overfit')
        page.locator('#check-evidence').click()
        page.locator('#reject-correction').click()
        expect(page.locator('#correction-state')).to_contain_text('original caption retained')
        page.locator('#slide-selector').select_option('recall')
        assert page.locator('#check-evidence').is_disabled()
        page.locator('#save-later').click()
        page.locator('[data-page="review"]').click()
        expect(page.locator('#saved-total')).to_have_text('3')
        # Storage retains both user-selected words and review status.
        review_key='iis-a2-lecture-companion-v2-review'
        stored=page.evaluate("key=>localStorage.getItem(key)",review_key)
        assert 'word-normal-standard deviation' in stored and 'likelihood' in stored and 'known' in stored
        # Mobile layout remains usable.
        mobile=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
        mobile.on('pageerror',lambda err: errors.append(str(err)))
        mobile.evaluate("""(saved) => { const data={'iis-a2-lecture-companion-v2-review':saved}; Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return Object.prototype.hasOwnProperty.call(data,k)?data[k]:null},setItem(k,v){data[k]=String(v)},removeItem(k){delete data[k]},clear(){Object.keys(data).forEach(k=>delete data[k])}}}) }""",stored)
        mobile.set_content(html)
        mobile.locator('[data-page="live"]').click()
        assert mobile.locator('#slide-content').is_visible()
        assert mobile.locator('#add-selection').is_visible()
        mobile.screenshot(path=str(EVIDENCE/'05_live_mobile.png'),full_page=True)
        mobile.locator('[data-page="review"]').click()
        expect(mobile.locator('#saved-total')).to_have_text('3')
        assert not errors, errors
        print('PASS: 25+ interaction and data-flow assertions; English/Chinese width ratio %.2f:1; 5 screenshots; no JS errors' % bounds['ratio'])
        browser.close()

if __name__=='__main__': run()
