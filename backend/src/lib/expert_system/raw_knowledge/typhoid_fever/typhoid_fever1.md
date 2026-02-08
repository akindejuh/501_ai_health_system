This logic tree is structured to provide the formal logic and production rules necessary for building a knowledge base for a medical expert system focused on **Typhoid Fever** (Enteric Fever), based on clinical progression, pathognomonic signs, and diagnostic weight.

### **I. Layer 1: Triage and Initial Febrile Assessment**
The system first identifies the presence of fever and rules out immediate life-threatening "General Danger Signs".
*   **IF** (Body Temperature $> 37.5^{\circ}C$):
    *   **IF** (Unable to drink/breastfeed) **OR** (Vomiting everything) **OR** (Convulsions) **OR** (Lethargy/Unconsciousness):
        *   **THEN** Classification = **Very Severe Disease**; Action = **URGENT REFERRAL**.
    *   **ELSE** Proceed to Layer 2.

### **II. Layer 2: Weekly Temporal and Pattern Logic**
Typhoid follows an insidious, weekly progression that serves as a primary weighted feature in the inference engine.
*   **IF (Fever Duration = 1–7 Days):**
    *   Check for "Step-ladder" pattern (gradual daily rise).
    *   Symptoms: Malaise, headache, non-productive cough.
    *   **ACTION:** Order **Blood Culture** (Gold standard in Week 1).
*   **IF (Fever Duration = 8–14 Days):**
    *   Check for continuous high fever ($104^{\circ}F / 40^{\circ}C$).
    *   Symptoms: Persistent abdominal pain, diarrhea (late stage), or early constipation.
    *   **ACTION:** Order **Typhidot (RDT)** or **Widal Test**.
*   **IF (Fever Duration $> 14$ Days):**
    *   **THEN** Severity = **High**.
    *   Check for Complications: Intestinal hemorrhage (melena), perforation (acute abdominal pain/guarding), or "Typhoid Stupor" (encephalopathy).

### **III. Layer 3: Physical Examination (Pathognomonic Logic)**
Clinical cues provide "tie-breaker" weights when symptoms overlap with Malaria or Dengue.
*   **Rule - Relative Bradycardia:** IF (High Fever present) **AND** (Heart rate is slower than expected for temperature), THEN weight for Typhoid increases.
*   **Rule - Rose Spots:** IF (Small, pink macules present on trunk), THEN probability of Typhoid is markedly elevated.
*   **Rule - Organomegaly:** IF (Palpable Hepatosplenomegaly), THEN Typhoid is likely.

### **IV. Layer 4: Diagnostic Integration (Weighted Reasoning)**
The knowledge engine must synthesize laboratory data using weighted heuristics to account for false positives.
*   **Blood Culture Rule:** IF (Result = Positive), THEN Diagnosis = **Confirmed Typhoid**.
*   **Widal Test Rule (Endemic Areas):** 
    *   IF (Anti-TO titer $\geq 1:80$ AND Anti-TH titer $\geq 1:160$), THEN Diagnosis = **Likely Typhoid**.
    *   **NOTE:** System must account for cross-reactivity with Malaria.
*   **Multi-Evidence Heuristic:** IF (Fever $> 7$ days) **AND** (Abdominal pain present) **AND** (Relative Bradycardia present), THEN Typhoid probability is High even if Widal results are borderline.

### **V. Layer 5: Classification and Management Output**
*   **IF (Classification = Uncomplicated Typhoid):**
    *   **THEN** Treatment = Oral **Ciprofloxacin** (500mg BD for 10–14 days) **OR** **Azithromycin**.
*   **IF (Classification = Severe/Complicated Typhoid):**
    *   **THEN** Treatment = IV **Ceftriaxone** (1-2g daily for 10–14 days).
    *   **IF** (Encephalopathy/Shock present), **THEN** consider **Dexamethasone**.

### **VI. Layer 6: Co-infection and Differential Safety Net**
*   **Tie-Breaker Rule:** IF (Fever is Cyclical with Chills/Sweats), THEN shift primary hypothesis to **Malaria**.
*   **Tie-Breaker Rule:** IF (Sudden onset high fever AND "Breakbone" joint pain AND Retro-orbital headache), THEN shift to **Dengue**.
*   **Re-evaluation Rule:** IF (Treatment for Malaria fails to resolve fever within 48 hours), THEN re-evaluate for **Malaria-Typhoid Co-infection**.