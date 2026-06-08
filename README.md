# The Unofficial Guide — Project 1

---

## Domain

My system covers student reviews of Computer Science professors at Cal Poly Pomona. I chose this domain because I studied at Cal Poly Pomona for my master’s, and many of the professors in this dataset were my professors or familiar names from the department.

This knowledge is valuable because official university pages usually show basic course descriptions, prerequisites, and instructor names, but they do not explain what students actually experience in class. Student reviews can help answer questions about grading style, exam difficulty, workload, attendance, projects, lecture quality, and whether students felt a professor was helpful.

---

## Document Sources

| #  | Source                                     | Type            | URL or file path                           |
| -- | ------------------------------------------ | --------------- | ------------------------------------------ |
| 1  | Yu Sun Rate My Professors reviews          | Local text file | `data/raw/yu_sun_rmp_reviews.txt`          |
| 2  | Gilbert Young Rate My Professors reviews   | Local text file | `data/raw/gilbert_young_rmp_reviews.txt`   |
| 3  | Ericsson Marin Rate My Professors reviews  | Local text file | `data/raw/ericsson_marin_rmp_reviews.txt`  |
| 4  | Salam Salloum Rate My Professors reviews   | Local text file | `data/raw/salam_salloum_rmp_reviews.txt`   |
| 5  | David Johannsen Rate My Professors reviews | Local text file | `data/raw/david_johannsen_rmp_reviews.txt` |
| 6  | Xuesong Zhang Rate My Professors reviews   | Local text file | `data/raw/xuesong_zhang_rmp_reviews.txt`   |
| 7  | Crisrael Lucero Rate My Professors reviews | Local text file | `data/raw/crisrael_lucero_rmp_reviews.txt` |
| 8  | David Gershman Rate My Professors reviews  | Local text file | `data/raw/david_gershman_rmp_reviews.txt`  |
| 9  | Keivan Navi Rate My Professors reviews     | Local text file | `data/raw/keivan_navi_rmp_reviews.txt`     |
| 10 | Rick Ramirez Rate My Professors reviews    | Local text file | `data/raw/rick_ramirez_rmp_reviews.txt`    |

---

## Chunking Strategy

**Chunk size:**

I used one full student review as one chunk. I originally considered splitting unusually long reviews around 700 characters, but during testing that created sentence fragments that lost professor and course context. Keeping full reviews together worked better because each review is already a complete opinion about one professor and course.

**Overlap:**

I did not use overlap in the final version. Since each review stayed together as one chunk, overlap was not needed. Overlap would have been more useful if I were splitting long articles or guides into fixed-size chunks.

**Why these choices fit your documents:**

My documents are review-heavy, not long guide-style documents. Each review usually includes the professor name, course, date, quality score, difficulty score, tags, and the student’s opinion. If I split reviews mechanically, the chunk could lose important context like which professor or course the review was about. Keeping each review together makes retrieval easier because each chunk is readable and self-contained.

**Final chunk count:**

The ingestion script loaded 10 raw documents and created 229 chunks.

Chunk counts by file:

```text
crisrael_lucero_rmp_reviews.txt: 13 chunks
david_gershman_rmp_reviews.txt: 35 chunks
david_johannsen_rmp_reviews.txt: 27 chunks
ericsson_marin_rmp_reviews.txt: 12 chunks
gilbert_young_rmp_reviews.txt: 22 chunks
keivan_navi_rmp_reviews.txt: 37 chunks
rick_ramirez_rmp_reviews.txt: 3 chunks
salam_salloum_rmp_reviews.txt: 26 chunks
xuesong_zhang_rmp_reviews.txt: 35 chunks
yu_sun_rmp_reviews.txt: 19 chunks
```

### Sample Chunks

**Sample Chunk 1**
**Source:** `crisrael_lucero_rmp_reviews.txt`

```text
Professor: Crisrael Lucero
Department: Computer Science
School: Cal Poly Pomona

Review 1:
Course: 4310
Date: May 24th, 2026
Quality: 5.0
Difficulty: 4.0
Tags: Group projects; Amazing lectures; Caring
Review Text: The reviewer says Professor Lucero is very knowledgeable because of his industry experience. Exams are tough, but the group project is fun. Programming assignments are interesting and directly related to what students are learning. Three-hour lectures can be rough, but he makes them engaging with memes and several breaks. The reviewer says he is trustworthy because he actively works in industry.
```

**Sample Chunk 2**
**Source:** `crisrael_lucero_rmp_reviews.txt`

```text
Professor: Crisrael Lucero
Department: Computer Science
School: Cal Poly Pomona

Review 2:
Course: 2600
Date: Jan 21st, 2026
Quality: 5.0
Difficulty: 4.0
Tags: Amazing lectures; Caring; Lecture heavy
Review Text: Professor Lucero is described as caring. His lectures are long, almost three hours, but he gives breaks. The reviewer says his lectures are engaging overall. He is communicative about homework questions and computer science in general. The reviewer describes him as a great professor.
```

**Sample Chunk 3**
**Source:** `crisrael_lucero_rmp_reviews.txt`

```text
Professor: Crisrael Lucero
Department: Computer Science
School: Cal Poly Pomona

Review 3:
Course: 2600
Date: Nov 4th, 2025
Quality: 5.0
Difficulty: 4.0
Tags: Amazing lectures; Clear grading criteria; Inspirational
Review Text: The reviewer says Professor Lucero genuinely cares and teaches for fun. He wants students to succeed and goes to great lengths to help them feel successful and prepared for the future. The class is difficult for students who expect to coast, so students should be ready to be challenged. The curriculum is reasonable, and the reviewer wishes there were more professors like him.
```

**Sample Chunk 4**
**Source:** `crisrael_lucero_rmp_reviews.txt`

```text
Professor: Crisrael Lucero
Department: Computer Science
School: Cal Poly Pomona

Review 4:
Course: 2600
Date: Feb 2nd, 2025
Quality: 5.0
Difficulty: 3.0
Tags: Amazing lectures; Inspirational; Hilarious
Review Text: Professor Lucero is described as kind, intelligent, and humorous. His lectures were engaging and in depth. Exams were somewhat challenging, but there were many extra credit opportunities. Outside of class, he was approachable, engaged with students, and offered valuable industry insight. The reviewer says he is one of the best professors they have had at Cal Poly Pomona.
```

**Sample Chunk 5**
**Source:** `crisrael_lucero_rmp_reviews.txt`

```text
Professor: Crisrael Lucero
Department: Computer Science
School: Cal Poly Pomona

Review 5:
Course: 2600
Date: Jan 4th, 2025
Quality: 5.0
Difficulty: 3.0
Tags: Inspirational; Respected; Accessible outside class
Review Text: The reviewer describes Professor Lucero as fun, accessible on Discord, and good at making the course interesting. Exams are somewhat difficult, so students should study. The course covers UNIX commands and C++ programming. The reviewer notes that he currently works at Google and cares about helping students with career advice and expertise. There are many extra credit opportunities.
```

---

## Embedding Model

**Model used:**

I used `sentence-transformers/all-MiniLM-L6-v2`.

I chose this model because it runs locally, does not require an API key, and is lightweight enough for this project. It worked well for embedding short review chunks and searching for semantically related professor-review content.

The vector store is ChromaDB. I stored the chunk text along with metadata including the source filename and chunk index. I used top-k = 5 for retrieval.

**Production tradeoff reflection:**

If I were deploying this system for real users and cost was not a constraint, I would compare embedding models based on accuracy, latency, context length, and cost. A larger embedding model might better understand informal student language, slang, or mixed positive/negative opinions, but it might also be slower or more expensive. I would also consider privacy, because local embeddings keep the data on the user’s machine, while API-hosted embeddings may provide stronger retrieval quality but require sending text to an external service.

---

## Grounded Generation

**System prompt grounding instruction:**

The system prompt in `generate.py` tells the model:

```text
Use ONLY the provided retrieved context.
Do not use outside knowledge.
Do not guess.
If the provided context does not contain enough information to answer the question, say:
"I don't have enough information in the provided reviews to answer that."
```

The prompt also tells the model to mention professor names only if they are supported by the retrieved context.

**How source attribution is surfaced in the response:**

Source attribution is added programmatically after generation. The system collects the unique source filenames from the retrieved chunks and appends them to the answer as `Sources used:`. The Gradio interface also shows the retrieved source filenames in a separate “Retrieved from” box. This prevents the system from relying only on the LLM to remember to cite sources.

---

## Retrieval Test Examples

### Retrieval Test 1

**Query:** Which professor is most often described as having tough or test-heavy grading?

**Top returned chunks:**

1. `david_gershman_rmp_reviews.txt`, chunk 24, distance `0.4411`
2. `ericsson_marin_rmp_reviews.txt`, chunk 1, distance `0.4682`
3. `david_gershman_rmp_reviews.txt`, chunk 30, distance `0.4728`
4. `ericsson_marin_rmp_reviews.txt`, chunk 6, distance `0.4753`
5. `david_gershman_rmp_reviews.txt`, chunk 4, distance `0.4825`

**Why relevant:** The returned chunks mention “Tough grader,” “Test heavy,” quizzes, exams, grading issues, and difficult tests. David Gershman appears multiple times, which matches the expected answer.

### Retrieval Test 2

**Query:** Which professor do students praise for industry experience, career advice, mentorship, and practical assignments?

**Top returned chunks:**

1. `yu_sun_rmp_reviews.txt`, chunk 15, distance `0.4933`
2. `crisrael_lucero_rmp_reviews.txt`, chunk 0, distance `0.4992`
3. `crisrael_lucero_rmp_reviews.txt`, chunk 11, distance `0.5116`
4. `crisrael_lucero_rmp_reviews.txt`, chunk 3, distance `0.5236`
5. `yu_sun_rmp_reviews.txt`, chunk 4, distance `0.5369`

**Why relevant:** The returned chunks mention career preparation, job applications, mentorship, industry experience, big tech experience, assignments related to real problems, and career advice. These are all related to the query.

### Retrieval Test 3

**Query:** Which professor is commonly described as easy, chill, or lenient?

**Top returned chunks:**

1. `yu_sun_rmp_reviews.txt`, chunk 5, distance `0.4986`
2. `ericsson_marin_rmp_reviews.txt`, chunk 11, distance `0.5335`
3. `gilbert_young_rmp_reviews.txt`, chunk 13, distance `0.5371`
4. `crisrael_lucero_rmp_reviews.txt`, chunk 1, distance `0.5384`
5. `ericsson_marin_rmp_reviews.txt`, chunk 3, distance `0.5479`

**Why relevant or weak:** The first two chunks are relevant because they mention “easy A,” “not too difficult,” and “chill.” Some later chunks are weaker because they include general positive comments like caring or helpful rather than directly saying the professor is easy or lenient.

---

## Generated Response Examples

### Example 1

**Question:** Which professor is most often described as having tough or test-heavy grading?

**Response:**

```text
Based on the provided reviews, Professor David Gershman and Professor Ericsson Marin are both described as having tough or test-heavy grading. However, Professor Gershman is described with these terms in multiple reviews, whereas Professor Marin is described with these terms in only one review. Therefore, Professor David Gershman is most often described as having tough or test-heavy grading.

Sources used: david_gershman_rmp_reviews.txt, ericsson_marin_rmp_reviews.txt
```

### Example 2

**Question:** Which professor do students praise for industry experience, career advice, mentorship, and practical assignments?

**Response:**

```text
Based on the provided context, students praise Professor Crisrael Lucero for industry experience, career advice, mentorship, and practical assignments. Reviewers mention that he has extensive industry experience, creates assignments related to real problems, and offers valuable industry insight, career advice, and mentorship.

Sources used: crisrael_lucero_rmp_reviews.txt, yu_sun_rmp_reviews.txt
```

### Out-of-scope Query

**Question:** What is the best parking lot at Cal Poly Pomona?

**Response:**

```text
I don't have enough information in the provided reviews to answer that.

Sources used: crisrael_lucero_rmp_reviews.txt, david_gershman_rmp_reviews.txt, gilbert_young_rmp_reviews.txt
```

This is the expected behavior because the source documents are professor reviews, not parking information.

---

## Interface

The interface is a Gradio web app in `app.py`.

**Input:** A natural-language question about Cal Poly Pomona Computer Science professor reviews.

**Output:** A grounded answer and a list of retrieved source documents.

**Sample interaction:**

```text
User question:
Which professor is most often described as having tough or test-heavy grading?

Answer:
Based on the provided reviews, Professor David Gershman and Professor Ericsson Marin are both described as having tough or test-heavy grading. However, Professor Gershman is described with these terms in multiple reviews, whereas Professor Marin is described with these terms in only one review. Therefore, Professor David Gershman is most often described as having tough or test-heavy grading.

Retrieved from:
- david_gershman_rmp_reviews.txt
- ericsson_marin_rmp_reviews.txt
```

---

## Evaluation Report

| # | Question                                                                                                          | Expected answer                                                                                                                                                                                                                                                             | System response (summarized)                                                                                                                                                                                          | Retrieval quality  | Response accuracy  |
| - | ----------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------ |
| 1 | Which professor is most often described as having tough or test-heavy grading?                                    | David Gershman should be identified because many reviews describe his CS2600 classes as test-heavy, quiz-heavy, graded by few things, and difficult.                                                                                                                        | The system said David Gershman and Ericsson Marin are both described as tough/test-heavy, but Gershman appears more often, so Gershman is the main answer.                                                            | Relevant           | Accurate           |
| 2 | Which professor do students praise for industry experience, career advice, mentorship, and practical assignments? | Yu Sun and Crisrael Lucero should both appear. Yu Sun may appear for practical lectures, latest technology, job applications, career planning, and mentorship. Crisrael Lucero should appear for industry experience, practical assignments, career advice, and mentorship. | The system identified Crisrael Lucero and explained that reviews mention industry experience, real-problem assignments, industry insight, career advice, and mentorship. It retrieved Yu Sun but did not discuss him. | Relevant           | Partially accurate |
| 3 | Which professor is commonly described as easy, chill, or lenient?                                                 | David Johannsen should be a strong answer because many reviews describe his classes as easy, chill, low-stress, flexible with deadlines, and lenient. Yu Sun may also appear for easy project-based classes.                                                                | The system mentioned Ericsson Marin as “chill” and Yu Sun as an “easy A,” but did not mention David Johannsen.                                                                                                        | Partially relevant | Partially accurate |
| 4 | What do students say about Keivan Navi’s teaching style?                                                          | Students often say he is knowledgeable, caring, and passionate, but his lectures can be disorganized or confusing. Many reviews also say participation matters a lot.                                                                                                       | The system said Navi is lecture-heavy, unclear at times, disorganized, confusing, and sometimes requires self-teaching, while also being intelligent and passionate.                                                  | Relevant           | Accurate           |
| 5 | Which professor is criticized for slow grading or not grading until late in the semester?                         | Ericsson Marin, David Johannsen, and David Gershman may appear, but Ericsson Marin should be included because several reviews mention grading delays or not grading until the end of the semester.                                                                          | The system identified David Gershman, Ericsson Marin, and Gilbert Young. It included Marin and described grading delays for each.                                                                                     | Relevant           | Accurate           |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**

Which professor is commonly described as easy, chill, or lenient?

**What the system returned:**

The system returned Ericsson Marin and Yu Sun in the answer. It also retrieved sources from Crisrael Lucero and Gilbert Young. It did not mention David Johannsen, even though David Johannsen was expected because many reviews describe his classes as easy, chill, low-stress, flexible, and lenient.

**Root cause (tied to a specific pipeline stage):**

The failure happened mainly during retrieval. The query used broad positive terms like “easy,” “chill,” and “lenient.” These words, or semantically similar words like “nice,” “caring,” “helpful,” and “not too difficult,” appear across many professor reviews. Because the system uses semantic embedding search without professor-level aggregation or metadata filtering, it retrieved mixed positive reviews instead of the strongest David Johannsen evidence.

**What you would change to fix it:**

I would add a reranking or aggregation step after retrieval. For example, the system could retrieve more than 5 chunks, group results by professor, and count how many strong matching chunks each professor has before generating the answer. I could also add metadata filtering or keyword scoring for terms like “easy A,” “lenient,” “flexible,” and “low-stress.”

---

## Spec Reflection

**One way the spec helped you during implementation:**

The spec helped me make a better chunking decision. Since I had already written that my documents were short student reviews, I knew that one review per chunk made more sense than splitting the text randomly. When my first version split long reviews into sentence fragments, I could compare that output to my original chunking reasoning and see that it was not a good fit.

**One way your implementation diverged from the spec, and why:**

My original spec said I might split unusually long reviews around 700 characters with overlap. During Milestone 3, I tested that and saw chunks starting in the middle of sentences, which made them lose professor and course context. I changed the implementation to keep full reviews together instead. This was a better choice because the chunks became readable, self-contained, and easier to cite.

---

## AI Usage

**Instance 1**

* *What I gave the AI:* I gave ChatGPT my document structure and chunking strategy from `planning.md`.
* *What it produced:* It helped draft an `ingest.py` script that loaded `.txt` files, cleaned text, split reviews into chunks, and saved them to `data/chunks.jsonl`.
* *What I changed or overrode:* The first version split long chunks by character count, which created fragments. I changed the implementation to keep complete reviews together. I also fixed file reading to handle Windows-style encoding characters.

**Instance 2**

* *What I gave the AI:* I gave ChatGPT my retrieval approach and asked for code using `all-MiniLM-L6-v2` with ChromaDB.
* *What it produced:* It helped draft `build_index.py` and `query.py`.
* *What I changed or overrode:* After testing, I changed the ChromaDB collection to use cosine distance because the first distance scores were too high and harder to interpret. I also adjusted one evaluation query to better match what the system was retrieving.

**Instance 3**

* *What I gave the AI:* I gave ChatGPT the actual outputs from my Gradio app for all 5 evaluation questions.
* *What it produced:* It helped organize the evaluation report and failure case explanation.
* *What I changed or overrode:* I reviewed the accuracy judgments myself and marked Question 2 and Question 3 as partially accurate instead of presenting all results as perfect.

---

## Demo Video Notes

In my demo video, I show:

1. The Gradio app running.
2. A successful query about test-heavy grading.
3. A successful query about industry experience and career advice.
4. An out-of-scope parking question where the system refuses to answer.
5. The weak case about easy/chill/lenient professors.
6. A short walkthrough of the evaluation report in this README.
