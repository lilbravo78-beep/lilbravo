# Change record — Lecture Companion

## v4 (current)

**Student requests:** (1) keep vocabulary and caption corrections in separate Review lists, with a complete after-class correction decision flow; (2) when selecting an unfamiliar term in Live, show its Chinese meaning immediately and allow the meaning to be edited.

### Changes implemented

- **Live — bilingual word selection:** Highlight a term on a prepared English slide. The vocabulary strip immediately shows a Chinese meaning if the term matches the imported CSV glossary or the slide's prepared terminology. Open **+ Add a word** to see the pre-filled, editable translation field and optionally add a personal note. The user can change the suggested translation before saving. If there is no matching entry, the system explicitly reports this rather than inventing an AI translation; students can supply one manually.
- **Review — two separate lists:** Vocabulary and concepts are kept in **Vocabulary Review** with their existing reveal/mark/remove controls. Scripted AI caption flags now appear only in **Caption Correction Review**.
- **Caption records:** When a flagged prepared example is opened in Live, it is automatically saved as **Pending** with its original caption, suggested correction (if any), supporting evidence and source. The student is not required to decide immediately.
- **After-class correction:** Each caption record offers **Review evidence → Accept correction**, **Reject suggestion** or **Keep pending**. Where the prepared evidence is unavailable, the Accept action is disabled. An accepted decision is restored on the corresponding Live slide; rejected suggestions leave its original subtitle in place.
- **Persistence and continuity:** Both lists and caption decisions use localStorage; v2/v3 saved cards are retained when available. Legacy caption statuses are normalised to Pending. Example restart resets a demonstration decision to Pending without erasing its recorded flag.
- **Testing and evidence:** Added automated v4 screenshots, a targeted test script and a test summary. The test environment uses a localStorage mock for persistence checks and is not a user study.

### Deliberately not implemented

No live microphone transcription, live translation, genuine AI flag detection, PPT semantic analysis, arbitrary AI vocabulary definition, pronunciation/audio playback, or automatic return to the original source slide/lecture recording. These remain future designs.

## v3 (previous iteration)

- Widened the original English slide versus the Chinese helper panel.
- Added selection of a word/phrase directly on the English slide, editable meaning/note and local vocabulary save.

## v2 (previous iteration)

- Combined Prepare, Live, and Review in a single offline interactive teaching demonstration.

## v1 (initial exploration)

- Scripted gradient, overfitting and insufficient-evidence caption-correction scenarios with student decision controls.

This file is a transparent design evolution summary. It does not imply that uncommitted earlier iterations have genuine historical Git commits.
