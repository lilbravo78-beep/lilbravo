# Lecture Companion — IIS A2 prototype v4

An offline interactive prototype for students who use English as a second language in university STEM lectures. **Live is the core stage**; Prepare supports it with terminology, and Review allows students to revisit words and potentially incorrect captions without interrupting the lecture.

## Run it

Unzip the folder, open `IIS_A2_Prototype_v4`, and double-click **`index.html`**. Tested in an automated Chromium environment; intended for current Chrome, Edge and Safari. No server, internet connection, API key, installation, or real microphone is needed. Browser-local data can be cleared by the browser or a reset action, and may be isolated by file path or origin.

## Demonstration walkthrough

1. **Prepare:** Select `sample_glossary.csv` or click **Load sample glossary**. Its entries appear in the table. PDF uploads can be previewed locally; they are **not parsed** into new lecture content.
2. **Live — word and meaning:** Open **Normal distribution**, highlight **standard deviation** in the English slide. The word **and its Chinese meaning (标准差)** appear immediately in the vocabulary strip below the slide, using the built-in demo glossary. Click **+ Add a word**: the meaning is pre-filled and **editable**. Change it if desired and click **Save to Review**. For words without a match in the uploaded or built-in glossary, the prototype says no meaning was found; students can enter a meaning themselves. No automatic AI dictionary/translation service is connected.
3. **Review — vocabulary:** Under **Vocabulary Review**, reveal the saved meaning, mark a term as understood, or remove it. Words and concepts are stored separately from caption flags.
4. **Live — caption flag:** Choose **Gradient direction**. The scripted flag is **automatically recorded** in **Caption Correction Review** without forcing an immediate choice. Expand **Caption review** and click **Save for later**, or simply continue to Review. (The simulated AI suggestions are fixed examples.)
5. **Review — correction:** Under **Caption Correction Review**, inspect the original Chinese subtitle, suggested change and prepared evidence. Click **Review evidence** before using **Accept correction**. You can also **Reject suggestion** or **Keep pending**. An accepted correction is reflected in the demo caption when you return to its slide in Live.
6. **Other cases:** Open **Overfitting** to see a false AI suggestion that students can reject. Open **Recall** to see an insufficient-evidence case. No correction is proposed there, so **Accept** stays unavailable; the record may remain pending.
7. **Persistence:** Refresh in your browser and reopen Review. The vocabulary and caption decisions should remain, subject to the browser's localStorage rules.

## Implemented locally

- Three-stage Prepare / Live / Review navigation.
- CSV glossary import, preview, clearing and storage.
- Browser PDF preview (not text extraction or analysis).
- Prepared wide English demo slides and brief Chinese explanations.
- Text selection in the English slide, **immediate Chinese-meaning lookup in the imported glossary or the matching prepared slide terminology**, editable before saving. Unmatched terms are explicitly marked as such; arbitrary new meanings are not generated.
- **Vocabulary Review**, including saved meaning, notes, source-slide label, understood status, removal and browser storage.
- **Caption Correction Review**, as an independent list. Flagged examples are recorded on first visit; the stored record includes the original subtitle, proposed change, evidence text/source when available, and pending/accepted/rejected status. Decisions persist in localStorage. Existing v2/v3 records are reused where available.
- Scripted Live correction controls (evidence, accept, reject, defer, restart); accepted decisions can be restored in Live after returning to a slide.
- Responsive layout, including narrow mobile-sized browser windows.

## Simulated vs planned

**Simulated / prepared:** English lecture excerpts, Chinese captions and support notes, slide evidence, and the three AI warning scenarios. The app does **not** use real-time speech recognition, translation or AI reasoning. Flag detection is a scripted demonstration, not an accuracy claim. The sample glossary and built-in terminology supply known Chinese meanings.

**Not implemented / future work:** Automatic understanding of uploaded slides; live speech-to-text and simultaneous translation; semantic checking against the uploaded course materials; reliable arbitrary-word definitions; pronunciation playback; jump-back to the exact original slide; recording/transcript playback or lecturer-accent practice; automatic identification of teacher-spoken example sentences; remote user accounts and synchronisation; ChatGPT knowledge assistance. These should be marked **planned**, not implemented, in the report and system diagram.

**Important design constraint:** Slide–caption disagreement is only a possible inconsistency, not proof of a translation error. For the Recall case, there is insufficient evidence to support an automatic correction.

## Materials and attribution

- The Normal distribution and paired t-test demo summaries were adapted from the student's supplied statistics bilingual study aid (`EMS2026_Lecture_2_English_Main_中文辅助理解版(3).pdf`, relevant study-aid pages 7–10, 31–32).
- The informed consent summary was adapted from the supplied ethics bilingual study aid (`EMS2026_Lecture_4_English_Main_中文辅助理解版_模板一致(1).pdf`, relevant pages 15–19).
- Gradient, Overfitting and Recall are fictional, prepared computing examples adapted from the earlier A2 prototype.
- The visible slides are **newly written demonstration summaries, not copied original slide images**. Source lecture PDFs are **not distributed** in this package and should not be uploaded to public GitHub without permission.

## Development, testing, and AI disclosure

Version progression: v1 scripted caption correction; v2 added Prepare / Live / Review; v3 enlarged the English slide and allowed manual vocabulary selection and save; **v4** separated vocabulary and caption Review, automatically logged caption flags, added persistent Accept/Reject/Pending status, and showed glossary-based Chinese meanings as soon as a term is highlighted, with an editable field before saving. See `WHAT_CHANGED.md` for the v4 change record. Earlier v1–v3 work was not reconstructed as Git commits; do not present it as Git commit history if it was not committed at the time.

**AI assistance:** ChatGPT generated and revised prototype code, documentation and automated browser-test scripts in response to the student's design requests. The user developed the interaction requirements and assessed the design. Automated screenshots and test assertions are **not independent user-study data**. The student should perform and document their own final hands-on verification before coursework submission.

**Developer verification:** In an environment with Python, Playwright and Chromium, run `python test_prototype.py`. The test uses a Chromium browser and mocks localStorage to reconstruct a fresh document because the test sandbox prohibits navigation to local files and loopback URLs. It is an implementation smoke test, **not** a real-world learning evaluation. `evidence/v4_*.png` are generated browser screenshots. `evidence/v4_smoke_test_summary.txt` reports the checked cases. Old `evidence/0*.png` are historical v3 screenshots and should not be mistaken for v4 screenshots.

## Coursework reminder

The report and architecture diagram must distinguish implemented interactions from prepared AI demonstrations and future ideas. The assessed artifact is the current repository commit containing **v4**, not an imagined complete live-translation service.
