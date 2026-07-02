# Krampis Zoom — Prep Notes
## Living document — last updated July 2, 2026
## Meeting scheduled: next week (evening), exact time TBD
## Attendees: Gary Welz, Konstantinos Krampis, Krampis student

---

## Before the call — send these materials

- [ ] Share the GCS validation package URL with Krampis and student
      (URL to be confirmed once package is fully staged)
- [ ] Send the GLMP From Square One HTML document
      (glmp-from-square-one-v2.html — opens in any browser,
      renders the lac operon flowchart live)
- [ ] Send Krampis the supervisor note
      (krampis-supervisor-note.md — informal one-pager)
- [ ] Confirm Zoom link and send calendar invite

---

## Opening the call — talking points

**Start with the picture, not the text.**

Open by sharing your screen and showing the lac operon flowchart
from the From Square One HTML document. Let it sit for a moment.
Then say something like:

*"This is where the project started — with a picture. The idea that
a molecular regulatory process could be represented as a logical
circuit diagram. Before any database, before any decoder, before
any of the computer science work — this picture. Everything we've
done since is an attempt to rigorously test whether that picture
is right."*

Then walk through the five-step research logic:

---

## The five-step logic — talking points for the Zoom

Use these as a verbal guide, not a script. The goal is to give
Konstantinos and the student a clear mental model of where they
fit in the research program.

**Step 1 — The flowcharts exist and are growing**
"We've used AI to generate flowcharts of 217 regulatory processes
across multiple organisms, and we're actively scaling toward 1,000+.
The batch generation runs overnight automatically — new circuits are
being added continuously. We're also building a curated research paper
collection alongside the flowcharts. Each flowchart represents a
hypothesis about how the regulatory logic works. We've been selective
about where we started — the most well-documented systems, like the
three E. coli operons you'll be looking at."

**Step 2 — The open question (this is their job)**
"Before we can do anything else with these charts — publish them,
use them to train models, build a knowledge engine — we need to
know: are they right? Do they accurately represent the biology?
That's step 2, and it's the pivotal step. Everything else rests on
a yes answer. Your student is the first person outside our core
team to look at these charts as a biologist and tell us whether
they hold up."

*Pause here. Let the weight of that land.*

"We're not asking for a comprehensive review of all 217. We're
starting with three — the lac, ara, and trp operons. These are the
most studied regulatory circuits in all of E. coli biology. If the
charts are wrong for these, we need to know immediately. If they're
right, we have a foundation."

**Step 3 — What we're doing computationally (their context)**
"Meanwhile, we're also attacking this from the DNA sequence side.
We've built a pipeline that scans the actual DNA for the binding
sites the charts predict should be there. The lac operon chart says
LacI should bind at a specific location — we've found it. The trp
operon chart says TrpR should bind — we've found it. So the
computational evidence is building. But we need the biological
validation to know that what we're finding in the DNA actually
maps to real regulatory behavior, not just sequence similarity."

**Step 4 and 5 — The bigger picture (briefly)**
"If this works — and we have good reason to think it will — the
next steps are a methods paper, then scaling to hundreds of circuits,
then cross-validation with tools like Evo 2 and RegVelo. That's
where your lab's expertise becomes central. But we're not there yet.
We're at step 2."

---

## The student background question — ask early

Ask Konstantinos in the first few minutes:

*"Before we get into the details — can you tell us a bit about
your student's background? Are they coming from more of a biology
side or more of a computer science / bioinformatics side? We have
two tracks prepared and I want to make sure they get the one that
fits them best."*

Then present both tracks clearly:
- **Biology track:** read the annotation review document, check the
  logic gate assignments against primary literature and databases,
  write a structured report. 8 hours, 3 weeks.
- **Computation track:** write a Python analysis comparing our
  predicted binding sites against RegulonDB, produce overlap
  statistics. 10-11 hours, 3 weeks.

If the student seems strong in both: suggest they do the computation
track first (more structured, less ambiguous) and then informally
review the annotation document afterward.

---

## Krampis' role — frame it clearly and lightly

*"Konstantinos, what I'm asking of you is primarily to point your
student at the package and supervise at whatever level works for
your schedule. If you happen to glance at the annotation review
document and have a bioinformatics reaction to our FIMO methodology,
that's genuinely useful — but there's no obligation or timeline
on your end. You're the connection; the student does the hands-on
work."*

Keep it light. He said this is "tough with family and July 4th
travel" — he's already stretched. Frame his role as minimal and
flexible.

---

## Items to confirm on the call

- [ ] Student's background (biology vs computation)
- [ ] Student's availability — how many hours per week this summer?
- [ ] Does Konstantinos want a brief intro call with the student
      before they start, or just send them the package?
- [ ] His preferred communication channel for updates
      (email, Slack, occasional Zoom check-in?)
- [ ] Any initial reactions to the From Square One document

---

## What NOT to bring up on this call

- The methods paper submission status (not relevant to their task)
- The decoder architecture details (too technical, not their concern)
- Nathan Lents (not confirmed, don't pre-announce)
- The 217-circuit catalog size (sounds like a lot; focus on the 3)
- Phase 3 batch runner (completely irrelevant to this audience)
- Specific timelines beyond "approximately 3 weeks"

---

## Updates to add before the call

*This section to be filled in as the project progresses:*

- [ ] Confirm GCS validation package URL (staging in progress)
- [ ] Note any new decode results relevant to the student's task
- [ ] Update "where the decoder stands" table if new circuits decoded
- [ ] Add any feedback from Lents if received before the call
- [ ] Confirm exact Zoom date/time when scheduled

---

## Follow-up after the call

- [ ] Send Krampis the GCS package URL and From Square One HTML
- [ ] Send student-specific welcome email with their assigned track
- [ ] Set a check-in reminder for 2 weeks after student starts
- [ ] Note student's name and background in project records
