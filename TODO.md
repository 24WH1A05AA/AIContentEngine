# TODO - Debug voiceover generation / “viover” not generated

## Step 1
- Confirm voiceover generation path in `app.py` and failure handling.

## Step 2
- Improve error visibility:
  - In `voiceover.py`, include provider-specific errors (OpenAI TTS vs ElevenLabs) rather than returning False silently.
  - In `app.py`, show exception details inside the warning so we can see what failed.
  - ✅ Implemented provider-specific failure reasons in `voiceover.py` and improved warnings in `app.py`.


## Step 3
- Ensure narration script generation failures surface as `VoiceoverError` with underlying reason.

## Step 4
- Update/extend `test_stage2_unit.py` to validate `voiceover` functions raise properly when no API keys are set (structure-level tests).

## Step 5
- Run tests (`pytest` or the existing test scripts) and run Streamlit once to verify an MP3 file is produced in `voiceovers/`.

