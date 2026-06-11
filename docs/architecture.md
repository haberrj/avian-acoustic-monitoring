
1. Start services (Docker DB)

LOOP:

2. Capture audio (30s)
3. Pre-filter / quick checks (optional)
4. Run bird detection (BirdNET)
5. Validate results (confidence threshold)

6. Privacy handling:
   - if no bird OR suspicious → discard

7. Store metadata in DB
8. Delete raw audio

REPEAT
