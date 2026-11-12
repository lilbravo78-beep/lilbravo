"""Automated browser smoke checks for v4 (AI-generated test code, not a user study)."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).parent
EVIDENCE=ROOT/'evidence'
EVIDENCE.mkdir(exist_ok=True)


def select_text(page, phrase):
    # Interact with the same browser text selection API as a user highlighting words.
    page.evaluate("""phrase => {
      const elements=[...document.querySelectorAll('#slide-content li, #slide-title')];
      const elem=elements.find(e=>e.textContent.toLowerCase().includes(phrase.toLowerCase()));
      if(!elem)throw Error('Target not on demo slide: '+phrase);
      const node=elem.firstChild;const start=node.textContent.toLowerCase().indexOf(phrase.toLowerCase());
      const range=document.createRange();range.setStart(node,start);range.setEnd(node,start+phrase.length);
      const sel=window.getSelection();sel.removeAllRanges();sel.addRange(range);
      document.getElementById('slide-content').dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));
    }""",phrase)


def run():
    errors=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        context=browser.new_context(viewport={'width':1420,'height':960},device_scale_factor=1)
        page=context.new_page()
        page.on('pageerror',lambda error:errors.append(str(error)))
        html=ROOT.joinpath('index.html').read_text(encoding='utf-8')
        page.evaluate("""() => { const data={}; Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return Object.prototype.hasOwnProperty.call(data,k)?data[k]:null},setItem(k,v){data[k]=String(v)},removeItem(k){delete data[k]},clear(){Object.keys(data).forEach(k=>delete data[k])}}}) }""")
        page.set_content(html)
        assert page.locator('#page-prepare').is_visible()
        page.locator('#load-example').click()
        expect(page.locator('#glossary-status')).to_contain_text('4 terms')
        page.screenshot(path=str(EVIDENCE/'v4_01_prepare.png'),full_page=True)

        page.locator('#go-live').click()
        bounds=page.evaluate("""() => {const a=document.querySelector('#original-slide-heading').closest('.panel').getBoundingClientRect(); const b=document.querySelector('.cn-card').getBoundingClientRect();return a.width/b.width} """)
        assert bounds>2.15,bounds
        select_text(page,'standard deviation')
        expect(page.locator('#selected-meaning')).to_contain_text('标准差')
        expect(page.locator('#selected-meaning')).to_contain_text('Prepared slide glossary')
        page.screenshot(path=str(EVIDENCE/'v4_02_live_auto_meaning.png'),full_page=True)
        page.locator('#add-selection').click()
        expect(page.locator('#word-term')).to_have_value('standard deviation')
        expect(page.locator('#word-translation')).to_have_value('标准差')
        page.locator('#word-translation').fill('标准差（我的释义）')
        page.locator('#word-note').fill('Revisit after class')
        page.screenshot(path=str(EVIDENCE/'v4_03_editable_meaning.png'),full_page=True)
        page.locator('#save-selected-word').click()
        expect(page.locator('#word-feedback')).to_contain_text('added to Review')
        page.locator('[data-page="review"]').click()
        expect(page.locator('#saved-total')).to_have_text('1')
        expect(page.locator('#caption-total')).to_have_text('0')
        page.locator('#review-cards .reviewcard').first.get_by_role('button',name='Reveal explanation').click()
        expect(page.locator('#review-cards .reviewcard').first).to_contain_text('标准差（我的释义）')
        page.screenshot(path=str(EVIDENCE/'v4_04_vocabulary_review.png'),full_page=True)

        # Scripted AI flag appears automatically in a separate caption-review list.
        page.locator('[data-page="live"]').click()
        page.locator('#slide-selector').select_option('gradient')
        expect(page.locator('#caption-total')).to_have_text('1')
        page.locator('#correction-panel').evaluate('(node)=>node.open=true')
        page.locator('#save-later').click()
        expect(page.locator('#correction-state')).to_contain_text('Pending in Caption Correction Review')
        page.locator('[data-page="review"]').click()
        expect(page.locator('#saved-total')).to_have_text('1')
        expect(page.locator('#caption-pending')).to_have_text('1')
        expect(page.locator('#caption-cards .caption-card')).to_have_count(1)
        expect(page.locator('#caption-cards')).to_contain_text('梯度指向函数下降最快的方向')
        expect(page.locator('#caption-cards')).to_contain_text('梯度指向函数上升最快的方向')
        accept=page.locator('#caption-cards .caption-card').first.get_by_role('button',name='Accept correction')
        assert accept.is_disabled()
        page.locator('#caption-cards .caption-card').first.get_by_role('button',name='Review evidence').click()
        assert accept.is_enabled()
        page.screenshot(path=str(EVIDENCE/'v4_05_caption_review_pending.png'),full_page=True)
        accept.click()
        expect(page.locator('#caption-reviewed')).to_have_text('1')
        expect(page.locator('#caption-cards .caption-card').first).to_contain_text('Accepted')
        page.locator('[data-page="live"]').click()
        expect(page.locator('#chinese-caption')).to_contain_text('上升最快')

        # The incorrect overfitting flag can be rejected after saving.
        page.locator('#slide-selector').select_option('overfit')
        expect(page.locator('#caption-total')).to_have_text('2')
        page.locator('[data-page="review"]').click()
        page.locator('#caption-cards .caption-card').first.get_by_role('button',name='Reject suggestion').click()
        expect(page.locator('#caption-reviewed')).to_have_text('2')
        expect(page.locator('#caption-cards .caption-card').first).to_contain_text('Rejected')

        # No supporting evidence -> remain pending and cannot accept.
        page.locator('[data-page="live"]').click()
        page.locator('#slide-selector').select_option('recall')
        expect(page.locator('#caption-total')).to_have_text('3')
        page.locator('[data-page="review"]').click()
        recall_card=page.locator('#caption-cards .caption-card').first
        expect(recall_card).to_contain_text('No correction proposed')
        recall_card.get_by_role('button',name='Review evidence').click()
        assert recall_card.get_by_role('button',name='Accept correction').is_disabled()
        recall_card.get_by_role('button',name='Keep pending').click()
        expect(page.locator('#caption-pending')).to_have_text('1')
        page.screenshot(path=str(EVIDENCE/'v4_06_two_review_lists.png'),full_page=True)

        # Unknown selection receives an honest fallback; user can supply a meaning.
        page.locator('[data-page="live"]').click()
        page.locator('#slide-selector').select_option('normal')
        select_text(page,'spread')
        expect(page.locator('#selected-meaning')).to_contain_text('No matching Chinese meaning')
        page.locator('#add-selection').click()
        page.locator('#word-term').fill('likelihood')
        page.locator('#word-translation').fill('似然')
        page.locator('#save-selected-word').click()
        expect(page.locator('#saved-total')).to_have_text('2')

        # Reconstruct a fresh document with the recorded localStorage contents.
        # The sandbox browser blocks file:// and localhost navigation, so native reload
        # is unavailable in automated tests; manual browser refresh should be checked separately.
        stored_json=page.evaluate("""() => ({
          'iis-a2-lecture-companion-v2-review':localStorage.getItem('iis-a2-lecture-companion-v2-review'),
          'iis-a2-lecture-companion-v2-glossary':localStorage.getItem('iis-a2-lecture-companion-v2-glossary')
        })""")
        fresh=context.new_page()
        fresh.on('pageerror',lambda error:errors.append(str(error)))
        fresh.evaluate("""initial => {const data={...initial};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return Object.prototype.hasOwnProperty.call(data,k)?data[k]:null},setItem(k,v){data[k]=String(v)},removeItem(k){delete data[k]},clear(){Object.keys(data).forEach(k=>delete data[k])}}})}""",stored_json)
        fresh.set_content(html)
        page=fresh
        page.locator('[data-page="review"]').click()
        expect(page.locator('#saved-total')).to_have_text('2')
        expect(page.locator('#caption-total')).to_have_text('3')
        expect(page.locator('#caption-reviewed')).to_have_text('2')
        expect(page.locator('#caption-pending')).to_have_text('1')
        page.screenshot(path=str(EVIDENCE/'v4_07_persisted_after_reload.png'),full_page=True)

        # Mobile layout can access both review lists without horizontal scrolling.
        mobile=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1)
        mob=mobile.new_page();mob.on('pageerror',lambda error:errors.append(str(error)))
        mob.evaluate("""() => { const data={}; Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return Object.prototype.hasOwnProperty.call(data,k)?data[k]:null},setItem(k,v){data[k]=String(v)},removeItem(k){delete data[k]},clear(){Object.keys(data).forEach(k=>delete data[k])}}}) }""")
        mob.set_content(html)
        mob.locator('[data-page="live"]').click()
        assert mob.locator('#slide-content').is_visible()
        mob.locator('#slide-selector').select_option('gradient')
        mob.locator('[data-page="review"]').click()
        expect(mob.locator('#caption-cards .caption-card')).to_have_count(1)
        page_width=mob.evaluate('document.documentElement.scrollWidth')
        assert page_width<=390, f'horizontal overflow: {page_width}'
        mob.screenshot(path=str(EVIDENCE/'v4_08_mobile_review.png'),full_page=True)
        assert not errors,errors
        print('PASS: glossary import; v4 direct meaning; edit+save; separate review lists; caption auto-archive; accept/reject/pending; no-evidence guard; reload persistence; mobile no overflow; zero JS errors')
        browser.close()

if __name__=='__main__':run()
