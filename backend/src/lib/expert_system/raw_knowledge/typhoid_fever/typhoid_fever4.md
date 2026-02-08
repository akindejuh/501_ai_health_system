This logic tree incorporates further refinements from the sources, specifically targeting host risk factors, syndrome-based classification for differential diagnosis, weighted symptom importance derived from explainable AI models, and detailed diagnostic pitfalls.

### **I. Layer 1: Host Factors and Susceptibility Logic**
The knowledge engine should weight the "Infectious Dose" based on the patient's biological profile.
*   **Rule - Acidity Defense:** IF (Patient history includes **PPI/antacid use**, **gastrectomy**, or **hypochlorhydria**), THEN reduce the required infectious dose threshold; bacteria bypass the gastric acid barrier more easily.
*   **Rule - Biological Predisposition:** IF (Blood Group = **Type O**), THEN assign a higher weight to the susceptibility for severe infection.
*   **Rule - Exposure Weighting:** IF (Source = **Street Food**), THEN infectious dose required is significantly lower ($10^{2}$–$10^{4}$ CFU) than for water-borne transmission.

### **II. Layer 2: Syndromic Classification (Front-End Filter)**
Instead of individual symptoms, the engine can categorize patients into major clinical syndromes to guide the differential.
*   **Syndrome - Undifferentiated Fever:** IF (Fever Duration $> 7$ days) AND (No focal source), THEN include **Malaria**, **Typhoid**, and **Scrub Typhus** in the primary differential.
*   **Syndrome - Fever with Rash:**
    *   IF (Rash = **Measles-like/Diffuse**), THEN Weight = **Dengue**.
    *   IF (Rash = **Sparse/Sparse pink macules**), THEN Weight = **Typhoid**.
*   **Syndrome - Fever with Encephalopathy:**
    *   IF (Convulsions = Sudden), THEN Weight = **Cerebral Malaria**.
    *   IF (Mental Status = "Typhoid Stupor"/Gradual confusion), THEN Weight = **Typhoid**.

### **III. Layer 3: Weighted Symptom Importance (XAI-Derived)**
Based on diagnostic modeling (XGBoost/Random Forest feature importance), the engine should apply the following weights to inputs:
*   **High-Priority Features (Max Weight):** **Bitter taste in mouth**, **Lethargy**, **Chills and rigors**, and **Body/Muscle pain**.
*   **Rule - High Confidence Exclusion:** IF (**Stepwise rise fever**, **Headache**, and **Constipation**) are all ABSENT, THEN the probability of Typhoid is significantly reduced.
*   **Differential - Headache Severity:** IF (Headache = **Mild to Moderate**), THEN prioritize **Typhoid**; IF (Headache = **Intense/Persistent**), THEN prioritize **Dengue**.

### **IV. Layer 4: Diagnostics Integrity and Pitfall Filters**
This layer manages the high error rates in standard serological testing.
*   **Rule - Culture Maximization:** IF (Suspected Typhoid), THEN collect **2–3 separate blood culture samples**; bacteremia is often low-grade and may be missed in a single sample.
*   **Rule - Widal False Negative Filter:** IF (Widal = Negative) AND (History of **prior antibiotics** OR **immunosuppression**), THEN disregard the negative result and proceed to Bone Marrow Culture.
*   **Rule - Widal Statistical Weight:** Assign a low positive predictive value to Widal tests in endemic areas (PPV can be as low as **5.7%**); use primarily for ruling out disease due to high negative predictive value.

### **V. Layer 5: Expanded Management and Prognosis Logic**
*   **Rule - Resistance Empiricism:** IF (Local resistance patterns are unknown), THEN empiric treatment = **Oral Ciprofloxacin (500mg BD)** OR **IV Ceftriaxone (1–2g daily)** for 10–14 days.
*   **Rule - Alternative Therapeutics:** IF (First-line agents are unavailable), THEN utilize **Ampicillin**, **Chloramphenicol**, or **Trimethoprim-sulfamethoxazole (TMP-SMX)**.
*   **Rule - Mortality Risk Projection:** IF (Patient remains untreated), THEN assign a **20% mortality risk weight** from complications such as internal bleeding or sepsis.

### **VI. Layer 6: Pathophysiology Progression Detail**
*   **Rule - Reticulo-endothelial Pathway:** Logic weight for splenomegaly and hepatomegaly is highest in **Week 2** as the bacteria disseminate from the **Peyer's patches** into the bloodstream and organs.

(NO MORE RULES)