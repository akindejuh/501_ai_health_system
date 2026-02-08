Building on the previous structure, this expanded logic tree incorporates advanced fuzzy membership ranges, species-specific diagnostic pathways, detailed pediatric Integrated Management of Childhood Illness (IMCI) thresholds, and comparative tie-breaker weights to distinguish malaria from overlapping tropical fevers.

### **I. Quantitative Fever Logic (Layer 1: Fuzzification)**
*   **A. Temperature Range Membership**
    *   **Rule:** Assign membership values based on axillary temperature:
        *   **Normal:** $36.6^{\circ}C$ to $37.0^{\circ}C$.
        *   **Low Fever:** $37.1^{\circ}C$ to $37.9^{\circ}C$.
        *   **High Fever:** $38.0^{\circ}C$ to $40.0^{\circ}C$.
*   **B. Temporal Patterns**
    *   **Logic:** IF (Fever = Cyclical/Paroxysmal) AND (Fever duration is $\geq$ 48–72 hours) THEN **Action:** Highly favor Malaria over the "step-ladder" onset of Typhoid.

### **II. Species-Specific Symptom Logic (Layer 2)**
*   **A. *P. falciparum* (Malignant Tertian)**
    *   **Inference Rule:** IF (Symptoms = Dizziness) OR (Symptoms = Seizures/Convulsions) OR (Symptoms = Severe Anemia) THEN **Target Specie:** Likely *P. falciparum*.
*   **B. *P. vivax* and *P. ovale***
    *   **Inference Rule:** IF (Symptoms = Diarrhea) AND (Symptoms = Extreme Fatigue) THEN **Target Specie:** Consider *P. vivax* or *P. ovale*.
    *   **Relapse Logic:** IF (History = Past Malaria infection within 1 year) THEN **Weight:** Favor *P. vivax/ovale* due to liver hypnozoites.
*   **C. *P. malariae***
    *   **Inference Rule:** IF (Fever = Persistent High Grade) AND (Recent Travel = Africa/Endemic zone) THEN **Target Specie:** Consider *P. malariae*.

### **III. Pediatric IMCI Diagnostic Thresholds (Layer 3: Patients 2mo–5yr)**
*   **A. Respiratory Distress Logic (Differential for Malaria vs. Pneumonia)**
    *   **Logic Rule 1 (Fast Breathing):** 
        *   IF (Age = 2–12 months) AND (Breaths $\geq 50/min$) THEN **Weight:** Favor Severe Malaria/Pneumonia.
        *   IF (Age = 12 months–5 years) AND (Breaths $\geq 40/min$) THEN **Weight:** Favor Severe Malaria/Pneumonia.
    *   **Logic Rule 2 (Danger Signs):** IF (Chest Indrawing = Present) OR (Stridor in calm child = Present) THEN **Classification:** Very Severe Disease; **Action:** Urgent Referral.
*   **B. Comorbidity Constraints**
    *   **HIV Interaction:** IF (Patient = HIV Exposed/Infected) AND (Symptom = Chest Indrawing) THEN **Action:** Immediate Amoxicillin dose + Urgent Referral for Malaria/Pneumonia stabilization.

### **IV. Advanced Complication Monitoring (Layer 4)**
*   **A. Hemoglobinuria (Blackwater Fever)**
    *   **Logic Rule:** IF (Malaria = Suspected) AND (Urine Color = Dark/Black/Red) THEN **Diagnosis:** Hemoglobinuria; **Action:** Immediate Renal assessment and stabilization.
*   **B. Hematological Differences (Tie-Breaker Logic)**
    *   **Logic Rule (Malaria):** IF (Lab Results = Low Red Blood Cell Count) AND (Lab Results = Low Hemoglobin) THEN **Weight:** Favor Malaria.
    *   **Logic Rule (Dengue):** IF (Lab Results = Low Platelet Count) AND (Clinical Sign = Bleeding Gums/Nose) THEN **Weight:** Favor Dengue.

### **V. Diagnostic Confidence & Bayesian Integration (Layer 5)**
*   **A. Reliability Logic**
    *   **Microscopy (Blood Smear):** Sensitivity (73%–88%), Specificity (91.4%–98.3%).
    *   **RDT:** Sensitivity (80%–90%), Specificity (86%–99%).
*   **B. Recursive Testing Rule**
    *   **Logic Rule:** IF (Clinical Suspicion = High) AND (Initial RDT = Negative) THEN **Requirement:** Repeat blood smears every 12–24 hours for a total of three sets before rule-out.

### **VI. Pharmacological Selection Constraints (Layer 6)**
*   **A. Pregnancy and Age Adjustments**
    *   **Rule 1 (Contraindication):** IF (Patient = Pregnant) OR (Age < 8 years) THEN **Action:** **Avoid Doxycycline** for Malaria prophylaxis or co-infection treatment.
    *   **Rule 2 (Alternative):** IF (Malaria = Severe) AND (Patient = Pregnant/Child) THEN **Selection:** Clindamycin is the recommended alternative to Doxycycline.
*   **B. Malnutrition Interaction**
    *   **Zinc/Iron Rule:** IF (Patient = Diarrhea present) THEN **Action:** Give Zinc (20mg daily); IF (Patient = Severe Acute Malnutrition) THEN **Action:** **Do not give Iron** if child is already on Ready-to-Use Therapeutic Food (RUTF).

### **VII. System Re-Evaluation Logic (Layer 7)**
*   **A. Persistence Protocol**
    *   **Logic Rule:** IF (Malaria treatment started) AND (Fever persists > 48 hours) THEN **Inference Engine Action:** Re-run differential diagnosis logic to check for **Malaria-Typhoid co-infection** (incidence rate 3.9%–6.7%).
*   **B. Clinical Staging Update**
    *   **Logic Rule:** IF (Follow-up Visit) AND (Symptom = Not gaining weight for 3 months) THEN **Action:** Non-urgent referral to assess for underlying HIV clinical stage progression or chronic comorbidity.