import streamlit as st
import requests
import time
import base64
import re
import random
import urllib.parse
from datetime import datetime, timedelta
from pypdf import PdfReader
from concurrent.futures import ThreadPoolExecutor, as_completed

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Nyaya-Agent | Chambers OS", page_icon="⚖️", layout="wide")

# 2. VERBATIM SENIOR-ADVOCATE DRAFTING BLUEPRINTS (ALL 7 DOCUMENTS PRE-AUDITED & HARDENED)
DRAFT_BLUEPRINTS = {
    "Statutory Demand Notice (Sec 138 NI Act)": """
DRAFTING BLUEPRINT — STATUTORY DEMAND NOTICE UNDER SECTION 138 READ WITH SECTION 141 NI ACT, 1881:
STRICT RULES FOR THIS TEMPLATE:
- Output ONLY the formal Legal Notice below. Do NOT output any internal notes or parenthetical instructions.
- Populate all known facts from the record and keep bold `[INSERT ...]` placeholders in ALL CAPS for any fact not present in the record (such as collecting bank branch or return memo receipt date).
- Do NOT array any non-signatory family member or independent non-executive director who is legally immune under Section 141 NI Act / SMS Pharmaceuticals Ltd. v. Neeta Bhalla.
- If the prior case audit established that the cheque is already stale (>3 months) or time-barred, include this 1-line caution at the very top: `[CHAMBERS ADVISORY NOTE: As per the case audit, this cheque was presented beyond the 3-month validity window under Section 138 Proviso (a); verify whether a Civil Recovery Notice / Order XXXVII Summary Suit should be issued instead.]`

BY REGISTERED POST A.D. / SPEED POST / EMAIL

[NAME OF ADVOCATE]
Advocate | Enrollment No.: [INSERT ENROLLMENT NO.]
Chamber / Office: [INSERT CHAMBER / OFFICE ADDRESS]
Email: [INSERT EMAIL] | Mobile: [INSERT MOBILE NO.]

Ref. No.: [INSERT REF. NO.]
Date: [INSERT DATE OF DISPATCH]

To,
1. [Full Name & Registered Address of Drawer Company / Firm / Individual] ("Noticee No. 1")
2. [Full Name & Address of Authorized Signatory / Active Director In-Charge u/s 141 NI Act] ("Noticee No. 2")

SUBJECT: STATUTORY DEMAND NOTICE UNDER SECTION 138 READ WITH SECTION 141 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881 FOR DISHONOUR OF CHEQUE NO. [INSERT CHEQUE NO.] DATED [INSERT DRAW DATE] FOR RS. [INSERT EXACT CHEQUE AMOUNT]/-.

Sir/Madam,

Under instructions from and on behalf of my Client, [Full Name, Constitution & Address of Payee / Complainant] (hereinafter referred to as "my Client"), I hereby serve upon you the following Statutory Legal Demand Notice under Section 138 read with Section 141 of the Negotiable Instruments Act, 1881:

1. **COMMERCIAL TRANSACTION & LEGALLY ENFORCEABLE DEBT:** That my Client is engaged in the business of [insert business/supply description from record] and supplied goods/services to Noticee No. 1 against Invoice / Contract No. [insert invoice/ref from record] dated [insert date from record], thereby giving rise to a liquidated and legally enforceable debt and liability of Rs. [Insert Exact Principal Cheque Amount]/- (Rupees [Insert Amount in Words] Only).
2. **VICARIOUS LIABILITY UNDER SECTION 141 NI ACT:** That Noticee No. 1 is a [Company / Partnership Firm] and Noticee No. 2 is the Authorized Signatory of the dishonoured instrument in question and was, at the time the offence was committed, in charge of and directly responsible to Noticee No. 1 for the conduct of its day-to-day business and affairs within the meaning of Section 141 of the Negotiable Instruments Act, 1881.
3. **ISSUANCE OF NEGOTIABLE INSTRUMENT:** That in discharge of the aforesaid legally enforceable debt and liability, you issued Cheque No. [Insert Cheque No.] dated [Insert Draw Date] for an assured sum of Rs. [Insert Exact Cheque Amount]/- (Rupees [Insert Amount in Words] Only) drawn on [Insert Drawee Bank & Branch from record or `[INSERT DRAWEE BANK & BRANCH]`] in favour of my Client.
4. **PRESENTATION & DISHONOUR OF INSTRUMENT:** That my Client presented the aforesaid cheque for encashment through its collecting banker, [Insert Collecting Bank & Branch from record or `[INSERT COLLECTING BANK & BRANCH]`]; however, the said cheque was returned unpaid and dishonoured by your banker with the endorsement "[Insert Dishonour Reason, e.g., Funds Insufficient / Account Closed]" vide Bank Return Memo dated [Insert Return Memo Date or `[INSERT RETURN MEMO DATE]`], intimation whereof was received by my Client on [Insert Return Memo Receipt Date or `[INSERT RETURN MEMO RECEIPT DATE]`].
5. **STATUTORY PRESUMPTION UNDER SECTIONS 118 & 139 NI ACT:** That the dishonour of the aforesaid cheque establishes your failure to honour a valid negotiable instrument issued towards a legally enforceable debt. Under Sections 118(a) and 139 of the Negotiable Instruments Act, 1881, there is a statutory presumption that the said cheque was drawn for consideration and in discharge of a legally enforceable debt or liability.
6. **STATUTORY DEMAND UNDER SECTION 138 PROVISO (b) & (c) (SEVERED DEMAND PER SUMAN SETHI V. AJAY K. CHURIWAL):** I, therefore, under instructions from my Client, hereby call upon you to pay the exact dishonoured cheque amount of **Rs. [Insert Exact Cheque Amount]/- (Rupees [Insert Amount in Words] Only)** to my Client within a clear period of **15 (FIFTEEN) DAYS** from the date of receipt of this Legal Notice. Separately and severably from the above statutory demand of the principal cheque amount, you are also called upon to pay a sum of Rs. [INSERT NOTICE COST, E.G., 15,000]/- towards the professional charges of this Legal Notice.
7. **CONSEQUENCES OF DEFAULT:** Take explicit notice that in the event you fail to pay the aforesaid principal cheque amount of Rs. [Insert Exact Cheque Amount]/- within 15 (fifteen) clear days from the date of receipt of this Notice, my Client shall be constrained to institute criminal prosecution against you under Section 138 read with Sections 141 and 142 of the Negotiable Instruments Act, 1881 and Section 223 of the Bharatiya Nagarik Suraksha Sanhita, 2023 before the competent Court of the Learned Judicial Magistrate First Class (wherein you shall be liable for imprisonment for a term which may extend to two years, or with fine which may extend to twice the amount of the cheque, or with both), besides instituting summary civil recovery proceedings under Order XXXVII of the Code of Civil Procedure, 1908 along with statutory interest @ 18% per annum under Section 80 of the Negotiable Instruments Act, 1881, entirely at your risk, cost, and consequences.

A copy of this Statutory Legal Notice is retained in my office for record and further legal proceedings.

Yours faithfully,
[NAME OF ADVOCATE]
Advocate — Counsel for the Notice-Sender
""",

    "Reply to Legal Demand Notice (Defense)": """
DRAFTING BLUEPRINT — REPLY TO LEGAL DEMAND NOTICE (DEFENSE):
STRICT DEFENSE PLEADING RULES:
1. Output ONLY the formal Legal Reply below.
2. NEVER refer to your own Clients as "Accused No. 1" or "Accused No. 2" (no court has taken cognizance yet). Always refer to them as **"Noticee No. 1"** and **"Noticee No. 2"** or **"my Clients"**.
3. NEVER use colloquial slang like "dead on arrival". Always use formal statutory language: *"void ab initio, non-est in the eyes of law, and legally unenforceable"*.
4. NEVER invent an unverified factual defense (like "blank security cheque") in Part II—always keep the bold bracketed placeholders `[INSERT CLIENT'S SPECIFIC FACTUAL DEFENSE REGARDING THE UNDERLYING TRANSACTION]` and `[INSERT CLIENT'S FACTUAL DEFENSE REGARDING CUSTODY / ISSUANCE OF THE CHEQUE]` intact so the lawyer fills in the client's verified instructions.
5. Under PART II, you MUST reply sequentially to EVERY SINGLE PARAGRAPH of the Notice under reply from Para 1 to the final paragraph—never skip any paragraph.

WITHOUT PREJUDICE
BY REGISTERED POST A.D. / SPEED POST / EMAIL

[NAME OF ADVOCATE]
Advocate | Enrollment No.: [INSERT ENROLLMENT NO.]
Chamber / Office: [INSERT CHAMBER / OFFICE ADDRESS]
Email: [INSERT EMAIL] | Mobile: [INSERT MOBILE NO.]

Ref. No.: [INSERT REF. NO.]
Date: [INSERT DATE OF REPLY]

To,
[Extract Exact Name & Chamber Address of Complainant's Advocate from the Notice, or `Counsel for [Complainant Name], [INSERT ADDRESS OF COMPLAINANT'S ADVOCATE]`]

SUBJECT: REPLY ON BEHALF OF MY CLIENTS, (1) [NAME OF NOTICEE NO. 1] AND (2) [NAME OF NOTICEE NO. 2], TO YOUR DEFECTIVE AND LEGALLY UNSUSTAINABLE DEMAND NOTICE DATED [NOTICE DATE] ISSUED ON BEHALF OF [COMPLAINANT NAME].

Sir/Madam,

Under instructions from and on behalf of my Clients, (1) [Full Name & Address of Noticee No. 1] (hereinafter referred to as "Noticee No. 1") and (2) [Full Name & Address of Noticee No. 2] (hereinafter referred to as "Noticee No. 2"), I hereby serve upon you the following formal Reply to your Legal Demand Notice dated [Date of Notice]:

PRELIMINARY STATEMENT OF OMNIBUS DENIAL:
At the very outset, my Clients deny each and every allegation, averment, contention, and pecuniary demand contained in your Legal Notice under reply in toto as false, frivolous, vexatious, and unsustainable in law and on facts. Save and except what is expressly admitted hereinbelow strictly as a matter of record, nothing stated in your Notice under reply shall be deemed admitted merely for want of specific traversal.

PART I — PRELIMINARY LEGAL & STATUTORY OBJECTIONS:
Without prejudice to the merits of the dispute, your Legal Notice dated [Date of Notice] is *void ab initio*, *non-est* in the eyes of law, and incapable of giving rise to any valid cause of action under Section 138 read with Section 142 of the Negotiable Instruments Act, 1881 on the following fatal statutory grounds:

1. **BAR OF LIMITATION / STALE INSTRUMENT UNDER SECTION 138 PROVISO (a) NI ACT:** (Set out the exact cheque draw date, the 3-calendar-month expiry date under Section 138 Proviso (a) of the NI Act read with *Shri Ishar Alloy Steels Ltd. v. Jayaswal Neco Ltd.*, (2001) 3 SCC 609, and how the admission in Para 3 of the notice that the cheque was presented on [Presentation Date]—after expiry of the 3-month statutory validity—renders the instrument stale and the notice *void ab initio*).
2. **ILLEGAL & INDIVISIBLE OMNIBUS DEMAND UNDER SECTION 138 PROVISO (b) NI ACT:** (Set out how Para 6 of the notice demands an indivisible consolidated sum of Rs. [Omnibus Amount]/- merging unquantified damages and penalties with the principal cheque amount of Rs. [Cheque Amount]/- without statutory severance, directly violating the law laid down by the Hon'ble Supreme Court in *Suman Sethi v. Ajay K. Churiwal*, (2000) 2 SCC 380 and *Rahul Builders v. Arihant Fertilizers & Chemical*, (2008) 2 SCC 321, which vitiates the notice in its entirety).
3. **ILLEGAL TRUNCATION OF MANDATORY 15-DAY CURE WINDOW UNDER SECTION 138 PROVISO (c) R/W SECTION 142(1)(b) NI ACT:** (Set out how Para 7 of the notice grants only 07 days for payment instead of the mandatory 15 clear days from receipt prescribed under Section 138 Proviso (c), preventing any lawful cause of action from accruing under Section 142(1)(b) of the NI Act in light of the Three-Judge Bench judgment in *Yogendra Pratap Singh v. Savitri Pandey*, (2014) 10 SCC 713).
4. **IMPERMISSIBLE IMPLEADMENT OF NON-SIGNATORY / NON-EXECUTIVE DIRECTOR UNDER SECTION 141 NI ACT:** (Set out how Para 2 of the notice explicitly admits that Noticee No. 2 is a non-executive director who does not participate in day-to-day business operations and did not sign the instrument, barring any vicarious liability under Section 141 of the NI Act in terms of *SMS Pharmaceuticals Ltd. v. Neeta Bhalla*, (2005) 8 SCC 89, *Pooja Ravinder Devidasani v. State of Maharashtra*, (2014) 16 SCC 1, and *Aparna A. Shah v. Sheth Developers Pvt. Ltd.*, (2013) 8 SCC 71).

PART II — PARA-WISE REPLY ON MERITS:
Without prejudice to the preliminary statutory objections set out in Part I above, which strike at the very root of maintainability, the para-wise reply to your Notice is as under:

1. **Reply to Para 1:** That the contents of Para 1 of your Notice under reply are denied as false and incorrect. It is specifically denied that a sum of Rs. [Cheque Amount]/- is due or payable by Noticee No. 1 to your Client towards any legally enforceable debt or liability. [INSERT CLIENT'S SPECIFIC FACTUAL DEFENSE REGARDING THE UNDERLYING TRANSACTION].
2. **Reply to Para 2:** That the contents of Para 2 of your Notice are admitted strictly to the extent of your own categorical admission on record that Noticee No. 2 ([Name]) is a non-executive director who neither participates in day-to-day business operations nor signed the cheque in question. The rest of Para 2 attempting to fasten vicarious liability upon Noticee No. 2 is denied as wholly illegal and contrary to Section 141 of the NI Act (*SMS Pharmaceuticals Ltd. v. Neeta Bhalla*).
3. **Reply to Para 3:** That the contents of Para 3 of your Notice are denied to the extent they allege that Cheque No. [No.] dated [Draw Date] was issued towards discharge of a subsisting legally enforceable liability ([INSERT CLIENT'S FACTUAL DEFENSE REGARDING CUSTODY / ISSUANCE OF THE CHEQUE]). Without prejudice, your own admission in Para 3 that the cheque dated [Draw Date] was presented to the drawee bank only on [Presentation Date]—after its 3-month statutory validity had already expired on [Expiry Date]—establishes on the face of the record that the instrument was stale under Section 138 Proviso (a) of the NI Act.
4. **Reply to Para 4:** That the contents of Para 4 of your Notice regarding the bank return memo are a matter of bank record; however, it is denied that the return of a stale cheque presented beyond its 3-month validity period gives rise to any penal offence under Section 138 of the NI Act.
5. **Reply to Para 5:** That the contents of Para 5 of your Notice are vehemently denied in toto. The allegations of mala fide intent, dishonesty, or inducement are false and baseless, and no statutory presumption under Section 139 of the NI Act can be invoked in respect of a stale instrument and a statutorily defective notice.
6. **Reply to Para 6:** That the contents of Para 6 of your Notice are denied as illegal and unsustainable in law. Your consolidated, indivisible omnibus demand of Rs. [Omnibus Amount]/- clubbing arbitrary damages and penalties with the principal cheque amount of Rs. [Cheque Amount]/- without severance invalidates the demand notice under Section 138 Proviso (b) of the NI Act (*Suman Sethi v. Ajay K. Churiwal*).
7. **Reply to Para 7:** That the contents of Para 7 of your Notice are denied in toto. Your demand calling upon my Clients to make payment within 07 days under threat of criminal prosecution is in direct violation of the mandatory 15-day cure period prescribed under Section 138 Proviso (c) read with Section 142(1)(b) of the NI Act (*Yogendra Pratap Singh v. Savitri Pandey*).

PART III — CONCLUDING DEMAND & NOTICE OF COSTS:
In view of the fatal statutory infirmities placed on record hereinabove, your Legal Notice dated [Date] is *void ab initio*, *non-est* in the eyes of law, and legally unenforceable. You are hereby called upon to advise your Client to withdraw the said defective Notice forthwith in writing within 7 (seven) days of receipt of this Reply. Take explicit notice that if your Client institutes any false, malicious, or premature criminal complaint on the basis of this void Notice, this Reply shall be placed before the Learned Judicial Magistrate First Class at the pre-cognizance stage under the First Proviso to Section 223(1) of the Bharatiya Nagarik Suraksha Sanhita, 2023, and my Clients shall immediately move the Hon'ble High Court under Section 528 of the BNSS, 2023 for quashing of proceedings, besides initiating proceedings for malicious prosecution under Section 248 of the Bharatiya Nyaya Sanhita, 2023 and seeking exemplary costs, entirely at your Client's risk, cost, and peril.

A copy of this Reply is retained in my office for record and production before the competent Court of Law.

Yours faithfully,
[NAME OF ADVOCATE]
Advocate — Counsel for the Noticees
""",

    "Complaint u/s 138 NI Act r/w Sec 223 BNSS": """
DRAFTING BLUEPRINT — CRIMINAL COMPLAINT UNDER SECTION 138 R/W SECTIONS 141 & 142 NI ACT AND SECTION 223 BNSS, 2023:
STRICT RULES FOR THIS TEMPLATE:
- Output ONLY the complete Court Complaint package below (Cause Title, Verbatim Complaint Paragraphs 1–12, Prayer, Verification, Page-Separated Section 145(1) Pre-Summoning Evidence Affidavit, List of Witnesses, and List of Documents).
- Do NOT array any non-executive director who is legally immune under Section 141 NI Act.
- Never invent missing dates or bank names; keep bold `[INSERT ...]` placeholders in ALL CAPS for any missing fact.
- Keep `... COMPLAINANT` and `... ACCUSED PERSON(S)` on their own separate line below the party address so they right-align cleanly.

IN THE COURT OF THE LEARNED JUDICIAL MAGISTRATE FIRST CLASS (NI ACT), AT [INSERT DISTRICT / COURTS COMPLEX]
COMPLAINT CASE NO. ________ OF 2026

IN THE MATTER OF:
[Full Name, Constitution & Registered Address of Complainant]
Through its Authorized Representative / Proprietor [INSERT NAME OF AUTHORIZED REPRESENTATIVE]
... COMPLAINANT

VERSUS

1. [Full Name & Registered Address of Accused No. 1 Company / Firm / Drawer]
2. [Full Name & Address of Accused No. 2 Authorized Signatory / Active Director u/s 141 NI Act]
... ACCUSED PERSON(S)

COMPLAINT UNDER SECTION 138 READ WITH SECTIONS 141 AND 142 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881 READ WITH SECTION 210 AND SECTION 223 OF THE BHARATIYA NAGARIK SURAKSHA SANHITA, 2023

MOST RESPECTFULLY SHOWETH:

1. **DESCRIPTION & COMPETENCY OF COMPLAINANT:** That the Complainant is a [Company / Partnership Firm / Proprietorship Concern] having its registered office at [Insert Address from record], and the present Complaint is being instituted through its Authorized Representative / Proprietor, Mr./Ms. [INSERT NAME OF AUTHORIZED REPRESENTATIVE], who is duly authorized vide Board Resolution / Letter of Authority dated [INSERT AUTHORITY DATE] to sign, verify, institute, and depose in the present proceedings, and is fully conversant with the facts and records of the case. The Complainant is the "payee" and "holder in due course" of the dishonoured cheque in question within the meaning of Section 142(1)(a) of the Negotiable Instruments Act, 1881.
2. **DESCRIPTION OF ACCUSED & MANDATORY AVERMENTS UNDER SECTION 141 NI ACT:** That Accused No. 1 is a [Company / Firm] having its registered office at [Insert Address from record]. Accused No. 2, [Insert Name of Signatory or `[INSERT NAME OF AUTHORIZED SIGNATORY]`], is the Authorized Signatory who signed the cheque in question and was, at the time the offence was committed, in charge of and directly responsible to Accused No. 1 for the conduct of its day-to-day business and affairs within the meaning of Section 141(1) of the Negotiable Instruments Act, 1881 (*SMS Pharmaceuticals Ltd. v. Neeta Bhalla*, (2005) 8 SCC 89). Furthermore, the offence was committed with the active consent and connivance of Accused No. 2 within the meaning of Section 141(2) of the NI Act.
3. **COMMERCIAL TRANSACTION & LEGALLY ENFORCEABLE DEBT:** That in the ordinary course of business, the Accused approached the Complainant for the supply of [Insert Goods / Services from record], and the Complainant duly supplied the same against Invoice No. [Insert Invoice No. from record] dated [Insert Invoice Date from record] for a total legally enforceable debt and liability of Rs. [Insert Exact Cheque Amount]/- (Rupees [Insert Amount in Words] Only) within the meaning of the Explanation to Section 138 of the Negotiable Instruments Act, 1881.
4. **ISSUANCE OF CHEQUE IN DISCHARGE OF LIABILITY:** That in discharge of the aforesaid legally enforceable debt and liability, the Accused issued Cheque No. [Insert Cheque No.] dated [Insert Draw Date] for an assured sum of Rs. [Insert Exact Cheque Amount]/- (Rupees [Insert Amount in Words] Only) drawn on [Insert Drawee Bank & Branch from record] in favour of the Complainant, with the categorical assurance that the said cheque would be honoured upon presentation.
5. **PRESENTATION OF CHEQUE [SEC 138 PROVISO (a)]:** That relying upon the assurances of the Accused, the Complainant presented the aforesaid Cheque No. [Insert Cheque No.] for encashment through its collecting banker, [INSERT COMPLAINANT'S COLLECTING BANK & BRANCH], on [Insert Presentation Date], for encashment in accordance with Proviso (a) to Section 138 of the Negotiable Instruments Act, 1881.
6. **DISHONOUR OF CHEQUE & BANK RETURN MEMO:** That the aforesaid cheque was returned unpaid and dishonoured by the banker of the Accused vide Bank Return Memo dated [Insert Return Memo Date] with the remarks "[Insert Dishonour Reason, e.g., Funds Insufficient]", which Return Memo was received by the Complainant from its banker on [Insert Return Memo Receipt Date or `[INSERT RETURN MEMO RECEIPT DATE]`].
7. **SERVICE OF STATUTORY DEMAND NOTICE WITHIN 30 DAYS [SEC 138 PROVISO (b)]:** That thereafter, within the statutory period of 30 (thirty) days from the receipt of intimation of dishonour from the bank (excluding the day of receipt in terms of Section 9 of the General Clauses Act, 1897 and *Econ Antri Ltd. v. Rom Industries Ltd.*), the Complainant through its Counsel dispatched a Statutory Legal Demand Notice dated [Insert Notice Date] via Speed Post / Registered Post A.D. calling upon the Accused to pay the dishonoured cheque amount of Rs. [Insert Exact Cheque Amount]/- within 15 (fifteen) clear days of the receipt thereof.
8. **DELIVERY OF NOTICE, EXPIRY OF 15-DAY CURE PERIOD & ACCRUAL OF CAUSE OF ACTION [SEC 138 PROVISO (c)]:** That the aforesaid Statutory Demand Notice was duly served upon the Accused on [INSERT NOTICE DELIVERY DATE] as evidenced by the official Postal Tracking Report. Despite due service of the Statutory Demand Notice, the Accused failed and neglected to make payment of the dishonoured cheque amount within the mandatory period of 15 (fifteen) clear days, which expired on [INSERT 15TH DAY EXPIRY DATE]. Consequently, the cause of action to institute the present Complaint accrued on the 16th day, i.e., on [INSERT 16TH DAY CAUSE OF ACTION DATE], in terms of *Yogendra Pratap Singh v. Savitri Pandey*, (2014) 10 SCC 713.
9. **STATUTORY PRESUMPTION UNDER SECTIONS 118 & 139 NI ACT:** That under Sections 118(a) and 139 of the Negotiable Instruments Act, 1881, there is a mandatory statutory presumption that the cheque in question was drawn for consideration and issued by the Accused in discharge of a legally enforceable debt and liability.
10. **LIMITATION COMPLIANCE UNDER SECTION 142(1)(b) NI ACT:** That the present Complaint is being filed within the statutory limitation period of 1 (one) calendar month from the date on which the cause of action arose under Section 142(1)(b) read with Proviso (c) to Section 138 of the Negotiable Instruments Act, 1881.
11. **TERRITORIAL JURISDICTION UNDER SECTION 142(2)(a) NI ACT:** That the dishonoured cheque was delivered for collection through the bank account maintained by the Complainant with its collecting banker, [INSERT COMPLAINANT'S COLLECTING BANK & BRANCH], which is situated within the local territorial limits of this Hon'ble Court. Accordingly, this Hon'ble Court has the requisite territorial jurisdiction to entertain and try the present Complaint under Section 142(2)(a) of the Negotiable Instruments Act, 1881 (*Bridgestone India Pvt. Ltd. v. Inderpal Singh*, (2016) 2 SCC 75).
12. **MANDATORY DISCLOSURE PER DAMODAR S. PRABHU V. SAYED BABALAL H., (2010) 5 SCC 663:** That the Complainant categorically declares and affirms that no other criminal complaint has been filed or is pending before this Hon'ble Court or any other Court in India between the parties in respect of the dishonour of the aforesaid Cheque No. [Insert Cheque No.] dated [Insert Draw Date].

PRAYER:
It is, therefore, most respectfully prayed that this Hon'ble Court may graciously be pleased to:
(a) Issue notice to the Accused in compliance with the First Proviso to Section 223(1) of the Bharatiya Nagarik Suraksha Sanhita, 2023 and take cognizance of the offence committed by the Accused under Section 138 read with Sections 141 and 142 of the Negotiable Instruments Act, 1881;
(b) Issue summons and process against the Accused under Section 227 of the Bharatiya Nagarik Suraksha Sanhita, 2023 and try the Accused in accordance with the summary trial procedure under Section 143 of the NI Act read with Sections 283 to 288 of the BNSS, 2023;
(c) Direct the Accused to pay interim compensation to the Complainant to the extent of 20% of the cheque amount under Section 143A of the Negotiable Instruments Act, 1881;
(d) Convict and sentence the Accused to imprisonment for a term extending to 2 (two) years and impose a fine extending to twice the amount of the cheque under Section 138 of the NI Act, and award appropriate compensation to the Complainant out of the fine amount under Section 395 of the Bharatiya Nagarik Suraksha Sanhita, 2023; and
(e) Pass such other or further order(s) as this Hon'ble Court may deem fit and proper in the facts and circumstances of the case and in the interest of justice.

Place: [INSERT PLACE]
Date: [INSERT DATE]

COMPLAINANT
THROUGH
[NAME OF ADVOCATE]
Advocate — Counsel for the Complainant
Enrollment No.: [INSERT ENROLLMENT NO.]

VERIFICATION:
Verified at [INSERT PLACE] on this [INSERT DAY] day of [INSERT MONTH], 2026 that the contents of Paragraphs 1 to 12 of the above Complaint are true and correct to my personal knowledge and belief derived from the official records of the Complainant maintained in the ordinary course of business, and nothing material has been concealed therefrom.

COMPLAINANT

---
IN THE COURT OF THE LEARNED JUDICIAL MAGISTRATE FIRST CLASS (NI ACT), AT [INSERT DISTRICT / PLACE]
COMPLAINT CASE NO. ________ OF 2026

IN THE MATTER OF:
[Complainant Name]
... COMPLAINANT
VERSUS
[Accused Name(s)]
... ACCUSED PERSON(S)

PRE-SUMMONING EVIDENCE BY WAY OF AFFIDAVIT OF THE COMPLAINANT UNDER SECTION 145(1) OF THE NEGOTIABLE INSTRUMENTS ACT, 1881

I, [INSERT NAME OF DEPONENT], S/o [INSERT FATHER'S NAME], aged about [INSERT AGE] years, Authorized Representative / Proprietor of the Complainant, having office at [Insert Address], do hereby solemnly affirm and declare on oath as under:

1. **COMPETENCY OF DEPONENT:** That I am the Authorized Representative / Proprietor of the Complainant in the above-captioned case and am well conversant with the facts and circumstances of the case on the basis of official records maintained by the Complainant. I am competent to swear and depose the present Affidavit under Section 145(1) of the Negotiable Instruments Act, 1881. The Copy of the Board Resolution / Authority Letter is exhibited hereto as **Ex. CW-1/1**.
2. **ADOPTION OF COMPLAINT AVERMENTS:** That the accompanying Complaint under Section 138 read with Sections 141 and 142 of the Negotiable Instruments Act, 1881 has been drafted by my Counsel under my instructions. I adopt and reiterate the contents of Paragraphs 1 to 12 of the accompanying Complaint as part and parcel of my examination-in-chief by way of this Affidavit, the same not being repeated herein for the sake of brevity.
3. **EXHIBITION OF PRIMARY DOCUMENTS:** That the Invoice / Statement of Account evidencing the legally enforceable debt of Rs. [Insert Exact Cheque Amount]/- is exhibited as **Ex. CW-1/2**. The Original Dishonoured Cheque No. [Insert Cheque No.] dated [Insert Draw Date] for Rs. [Insert Exact Cheque Amount]/- is exhibited as **Ex. CW-1/3**. The Original Bank Return Memo dated [Insert Return Memo Date] is exhibited as **Ex. CW-1/4**. The Office Copy of the Statutory Legal Demand Notice dated [Insert Notice Date] is exhibited as **Ex. CW-1/5**. The Original Postal Receipt(s) and Internet Tracking Report along with the mandatory Certificate under Section 63 of the Bharatiya Sakshya Adhiniyam, 2023 (earlier Section 65B IEA) are exhibited collectively as **Ex. CW-1/6 (Colly)**.
4. **NON-PAYMENT & LIMITATION:** That the Accused have failed to make payment of the dishonoured cheque amount within 15 clear days of service of the Statutory Demand Notice, and the Complaint has been instituted within statutory limitation.

DEPONENT

VERIFICATION:
Verified at [INSERT PLACE] on this [INSERT DAY] day of [INSERT MONTH], 2026 that the contents of Paragraphs 1 to 4 of my above Evidence Affidavit are true and correct to my knowledge and belief, and nothing material has been concealed therefrom.

DEPONENT

---
LIST OF WITNESSES
1. Mr./Ms. [INSERT NAME OF COMPLAINANT WITNESS], Complainant / Authorized Representative of the Complainant.
2. Concerned Bank Official / Record Clerk from [INSERT COMPLAINANT'S COLLECTING BANK & BRANCH], along with certified bank records (if required).
3. Concerned Bank Official / Record Clerk from [Insert Drawee Bank & Branch], along with account opening form and specimen signatures of the Accused (if required).
4. Any other witness with the prior permission of this Hon'ble Court.

LIST OF DOCUMENTS ATTACHED WITH THE COMPLAINT
| S.No. | Description of Document | Exhibit Mark | Original / Copy |
| :--- | :--- | :--- | :--- |
| 1. | Board Resolution / Letter of Authority | Ex. CW-1/1 | Copy / Original |
| 2. | Tax Invoice / Ledger Statement dated [Insert Invoice Date] | Ex. CW-1/2 | Office Copy |
| 3. | Original Cheque No. [Insert Cheque No.] dated [Insert Draw Date] for Rs. [Insert Exact Cheque Amount]/- | Ex. CW-1/3 | Original |
| 4. | Original Bank Return Memo dated [Insert Return Memo Date] | Ex. CW-1/4 | Original |
| 5. | Signed Office Copy of Statutory Legal Demand Notice dated [Insert Notice Date] | Ex. CW-1/5 | Office Copy |
| 6. | Original Postal Receipt(s), Tracking Report & Sec 63 BSA Certificate | Ex. CW-1/6 | Original |

Place: [INSERT PLACE]
Date: [INSERT DATE]

[NAME OF ADVOCATE]
Advocate — Counsel for the Complainant
""",

    "Sec 528 BNSS (482 CrPC) Quashing Petition": """
DRAFTING BLUEPRINT — HIGH COURT QUASHING PETITION UNDER SECTION 528 OF THE BHARATIYA NAGARIK SURAKSHA SANHITA, 2023 (EARLIER SECTION 482 CRPC):
STRICT RULES FOR THIS TEMPLATE:
- Output ONLY the complete High Court Quashing Petition package below (Cause Title, Verbatim Paragraphs, Questions of Law, Chronological Facts in numbered sub-paragraphs 3.1 to 3.4, Grounds A–E, Mandatory Non-Filing Declaration, Prayer, and Page-Separated Supporting Affidavit).
- DYNAMIC STATE & HIGH COURT MAPPING: Identify the State/UT from the court/bank/party addresses in the uploaded document and use the exact official High Court title and State Respondent name (e.g., "IN THE HIGH COURT OF PUNJAB AND HARYANA AT CHANDIGARH" & "State of Haryana"; "IN THE HIGH COURT OF JUDICATURE AT BOMBAY" & "State of Maharashtra"; "IN THE HIGH COURT OF JUDICATURE AT ALLAHABAD" & "State of Uttar Pradesh"; "IN THE HIGH COURT OF DELHI AT NEW DELHI" & "State of NCT of Delhi"). Never write "High Court of New Delhi" or "High Court of Judicature at New Delhi". If no city/state is mentioned in the record, keep the neutral placeholders `IN THE HIGH COURT OF [INSERT STATE] AT [INSERT BENCH]` and `State of [INSERT STATE]`.
- Never invent Complaint Case Numbers or Summoning Order dates; keep bold `[INSERT ...]` placeholders in ALL CAPS.
- Keep `... PETITIONER(S)` and `... RESPONDENT(S)` on their own separate line below the party addresses.

IN THE HIGH COURT OF [INSERT STATE, E.G., DELHI AT NEW DELHI / PUNJAB AND HARYANA AT CHANDIGARH / JUDICATURE AT BOMBAY]
EXTRAORDINARY CRIMINAL JURISDICTION
CRIMINAL MISC. PETITION NO. ________ OF 2026

IN THE MATTER OF:
1. [Full Name & Registered Address of Petitioner No. 1 / Drawer Company]
2. [Full Name & Residential Address of Petitioner No. 2 / Director]
... PETITIONER(S)

VERSUS

1. State of [INSERT STATE] (Through Standing Counsel / Public Prosecutor)
2. [Full Name & Address of Complainant / Respondent No. 2]
... RESPONDENT(S)

PETITION UNDER SECTION 528 OF THE BHARATIYA NAGARIK SURAKSHA SANHITA, 2023 (CORRESPONDING TO SECTION 482 OF THE CODE OF CRIMINAL PROCEDURE, 1973) SEEKING QUASHING OF CRIMINAL COMPLAINT CASE NO. [INSERT COMPLAINT CASE NO.] TITLED "[COMPLAINANT] V. [ACCUSED]" UNDER SECTION 138 READ WITH SECTION 141 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881 PENDING BEFORE THE LEARNED JUDICIAL MAGISTRATE FIRST CLASS (NI ACT), [INSERT DISTRICT / COURT], THE IMPUGNED SUMMONING ORDER DATED [INSERT SUMMONING ORDER DATE], AND ALL CONSEQUENTIAL PROCEEDINGS ARISING THEREFROM.

MOST RESPECTFULLY SHOWETH:

1. **INVOCATION OF INHERENT JURISDICTION:** That by way of the present Petition under Section 528 of the Bharatiya Nagarik Suraksha Sanhita, 2023 (corresponding to Section 482 of the erstwhile Code of Criminal Procedure, 1973), the Petitioner(s) invoke the inherent and extraordinary jurisdiction of this Hon'ble Court to prevent manifest abuse of the process of the Court and to secure the ends of justice, seeking quashing of Criminal Complaint Case No. [INSERT COMPLAINT CASE NO.], the impugned Summoning Order dated [INSERT SUMMONING ORDER DATE], and the underlying defective Legal Demand Notice dated [Insert Notice Date].

2. **SUBSTANTIAL QUESTIONS OF LAW INVOLVED:**
That the present Petition raises the following substantial Questions of Law of public and statutory importance:
- **QUESTION A:** Whether a criminal prosecution under Section 138 of the Negotiable Instruments Act, 1881 is maintainable where the Respondent's own statutory notice/complaint admits on the face of the record that Cheque No. [Insert Cheque No.] dated [Insert Draw Date] was presented to the drawee bank on [Insert Presentation Date], after the expiry of the mandatory 3-calendar-month validity period under Proviso (a) to Section 138 of the NI Act (*Shri Ishar Alloy Steels Ltd. v. Jayaswal Neco Ltd.*, (2001) 3 SCC 609)?
- **QUESTION B:** Whether a Legal Demand Notice that demands an indivisible, consolidated omnibus sum of Rs. [Insert Omnibus Amount]/- (merging unquantified damages and penalties with the principal cheque amount of Rs. [Insert Exact Cheque Amount]/- without severance) complies with Proviso (b) to Section 138 of the NI Act, or is *void ab initio* under the binding ratio of *Suman Sethi v. Ajay K. Churiwal*, (2000) 2 SCC 380 and *Rahul Builders v. Arihant Fertilizers & Chemical*, (2008) 2 SCC 321?
- **QUESTION C:** Whether a Legal Demand Notice that truncates the mandatory 15-day statutory cure period to [Insert Truncated Days, e.g., 07] days under threat of immediate prosecution satisfies Proviso (c) to Section 138 read with Section 142(1)(b) of the NI Act in light of the Three-Judge Bench decision of the Hon'ble Supreme Court in *Yogendra Pratap Singh v. Savitri Pandey*, (2014) 10 SCC 713?
- **QUESTION D:** Whether a non-signatory, non-executive director against whom the statutory notice/complaint itself contains an express admission of non-involvement in day-to-day business operations can be vicariously prosecuted under Section 141 of the NI Act in light of *SMS Pharmaceuticals Ltd. v. Neeta Bhalla*, (2005) 8 SCC 89 and *Pooja Ravinder Devidasani v. State of Maharashtra*, (2014) 16 SCC 1?

3. **BRIEF CHRONOLOGICAL FACTS OF THE CASE:**
3.1. **Alleged Commercial Transaction:** That Respondent No. 2 alleges to have supplied goods/services to Petitioner No. 1 under Invoice No. [Insert Invoice No.] dated [Insert Invoice Date] for a stated sum of Rs. [Insert Exact Cheque Amount]/-.
3.2. **Issuance & Late Presentation of Instrument:** That Cheque No. [Insert Cheque No.] bears the draw date of [Insert Draw Date] for Rs. [Insert Exact Cheque Amount]/- drawn on [Insert Drawee Bank & Branch]. Under Section 138 Proviso (a) of the NI Act, the 3-calendar-month validity of the said instrument expired on [Insert 3-Month Expiry Date]. However, as admitted in Para 3 of Respondent No. 2's own Legal Notice, the cheque was presented to the drawee bank only on [Insert Presentation Date], after the instrument had already become stale, and was returned vide Return Memo dated [Insert Return Memo Date].
3.3. **Service of Statutorily Defective Demand Notice:** That Respondent No. 2 thereafter issued a defective Legal Demand Notice dated [Insert Notice Date] which (i) demanded an illegal, indivisible omnibus sum of Rs. [Insert Omnibus Amount]/- instead of the cheque amount of Rs. [Insert Exact Cheque Amount]/- (Para 6), (ii) illegally truncated the mandatory 15-day cure window to [Insert Days, e.g., 07] days (Para 7), and (iii) arrayed Petitioner No. 2 despite admitting in Para 2 that Petitioner No. 2 is a non-executive director who neither participates in day-to-day business operations nor signed the instrument.
3.4. **Impugned Summoning Order:** That despite the aforesaid express statutory bars apparent on the face of the record, the Learned Trial Court mechanically took cognizance and passed the impugned Summoning Order dated [INSERT SUMMONING ORDER DATE] in Criminal Complaint Case No. [INSERT COMPLAINT CASE NO.].

4. **GROUNDS FOR QUASHING:**
That the impugned Criminal Complaint and Summoning Order are manifestly illegal, without jurisdiction, and constitute a gross abuse of the criminal justice machinery on the following amongst other grounds:

- **GROUND A: BECAUSE THE CHEQUE WAS STALE AND PRESENTED BEYOND THREE MONTHS UNDER SECTION 138 PROVISO (a) NI ACT:** That under Proviso (a) to Section 138 of the NI Act, presentation of the cheque to the drawee bank within 3 calendar months from the date on which it is drawn is an absolute statutory condition precedent. In the present case, Cheque No. [Insert Cheque No.] was drawn on [Insert Draw Date] and its 3-month validity expired on [Insert Expiry Date]. By the Respondent's own admission in Para 3 of the Notice, the instrument was presented on [Insert Presentation Date]—after expiry of its validity. Per *Shri Ishar Alloy Steels Ltd. v. Jayaswal Neco Ltd.*, (2001) 3 SCC 609, dishonour of a stale instrument cannot attract penal liability under Section 138 NI Act.
- **GROUND B: BECAUSE THE STATUTORY NOTICE IS VITIATED BY AN ILLEGAL INDIVISIBLE OMNIBUS DEMAND UNDER SECTION 138 PROVISO (b) NI ACT:** That in Para 6 of the Notice, Respondent No. 2 demanded a consolidated lump sum of Rs. [Insert Omnibus Amount]/- instead of the cheque amount of Rs. [Insert Exact Cheque Amount]/-, arbitrarily clubbing unquantified damages and penalties without severance. In *Suman Sethi v. Ajay K. Churiwal*, (2000) 2 SCC 380 and *Rahul Builders v. Arihant Fertilizers*, (2008) 2 SCC 321, the Hon'ble Supreme Court settled the law that an omnibus demand for a consolidated amount exceeding the cheque sum without clear severance invalidates the notice in toto.
- **GROUND C: BECAUSE THE NOTICE ILLEGALLY TRUNCATED THE MANDATORY 15-DAY STATUTORY CURE PERIOD UNDER SECTION 138 PROVISO (c) R/W SECTION 142(1)(b) NI ACT:** That Proviso (c) to Section 138 read with Section 142(1)(b) of the NI Act mandates a clear 15-day cure period from the date of receipt of notice before any cause of action can accrue on Day 16 (*Yogendra Pratap Singh v. Savitri Pandey*, (2014) 10 SCC 713). In Para 7 of the Notice, Respondent No. 2 unlawfully restricted the cure period to [Insert Days, e.g., 07 (SEVEN) DAYS], rendering the notice statutorily infirm.
- **GROUND D: BECAUSE IMPLEADMENT OF A NON-SIGNATORY NON-EXECUTIVE DIRECTOR VIOLATES SECTION 141 NI ACT:** That in Para 2 of the Notice, Respondent No. 2 explicitly admitted that Petitioner No. 2 ([Insert Name of Non-Executive Director]) is a non-executive director who does not participate in day-to-day business operations and did not sign the instrument. In light of the Three-Judge Bench ruling in *SMS Pharmaceuticals Ltd. v. Neeta Bhalla*, (2005) 8 SCC 89, *Pooja Ravinder Devidasani v. State of Maharashtra*, (2014) 16 SCC 1, and *Aparna A. Shah v. Sheth Developers Pvt. Ltd.*, (2013) 8 SCC 71, prosecuting a non-signatory, non-executive director in the face of such an admission is a textbook abuse of process.
- **GROUND E: BECAUSE CONTINUATION OF PROCEEDINGS VIOLATES PEPSI FOODS AND BHAJAN LAL PARAMETERS:** That as held by the Hon'ble Supreme Court in *Pepsi Foods Ltd. v. Special Judicial Magistrate*, (1998) 5 SCC 749, summoning of an accused in a criminal case is a serious matter and a Magistrate cannot act as a silent spectator. Furthermore, the present case falls squarely within Categories (1), (3), and (6) of *State of Haryana v. Bhajan Lal*, 1992 Supp (1) SCC 335, as the uncontroverted allegations in the notice/complaint disclose an express statutory bar to the institution and continuance of the proceeding.

5. **MANDATORY NON-FILING DECLARATION:**
That the Petitioner(s) have not filed any other similar petition seeking quashing of the impugned Criminal Complaint or Summoning Order either before this Hon'ble Court, the Hon'ble Supreme Court of India, or any other Court in India, and the Petitioner(s) have no other equally efficacious alternative remedy available in law.

PRAYER:
In light of the facts and grounds stated hereinabove, it is most respectfully prayed that this Hon'ble Court may graciously be pleased to:
(a) Call for the records of Criminal Complaint Case No. [INSERT COMPLAINT CASE NO.] titled "[Complainant Name] v. [Accused Name]" pending before the Court of the Learned Judicial Magistrate First Class (NI Act), [INSERT DISTRICT / COURT], and quash the said Criminal Complaint, the impugned Summoning Order dated [INSERT SUMMONING ORDER DATE], and all consequential proceedings arising therefrom qua the Petitioner(s);
(b) Grant an *ad-interim ex-parte* stay of all further proceedings in Criminal Complaint Case No. [INSERT COMPLAINT CASE NO.] before the Learned Trial Court during the pendency and final disposal of the present Petition; and
(c) Pass such other or further order(s) as this Hon'ble Court may deem fit and proper in the interest of justice.

Place: [INSERT PLACE]
Date: [INSERT DATE]

PETITIONER(S)
THROUGH
[NAME OF ADVOCATE]
Advocate — Counsel for the Petitioner(s)
Enrollment No.: [INSERT ENROLLMENT NO.]

---
IN THE HIGH COURT OF [INSERT STATE, E.G., DELHI AT NEW DELHI / PUNJAB AND HARYANA AT CHANDIGARH / JUDICATURE AT BOMBAY]
CRIMINAL MISC. PETITION NO. ________ OF 2026

IN THE MATTER OF:
[Petitioner Name(s)]
... PETITIONER(S)
VERSUS
State of [INSERT STATE] & Anr.
... RESPONDENT(S)

SUPPORTING AFFIDAVIT

I, [INSERT NAME OF DEPONENT / PETITIONER], S/o [INSERT FATHER'S NAME], aged about [INSERT AGE] years, R/o [Insert Address], do hereby solemnly affirm and state on oath as under:

1. **COMPETENCY OF DEPONENT:** That I am the Petitioner / Authorized Representative of Petitioner No. 1 in the accompanying Petition under Section 528 of the Bharatiya Nagarik Suraksha Sanhita, 2023 and am well conversant with the facts and records of the case, and am competent to swear the present Affidavit.
2. **ADOPTION OF PETITION CONTENTS:** That the accompanying Petition under Section 528 of the BNSS, 2023 has been drafted by my Counsel under my instructions, and the contents of Paragraphs 1 to 5 thereof have been read over and explained to me, which are true and correct to my knowledge based on official records and legal advice believed to be true.
3. **CERTIFICATION OF ANNEXURES:** That the annexures annexed to the accompanying Petition are true copies of their respective originals.

DEPONENT

VERIFICATION:
Verified at [INSERT PLACE] on this [INSERT DAY] day of [INSERT MONTH], 2026 that the contents of Paragraphs 1 to 3 of my above Affidavit are true and correct to my knowledge and belief, and nothing material has been concealed therefrom.

DEPONENT
""",

    "Civil Recovery Notice / Order XXXVII Summary Suit Draft": """
DRAFTING BLUEPRINT — SUMMARY SUIT PLAINT UNDER ORDER XXXVII OF THE CODE OF CIVIL PROCEDURE, 1908 (WITH SECTION 80 NI ACT INTEREST):
STRICT RULES FOR THIS TEMPLATE:
- Output ONLY the complete Order XXXVII Summary Suit Plaint package below (Cause Title, Verbatim Paragraphs 1–12 including Order XXXVII Rule 2(1)(b) mandatory declaration and Section 80 NI Act 18% statutory interest, Prayer, Order VI Rule 15 CPC Verification, and Page-Separated Supporting Affidavit).
- Under civil law, a company is a distinct juristic entity; array ONLY the Drawer Company/Firm as the Defendant unless a personal guarantee by a director is explicitly in the record. Do NOT output any internal notes in the Cause Title.
- Keep `... PLAINTIFF` and `... DEFENDANT` on their own separate line below the party addresses.
- Never invent missing dates or bank names; keep bold `[INSERT ...]` placeholders in ALL CAPS.

IN THE COURT OF THE LEARNED DISTRICT JUDGE / SENIOR CIVIL JUDGE, AT [INSERT DISTRICT / PLACE]
SUMMARY CIVIL SUIT NO. ________ OF 2026
(SUIT UNDER ORDER XXXVII OF THE CODE OF CIVIL PROCEDURE, 1908)

IN THE MATTER OF:
[Full Name, Constitution & Registered Address of Plaintiff / Payee]
Through its Authorized Representative / Proprietor [INSERT NAME OF AUTHORIZED REPRESENTATIVE]
... PLAINTIFF

VERSUS

[Full Name, Constitution & Registered Address of Defendant / Drawer Company]
... DEFENDANT

SUIT UNDER ORDER XXXVII OF THE CODE OF CIVIL PROCEDURE, 1908 FOR RECOVERY OF RS. [INSERT PRINCIPAL CHEQUE AMOUNT]/- (RUPEES [INSERT AMOUNT IN WORDS] ONLY) ALONG WITH STATUTORY INTEREST @ 18% PER ANNUM UNDER SECTION 80 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881 AND PENDENTE LITE AND FUTURE INTEREST UNDER SECTION 34 CPC

MOST RESPECTFULLY SHOWETH:

1. **DESCRIPTION & COMPETENCY OF PLAINTIFF:** That the Plaintiff is a [Company / Partnership Firm / Proprietorship] having its office at [Insert Address from record] and is engaged in the business of [Insert Business Description from record]. The present Suit is being instituted through Mr./Ms. [INSERT NAME OF AUTHORIZED REPRESENTATIVE], who is duly authorized to sign, verify, and institute the present Plaint under Order VI Rule 14 / Order XXIX Rule 1 of the Code of Civil Procedure, 1908.
2. **DESCRIPTION OF DEFENDANT:** That the Defendant, [Insert Name of Drawer Company / Entity], is a [Company incorporated under the Companies Act / Entity] having its registered office at [Insert Address from record], and can be served with the summons for appearance under Order XXXVII Rule 2 of the Code of Civil Procedure, 1908 at the said address.
3. **COMMERCIAL SUPPLY & LIQUIDATED DEBT:** That pursuant to purchase orders placed by the Defendant, the Plaintiff supplied and delivered [Insert Goods / Services from record] to the Defendant against Tax Invoice No. [Insert Invoice No.] dated [Insert Invoice Date] for an agreed and liquidated sum of Rs. [Insert Exact Cheque Amount]/- (Rupees [Insert Amount in Words] Only). The Defendant duly received and accepted the said goods without any contemporaneous protest or demur.
4. **ISSUANCE OF NEGOTIABLE INSTRUMENT:** That in acknowledgement and discharge of the aforesaid liquidated commercial debt, the Defendant issued Cheque No. [Insert Cheque No.] dated [Insert Draw Date] for a sum of Rs. [Insert Exact Cheque Amount]/- (Rupees [Insert Amount in Words] Only) drawn on [Insert Drawee Bank & Branch] in favour of the Plaintiff.
5. **DISHONOUR OF INSTRUMENT:** That when the Plaintiff presented the aforesaid Cheque No. [Insert Cheque No.] for encashment through its banker on [Insert Presentation Date], the same was returned unpaid and dishonoured vide Bank Return Memo dated [Insert Return Memo Date] with the endorsement "[Insert Dishonour Reason, e.g., Funds Insufficient]".
6. **SUBSISTING CIVIL LIABILITY ON DISHONOURED INSTRUMENT:** That notwithstanding the dishonour of the instrument or any technical timeline governing summary criminal prosecution under Section 138 of the Negotiable Instruments Act, 1881, the dishonoured Cheque No. [Insert Cheque No.] constitutes a bill of exchange / negotiable instrument and an unconditional written acknowledgement of debt. The Defendant has failed and neglected to pay the principal sum of Rs. [Insert Exact Cheque Amount]/- despite written demand dated [Insert Notice Date].
7. **STATUTORY ENTITLEMENT TO INTEREST @ 18% PER ANNUM UNDER SECTION 80 NI ACT:** That since no rate of interest is specified in the dishonoured instrument itself, the Plaintiff is statutorily entitled to recover interest on the principal cheque amount of Rs. [Insert Exact Cheque Amount]/- at the mandatory statutory rate of **18% (eighteen percent) per annum** calculated from the date the instrument ought to have been paid up to realization, in terms of **Section 80 of the Negotiable Instruments Act, 1881**, which accrued interest up to the date of filing of the present Suit amounts to Rs. [INSERT QUANTIFIED INTEREST AMOUNT UP TO DATE OF FILING]/-, making an aggregate liquidated claim of Rs. [INSERT TOTAL OF PRINCIPAL PLUS SECTION 80 INTEREST]/-.
8. **MANDATORY STATUTORY AVERMENT UNDER ORDER XXXVII RULE 2(1)(b) OF THE CODE OF CIVIL PROCEDURE, 1908:** That the Plaintiff institutes the present Suit under the summary procedure enshrined in Order XXXVII of the Code of Civil Procedure, 1908, as the suit seeks only to recover a debt or liquidated demand in money payable by the Defendant with interest arising on a written contract/invoice and on a dishonoured Negotiable Instrument (Cheque No. [Insert Cheque No.] dated [Insert Draw Date]). **The Plaintiff specifically avers in compliance with Order XXXVII Rule 2(1)(b) of the Code of Civil Procedure, 1908 that no relief which does not fall within the ambit of Order XXXVII Rule 2 CPC has been claimed in the present Plaint**, and the title of the Suit has been specifically superscribed *"Under Order XXXVII of the Code of Civil Procedure, 1908"*.
9. **CAUSE OF ACTION:** That the cause of action for filing the present Suit first arose on [Insert Invoice Date] when the goods were supplied under Invoice No. [Insert Invoice No.]; it further arose on [Insert Draw Date] when the Defendant issued Cheque No. [Insert Cheque No.] for Rs. [Insert Exact Cheque Amount]/-; it further arose on [Insert Dishonour Date] when the said cheque was dishonoured; it further arose on [Insert Notice Date] when written demand was served upon the Defendant; and the cause of action is continuing from day to day as the liquidated debt remains unpaid.
10. **TERRITORIAL & PECUNIARY JURISDICTION UNDER SECTION 20 CPC:** That the Defendant carries on business and has its registered office at [Insert City/Place], the goods were supplied from [Insert City/Place], and the cheque was payable at [Insert City/Place], within the local territorial limits of this Hon'ble Court. Further, the value of the Suit falls within the pecuniary jurisdiction of this Hon'ble Court under Section 20 of the Code of Civil Procedure, 1908.
11. **LIMITATION:** That the commercial supply and issuance of Cheque No. [Insert Cheque No.] dated [Insert Draw Date] took place within three years prior to the institution of the present Suit; hence, the present Suit is instituted well within the statutory limitation period of 3 (three) years prescribed under Articles 19, 35, and 40 of the Schedule to the Limitation Act, 1963.
12. **VALUATION & COURT FEE:** That the value of the Suit for the purposes of court fee and jurisdiction is fixed at Rs. [INSERT TOTAL SUIT VALUATION]/, on which the requisite *ad-valorem* Court Fee of Rs. [INSERT COURT FEE AMOUNT]/- has been affixed hereto.

PRAYER:
It is, therefore, most respectfully prayed that this Hon'ble Court may graciously be pleased to:
(a) Pass a Summary Money Decree under Order XXXVII of the Code of Civil Procedure, 1908 in favour of the Plaintiff and against the Defendant for the principal sum of **Rs. [Insert Exact Cheque Amount]/- (Rupees [Insert Amount in Words] Only)** together with accrued statutory interest of Rs. [INSERT QUANTIFIED INTEREST]/- @ 18% per annum under Section 80 of the Negotiable Instruments Act, 1881 up to the date of filing of the Suit;
(b) Award *pendente lite* and future interest @ 18% per annum on the decreetal amount from the date of institution of the Suit till actual and final realization under Section 80 of the NI Act read with Section 34 of the Code of Civil Procedure, 1908;
(c) Award the entire costs of the Suit including Court Fees and Pleader's Fee in favour of the Plaintiff and against the Defendant under Section 35 of the Code of Civil Procedure, 1908; and
(d) Pass such other or further order(s) as this Hon'ble Court may deem fit and proper in the interest of justice.

Place: [INSERT PLACE]
Date: [INSERT DATE]

PLAINTIFF
THROUGH
[NAME OF ADVOCATE]
Advocate — Counsel for the Plaintiff
Enrollment No.: [INSERT ENROLLMENT NO.]

VERIFICATION (UNDER ORDER VI RULE 15 OF THE CODE OF CIVIL PROCEDURE, 1908):
Verified at [INSERT PLACE] on this [INSERT DAY] day of [INSERT MONTH], 2026 that the contents of Paragraphs 1 to 5 and 9 of the above Plaint are true and correct to my personal knowledge derived from the official records of the Plaintiff maintained in the ordinary course of business, and the contents of Paragraphs 6 to 8 and 10 to 12 are believed to be true on legal advice received, and the last paragraph is the humble Prayer before this Hon'ble Court.

PLAINTIFF

---
IN THE COURT OF THE LEARNED DISTRICT JUDGE / SENIOR CIVIL JUDGE, AT [INSERT PLACE]
SUMMARY CIVIL SUIT NO. ________ OF 2026

IN THE MATTER OF:
[Plaintiff Name]
... PLAINTIFF
VERSUS
[Defendant Name]
... DEFENDANT

AFFIDAVIT IN SUPPORT OF PLAINT UNDER ORDER VI RULE 15(4) OF THE CODE OF CIVIL PROCEDURE, 1908

I, [INSERT NAME OF DEPONENT], S/o [INSERT FATHER'S NAME], aged about [INSERT AGE] years, Authorized Representative / Proprietor of the Plaintiff, having office at [Insert Address], do hereby solemnly affirm and declare on oath as under:

1. **COMPETENCY OF DEPONENT:** That I am the Authorized Representative / Proprietor of the Plaintiff in the above-captioned Summary Suit under Order XXXVII CPC and am well conversant with the facts and records of the case, and am competent to swear the present Affidavit.
2. **ADOPTION OF PLAINT AVERMENTS:** That the accompanying Plaint under Order XXXVII of the Code of Civil Procedure, 1908 has been drafted by my Counsel under my instructions, and the contents of Paragraphs 1 to 12 and the Verification clause thereof are true and correct to my knowledge based on official records and legal advice believed to be true.

DEPONENT

VERIFICATION:
Verified at [INSERT PLACE] on this [INSERT DAY] day of [INSERT MONTH], 2026 that the contents of Paragraphs 1 and 2 of my above Affidavit are true and correct to my knowledge and belief, and nothing material has been concealed therefrom.

DEPONENT
""",

    "Court List of Dates & Events (LoD)": """
DRAFTING BLUEPRINT — SYNOPSIS & CHRONOLOGICAL LIST OF DATES AND EVENTS (LoD):
STRICT RULES FOR THIS TEMPLATE:
- Output ONLY the formal Court Cause Title, Synopsis paragraph, and 4-Column Chronological Markdown Table below.
- Never use `<br>` tags inside table cells. Use `[INSERT DATE]` for any missing date.
- Keep `... COMPLAINANT / PETITIONER / PLAINTIFF` and `... ACCUSED / RESPONDENT / DEFENDANT` on their own separate line below the party names.

IN THE COURT OF [INSERT COURT NAME] AT [INSERT PLACE]
CASE / PETITION NO. ________ OF 2026

IN THE MATTER OF:
[Full Name of Complainant / Petitioner / Plaintiff]
... COMPLAINANT / PETITIONER / PLAINTIFF

VERSUS

[Full Name of Accused / Respondent / Defendant]
... ACCUSED / RESPONDENT / DEFENDANT

SYNOPSIS OF CASE & DECISIVE STATUTORY ISSUES:
Write a formal, authoritative 1-paragraph courtroom Synopsis setting out the nature of the proceeding, the cheque details (Cheque No., Draw Date, Amount, Presentation Date, Return Memo Date, and Notice Date), and each decisive statutory bar or cause of action with exact Supreme Court citations (*Shri Ishar Alloy Steels Ltd.*, *Suman Sethi*, *Yogendra Pratap Singh*, and *SMS Pharmaceuticals*).

CHRONOLOGICAL LIST OF DATES AND EVENTS:
| S.No. | Date | Chronological Event & Statutory Significance | Page / Para Ref. |
| :--- | :--- | :--- | :--- |
(Populate every chronological milestone in its own row: 1. Invoice / Transaction Date; 2. Cheque Draw Date; 3. Expiry of 3-Calendar-Month Statutory Validity u/s 138 Proviso (a); 4. Actual Cheque Presentation Date & Late Day-Count; 5. Bank Return Memo Date; 6. Defective Legal Demand Notice Date, Omnibus Sum Demanded u/s 138(b), Truncated Cure Period u/s 138(c), and Non-Executive Director Admission u/s 141; 7. Present Proceeding / Relief Sought).

Place: [INSERT PLACE]
Date: [INSERT DATE]

FILED BY:
[NAME OF ADVOCATE]
Advocate — Counsel for the Party
Enrollment No.: [INSERT ENROLLMENT NO.]
""",

    "Vakalatnama (Court Authorization Form)": """
DRAFTING BLUEPRINT — COURT-READY VAKALATNAMA:
STRICT RULES FOR THIS TEMPLATE:
- Output ONLY the formal Court Vakalatnama below.
- Populate the Court Name, Party Names, and exact Party Roles (e.g., COMPLAINANT and ACCUSED for Sec 138 NI Act; PETITIONER and RESPONDENT for Sec 528 BNSS; PLAINTIFF and DEFENDANT for Civil Suits) from the record.
- Put `IN THE MATTER OF:`, each Party Name, and each `... ROLE` on their own separate lines.

IN THE COURT OF [INSERT COURT NAME] AT [INSERT PLACE]
CASE / COMPLAINT / PETITION NO. ________ OF 2026

IN THE MATTER OF:

[Insert Full Name of Complainant / Petitioner / Plaintiff from Record]
... [Select Exact Role: COMPLAINANT / PETITIONER / PLAINTIFF]

VERSUS

[Insert Full Name of Accused / Respondent / Defendant from Record]
... [Select Exact Role: ACCUSED / RESPONDENT / DEFENDANT]

VAKALATNAMA

KNOW ALL TO WHOM THESE PRESENTS SHALL COME that I/We, the undersigned **[Insert Full Name of Client Entity/Individual from Record, and `[INSERT COMPLETE ADDRESS]` if address is not on record]**, being the **[Complainant / Petitioner / Plaintiff / Accused / Respondent / Defendant]** in the above-captioned matter, do hereby appoint, retain, and engage:

[NAME OF ADVOCATE]
Advocate | Enrollment No.: [INSERT ENROLLMENT NO.]
Chamber / Office: [INSERT CHAMBER / OFFICE ADDRESS]
Email: [INSERT EMAIL] | Mobile: [INSERT MOBILE NO.]

(hereinafter called the "Advocate(s)") to be my/our true and lawful Advocate(s) to act, appear, and plead for me/us in the above-captioned matter on the following terms:

1. **AUTHORITY TO APPEAR & PLEAD:** To appear, act, and plead for me/us before the aforesaid Hon'ble Court or any other Court or Tribunal to which the said matter may be transferred, committed, or appealed, and to file complaints, petitions, plaints, written statements, replies, affidavits, applications, and documents.
2. **AUTHORITY TO EXAMINE & CONDUCT TRIAL:** To summon and examine witnesses, cross-examine opposing witnesses, file applications under the Negotiable Instruments Act, 1881, Bharatiya Nagarik Suraksha Sanhita, 2023, Bharatiya Sakshya Adhiniyam, 2023, or Code of Civil Procedure, 1908, and obtain certified copies of judicial records.
3. **AUTHORITY TO COMPROMISE, COMPOUND & RECEIVE MONIES:** To compound the offence under Section 147 of the Negotiable Instruments Act, 1881, refer the dispute to mediation/Lok Adalat, withdraw or settle the matter under my/our instructions, and receive or deposit any cheques, demand drafts, interim compensation under Section 143A NI Act, or decreetal/settlement amounts on my/our behalf.
4. **AUTHORITY TO APPOINT ASSOCIATE COUNSEL:** To appoint and instruct any other Advocate or junior counsel to appear and act on my/our behalf whenever necessary.
5. **RATIFICATION & UNDERTAKING:** I/We hereby agree to ratify and confirm all lawful acts done by my/our said Advocate(s) in pursuance of this engagement as if done by me/us personally, and undertake to appear before the Hon'ble Court on every date of hearing as directed.

IN WITNESS WHEREOF, I/We have signed and executed this Vakalatnama at [INSERT PLACE] on this [INSERT DAY] day of [INSERT MONTH], 2026.

IDENTIFIED & ACCEPTED BY:

[NAME OF ADVOCATE]
Advocate | Enrollment No.: [INSERT ENROLLMENT NO.]
(Signature of Advocate)

CLIENT(S) / EXECUTANT(S) SIGNATURE BLOCK:
| S.No. | Name & Designation of Executant / Client | Role in Case | Signature & Stamp |
| :--- | :--- | :--- | :--- |
| 1. | [Insert Name of Client No. 1] | [Insert Role] | [SIGN HERE] |
| 2. | [Insert Name of Client No. 2 / Authorized Signatory] | [Insert Role] | [SIGN HERE] |
"""
}

# 3. MASTER AUDIT SYSTEM ROLE (FOR CHAT & PDF DOCKET AUDITS — MODES 1, 2 & 3)
SYSTEM_ROLE = """
You are an expert Indian Litigation & Chambers Audit Engine (Agent VIDHI).
Your job is to audit case facts/documents, identify every legal flaw, tell the lawyer the EXACT next procedural step for BOTH sides (Defense and Complainant) based on the current stage of the matter, and direct them to generate the required documents via **Section II: Agent LEKHAK (Drafting Engine)** and **Section III: Agent DOOT (Clerk & Dispatch)** in the sidebar.

CORE LEGAL & MATH RULES (PERFORM AUTOMATICALLY):
1. Calendar Math [Sec 9 General Clauses Act]:
   - Cheque Validity [Sec 138 Proviso (a)]: 3 calendar months from Draw Date to presentation at drawee bank (e.g., 20 June expires 20 Sept; presenting on 25 Sept is 5 days late = STALE/EXPIRED).
   - Notice Window [Sec 138 Proviso (b)]: 30 days from the date the Complainant RECEIVES the bank Return Memo. Always EXCLUDE the day of receipt (Econ Antri Ltd. v. Rom Industries).
   - Cure & Filing Window [Sec 138 Proviso (c) & Sec 142(1)(b)]: Notice must grant a full 15-day cure period from delivery. Cause of action accrues on Day 16 (Yogendra Pratap Singh v. Savitri Pandey). Complaint must be filed within 1 calendar month thereafter.
2. Core Statutory & Precedent Checks:
   - Time-Barred Debt: Debt >3 years old without fresh written acknowledgment u/s 18 Limitation Act or Sec 25(3) Contract Act is unenforceable.
   - Part-Payments & Omnibus Demand: Unendorsed part-payment before presentation violates Sec 56 NI Act (Dashrathbhai Trikambhai Patel). Demanding an indivisible omnibus amount (adding unquantified damages/penalties to the cheque sum without bifurcation) invalidates the notice (Suman Sethi v. Ajay K. Churiwal; Rahul Builders).
   - Vicarious Liability & Non-Signatories: Only the signatory/drawer of an account maintained by them is liable u/s 138 (Aparna A. Shah). Company directors require specific Sec 141 averments of day-to-day conduct of business; non-executive directors without active role cannot be prosecuted (SMS Pharmaceuticals Ltd. v. Neeta Bhalla).
   - Territorial Jurisdiction [Sec 142(2) NI Act]: Lies strictly at the payee's collecting bank branch (for account presentation) or drawee bank (Bridgestone India)—never where the lawyer's chamber dispatched the notice.
   - Old-to-New Code Crosswalk: Cite both where helpful (Sec 482 CrPC / Sec 528 BNSS for Quashing; Sec 200 CrPC / Sec 223 BNSS for Cognizance; Sec 65B IEA / Sec 63 BSA for Electronic Evidence; Sec 420 IPC / Sec 318(4) BNS for Cheating).

STRICT ACCURACY & FORMATTING RULES:
- ZERO HALLUCINATION: Never invent facts or manufacture defects from normal boilerplate (e.g., a lawyer's chamber letterhead address in a Demand Notice is NOT a territorial jurisdiction defect).
- NEVER ECHO PROMPT INSTRUCTIONS: Never print internal instructions or template directions in your response. Output only the final legal analysis.
- HIGH RECALL & UTILITY: Never hide or suppress a genuine factual, procedural, or statutory flaw. Every point must be accurate, grounded in the text, and useful.
- NO HTML IN TABLES: NEVER use `<br>` or any HTML tags inside Markdown tables. Keep table cells on a single line using dashes (`—`) or semicolons (`;`).
- DUAL-SIDE STAGE-AWARE NEXT STEPS (CRITICAL): Always state the next step AND the exact template to select in **Agent LEKHAK (Drafting Engine)** for BOTH **Defense** and **Complainant** from these 7 options:
  1. `"Statutory Demand Notice (Sec 138 NI Act)"`
  2. `"Reply to Legal Demand Notice (Defense)"`
  3. `"Complaint u/s 138 NI Act r/w Sec 223 BNSS"`
  4. `"Sec 528 BNSS (482 CrPC) Quashing Petition"`
  5. `"Civil Recovery Notice / Order XXXVII Summary Suit Draft"`
  6. `"Court List of Dates & Events (LoD)"`
  7. `"Vakalatnama (Court Authorization Form)"`

===================================================================
MODE 1: WHEN NO PDF IS UPLOADED
- If the user enters CASE FACTS WITH DATES:
  **CASE STAGE & VERDICT:** [Current Stage | MAINTAINABLE / TIME-BARRED / PREMATURE / DEFECTIVE — 1-sentence bottom line]
  ### 1. Timeline & Limitation Check
  | Stage & Provision | Dates & AI Day-Count | Statutory Limit | Status |
  | :--- | :--- | :--- | :--- |
  ### 2. Legal Audit & Findings
  * **[Title of Finding / Defect]:** Exact statutory section, Supreme Court precedent, and legal impact.
  ### 3. Immediate Next Course of Action & Document Generation
  * **If Acting for Defense (Noticee / Accused):** Exact next procedural step and defense strategy.
  * **If Acting for Complainant (Payee / Claimant):** Exact next procedural step, curability, or civil recovery route.
  * **Generate in Nyaya-Agent Now (Agent LEKHAK & Agent DOOT):**
    * **For Defense:** Select **`"[Exact Defense Template Name]"`** (and **`"[2nd Defense Template if applicable]"`**)
    * **For Complainant:** Select **`"[Exact Complainant Template Name]"`** + **`"Vakalatnama (Court Authorization Form)"`**

- If the user asks a GENERAL / CONCEPTUAL LEGAL QUESTION (no case dates):
  Answer directly and clearly in under 180 words using clean headings and bullet points with exact statutory sections and Supreme Court precedents. Do NOT show a timeline table if no dates are involved.

===================================================================
MODE 2: WHEN PDF DOCKET(S) ARE UPLOADED (CASE AUDIT & ACTION PLAN)
**DOCUMENT STAGE & VERDICT:** [Document Type & Procedural Stage | FATALLY DEFECTIVE / MAINTAINABLE — 1-line outcome]

### 1. Statutory Timeline & Quantum Snapshot
| Stage / Check | Document Facts & AI Date Math (`[PAGE X]`, Para) | Statutory Requirement | Status |
| :--- | :--- | :--- | :--- |

### 2. Identified Legal & Procedural Defects
* **[Clear Title of Defect] (`[PAGE X]`, Para Y):**
  * **The Flaw:** Exact dates, amounts, or admissions in the text.
  * **The Law:** Exact Section and Supreme Court precedent violated.
  * **Legal Impact:** How this affects the validity of the notice, complaint, or party array.

### 3. Next Course of Action & Document Generation
* **If Acting for Defense (Recipient / Noticee / Accused):** State the immediate next procedural step (e.g., serve a formal Reply to Notice locking in all statutory objections on record and warning against malicious prosecution u/s 223(1) BNSS, or move the High Court u/s 528 BNSS for quashing if a complaint/summoning order is already passed).
* **If Acting for Complainant (Sender / Payee / Claimant):** State whether each defect can be cured (e.g., re-present cheque if still within 3 months, issue a corrected severed notice if still within 30 days of Return Memo, or abandon Sec 138 criminal prosecution if the cheque is stale and institute a Summary Suit u/o XXXVII CPC with 18% interest u/s 80 NI Act).
* **Generate in Nyaya-Agent Now (Sidebar — Agent LEKHAK & Agent DOOT):**
  * **If Acting for Defense:** Select **`"Reply to Legal Demand Notice (Defense)"`** (at Pre-Cognizance Notice stage) OR **`"Sec 528 BNSS (482 CrPC) Quashing Petition"`** + **`"Court List of Dates & Events (LoD)"`** + **`"Vakalatnama (Court Authorization Form)"`** (if Summons/Complaint is issued).
  * **If Acting for Complainant:** Select **`"Civil Recovery Notice / Order XXXVII Summary Suit Draft"`** + **`"Vakalatnama (Court Authorization Form)"`** (where Sec 138 is time-barred/stale) OR **`"Statutory Demand Notice (Sec 138 NI Act)"`** / **`"Complaint u/s 138 NI Act r/w Sec 223 BNSS"`** (where timelines are valid).

*(Note: If the uploaded PDF is a Court Judgment/Order, summarize: **1. Bench & Holding**, **2. Key Facts**, **3. Core Ratio & Paragraphs (`[PAGE X]`)**, and **4. How to Deploy This Precedent**).*

===================================================================
MODE 3: FOLLOW-UP QUESTIONS IN CHAT
- Answer directly and concisely (~120 words).
- Always do the calendar math or check `[PAGE X]` facts first before stating the final verdict.
- Only include a table if comparing multiple dates or provisions (never use `<br>` inside table cells).
"""

# 4. EDITORIAL COURTROOM UI (Crisp White Canvas, Pure Black Times New Roman, Burnished Gold Headings & Protected Icons)
st.markdown("""
    <style>
    /* Global Canvas & Editorial Typography */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* CRITICAL FIX: Protect Streamlit Material Icons (arrows, upload, sidebar toggle) */
    [data-testid="stIconMaterial"],
    span[data-testid="stIconMaterial"],
    .material-symbols-rounded,
    [translate="no"] {
        font-family: 'Material Symbols Rounded' !important;
        font-weight: normal !important;
        font-style: normal !important;
    }

    /* Force Light Mode on Top Bar & Bottom Chat Bar */
    header[data-testid="stHeader"],
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }
    [data-testid="stChatInput"] textarea {
        background-color: #FAF9F5 !important;
        color: #111111 !important;
        border: 1px solid #C8BFA8 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
    }

    /* Ensure all standard paragraphs, lists, and chat output render in crisp black Times New Roman */
    .stMarkdown p, .stMarkdown li, [data-testid="stChatMessageContent"] p, [data-testid="stChatMessageContent"] li {
        color: #111111 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        font-size: 1.07rem;
        line-height: 1.65;
    }

    /* Burnished Courtroom Gold Headings */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #8B6914 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em;
        border-bottom: 1px solid #E6DEC8;
        padding-bottom: 5px;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    /* Clean Archival Parchment Sidebar */
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div {
        background-color: #FAF9F5 !important;
        border-right: 1px solid #E5E0D5;
    }
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown h4 {
        color: #8B6914 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        font-size: 1.02rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 1px solid #E5E0D5;
        padding-bottom: 4px;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    [data-testid="stSidebar"] label p,
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #111111 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
    }

    /* Force Crisp White on All Dropdowns, Inputs, Forms & File Uploaders */
    [data-testid="stForm"],
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"],
    input, textarea,
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] button {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border-color: #C8BFA8 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
    }
    ul[data-baseweb="menu"],
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
    }

    /* Subtle Sovereign Indian Tricolour Accent & Editorial Masthead */
    .sovereign-masthead {
        background-color: #FFFFFF;
        border: 1px solid #E5E0D5;
        border-left: 4px solid #8B6914;
        border-radius: 2px;
        margin-bottom: 22px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        overflow: hidden;
    }
    .tricolour-rule {
        height: 3px;
        width: 100%;
        background: linear-gradient(
            90deg,
            #C86428 0%, #C86428 33.33%,
            #FFFFFF 33.33%, #FFFFFF 66.66%,
            #1B6B2F 66.66%, #1B6B2F 100%
        );
        border-bottom: 1px solid #EBE6DC;
    }
    .masthead-body {
        padding: 14px 20px 12px 20px;
    }
    .masthead-kicker {
        color: #8B6914;
        font-family: 'Times New Roman', Times, Georgia, serif;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .masthead-title {
        color: #111111;
        font-family: 'Times New Roman', Times, Georgia, serif;
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0 0 4px 0;
        letter-spacing: -0.01em;
    }
    .masthead-sub {
        color: #333333;
        font-family: 'Times New Roman', Times, Georgia, serif;
        font-size: 0.96rem;
        margin: 0;
    }

    /* Courtroom Pleading Cards for Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E0D5;
        border-left: 3px solid #8B6914;
        border-radius: 3px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }

    /* High-Contrast Judicial Tables */
    .stMarkdown table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0 18px 0;
        background-color: #FFFFFF;
    }
    .stMarkdown th {
        background-color: #F8F5EC;
        color: #8B6914 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        font-weight: 700;
        text-align: left;
        padding: 9px 12px;
        border: 1px solid #D5CBB8;
    }
    .stMarkdown td {
        padding: 8px 12px;
        border: 1px solid #E5E0D5;
        color: #111111 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
    }

    /* Active Docket Badge */
    .docket-badge {
        background-color: #FFFFFF;
        border: 1px solid #DCD5C6;
        border-left: 3px solid #8B6914;
        padding: 8px 11px;
        border-radius: 2px;
        font-size: 0.88rem;
        color: #111111;
        margin: 6px 0 10px 0;
        font-family: 'Times New Roman', Times, Georgia, serif;
    }

    /* Crisp White & Burnished Gold Buttons */
    .stButton > button,
    .stButton > button[kind="primary"],
    .stButton > button[kind="secondary"],
    [data-testid="stFormSubmitButton"] > button,
    .stDownloadButton > button,
    [data-testid="stLinkButton"] > a {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1.5px solid #8B6914 !important;
        border-radius: 2px !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em;
        box-shadow: none !important;
    }
    .stButton > button p,
    [data-testid="stFormSubmitButton"] > button p,
    .stDownloadButton > button p,
    [data-testid="stLinkButton"] > a p {
        color: #111111 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        font-weight: 700 !important;
    }
    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stLinkButton"] > a:hover {
        background-color: #8B6914 !important;
        color: #FFFFFF !important;
        border-color: #8B6914 !important;
    }
    .stButton > button:hover p,
    [data-testid="stFormSubmitButton"] > button:hover p,
    .stDownloadButton > button:hover p,
    [data-testid="stLinkButton"] > a:hover p {
        color: #FFFFFF !important;
    }
    [data-testid="stExpander"],
    [data-testid="stExpander"] summary {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #E5E0D5 !important;
        border-radius: 2px !important;
        margin-bottom: 8px;
    }
    [data-testid="stExpander"] summary p {
        color: #111111 !important;
        font-family: 'Times New Roman', Times, Georgia, serif !important;
        font-weight: 600 !important;
    }
    </style>
    
    <div class="sovereign-masthead">
        <div class="tricolour-rule"></div>
        <div class="masthead-body">
            <div class="masthead-kicker">Sovereign Indian Litigation Chambers Infrastructure</div>
            <div class="masthead-title">NYAYA-AGENT</div>
            <p class="masthead-sub"><b>NETRA</b> (Docket &amp; Vision Ingestion) &nbsp;&bull;&nbsp; <b>VIDHI</b> (Limitation &amp; Precedent Audit) &nbsp;&bull;&nbsp; <b>LEKHAK</b> (Senior Pleading Engine) &nbsp;&bull;&nbsp; <b>DOOT</b> (Chambers Clerk)</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. SESSION STATE INITIALIZATION
if "messages" not in st.session_state:
    st.session_state.messages = []
if "docket_text" not in st.session_state:
    st.session_state.docket_text = ""
if "docket_vision_files" not in st.session_state:
    st.session_state.docket_vision_files = []
if "docket_signature" not in st.session_state:
    st.session_state.docket_signature = ""
if "docket_summary" not in st.session_state:
    st.session_state.docket_summary = ""
if "total_pages" not in st.session_state:
    st.session_state.total_pages = 0
if "generated_draft" not in st.session_state:
    st.session_state.generated_draft = ""
if "generated_draft_title" not in st.session_state:
    st.session_state.generated_draft_title = ""
if "pending_request" not in st.session_state:
    st.session_state.pending_request = None
if "doot_whatsapp_msg" not in st.session_state:
    st.session_state.doot_whatsapp_msg = ""
if "doot_calendar_ics" not in st.session_state:
    st.session_state.doot_calendar_ics = ""

# 6. DETERMINISTIC COURTROOM WORD (.DOC) & CALENDAR (.ICS) RENDERING ENGINES
def create_ics_alert(event_title, deadline_date, description):
    dt_start = deadline_date.strftime("%Y%m%d")
    dt_end = (deadline_date + timedelta(days=1)).strftime("%Y%m%d")
    now_stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    clean_desc = re.sub(r'[\r\n]+', ' ', description)[:400]
    ics_content = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//Nyaya-Agent//Agent DOOT Chambers Clerk//EN\r\n"
        "CALSCALE:GREGORIAN\r\n"
        "METHOD:PUBLISH\r\n"
        "BEGIN:VEVENT\r\n"
        f"UID:nyaya-doot-{now_stamp}@chambers.os\r\n"
        f"DTSTAMP:{now_stamp}\r\n"
        f"DTSTART;VALUE=DATE:{dt_start}\r\n"
        f"DTEND;VALUE=DATE:{dt_end}\r\n"
        f"SUMMARY:⚖️ [NYAYA-AGENT DEADLINE] {event_title}\r\n"
        f"DESCRIPTION:{clean_desc}\r\n"
        "BEGIN:VALARM\r\n"
        "TRIGGER:-PT24H\r\n"
        "ACTION:DISPLAY\r\n"
        "DESCRIPTION:Statutory Legal Deadline Reminder (Agent DOOT)\r\n"
        "END:VALARM\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    return ics_content.encode("utf-8")

def format_inline_md(text):
    text = text.replace("`", "")
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^\*\n]+)\*(?!\*)', r'<i>\1</i>', text)
    text = re.sub(r'(\[[^\]]+\])', r'<b>\1</b>', text)
    while "<b><b>" in text or "</b></b>" in text:
        text = text.replace("<b><b>", "<b>").replace("</b></b>", "</b>")
    return text

def wrap_bold(inner_html):
    out = f"<b>{inner_html}</b>"
    while "<b><b>" in out or "</b></b>" in out:
        out = out.replace("<b><b>", "<b>").replace("</b></b>", "</b>")
    return out

def auto_bold_lead_in(line_html):
    m = re.match(
        r'^((?:\d+(?:\.\d+)?\.|[A-Z]\.|GROUND\s+[A-Z]|QUESTION\s+[A-Z])\s*[^:<]{2,95}:)(.*)$',
        line_html,
        flags=re.IGNORECASE
    )
    if m and not m.group(1).strip().startswith("<b>"):
        return f"{wrap_bold(m.group(1))}{m.group(2)}"
    return line_html

def create_word_doc(markdown_text, doc_title="Legal_Document"):
    cleaned = re.sub(r'<br\s*/?>', ' — ', markdown_text, flags=re.IGNORECASE)
    # Guardrail 1: Fix non-existent "High Court of (Judicature at) New Delhi" -> "High Court of Delhi at New Delhi"
    cleaned = re.sub(
        r'HIGH COURT OF (?:JUDICATURE AT )?NEW DELHI(?: AT NEW DELHI)?',
        'HIGH COURT OF DELHI AT NEW DELHI',
        cleaned,
        flags=re.IGNORECASE
    )
    # Guardrail 2: Fix any duplicate "AT [PLACE] AT [PLACE]" across Lower Courts, High Courts & Supreme Court headings
    cleaned = re.sub(
        r'(IN THE [A-Z\s\(\)]*COURT[^\n]*?)\bAT ([A-Z\s]{3,25}) AT \2\b',
        r'\1AT \2',
        cleaned
    )
    # Guardrail 3: Ensure "IN THE MATTER OF:" and "... ROLE" always break onto separate lines for Vakalatnama & Cause Titles
    cleaned = re.sub(r'(IN THE MATTER OF:)\s+', r'\1\n', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(
        r'([^\n])\s+(\.\.\.\s*(?:COMPLAINANT|ACCUSED|PETITIONER|RESPONDENT|PLAINTIFF|DEFENDANT|\[SELECT))',
        r'\1\n\2',
        cleaned,
        flags=re.IGNORECASE
    )
    cleaned = re.sub(r'^```[a-zA-Z]*\n', '', cleaned.strip())
    cleaned = re.sub(r'\n```$', '', cleaned.strip())
    
    lines = cleaned.split("\n")
    html_blocks = []
    in_table = False
    table_rows = []
    seen_letterhead_name = False

    def flush_table(rows):
        if not rows:
            return ""
        t_html = ["<table>"]
        for r_idx, r in enumerate(rows):
            cells = [format_inline_md(c.strip()) for c in r.strip("|").split("|")]
            tag = "th" if r_idx == 0 else "td"
            row_cells = "".join([f"<{tag}>{c}</{tag}>" for c in cells])
            t_html.append(f"<tr>{row_cells}</tr>")
        t_html.append("</table>")
        return "\n".join(t_html)

    for raw_line in lines:
        line = raw_line.strip()
        
        if line.startswith("|") and line.endswith("|"):
            if re.match(r'^\|[\s\-\:\|]+\|$', line):
                continue
            in_table = True
            table_rows.append(line)
            continue
        elif in_table:
            html_blocks.append(flush_table(table_rows))
            table_rows = []
            in_table = False

        if not line:
            continue

        if re.match(r'^(\-{3,}|\*{3,}|_{3,})$', line):
            if len(html_blocks) < 14:
                html_blocks.append("<hr>")
            else:
                html_blocks.append("<br clear=all style='mso-special-character:line-break;page-break-before:always'>")
            continue

        line = re.sub(r'^#{1,4}\s*', '', line)
        plain_upper = re.sub(r'\*+', '', line).strip().upper()

        # 1. Centered Court Headings, Pleading Titles & Short Top Dispatch Headers
        if (
            plain_upper in ["WITHOUT PREJUDICE", "WITHOUT PREJUDICE:", "LEGAL NOTICE", "INDEX", "SYNOPSIS", "SUPPORTING AFFIDAVIT", "VAKALATNAMA"]
            or any(plain_upper.startswith(p) for p in [
                "IN THE COURT OF", "IN THE HIGH COURT OF", "IN THE SUPREME COURT OF",
                "COMPLAINT CASE NO", "CRIMINAL MISC", "CRL.M.C.", "SUMMARY CIVIL SUIT",
                "CIVIL SUIT", "CASE / PETITION NO", "CASE / COMPLAINT / PETITION NO",
                "EXTRAORDINARY CRIMINAL JURISDICTION",
                "(SUIT UNDER ORDER", "COMPLAINT UNDER SECTION", "PETITION UNDER SECTION",
                "SUIT FOR RECOVERY", "SUIT UNDER ORDER",
                "PRE-SUMMONING EVIDENCE", "AFFIDAVIT IN SUPPORT",
                "LIST OF DOCUMENTS", "LIST OF WITNESSES", "CHRONOLOGICAL LIST OF DATES"
            ])
            or (
                len(plain_upper) < 85 and any(plain_upper.startswith(p) for p in [
                    "VERSUS", "V/S", "VS.", "BY REGISTERED POST"
                ])
            )
        ):
            html_blocks.append(f"<p class='court-center'>{wrap_bold(format_inline_md(line))}</p>")

        # 2. Letterhead Name vs. Bottom Signature Block for [NAME OF ADVOCATE]
        elif plain_upper.startswith("[NAME OF ADVOCATE]"):
            if not seen_letterhead_name and len(html_blocks) < 8:
                seen_letterhead_name = True
                html_blocks.append(f"<p class='letterhead-title'>{wrap_bold(format_inline_md(line))}</p>")
            else:
                html_blocks.append(f"<p class='sig-block'>{wrap_bold(format_inline_md(line))}</p>")

        # 3. Automatic Solid Divider Under Letterhead Email/Mobile Line
        elif plain_upper.startswith("EMAIL:") and len(html_blocks) < 12:
            html_blocks.append(f"<p class='left-line'>{format_inline_md(line)}</p>")
            html_blocks.append("<hr>")

        # 4. Top Notice Ref. No. & Date Block (Right-Aligned at Top of Notice/Reply)
        elif (plain_upper.startswith("REF. NO") or plain_upper.startswith("DATE:")) and len(html_blocks) < 16:
            html_blocks.append(f"<p class='date-ref-line'>{wrap_bold(format_inline_md(line))}</p>")

        # 5. Addressee "To," Block & "IN THE MATTER OF:"
        elif plain_upper in ["TO,", "TO:"] or plain_upper.startswith("IN THE MATTER OF:"):
            html_blocks.append(f"<p class='spaced-label'>{wrap_bold(format_inline_md(line))}</p>")

        elif plain_upper in ["SIR/MADAM,", "DEAR SIR/MADAM,", "SIR / MADAM,", "MOST RESPECTFULLY SHOWETH:"]:
            html_blocks.append(f"<p class='salutation-line'>{wrap_bold(format_inline_md(line))}</p>")

        # 6. Notice Sign-Off ("Yours faithfully,") vs. Court Deponent/Litigant Signature Block
        elif plain_upper in ["YOURS FAITHFULLY,", "YOURS TRULY,", "FILED BY:", "THROUGH", "THROUGH:", "IDENTIFIED & ACCEPTED BY:"]:
            html_blocks.append(f"<p class='signoff-line'>{wrap_bold(format_inline_md(line))}</p>")

        elif plain_upper in ["COMPLAINANT", "PETITIONER(S)", "PETITIONER", "PLAINTIFF", "DEPONENT"]:
            html_blocks.append(f"<p class='court-sig-right'>{wrap_bold(format_inline_md(line))}</p>")

        # 7. Cause Title Party Role Labels (... COMPLAINANT / ... ACCUSED / ... PETITIONER)
        elif plain_upper.startswith("...") or any(plain_upper.endswith(s) for s in [
            "... COMPLAINANT", "... ACCUSED", "... ACCUSED PERSON(S)",
            "... PETITIONER", "... PETITIONER(S)", "... RESPONDENT", "... RESPONDENT(S)",
            "... PLAINTIFF", "... DEFENDANT", "... COMPLAINANT / PETITIONER / PLAINTIFF",
            "... ACCUSED / RESPONDENT / DEFENDANT"
        ]):
            html_blocks.append(f"<p class='right-label'>{wrap_bold(format_inline_md(line))}</p>")

        # 8. Subject Box (Bold & Indented — No jagged multi-line underline)
        elif plain_upper.startswith("SUBJECT:") or plain_upper.startswith("SUB:"):
            html_blocks.append(f"<p class='subject-box'>{wrap_bold(format_inline_md(line))}</p>")

        # 9. Major Section Headings
        elif any(plain_upper.startswith(p) for p in [
            "PART I", "PART II", "PART III", "SECTION A", "SECTION B",
            "PRELIMINARY STATEMENT", "PRAYER", "VERIFICATION", "SYNOPSIS OF CASE", "CLIENT(S) / EXECUTANT(S)"
        ]):
            html_blocks.append(f"<p class='sec-heading'>{wrap_bold(format_inline_md(line))}</p>")

        # 10. Short Left-Aligned Lines (Addresses, Place/Date at bottom, Counsel titles) -> NEVER JUSTIFY
        elif len(line) < 95 and not re.match(r'^(\d+(?:\.\d+)?\.|\([a-z]\)|-\s|•\s|GROUND\s+[A-Z]|QUESTION\s+[A-Z]|Reply to Para|Without prejudice|KNOW ALL|IN WITNESS)', line, re.IGNORECASE):
            html_blocks.append(f"<p class='left-line'>{format_inline_md(line)}</p>")

        # 11. Full Legal Body Paragraphs & Numbered Clauses -> Justified + Auto-Bold Lead-In
        else:
            line = re.sub(r'^[-•]\s+', '', line)
            formatted_body = auto_bold_lead_in(format_inline_md(line))
            html_blocks.append(f"<p class='body-para'>{formatted_body}</p>")

    if in_table:
        html_blocks.append(flush_table(table_rows))

    html_content = "\n".join(html_blocks)

    word_xml = f"""<html xmlns:o='urn:schemas-microsoft-com:office:office'
          xmlns:w='urn:schemas-microsoft-com:office:word'
          xmlns='http://www.w3.org/TR/REC-html40'>
    <head>
        <meta charset="utf-8">
        <title>{doc_title}</title>
        <style>
            @page {{
                size: 8.5in 11.0in;
                margin: 1.0in 1.0in 1.0in 1.25in;
            }}
            body {{
                font-family: 'Times New Roman', serif;
                font-size: 12pt;
                color: #000000;
            }}
            p.court-center {{
                text-align: center;
                line-height: 1.4;
                margin-top: 4pt;
                margin-bottom: 6pt;
                font-size: 12pt;
                text-decoration: underline;
            }}
            p.letterhead-title {{
                text-align: left;
                line-height: 1.35;
                margin-top: 10pt;
                margin-bottom: 2pt;
                font-size: 13pt;
            }}
            p.date-ref-line {{
                text-align: right;
                line-height: 1.35;
                margin-top: 3pt;
                margin-bottom: 3pt;
                font-size: 12pt;
            }}
            p.spaced-label {{
                text-align: left;
                line-height: 1.35;
                margin-top: 12pt;
                margin-bottom: 3pt;
                font-size: 12pt;
            }}
            p.salutation-line {{
                text-align: left;
                line-height: 1.35;
                margin-top: 12pt;
                margin-bottom: 8pt;
                font-size: 12pt;
            }}
            p.right-label {{
                text-align: right;
                line-height: 1.35;
                margin-top: 2pt;
                margin-bottom: 8pt;
                font-size: 12pt;
            }}
            p.subject-box {{
                text-align: justify;
                line-height: 1.45;
                margin-top: 14pt;
                margin-bottom: 14pt;
                margin-left: 18pt;
                margin-right: 18pt;
                font-size: 12pt;
            }}
            p.sec-heading {{
                text-align: left;
                line-height: 1.45;
                margin-top: 14pt;
                margin-bottom: 8pt;
                font-size: 12pt;
                text-decoration: underline;
            }}
            p.left-line {{
                text-align: left;
                line-height: 1.35;
                margin-top: 2pt;
                margin-bottom: 3pt;
                font-size: 12pt;
            }}
            p.signoff-line {{
                text-align: left;
                line-height: 1.35;
                margin-top: 14pt;
                margin-bottom: 2pt;
                font-size: 12pt;
            }}
            p.sig-block {{
                text-align: left;
                line-height: 1.35;
                margin-top: 34pt;
                margin-bottom: 2pt;
                font-size: 12pt;
            }}
            p.court-sig-right {{
                text-align: right;
                line-height: 1.35;
                margin-top: 32pt;
                margin-bottom: 4pt;
                font-size: 12pt;
            }}
            p.body-para {{
                text-align: justify;
                line-height: 1.5;
                margin-top: 0pt;
                margin-bottom: 10pt;
                font-size: 12pt;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 10pt;
                margin-bottom: 12pt;
            }}
            th {{
                border: 1px solid #000000;
                background-color: #F2F2F2;
                padding: 6pt 8pt;
                text-align: left;
                font-weight: bold;
                font-size: 11pt;
            }}
            td {{
                border: 1px solid #000000;
                padding: 6pt 8pt;
                text-align: left;
                vertical-align: top;
                font-size: 11pt;
            }}
            hr {{
                border: 0;
                border-top: 1.5pt solid #000000;
                margin: 8pt 0 10pt 0;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>"""
    return word_xml.encode("utf-8")

# 7. MULTI-KEY POOL LOADER & ZERO-DOWNTIME MODEL ROUTER
def get_api_key_pool(user_input_key=""):
    if user_input_key.strip():
        return [k.strip() for k in user_input_key.split(",") if k.strip()]
    try:
        secret_val = st.secrets.get("GEMINI_API_KEY", "")
        if isinstance(secret_val, list):
            return [str(k).strip() for k in secret_val if str(k).strip()]
        return [k.strip() for k in str(secret_val).split(",") if k.strip()]
    except Exception:
        return []

def call_model(model_name, api_key_or_pool, payload):
    keys = api_key_or_pool if isinstance(api_key_or_pool, list) else [k.strip() for k in str(api_key_or_pool).split(",") if k.strip()]
    if not keys:
        return {"success": False, "model": model_name, "error": "No API Key configured", "time": 0.0}

    shuffled_keys = keys.copy()
    random.shuffle(shuffled_keys)

    start_time = time.time()
    last_error = ""

    for attempt_key in shuffled_keys:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={attempt_key}"
        for _ in range(2):
            try:
                res = requests.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=45
                )
                elapsed = time.time() - start_time
                if res.status_code == 200:
                    data = res.json()
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    return {"success": True, "model": model_name, "text": text, "time": elapsed}
                elif res.status_code in [429, 503]:
                    last_error = f"{res.status_code} (Quota/Busy)"
                    time.sleep(0.9 + random.uniform(0.1, 0.5))
                    continue
                else:
                    last_error = f"{res.status_code}"
                    break
            except Exception as e:
                last_error = str(e)
                break

    elapsed = time.time() - start_time
    return {"success": False, "model": model_name, "error": last_error, "time": elapsed}

# 8. DECLUTTERED CHAMBERS SIDEBAR (EDITORIAL HARVEY-STYLE WORKSPACE — ALL PARAMETERS INTACT)
with st.sidebar:
    cloud_keys = get_api_key_pool("")

    # SECTION I: PRIMARY DOCKET & AUDIT (AGENT NETRA & VIDHI)
    st.markdown("### I. Case Docket (NETRA & VIDHI)")
    uploaded_pdfs = st.file_uploader(
        "Upload Notice, Complaint, or Case File(s)",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload 1 or more PDFs to audit, or leave empty to enter facts in the main console."
    )
    
    trigger_audit = False
    
    if uploaded_pdfs:
        current_sig = "|".join([f"{f.name}:{f.size}" for f in uploaded_pdfs])
        if current_sig != st.session_state.docket_signature:
            with st.spinner("Agent NETRA: Indexing Case Docket & Exhibits..."):
                st.session_state.docket_signature = current_sig
                st.session_state.generated_draft = ""
                st.session_state.generated_draft_title = ""
                combined_text_blocks = []
                vision_files = []
                total_p = 0
                file_badges = []
                
                for pdf_file in uploaded_pdfs:
                    try:
                        raw_bytes = pdf_file.getvalue()
                        reader = PdfReader(pdf_file)
                        num_p = len(reader.pages)
                        total_p += num_p
                        
                        extracted_pages = []
                        for idx, page in enumerate(reader.pages):
                            page_txt = page.extract_text() or ""
                            if page_txt.strip():
                                tag = f"[PAGE {idx + 1}]" if len(uploaded_pdfs) == 1 else f"[{pdf_file.name} | PAGE {idx + 1}]"
                                extracted_pages.append(f"\n--- {tag} ---\n{page_txt}")
                        
                        doc_text = "\n".join(extracted_pages).strip()
                        if len(doc_text) > 30:
                            combined_text_blocks.append(f"\n=== DOCUMENT: {pdf_file.name} ===\n{doc_text}")
                            file_badges.append(f"• {pdf_file.name} ({num_p}p)")
                        else:
                            vision_files.append({
                                "name": pdf_file.name,
                                "base64": base64.b64encode(raw_bytes).decode("utf-8")
                            })
                            file_badges.append(f"• {pdf_file.name} ({num_p}p Scanned)")
                    except Exception:
                        raw_bytes = pdf_file.getvalue()
                        vision_files.append({
                            "name": pdf_file.name,
                            "base64": base64.b64encode(raw_bytes).decode("utf-8")
                        })
                        total_p += 1
                        file_badges.append(f"• {pdf_file.name} (Scanned)")
                
                st.session_state.docket_text = "\n".join(combined_text_blocks).strip()
                st.session_state.docket_vision_files = vision_files
                st.session_state.total_pages = total_p
                st.session_state.docket_summary = "<br>".join(file_badges)
        
        st.markdown(
            f"<div class='docket-badge'>"
            f"<b>Active Docket ({st.session_state.total_pages} Page(s)):</b><br>"
            f"{st.session_state.docket_summary}"
            f"</div>",
            unsafe_allow_html=True
        )
        trigger_audit = st.button("Audit Docket & Limitation (VIDHI)", use_container_width=True, type="primary")
    else:
        st.session_state.docket_text = ""
        st.session_state.docket_vision_files = []
        st.session_state.docket_signature = ""
        st.session_state.docket_summary = ""
        st.session_state.total_pages = 0

    # SECTION II: SENIOR PLEADING ENGINE (AGENT LEKHAK)
    st.markdown("### II. Pleading Engine (LEKHAK)")
    with st.form("draft_engine_form", border=False):
        draft_type = st.selectbox(
            "Select Legal Instrument",
            list(DRAFT_BLUEPRINTS.keys())
        )
        trigger_draft = st.form_submit_button("Draft Pleading (LEKHAK)", use_container_width=True)

    if st.session_state.generated_draft:
        safe_filename = re.sub(r'[^A-Za-z0-9]+', '_', st.session_state.generated_draft_title).strip('_') + ".doc"
        st.download_button(
            label="Download MS Word Pleading (.doc)",
            data=create_word_doc(st.session_state.generated_draft, st.session_state.generated_draft_title),
            file_name=safe_filename,
            mime="application/msword",
            use_container_width=True
        )
        st.caption("Counsel Review: Verify bracketed placeholders and dates in MS Word prior to filing.")

    # SECTION III: CLERK & CLIENT DISPATCH (COLLAPSIBLE DRAWER — AGENT DOOT)
    with st.expander("III. Clerk & Client Dispatch (DOOT)", expanded=bool(st.session_state.doot_whatsapp_msg)):
        doot_deadline_type = st.selectbox(
            "Statutory Deadline / Alert Type",
            [
                "15-Day Notice Cure Expiry (Sec 138(c) NI Act)",
                "30-Day Notice Dispatch Limit (Sec 138(b) NI Act)",
                "1-Month Complaint Filing Limit (Sec 142(1)(b))",
                "Sec 528 BNSS High Court Filing / Hearing"
            ]
        )
        doot_date = st.date_input("Statutory Deadline / Hearing Date", value=datetime.today() + timedelta(days=15))
        trigger_doot = st.button("Prepare Client Briefing & Alert", use_container_width=True)

        if st.session_state.doot_whatsapp_msg:
            st.text_area("Client Briefing (WhatsApp)", st.session_state.doot_whatsapp_msg, height=135)
            encoded_wa = urllib.parse.quote(st.session_state.doot_whatsapp_msg)
            st.link_button("Dispatch via WhatsApp", f"https://wa.me/?text={encoded_wa}", use_container_width=True)
            st.download_button(
                label="Download Calendar Alert (.ics)",
                data=st.session_state.doot_calendar_ics,
                file_name="Nyaya_Agent_Statutory_Deadline.ics",
                mime="text/calendar",
                use_container_width=True
            )

    # SECTION IV: CHAMBERS & ENGINE SETUP (COLLAPSIBLE DRAWER — AUTO-TUCKED WHEN CLOUD KEY ACTIVE)
    with st.expander("IV. Chambers & Engine Setup", expanded=not bool(cloud_keys)):
        user_api_key = st.text_input(
            "Google API Key",
            type="password",
            placeholder="Cloud Key Pool Active..." if cloud_keys else "Paste AI Studio Key(s)..."
        )
        api_key_pool = get_api_key_pool(user_api_key)
        if cloud_keys and not user_api_key.strip():
            st.caption(f"Chambers Cloud Key Active ({len(cloud_keys)} Key Pool)")

        routing_mode = st.radio(
            "Inference Mode",
            [
                "High Precision (3.8 → 3.6 → 3.1-Pro → 3.5)",
                "Parallel Race (3.6 → 3.5-Flash-Lite)"
            ],
            index=0
        )

    # HANDLE AGENT DOOT EXECUTION
    if trigger_doot:
        if not st.session_state.messages and not st.session_state.docket_text:
            st.warning("Run a Case Audit or enter case facts first so Agent DOOT can prepare the client briefing.")
        elif not api_key_pool:
            st.error("Please configure your Google API Key in Section IV or Streamlit Secrets.")
        else:
            with st.spinner("Agent DOOT: Preparing Client Briefing & Calendar Alert..."):
                case_ctx = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages[-4:]])
                if not case_ctx and st.session_state.docket_text:
                    case_ctx = st.session_state.docket_text[:8000]
                doot_prompt = f"""
                You are Agent DOOT (Autonomous Chambers Law Clerk). Based on the case audit/facts below, write a crisp, professional 5-line WhatsApp update for the Lawyer to send to their Client:
                - Line 1: *⚖️ CASE STATUS UPDATE — CHAMBERS BRIEFING*
                - Line 2: *Matter / Instrument:* (Parties, Cheque No. & Amount)
                - Line 3: *Legal Audit Verdict:* (1-sentence summary of key statutory finding)
                - Line 4: *Immediate Next Action:* (What pleading/step we are taking next)
                - Line 5: *Key Statutory Date:* {doot_deadline_type} on {doot_date.strftime('%d %b %Y')}.
                Keep it under 95 words, plain WhatsApp formatting (*bold*), no markdown tables.

                CASE CONTEXT:
                {case_ctx[:15000]}
                """
                doot_payload = {
                    "contents": [{"role": "user", "parts": [{"text": doot_prompt}]}],
                    "generationConfig": {"temperature": 0.1}
                }
                for m_name in ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-2.5-flash"]:
                    res = call_model(m_name, api_key_pool, doot_payload)
                    if res["success"]:
                        st.session_state.doot_whatsapp_msg = res["text"].strip()
                        st.session_state.doot_calendar_ics = create_ics_alert(
                            doot_deadline_type,
                            doot_date,
                            st.session_state.doot_whatsapp_msg
                        )
                        st.rerun()
                        break

    st.markdown("---")
    if st.button("New Matter / Clear Record", use_container_width=True):
        st.session_state.messages = []
        st.session_state.generated_draft = ""
        st.session_state.generated_draft_title = ""
        st.session_state.pending_request = None
        st.session_state.doot_whatsapp_msg = ""
        st.session_state.doot_calendar_ics = ""
        st.rerun()

# 9. DISPLAY CONVERSATION HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 10. CAPTURE USER ACTION (CHAT, AUDIT, OR DRAFT) & LOCK IN SESSION STATE
chat_prompt = st.chat_input("Enter case facts with dates, statutory queries, or questions regarding the uploaded docket...")

if trigger_audit and st.session_state.docket_signature:
    st.session_state.messages = []
    st.session_state.generated_draft = ""
    st.session_state.generated_draft_title = ""
    audit_prompt = (
        "**Agent Handoff (`NETRA → VIDHI` — Procedural & Limitation Audit):** Execute MODE 2 for the uploaded document(s). "
        "Verify all statutory timelines automatically, list every genuine legal/factual defect clearly with exact page/paragraph citations, "
        "and under Section 3 state the immediate next procedural step and exact **Agent LEKHAK** sidebar document to generate for "
        "BOTH **Defense (Noticee/Accused)** and **Complainant (Payee/Claimant)**."
    )
    st.session_state.messages.append({"role": "user", "content": audit_prompt})
    st.session_state.pending_request = {"is_draft": False, "draft_type": None}
    st.rerun()

elif trigger_draft:
    if not st.session_state.messages and not st.session_state.docket_signature:
        st.warning("Please upload a PDF docket or enter case facts in the console before generating a pleading.")
    else:
        draft_prompt = f"**Agent Handoff (`VIDHI → LEKHAK` — Senior Pleading Drafter):** Generate `{draft_type}`"
        st.session_state.messages.append({"role": "user", "content": draft_prompt})
        st.session_state.pending_request = {"is_draft": True, "draft_type": draft_type}
        st.rerun()

elif chat_prompt:
    st.session_state.messages.append({"role": "user", "content": chat_prompt})
    st.session_state.pending_request = {"is_draft": False, "draft_type": None}
    st.rerun()

# 11. RUN AI ENGINE (SURVIVES ANY WIDGET INTERACTION)
if st.session_state.pending_request:
    is_draft_generation = st.session_state.pending_request["is_draft"]
    active_draft_type = st.session_state.pending_request["draft_type"] or draft_type

    with st.chat_message("assistant"):
        if not api_key_pool:
            st.session_state.messages.pop()
            st.session_state.pending_request = None
            st.error("Please enter your Google API Key in Section IV of the sidebar or configure `GEMINI_API_KEY` in Streamlit Secrets.")
        else:
            spinner_text = (
                f"Agent LEKHAK: Drafting {active_draft_type}..."
                if is_draft_generation
                else "Agent VIDHI: Auditing Case Record & Statutory Timelines..."
            )
            with st.spinner(spinner_text):
                try:
                    gemini_contents = []
                    
                    # BRANCH A: DEDICATED SINGLE-DOCUMENT DRAFTING ENGINE (AGENT LEKHAK)
                    if is_draft_generation:
                        selected_blueprint = DRAFT_BLUEPRINTS[active_draft_type]
                        prior_context = "\n\n".join([
                            f"{m['role'].upper()}:\n{m['content']}"
                            for m in st.session_state.messages[:-1]
                        ])
                        parts_list = []
                        for v_file in st.session_state.docket_vision_files:
                            parts_list.append({
                                "inline_data": {
                                    "mime_type": "application/pdf",
                                    "data": v_file["base64"]
                                }
                            })
                        docket_block = (
                            f"\n\n=== UPLOADED CASE DOCKET ===\n{st.session_state.docket_text[:180000]}\n=== END DOCKET ===\n"
                            if st.session_state.docket_text else ""
                        )
                        draft_instruction = f"""
                        You are Agent LEKHAK, an elite Indian Legal Drafting Engine receiving a structured case handoff from Agent NETRA and Agent VIDHI.
                        Generate ONLY the single requested legal instrument below: "{active_draft_type}".
                        
                        STRICT LEGAL & ETHICAL COMPLIANCE RULES:
                        1. Output ONLY the formal legal document text itself following the exact verbatim paragraphs and structure in the Blueprint below. Do NOT summarize or shorten any paragraph of the Blueprint, and NEVER output any parenthetical drafting instructions.
                        2. Do NOT generate any other document besides "{active_draft_type}".
                        3. NEVER write "Nyaya-AI", "Nyaya-Agent", or "Senior Advocate" anywhere, and never write "Supreme Court of India" in the Advocate letterhead or signature block. Always use clean bracketed placeholders (`[NAME OF ADVOCATE]`, `[INSERT ENROLLMENT NO.]`, `[INSERT CHAMBER / OFFICE ADDRESS]`).
                        4. STRICT ANTI-FABRICATION RULE: Populate every exact date, cheque number, amount, party name, paragraph reference, and legal defect present in the Case Docket and Audit History below. However, NEVER invent or guess any date, bank branch, invoice number, factual defense, or case number that is missing from the record—always retain the bold bracketed placeholder in ALL CAPS (e.g., `[INSERT COLLECTING BANK & BRANCH]`, `[INSERT RETURN MEMO RECEIPT DATE]`) for any missing fact.

                        {selected_blueprint}
                        {docket_block}
                        === PRIOR CASE AUDIT & FACTS (FROM AGENT VIDHI) ===
                        {prior_context}
                        """
                        parts_list.append({"text": draft_instruction})
                        gemini_contents.append({"role": "user", "parts": parts_list})
                        
                    # BRANCH B: STANDARD CHAT OR PDF AUDIT FLOW (AGENT VIDHI)
                    else:
                        for i, msg in enumerate(st.session_state.messages):
                            api_role = "user" if msg["role"] == "user" else "model"
                            text = msg["content"]
                            parts_list = []
                            
                            if i == 0 and api_role == "user":
                                for v_file in st.session_state.docket_vision_files:
                                    parts_list.append({
                                        "inline_data": {
                                            "mime_type": "application/pdf",
                                            "data": v_file["base64"]
                                        }
                                    })
                                
                                if st.session_state.docket_text:
                                    pdf_context = (
                                        f"\n\n=== UPLOADED CASE DOCKET ({st.session_state.total_pages} Pages) ===\n"
                                        f"{st.session_state.docket_text[:180000]}\n"
                                        f"=== END OF DOCKET ===\n"
                                    )
                                    text = f"{SYSTEM_ROLE}{pdf_context}\n\nLawyer's Request:\n{text}"
                                    parts_list.append({"text": text})
                                elif st.session_state.docket_vision_files:
                                    text = f"{SYSTEM_ROLE}\n\nAnalyze the attached scanned PDF docket.\nLawyer's Request:\n{text}"
                                    parts_list.append({"text": text})
                                else:
                                    text = f"{SYSTEM_ROLE}\n\nLawyer's Request:\n{text}"
                                    parts_list.append({"text": text})
                            else:
                                parts_list.append({"text": text})
                                
                            gemini_contents.append({"role": api_role, "parts": parts_list})

                    payload = {
                        "contents": gemini_contents,
                        "generationConfig": {"temperature": 0.0}
                    }
                    
                    winner = None
                    errors = []
                    
                    # OPTION 1: HIGH MODE (TOP PRO & LATEST FULL MODELS + CROSS-GEN SAFETY NET)
                    if "High" in routing_mode:
                        high_models = [
                            "gemini-3.8-pro",
                            "gemini-3.8-flash",
                            "gemini-3.6-pro",
                            "gemini-3.1-pro",
                            "gemini-3.6-flash",
                            "gemini-3.5-flash",
                            "gemini-2.5-pro",
                            "gemini-2.5-flash"
                        ]
                        for model in high_models:
                            result = call_model(model, api_key_pool, payload)
                            if result["success"]:
                                winner = result
                                break
                            else:
                                errors.append(f"{result['model']} ({result['error']})")
                        mode_badge = "High Precision"
                        
                    # OPTION 2: PARALLEL RACE (3.6 DOWN TO 3.5-FLASH-LITE + 2.5 SAFETY NET)
                    else:
                        race_models = [
                            "gemini-3.6-flash",
                            "gemini-3.5-flash",
                            "gemini-3.5-flash-lite",
                            "gemini-2.5-flash",
                            "gemini-2.5-flash-lite"
                        ]
                        executor = ThreadPoolExecutor(max_workers=len(race_models))
                        futures = [executor.submit(call_model, model, api_key_pool, payload) for model in race_models]
                        for future in as_completed(futures):
                            result = future.result()
                            if result["success"]:
                                winner = result
                                break
                            else:
                                errors.append(f"{result['model']} ({result['error']})")
                        executor.shutdown(wait=False, cancel_futures=True)
                        mode_badge = "Parallel Race"
                    
                    if winner:
                        clean_output = re.sub(r'<br\s*/?>', ' — ', winner["text"], flags=re.IGNORECASE)
                        
                        st.markdown(clean_output)
                        docket_tag = f" | {st.session_state.total_pages}p Docket" if st.session_state.total_pages else ""
                        if is_draft_generation:
                            agent_badge = "Pipeline: `NETRA → VIDHI → LEKHAK`" if st.session_state.total_pages else "Pipeline: `VIDHI → LEKHAK`"
                        else:
                            agent_badge = "Pipeline: `NETRA → VIDHI`" if st.session_state.total_pages else "Agent: `VIDHI`"
                            
                        st.caption(f"{agent_badge} | {mode_badge} | `{winner['model']}` ({winner['time']:.2f}s){docket_tag}")
                        st.session_state.messages.append({"role": "assistant", "content": clean_output})
                        
                        if is_draft_generation:
                            st.session_state.generated_draft = clean_output
                            st.session_state.generated_draft_title = active_draft_type
                            
                        st.session_state.pending_request = None
                        st.rerun()
                    else:
                        st.session_state.messages.pop()
                        st.session_state.pending_request = None
                        st.error("All model clusters busy:\n" + "\n".join(errors))
                        
                except Exception as e:
                    st.session_state.messages.pop()
                    st.session_state.pending_request = None
                    st.error(f"System Error: {e}")
