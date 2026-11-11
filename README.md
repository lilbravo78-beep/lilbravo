# Lecture Companion — IIS A2 prototype v3

An offline interaction prototype for second-language students following English-medium STEM lectures. It shows how course materials, short Chinese support notes, and student-controlled vocabulary review could fit into the same learning journey.

## Open the prototype

Unzip the folder and double-click `index.html`. Use Chrome, Edge, or Safari. No internet connection, API key, or installation is required.

## What to try

1. **Prepare** — Load the sample glossary or import `sample_glossary.csv`. You can also choose a PDF to preview it in your browser.
2. **Live** — Open the **Normal distribution** example. The English slide occupies around 73% of the slide area; Chinese support notes take the remaining space.
3. **Save an unfamiliar word** — Highlight **standard deviation** in the English slide. Click **+ Add a word**. Edit the Chinese meaning or add a personal note, then choose **Save to Review**. You can also type a word manually without selecting any text.
4. **Review** — Open the Review tab. The word is listed with its source slide. Select **Reveal explanation** or **Mark as understood**. Refresh the page to check that the item is retained in this browser.
5. **Caption correction** — Back in Live, select **Gradient direction** and expand **Caption review**. Inspect the prepared evidence and accept the correction. In the Overfitting case, reject the false suggestion. In Recall, save the unresolved question.

## Implemented interactions

- Three-stage navigation: Prepare / Live / Review.
- Local CSV terminology import with a glossary preview.
- Prepared English slide display with a wider slide panel and narrower Chinese notes.
- **Student-chosen vocabulary:** select text on the English slide or type any unfamiliar term, add an optional Chinese meaning/personal note, and save it to Review. Duplicate entries are prevented for the same slide and term.
- Review cards for selected words, prepared concepts, and unresolved caption questions. Students can reveal explanations, change review status, or remove items.
- Browser localStorage for the glossary and Review list. Existing saved cards from prototype v2 use the same storage key.
- Caption-review decisions, evidence inspection, restart, and a visible event trace.
- Local PDF preview in Prepare (the PDF is not parsed or translated).

## Prepared or simulated behaviour

- The six English lecture examples, accompanying Chinese notes, and speech/caption excerpts are scripted teaching material.
- Translation error flags and retrieved evidence are demonstration cases, not responses from a connected AI service.
- Student-selected words are saved through normal browser interactions; any automatic Chinese meaning shown comes from the imported glossary or a built-in example, **not AI translation**. Other words can be recorded with students' own notes.

## Not yet implemented

- Real-time microphone transcription or translation.
- Automatic extraction, translation, or explanation of uploaded PDF/PPT content.
- Automatically selecting or synchronising lecture slides with speech.
- AI-based vocabulary definitions or spaced-repetition scheduling.

## Materials and attribution

- The Normal distribution and paired t-test demos are short summaries based on `EMS2026_Lecture_2_English_Main_中文辅助理解版(3).pdf`, especially pp. 7–10 and 31–32.
- The informed consent demo is based on `EMS2026_Lecture_4_English_Main_中文辅助理解版_模板一致(1).pdf`, especially pp. 15–19.
- The computing correction cases are adaptations of the earlier scripted A2 prototype. The displayed lecture pages are demonstration text, **not original PowerPoint slide images**.
- The supplied university teaching PDFs are **not** distributed in this ZIP. Confirm permissions before publishing teaching material in a public repository.

## AI assistance and development record

ChatGPT generated the initial v2 prototype from the student's three-stage design brief and updated it to v3 following two specific requests: (1) make the original slide larger than the Chinese support panel, and (2) allow the student to select any word or phrase on a slide and save it with optional notes. The generated code and supporting text should be reviewed, run and explained by the student before submission. Do not describe AI-assisted generation or automated tests as independent student work.

The included `evidence/` images and `test_prototype.py` were produced by an automated local Chromium test. They show functioning code, **not a supervised user study**. Record any subsequent hands-on testing and design decisions in the coursework development record.

## Developer verification

From the prototype folder, on a machine with Python and Playwright installed, run `python test_prototype.py` to repeat the automated checks. You do **not** need Python or Playwright to use the prototype normally.

## Coursework reminder

Update the A2 System Diagram, Storyboards, report and GitHub development evidence to describe this revised interface. Keep *implemented*, *simulated*, and *planned* components distinct.
