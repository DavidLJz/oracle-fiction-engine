# Oracle Engine: Data Extraction Prompt Design

This document contains the prompt engineering strategy for extracting unstructured narrative text (world bibles, character bios, plot summaries) into the structured YAML files required by the Oracle Engine.

## The Universal Extraction Prompt (Draft 1)

**Copy and paste the following prompt into your LLM of choice, followed by your source text:**

```text
You are an expert narrative designer and data architect. Your goal is to analyze the following unstructured story text and extract it into structured YAML formats for a randomized CLI storytelling engine. 

The engine uses two main types of data:
1. Random Tables (Lists of thematic elements)
2. Character Rosters (Characters defined by short, psychological or narrative "drives")

Analyze the provided text and generate the following two YAML blocks.

### RULES FOR EXTRACTION:

1. TABLES (tables.yaml format):
- Identify key environmental hazards, locations, narrative twists, factions, or items mentioned or implied in the text.
- Create 3 to 5 logical categories (e.g., `locations`, `hazards`, `npc_encounters`, `plot_twists`).
- Under each category, provide a list of 4 to 10 punchy, evocative strings. 
- Example format:
  tables:
    locations:
      - "The Neon Slums"
      - "The Upper Spire"

2. CHARACTERS (characters.yaml format):
- Identify the most important actors, factions, or entities in the text.
- For each character, distill their complex lore into 2 to 4 concise "drives" (key-value pairs). 
- Excellent drive keys include: `want`, `fear`, `secret`, `flaw`, `method`, `misunderstanding`, `goal`. 
- Ensure the values are actionable and create narrative friction.
- Example format:
  characters:
    Marcus:
      want: Avenge his fallen squad
      fear: Becoming the monster he is hunting
      flaw: Refuses to trust outsiders

### OUTPUT FORMAT:
Output ONLY valid YAML. Provide the tables under a `tables:` root key, and the characters under a `characters:` root key. Do not include markdown formatting outside of the YAML structure.

--- SOURCE TEXT BELOW ---
[INSERT YOUR TEXT HERE]
```

---

# Addendum: Universal vs. Specialized Prompts

While the Universal Prompt above is excellent for **one-shots, short stories, or brief synopses** (under 3,000 words), it will likely struggle with larger or more complex universes. 

Here is an evaluation of when to use the Universal prompt versus when to specialize:

### 1. Context Window & Attention Dilution (The Scale Problem)
- **Universal Issue:** If you feed an LLM a 50-page world bible, asking it to extract *both* characters and tables simultaneously will cause it to hallucinate, summarize too broadly, or skip minor (but interesting) details to save output tokens.
- **Specialized Solution:** Split the pipeline. 
  - *Prompt A:* "Read this text and ONLY extract the settings, weather, and factions into random tables."
  - *Prompt B:* "Read this text and ONLY extract the characters and their psychological drives."

### 2. Genre-Specific Drives (The Granularity Problem)
- **Universal Issue:** The universal prompt suggests general drives (`want`, `fear`, `secret`).
- **Specialized Solution:** Tailor the drive keys to the genre.
  - *Mystery Game:* Prompt the LLM to extract `motive`, `alibi`, `clue_hidden`, `relationship_to_victim`.
  - *Sci-Fi Combat:* Prompt the LLM to extract `primary_weapon`, `tactical_weakness`, `directive`.
  - *Political Intrigue:* Prompt the LLM to extract `public_stance`, `private_agenda`, `blackmail_material`.

### 3. Roster Segmentation (The Organization Problem)
- **Universal Issue:** It dumps all characters into one giant `characters` dictionary.
- **Specialized Solution:** If you have distinct factions, use targeted prompts to generate separate files (e.g., `extract_villains.md`, `extract_allies.md`) so you can utilize the engine's `include` feature (e.g., `master_roster.yaml`) effectively.

### Conclusion
**Start Universal, Pivot to Specialized.** Use the universal prompt to quickly prototype a new universe. When translating a massive, existing lore repository (like a D&D campaign setting or a novel draft), switch to specialized prompts that target one specific YAML file or one specific faction at a time to ensure high-fidelity, actionable data.

### Evaluation: Can a Single Prompt be Universal?

A single, universal prompt like the one above works remarkably well for **one-shots, short stories, or brief universe synopses** (under ~3,000 words). It successfully bridges the gap between unstructured prose and structured YAML in a single pass. 

However, **it is not universally optimal.** You will likely need specialized prompts when dealing with larger texts due to the following limitations:

1. **The Scale Problem (Context Dilution):** If you feed an LLM a massive 50-page world bible, asking it to extract *both* characters and tables simultaneously forces the model to compress its attention. It will likely hallucinate, summarize too broadly, or skip minor but interesting details to save on output tokens. 
    *   **Specialization:** Split the pipeline. Use one prompt strictly for "Settings & Tables" and another strictly for "Psychological Character Drives."
2. **The Granularity Problem (Genre Specifics):** The universal prompt suggests very general drives (`want`, `fear`, `secret`). 
    *   **Specialization:** Tailor the drive keys to the genre for much richer Oracle Engine outputs. For a Murder Mystery, prompt the LLM to extract `motive`, `alibi`, `clue_hidden`. For a Political Intrigue, prompt for `public_stance`, `private_agenda`, `blackmail_material`.
3. **The Organization Problem (Roster Segmentation):** A universal prompt dumps everything into one giant `characters` dictionary. 
    *   **Specialization:** If you have distinct factions, it's better to use targeted prompts (e.g., "Extract only the villains from this text") to generate separate files (`bad_guys.yaml`), which allows you to utilize the Oracle Engine's `include` feature cleanly via a `master_roster.yaml`.

**The Strategy:** Start with the Universal Prompt to rapidly prototype a new setting from a short summary. When translating a massive existing lore repository (like a D&D campaign setting), pivot to specialized, single-task prompts to ensure high-fidelity, actionable data!