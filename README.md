# ⚖️ Nyaya-Agent: Autonomous Legal Chambers OS (`v1.0`)

**Nyaya-Agent** is a Multi-Agent Legal Operating System engineered for Indian litigation chambers, focusing on **Negotiable Instruments Act, 1881 (Section 138 / 141 / 142)**, **Bharatiya Nagarik Suraksha Sanhita, 2023 (Section 223 / 528 BNSS)**, and **Order XXXVII CPC Summary Suits**.

Instead of a generic legal chatbot, Nyaya-Agent operates as an autonomous multi-agent pipeline that ingests case dockets, computes statutory limitation periods, flags fatal precedent traps, recommends dual-side litigation strategy (Defense & Complainant), and exports court-compliant Microsoft Word (`.doc`) pleadings.

---

## 🤖 Multi-Agent Architecture

### Active Swarm (`v1.0` Production)
1. **👁️ Agent `NETRA` (Docket & Multimodal Vision Ingestion Agent):**
   * Ingests multi-page PDF dockets, indexes page boundaries (`[PAGE X]`), and automatically routes scanned annexures/return memos to multimodal vision OCR.
   * **Zero-Data-Retention Security:** All client dockets are processed strictly in ephemeral session RAM (`st.session_state`) and are never written to disk or external databases.
2. **⚖️ Agent `VIDHI` (Procedural & Limitation Audit Agent):**
   * Performs automated calendar math under **Section 9 of the General Clauses Act, 1897** (3-month cheque validity under Sec 138 Proviso (a), 30-day notice window under Proviso (b), and 15-day cure window under Proviso (c) r/w Sec 142(1)(b)).
   * Audits dockets against binding Supreme Court precedents (*Shri Ishar Alloy Steels*, *Suman Sethi*, *Rahul Builders*, *Yogendra Pratap Singh*, *SMS Pharmaceuticals*, *Pooja Ravinder Devidasani*, *Dashrathbhai Trikambhai Patel*, and *Bridgestone India*).
   * Outputs actionable next steps and exact document recommendations for **both Defense and Complainant**.
3. **✍️ Agent `LEKHAK` (Senior Pleading & Courtroom Typography Agent):**
   * Receives the structured audit handoff from `NETRA` and `VIDHI` (`NETRA → VIDHI → LEKHAK`).
   * Drafts 6 verbatim, full-length legal instruments with strict anti-fabrication guardrails (`[INSERT ...]` bold placeholders for unverified facts to prevent uninstructed admissions).
   * Compiles clean HTML-to-Word (`.doc`) files with Times New Roman 12pt typography, 1.25-inch binding margins, right-aligned party roles/deponent blocks, and native page breaks (`page-break-before:always`).

### Upcoming Expansion (`v2.0` Roadmap)
4. **🔍 Agent `KHOJ` (E-Courts & Precedent Researcher Agent):** Live E-Courts and High Court archive integration for judge-specific precedent discovery.
5. **📬 Agent `DOOT` (Chambers Clerk & Dispatch Agent):** Automated `.ics` statutory deadline calendar alerts, Vakalatnama generation, and WhatsApp client status summaries.
6. **🗣️ Agent `BHASHA` (Sovereign Indic Legal Layer):** Regional district court translation and drafting support across Hindi, Punjabi, Haryanvi, and Tamil with DPDP Act compliance.

---

## 📜 Verified Court & Chamber Blueprints (`Agent LEKHAK`)
1. **Statutory Demand Notice (`Sec 138 r/w Sec 141 NI Act`)** — Severed principal cheque demand compliant with *Suman Sethi v. Ajay K. Churiwal*.
2. **Reply to Legal Demand Notice (`Defense`)** — Omnibus denial, Part I preliminary statutory objections, Part II para-wise merits traversal, and Part III pre-cognizance notice under the First Proviso to Sec 223(1) BNSS & Sec 248 BNS.
3. **Criminal Complaint (`Sec 138 NI Act r/w Sec 223 BNSS`)** — Complete 12-paragraph complaint, Prayer, Verification, page-separated **Sec 145(1) NI Act Pre-Summoning Evidence Affidavit**, List of Witnesses, and exhibited List of Documents (with Sec 63 BSA certificate).
4. **High Court Quashing Petition (`Sec 528 BNSS / Sec 482 CrPC`)** — Dynamic pan-India High Court Cause Title, Substantial Questions of Law, Chronological Facts, Grounds (`Pepsi Foods` & `Bhajan Lal`), Prayer with *ad-interim* stay, and page-separated Supporting Affidavit.
5. **Summary Civil Suit Plaint (`Order XXXVII CPC r/w Sec 80 NI Act`)** — Liquidated recovery plaint with mandatory Order XXXVII Rule 2(1)(b) declaration, 18% statutory interest under Sec 80 NI Act, Order VI Rule 15 CPC Verification, and Supporting Affidavit.
6. **Court List of Dates & Events (`LoD`)** — Formal courtroom Synopsis & 4-column chronological table for Trial Courts, High Courts, or the Supreme Court of India.

---

## ⚡ Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py