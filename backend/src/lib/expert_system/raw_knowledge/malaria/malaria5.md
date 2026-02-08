This sixth logic tree for malaria incorporates **organ-specific physical indicators**, **pre-referral rectal dosing protocols**, **antiarrhythmic IV considerations**, and **geographic resistome weighting** found in the sources.

### **I. Refined Physical Sign Logic (Layer 1)**
*   **A. Specific Cutaneous and Oral Triggers**
    *   **Logic Rule:** IF (Physical Sign = Sour lips) OR (Physical Sign = Bitterness in the mouth) THEN **Weight:** Increase suspicion for Malaria.
    *   **Logic Rule:** IF (Symptom = Coldness) AND (Fever = Present) THEN **Action:** Trigger the "Cold Stage" paroxysm logic.
*   **B. Joint and Muscle Specificity**
    *   **Rule:** IF (Symptom = Aching joints) OR (Symptom = Body aches) THEN **Probability:** High likelihood of Malaria; IF (Symptom = Retro-orbital pain) THEN **Probability:** Favor Dengue.

### **II. Organ-Specific Manifestation Logic (Layer 2)**
*   **A. Splenic and Hepatic Rules**
    *   **P. falciparum Logic:** IF (Malaria = Suspected) AND (Clinical Sign = Enlargement of the spleen) THEN **Species Weight:** Favor *P. falciparum*.
    *   **Liver Involvement:** IF (Patient = Yellow eyes/Jaundice) AND (Fever = Cyclical) THEN **Diagnosis:** Likely severe malaria with hepatic involvement.
*   **B. Neurological Onset Pattern**
    *   **Logic Rule:** IF (Encephalopathy = Present) AND (Onset = Sudden convulsions) THEN **Diagnosis:** Cerebral Malaria; IF (Onset = Gradual stupor) THEN **Diagnosis:** Typhoid Encephalopathy.

### **III. Pre-Referral and Emergency Dosing Logic (Layer 3)**
*   **A. Rectal Artesunate Protocol**
    *   **Trigger Rule:** IF (Severe Malaria = Suspected) AND (Patient = Child < 6 years) AND (IV access = Not available) AND (Referral time > 6 hours) THEN **Action:** Administer **Artesunate Suppository**.
    *   **Dosage Logic:** Give a single dose of **10 mg/kg** body weight before urgent transfer.
*   **B. Pre-Referral Maintenance**
    *   **Logic Rule:** IF (General Danger Signs = Present) THEN **Action:** Administer first dose of appropriate antibiotic AND antimalarial AND **Keep the child warm** during transit.

### **IV. Advanced Severe Malaria IV Selection (Layer 4)**
*   **A. IV Quinidine Constraints**
    *   **Selection Rule:** IF (Malaria = Severe) AND (Artesunate = Unavailable) THEN **Action:** Use **IV Quinidine** (FDA-approved antiarrhythmic).
    *   **Co-Administration Requirement:** IF (Treatment = IV Quinidine) THEN **Mandatory Action:** Combine with Clindamycin, Doxycycline, or Tetracycline.
*   **B. Monitoring Response**
    *   **Rule:** IF (Treatment = Initiated) THEN **Action:** Monitor **Parasite Density** (number of infected cells per 100 RBCs) to determine clinical response and guide management.

### **V. Geographic Resistome Weighting (Layer 5)**
*   **A. Regional Resistance Adjustment**
    *   **Inference Rule:** IF (Travel History = Known Region) THEN **Weight:** Adjust drug selection based on local **Plasmodium resistance** to Chloroquine or Mefloquine.
*   **B. Species-to-Region Mapping**
    *   **Rule:** IF (Travel History = Africa) AND (Symptom = Mild Paroxysms) THEN **Species Weight:** Consider *P. ovale*.
    *   **Rule:** IF (Location = Odisha, India) THEN **Species Weight:** Consider *P. malariae*.

### **VI. Stability-First Triage Logic (Layer 6)**
*   **A. Procedure Termination Rule**
    *   **Logic Rule:** IF (General Danger Sign = Present) THEN **Action:** **Terminate standard diagnostic routine**; initiate emergency stabilization and urgent referral immediately.
*   **B. Comorbidity Delay Rule**
    *   **Logic Rule:** IF (Patient = HIV Infected) AND (Condition = Unstable/Severe Malaria) THEN **Action:** **Stabilize malaria first**; initiation of ART is not urgent and must wait until the patient is stable.

### **VII. Computational Confidence Logic (Layer 7)**
*   **A. Probability Calibration**
    *   **Rule:** Use **Log Loss** metrics to evaluate the difference between expected probabilities and actual class labels to ensure diagnostic estimates are well-calibrated and reliable.
*   **B. Diagnostic Threshold Logic**
    *   **Rule:** IF (Microscopy = Positive) AND (Parasitemia > 10%) THEN **Action:** Consider **Exchange Transfusion**; IF (Treatment = IV Artesunate) THEN **Action:** **Do not** recommend exchange transfusion.