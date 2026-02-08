Based on the sources, this fifth and final logic tree provides the final set of refinements for your knowledge engine, focusing on specific fuzzy logic thresholds, RDT-specific accuracy, and post-treatment prognostic rules.

### **I. Layer 1: Numerical Triage Logic (Fuzzy Set Boundaries)**
For a rule-based engine, these specific temperature thresholds from the sources define the categories for fever severity.
*   **Rule - Temperature Mapping:**
    *   **IF** (Temp $\leq 37.0^{\circ}C$), **THEN** Fever = **False**.
    *   **IF** (Temp $> 37.0^{\circ}C$ AND $\leq 38.3^{\circ}C$), **THEN** Fever = **Low Fever**.
    *   **IF** (Temp $> 38.3^{\circ}C$ AND $\leq 39.4^{\circ}C$), **THEN** Fever = **High Fever**.
    *   **IF** (Temp $> 39.4^{\circ}C$), **THEN** Fever = **Very High Fever**.
*   **Rule - Confidence Threshold:** IF (Patient presents with $> 2$ primary symptoms), THEN the system must trigger a **"Confirm Diagnosis"** dialogue to process secondary symptoms for Malaria/Dengue differentiation.

### **II. Layer 2: Diagnostic Tool Reliability Logic**
This layer integrates the specific performance metrics of rapid diagnostic tests (RDTs) found in the sources to adjust the engine's "Certainty Factor."
*   **Rule - Typhidot (RDT) Reliability:** IF (Typhidot = Positive), THEN assign high weight (Sensitivity **95–97%**; Specificity **>89%**).
*   **Rule - Widal Statistical Adjuster:** When utilizing the Widal test, the system must account for the following error margins:
    *   **IF** (Widal = Positive), THEN account for a **14% False Positive** risk.
    *   **IF** (Widal = Negative) AND (Testing is in Week 1), THEN account for a **10% False Negative** risk.

### **III. Layer 3: Advanced Laboratory Yield Nuances**
*   **Rule - Bone Marrow Yield:** IF (Patient has received antibiotics for $\leq 5$ days), THEN prioritize **Bone Marrow Culture** over blood culture, as it remains highly sensitive (80–95%) despite pre-treatment.
*   **Rule - Culture Timing:** Yield for blood cultures is strictly time-dependent:
    *   **Week 1 yield:** 40–80%.
    *   **Yield after Week 1:** Significantly decreases as bacteria disseminate to organs like Peyer's patches.

### **IV. Layer 4: Prognostic and Follow-up Logic**
The engine should manage the transition from acute illness to recovery or carrier status.
*   **Rule - Recovery Timeline (Stage IV):**
    *   **IF** (Antibiotic started), THEN improvement is expected within **2–3 days**.
    *   **IF** (Fever persists $> 48$ hours post-treatment), THEN activate **Differential Safety Net** for co-infection with Malaria or Dengue.
*   **Rule - Defervescence Monitoring:** IF (Fever begins to decline in Week 4), THEN flag the patient for **Chronic Carriage Screening**.
*   **Rule - Chronic Carrier Verification:** A patient is confirmed as a chronic carrier if they continue to shed *S. Typhi* in stool for **$> 1$ year**.

### **V. Layer 5: Patient Education Logic (Prevention Triggers)**
The system should output the following "Prevention Rules" based on the diagnosis:
*   **Rule - Water Safety:** IF (Typhoid Confirmed), THEN advise: **"Avoid unboiled/untreated water and ice made from non-bottled water"**.
*   **Rule - Food Hygiene:** IF (Typhoid Confirmed), THEN advise: **"Avoid raw street foods; only consume food that is well-cooked and served hot"**.

(NO MORE RULES)