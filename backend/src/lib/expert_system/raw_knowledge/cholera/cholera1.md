A detailed logic tree for a cholera knowledge engine, synthesized from the clinical guidelines and production rules provided in the sources, is organized into four major layers: **Clinical Suspicion**, **Dehydration Triage**, **Treatment Action**, and **Comorbidity Management**.

### I. Layer 1: Clinical Suspicion and Initial Screening
This layer identifies whether the patient should enter the cholera diagnostic pathway based on World Health Organization (WHO) suspicion criteria.

*   **Entry Condition:** Patient presents with **Acute Watery Diarrhea (AWD)** (more than three loose stools per day without blood).
    *   **Decision Node 1 (Endemic/Outbreak Area):**
        *   **YES:** Any patient presenting with AWD is a cholera suspect.
        *   **NO:** Proceed to Decision Node 2.
    *   **Decision Node 2 (Non-Endemic Area):**
        *   **IF** Patient age $\geq 5$ years AND develops **severe dehydration** or **dies from AWD** $\rightarrow$ **Cholera Suspect**.
        *   **ELSE** $\rightarrow$ Consider other gastrointestinal disorders (e.g., food poisoning, viral gastroenteritis).
    *   **Pathognomonic "Rice-Water" Rule:** IF stool is pale/milky with mucous flecks and has a fishy odor $\rightarrow$ **High Probability of Toxigenic Cholera**.

### II. Layer 2: Dehydration Assessment and Triage
Once suspected, the engine must classify the severity to determine the treatment setting.

*   **Logic Rule A: Severe Dehydration (Code Red)**
    *   **Condition:** Two or more of the following: Lethargic or unconscious; Sunken eyes; Unable to drink or drinking poorly; Skin pinch goes back very slowly ($>2$ seconds).
    *   **Sub-Rule (Shock):** IF signs include cold extremities, weak/fast pulse, or capillary refill $>3$ seconds $\rightarrow$ **Hypovolemic Shock**.
*   **Logic Rule B: Some Dehydration (Code Yellow)**
    *   **Condition:** Two or more of the following: Restless or irritable; Sunken eyes; Drinks eagerly/thirsty; Skin pinch goes back slowly.
*   **Logic Rule C: No Dehydration (Code Green)**
    *   **Condition:** Patient is alert, has normal eyes, drinks normally, and skin pinch returns immediately.

### III. Layer 3: Treatment Action Layer
This layer translates the triage status into specific medical interventions.

*   **Action for Code Red (Plan C):**
    *   **Immediate Action:** Rapid IV rehydration with **Ringer's Lactate** (preferred) or Normal Saline.
    *   **Volume Logic (Total $100\text{ ml/kg}$):**
        *   **Age $<1$ year:** $30\text{ ml/kg}$ in 1 hour; then $70\text{ ml/kg}$ in 5 hours.
        *   **Age $\geq 1$ year:** $30\text{ ml/kg}$ in 30 minutes; then $70\text{ ml/kg}$ in 2.5 hours.
    *   **Antibiotic Rule:** Give oral antibiotics (e.g., **Azithromycin** or **Doxycycline**) once the patient can swallow.
*   **Action for Code Yellow (Plan B):**
    *   **Action:** Supervised oral rehydration with **ORS** ($75\text{ ml/kg}$) over 4 hours.
    *   **Zinc Rule:** Start **Zinc supplementation** ($20\text{ mg}$ daily for 10–14 days).
*   **Action for Code Green (Plan A):**
    *   **Action:** Home management with ORS after each loose stool ($50\text{--}200\text{ ml}$ based on age).

### IV. Layer 4: Comorbidities and Laboratory Confirmation
This layer manages high-risk conditions and definitive testing.

*   **Decision Node: High-Risk Comorbidities?**
    *   **IF Severe Acute Malnutrition (SAM):** Use specialized rehydration (e.g., F75) and slower fluid rates to avoid heart failure.
    *   **IF Pregnancy:** Prioritize rapid rehydration to prevent spontaneous abortion or premature delivery in the third trimester.
    *   **IF Hypoglycemia:** Administer IV dextrose ($5\text{ ml/kg}$ of 10% solution).
*   **Laboratory Path (Confirmation):**
    *   **Order Stool Culture:** Isolating *Vibrio cholerae* O1 or O139 (Gold Standard).
    *   **Order Rapid Diagnostic Test (RDT):** Use for rapid detection in outbreak surveillance.
*   **Discharge Logic:**
    *   **Condition:** Stool output has decreased significantly ($<3$ episodes in 6 hours) AND patient is alert and drinking well.