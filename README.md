# The Unofficial Guide — Project 1


---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

**Domain:** Student reviews and practical experiences for CUNY (City University of New York) study abroad and exchange programs.

**Why this knowledge is valuable and hard to find:** Official university channels typically provide high-level, sanitized overviews but miss the nuanced, practical details. This knowledge base aggregates real student experiences (from Reddit) and official data to answer specific, hard-to-find questions about financial aid (FAFSA/TAP) applicability, credit transfer pitfalls, housing logistics, and day-to-day tips.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Reddit /r/CUNY (BMCC Study Abroad) | Local Fallback TXT | `documents/study_abroad_at_bmcc.txt` |
| 2 | StudyAbroad101 | URL | `https://www.studyabroad101.com/providers/cuny-college-of-staten-island` |
| 3 | Reddit /r/CUNY (QCC Study Abroad) | Local Fallback TXT | `documents/study_abroad_thru_qcc.txt` |
| 4 | BMCC Financial Aid | URL | `https://www.bmcc.cuny.edu/academics/success-programs/study-abroad/financial-aid-and-scholarships/` |
| 5 | CUNY Global Programs | URL | `https://www1.cuny.edu/sites/global/students/programs/programs-search/` |
| 6 | Hunter College Eligibility | URL | `https://www.hunter.cuny.edu/students/opportunities/study-abroad/eligibility-requirements/` |
| 7 | Reddit /r/CUNY (Affiliated Programs) | Local Fallback TXT | `documents/affiliated_programs_at_cuny.txt` |
| 8 | Reddit /r/CUNY (Eligibility) | Local Fallback TXT | `documents/eligibility_question.txt` |
| 9 | John Jay Testimonials | URL | `https://www.jjay.cuny.edu/academics/undergraduate-programs/international-studies-programs/study-abroad` |
| 10 | BMCC Testimonials | URL | `https://www.bmcc.cuny.edu/academics/success-programs/study-abroad/student-testimonials/` |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 characters.

**Overlap:** 50 characters.

**Why these choices fit your documents:** The corpus is a mix of unstructured conversational text (Reddit comments) and structured info (university policies). A 500-character chunk is small enough to keep the semantic focus tight on a single topic (e.g., a specific tip about FAFSA) but large enough to capture a complete thought. The 50-character overlap ensures that context isn't lost mid-sentence, which is vital for Reddit threads where pronouns often refer back to previous sentences. Before chunking, `BeautifulSoup` was used to strip all HTML tags from the URLs, and explicit source tags (e.g., `[Source: Reddit Review]`) were manually prepended to the local fallback txt files.

**Final chunk count:** 229

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` (via `sentence-transformers`).

**Production tradeoff reflection:** If deploying this for real users without cost constraints, I would consider a more powerful commercial model like OpenAI's `text-embedding-3-large` or a Voyage AI model fine-tuned for conversational text. These would likely capture the semantic nuances of informal Reddit reviews much better than the lightweight MiniLM model. I would also weigh the tradeoff between latency and accuracy (heavier models take longer to run) and look into models with strong multilingual support, as study abroad reviews frequently include foreign university names, cities, and cultural terms.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** `"Answer the question using only the information in the provided documents. If the documents provide limited information, state what is available and explicitly advise the user on where they can manually look for more information... based on hints in the context. If the documents don't contain any relevant information at all, say 'I don't have enough information on that.'"`

**How source attribution is surfaced in the response:** Instead of forcing the LLM to write messy inline citations within its generated response, the system programmatically aggregates all unique URLs/file paths from the retrieved ChromaDB chunks. It then appends a clean `📚 Retrieved Sources:` list at the very bottom of the Gradio UI output box.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Can I use my Pell Grant and TAP to pay for a BMCC study abroad program, and are there specific scholarships available? | Yes, federal financial aid (like Pell Grants) can typically be used, though state aid (TAP) may have specific restrictions. | The system correctly noted the documents lack info on Pell Grants/TAP, but listed available scholarships (Gilman/BMCC). It avoided hallucinating by explicitly advising the user to contact the financial aid office. | Partially relevant | Accurate (Avoided hallucination) |
| 2 | What is the minimum GPA and credit requirement to be eligible to study abroad through Hunter College? | Students generally need a minimum cumulative GPA (often 2.75 to 3.0 depending on the program) and must have completed a certain number of credits. | The system identified that students need a minimum GPA (2.75 - 3.0 depending on the program) and 24-30 credits at CUNY before going abroad. | Relevant | Accurate |
| 3 | According to Reddit reviews for CUNY affiliated programs, what is the biggest challenge with getting study abroad credits to transfer? | The most common challenge is getting specific foreign courses pre-approved by academic department advisors. | The system accurately pulled from the local Reddit txt file, stating the biggest challenge is getting specific foreign courses pre-approved by academic department advisors to fulfill major requirements instead of just electives. | Relevant | Accurate |
| 4 | What do student testimonials from John Jay and BMCC say about the impact of studying abroad on career or personal growth? | Improved cross-cultural communication, fostered independence, and often clarified career goals. | It successfully summarized that studying abroad fosters independence, provides strong language and cultural immersion, and helps clarify career interests. | Relevant | Accurate |
| 5 | What are the typical housing options? | Housing options usually include host families (homestays), or shared student apartments/dorms. | The system stated that housing is typically the responsibility of the student and isn't too expensive compared to NY. It explicitly advised the user to speak with a study abroad representative for more details, as the documents lacked specific housing types. | Partially relevant | Accurate (Avoided hallucination) |

**Retrieval quality:** Relevant   
**Response accuracy:** Accurate 

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** What are the typical housing options?

**What the system returned:** "Housing is typically the responsibility of the student, but it isn't too expensive... I don't have enough specific information on options like host families or dorms..."

**Root cause (tied to a specific pipeline stage):** The failure occurred due to limitations in the **Data Ingestion** and **Retrieval** stages. The expected answer (mentioning host families and dorms) was an assumption made during the planning phase. However, the actual document successfully retrieved by the system (`affiliated_programs_at_cuny.txt`) only contained a vague mention that "housing is typically on you". Because the LLM was heavily grounded by the generation prompt, it correctly refused to hallucinate the missing details (homestays/dorms), resulting in an incomplete, albeit honest, answer.

**What you would change to fix it:** To fix this, I need to improve the initial **Data Ingestion** stage. I would search for and scrape a specific CUNY article or an additional Reddit thread that explicitly discusses various housing options (e.g., homestays, student apartments) and add it to the `documents/` folder.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Writing the architecture and tool plan in advance made coding the `embed.py` and `generate.py` scripts much faster. Because I had already decided on the specific tools (`ChromaDB`, `all-MiniLM-L6-v2`, `Groq`) and the chunking parameters (500 chars / 50 overlap), I could immediately write prompts that gave the AI strict, clear instructions, drastically reducing trial-and-error during the coding phase.

**One way your implementation diverged from the spec, and why:** During the document ingestion phase, I planned to scrape Reddit URLs directly using `BeautifulSoup` and APIs. However, Reddit's strict anti-scraping security blocks (returning 403 Forbidden errors) prevented fetching the posts even when using proxies. As a result, I diverged from the spec by implementing a "Local Fallback" system in `ingest.py`, where I manually extracted the Reddit reviews into `.txt` files and wrote code to load them from a local `documents/` folder alongside the URLs.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I asked the AI tool to write `ingest.py` to scrape the Reddit URLs from my list using `requests` and `BeautifulSoup`.
- *What it produced:* It initially generated code using `requests.get`, but it hit Reddit's 403 network blocks. It then produced an alternative using the AllOrigins proxy to bypass the IP ban.
- *What I changed or overrode:* When the proxy servers kept timing out, I directed the AI to abandon the live-scraping approach for Reddit entirely. I overrode its output by instructing it to write a specific `load_local_txt_documents()` function to parse manually saved `.txt` files from a local directory instead.

**Instance 2**

- *What I gave the AI:* I asked the AI to add source citations to the final response, ensuring the LLM explicitly names which document the answer came from.
- *What it produced:* The AI modified the system prompt to force the LLM to write inline citations inside its generated text (e.g., placing `[Source: Local File: affiliated_programs_at_cuny.txt]` mid-sentence).
- *What I changed or overrode:* I found the inline citations too long and messy for the UI. I overrode the prompt to explicitly forbid inline citations, and instead directed the AI to write Python code that dynamically extracts unique URLs from the ChromaDB results and appends them as a clean list at the bottom of the Gradio Web UI.
