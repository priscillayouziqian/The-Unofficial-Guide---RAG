# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
**Domain:** Student reviews for CUNY (City University of New York) study abroad and exchange programs.

**Why this knowledge is valuable and hard to find:** Official university channels provide high-level overviews but miss practical details. This knowledge base aggregates real student experiences to answer specific, hard-to-find questions about financial aid (FAFSA/TAP) applicability, credit transferability, housing logistics, and day-to-day tips for budgeting and living abroad.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |reddit.com/r/CUNY| study abroad at BMCC| https://www.reddit.com/r/CUNY/comments/1j7crv4/anyone_here_studied_abroad_at_bmcc/|
| 2 | studyabroad101.com| 38 study abroad programs at CSI| https://www.studyabroad101.com/providers/cuny-college-of-staten-island|
| 3 |reddit.com/r/CUNY | study abroad thru QCC| https://www.reddit.com/r/CUNY/comments/1qpbwan/talk_about_your_experience_studying_abroad/|
| 4 |bmcc.cuny.edu | scholarships and financial aid| https://www.bmcc.cuny.edu/academics/success-programs/study-abroad/financial-aid-and-scholarships/|
| 5 | cuny.edu| available programs| https://www1.cuny.edu/sites/global/students/programs/programs-search/|
| 6 | hunter.cuny.edu| eligiblity requirements| https://www.hunter.cuny.edu/students/opportunities/study-abroad/eligibility-requirements/|
| 7 | reddit.com/r/CUNY| review for affiliated programs at CUNY| https://www.reddit.com/r/CUNY/comments/17bxq0j/cuny_study_abroad/|
| 8 |reddit.com/r/CUNY | eligibility question | https://www.reddit.com/r/CUNY/comments/11lhs5r/study_abroad/|
| 9 | jjay.cuny.edu| student testimonials| https://www.jjay.cuny.edu/academics/undergraduate-programs/international-studies-programs/study-abroad|
| 10 | bmcc.cuny.edu| student testimonials| https://www.bmcc.cuny.edu/academics/success-programs/study-abroad/student-testimonials/|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
500 characters.

**Overlap:**
**Overlap:** 50 characters.

**Reasoning:**
The corpus is a mix of unstructured conversational text (Reddit comments, student testimonials) and structured information (university financial aid policies). A 500-character chunk is small enough to keep the semantic focus tight on a single topic (e.g., a specific tip about housing or FAFSA) but large enough to capture a complete thought. The 50-character overlap ensures that context isn't lost mid-sentence, which is especially important for conversational Reddit threads where pronouns often refer back to previous sentences.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
`all-MiniLM-L6-v2` (via `sentence-transformers`).

**Top-k:**
5 chunks per query.

**Production tradeoff reflection:**
 If deploying this for real users without cost constraints, I would consider a more powerful commercial model like OpenAI's `text-embedding-3-large` or a Voyage AI model fine-tuned for conversational text. These would likely capture the semantic nuances of informal Reddit reviews much better. I would also weigh the tradeoff between latency and accuracy (heavier models take longer to run) and look into models with strong multilingual support, as study abroad reviews frequently include foreign university names, cities, and cultural terms.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Can I use my Pell Grant and TAP to pay for a BMCC study abroad program, and are there specific scholarships available? | Yes, federal financial aid (like Pell Grants) can typically be used, though state aid (TAP) may have specific restrictions. Students should also look into the Benjamin A. Gilman Scholarship and BMCC-specific grants. |
| 2 | What is the minimum GPA and credit requirement to be eligible to study abroad through Hunter College? | Students generally need a minimum cumulative GPA (often 2.75 to 3.0 depending on the program) and must have completed a certain number of credits (usually 24-30) at CUNY before going abroad. |
| 3 | According to Reddit reviews for CUNY affiliated programs, what is the biggest challenge with getting study abroad credits to transfer? | The most common challenge is getting specific foreign courses pre-approved by academic department advisors to ensure they fulfill major requirements rather than just counting as general electives. |
| 4 | What do student testimonials from John Jay and BMCC say about the impact of studying abroad on career or personal growth? | Testimonials emphasize that the experience improved their cross-cultural communication, fostered independence, and often clarified their career goals toward global or international fields. |
| 5 | what are the typical housing options and their benefits on CSI programs? | Housing options usually include host families (homestays), which provide strong language and cultural immersion, or shared student apartments/dorms, which offer greater independence. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Messy unstructured data from Reddit:** Reddit comments often contain slang, acronyms, or lack context without the parent comment. Chunking this text strictly by 500 characters might break a comment mid-thought, leading to retrieved context that the LLM cannot fully understand.

2. **Groq API Rate Limits:** Even though Groq's free tier is fast, there are often strict limits on requests per minute or tokens per minute. If multiple long documents are passed into the context window rapidly during testing, it might trigger rate-limit errors and break the generation step.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```text
[Documents: CUNY sites, Reddit, etc.]
         │ (Ingestion & Cleaning)
         ▼
[Chunking: 500 chars / 50 overlap]
         │
         ▼
[Embedding: sentence-transformers (all-MiniLM-L6-v2)]
         │
         ▼
[Vector Store: ChromaDB (Local)] ──► [Retrieval: Top 5 Chunks]
                                             │
                                             ▼
[User Query] ──────────────────────► [Generation: Groq (llama-3.3-70b-versatile)]
                                             │
                                             ▼
                                      [Final Answer]
```
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I plan to use **Claude Code**. I will provide it with my list of URLs and my Chunking Strategy (500 characters / 50 overlap). I expect it to produce a Python script using `requests` and `BeautifulSoup` to scrape the text, clean out HTML, and chunk the text. I will verify the output by checking a sample of the generated chunks to ensure they are the correct length and the text is readable.

**Milestone 4 — Embedding and retrieval:**
I will use **Claude Code**. I will provide the "Retrieval Approach" and "Architecture" sections, explicitly telling it to use `ChromaDB` and `sentence-transformers` (`all-MiniLM-L6-v2`). I expect it to output code that initializes a ChromaDB collection, embeds the chunked text, and creates a function to search the top 5 chunks. I will verify this by running test queries and printing out the retrieved chunks to see if they are relevant.

**Milestone 5 — Generation and interface:**
I will use **Claude Code**. I will provide my Groq requirement (`llama-3.3-70b-versatile`) and my 5 evaluation questions. I expect it to produce a script that connects to the Groq API, inserts the user query and retrieved ChromaDB chunks into a prompt template, and generates an answer. I will verify this by checking if the LLM's answers are accurately grounded in the provided chunks and comparing them to my "Expected answers."
