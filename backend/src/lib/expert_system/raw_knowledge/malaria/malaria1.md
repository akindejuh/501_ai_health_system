This logic tree is designed to structure a knowledge base for a malaria expert system, drawing from the clinical protocols and production rules found in the sources.

### **I. Triage and Initial Screening (Layer 1)**
*   **A. Check for Pediatric General Danger Signs (Patients < 5 years)**
    *   **Logic Rule:** IF (Inability to drink or breastfeed) OR (Vomits everything) OR (Convulsions) OR (Lethargic or unconscious) THEN **Output:** Urgent Referral/Pre-referral Treatment.
*   **B. Epidemiological Filtering (All Ages)**
    *   **Logic Rule:** IF (History of travel to endemic area) AND (Fever present or reported) THEN **Action:** Proceed to Malaria Pathway.
    *   **Logic Rule:** IF (Travel to endemic zone = No) THEN **Action:** Reduce weight for Malaria hypothesis.

### **II. Symptom-Based Logic (Layer 2)**
*   **A. The Malarial Paroxysm Rule (High-Weight Features)**
    *   **Step 1 (Cold Stage):** Check for sudden onset of chills and rigors.
    *   **Step 2 (Hot Stage):** Check for high-grade fever ($\geq 39.5^{\circ}C$).
    *   **Step 3 (Sweating Stage):** Check for profuse sweating as fever breaks.
    *   **Conclusion Logic:** IF (Fever = Intermittent) AND (Chills = Present) AND (Sweating = Present) THEN **Probability:** Malaria is highly likely.
*   **B. Associated General Symptoms**
    *   **Input Variables:** Headache, fatigue, nausea/vomiting, muscle/joint pain, abdominal pain, and bitter taste in the mouth.
    *   **Weighted Logic:** IF (Symptoms = BITAIM (Bitter taste), LTG (Lethargy), CHLNRIG (Chills), and FVR (Fever)) THEN **Probability:** Strong influence on Malaria diagnosis.

### **III. Diagnostic Integration (Layer 3)**
*   **A. Laboratory Verification**
    *   **Rule 1 (Microscopy):** IF (Blood Smear = Positive) THEN **Action:** Identify species and determine parasitemia density.
    *   **Rule 2 (RDT):** IF (Rapid Diagnostic Test = Positive) AND (Microscopy unavailable) THEN **Action:** Initiate treatment for confirmed malaria.
    *   **Rule 3 (Negative Results):** IF (Initial RDT = Negative) AND (Clinical suspicion = High) THEN **Action:** Repeat blood smears every 12–24 hours for a total of three sets.

### **IV. Severity Classification (Layer 4)**
*   **A. Uncomplicated Malaria**
    *   **Logic Rule:** IF (Fever = High) AND (Parasitemia = Detected) AND (Cerebral symptoms = Absent) AND (Organ dysfunction = Absent) THEN **Classification:** Uncomplicated Malaria.
*   **B. Severe Malaria (Critical Pathways)**
    *   **Pathway 1 (Cerebral):** IF (Malaria = Suspected) AND (Consciousness = Impaired or coma) THEN **Diagnosis:** Cerebral Malaria.
    *   **Pathway 2 (Respiratory):** IF (Malaria = Suspected) AND (Respiratory Rate = Increased) AND (Grunting or Chest Indrawing = Present) THEN **Diagnosis:** Severe Malaria (Respiratory Distress).
    *   **Pathway 3 (Renal/Hemoglobin):** IF (Malaria = Suspected) AND (Urine = Dark or Bloody) THEN **Diagnosis:** Severe Malaria (Hemoglobinuria/Blackwater Fever).

### **V. Management and Treatment Logic (Layer 5)**
*   **A. Medication Selection**
    *   **Rule 1 (P. falciparum):** IF (Species = P. falciparum) THEN **Treatment:** Artemisinin-based Combination Therapy (ACT).
    *   **Rule 2 (P. vivax/ovale):** IF (Species = P. vivax or P. ovale) THEN **Treatment:** ACT + Primaquine (to eradicate liver hypnozoites and prevent relapse).
    *   **Rule 3 (Severe Malaria):** IF (Condition = Severe) THEN **Action:** IV Artesunate (bolus at 0, 12, and 24 hours) or IV Quinine.
*   **B. Pediatric Supportive Care**
    *   **Rule 1 (Hypoglycemia):** IF (Malaria = Severe) THEN **Action:** Treat to prevent low blood sugar (Dextrose or sugar water).
    *   **Rule 2 (Anemia):** IF (Palmar Pallor = Severe) THEN **Action:** Refer urgently for blood transfusion.

### **VI. Safety Net and Co-infection Logic (Layer 6)**
*   **A. Re-Evaluation**
    *   **Logic Rule:** IF (Malaria treatment initiated) AND (Fever persists > 48 hours) THEN **Action:** Re-evaluate for Typhoid or Dengue co-infection.
*   **B. Tie-Breaker Logic (Malaria vs. Dengue)**
    *   **Tie-Breaker:** IF (Fever = Cyclical) AND (Anemia = Present) THEN **Weight:** Favor Malaria; IF (Fever = Sudden high) AND (Joint pain = "Breakbone") AND (Rash = Present) THEN **Weight:** Favor Dengue.