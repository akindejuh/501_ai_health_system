Building upon the previous triage and environmental logic trees, this final logic layer for a cholera knowledge engine focuses on **clinical sub-type classification**, **precision pharmacological dosing**, **specialized management for high-risk cohorts**, and **advanced facility engineering**.

### I. Layer 5: Clinical Sub-Type Classification
This layer refines the diagnosis beyond simple dehydration to identify the specific physiological state of the patient.

*   **Logic Rule 1: Non-Complicated Cholera**
    *   **Condition:** Watery diarrhea AND vomiting AND mild dehydration.
    *   **Action:** Oral rehydration therapy (ORT) as the primary intervention.
*   **Logic Rule 2: Complicated Cholera**
    *   **Condition:** Severe dehydration AND hypotension (low BP) AND/OR signs of electrolyte imbalance (e.g., muscle cramps, arrhythmia).
    *   **Action:** Immediate IV rehydration and electrolyte management.
*   **Logic Rule 3: Cholera with Shock**
    *   **Condition:** Very low BP AND weak/rapid pulse AND cold/clammy skin AND confusion.
    *   **Action:** Immediate bolus of IV fluids; consider vasopressors if unresponsive.
*   **Logic Rule 4: Asymptomatic (Carrier State)**
    *   **Condition:** No clinical symptoms AND history of exposure or travel to an endemic area in the last 10 days.
    *   **Action:** Monitoring and education on preventing transmission; bacterial shedding may last 1–10 days.

### II. Layer 6: Physiological Monitoring and Interval Logic
This layer governs the frequency of medical assessment based on the patient's triage code.

*   **Code Red (Severe) Monitoring Logic:**
    *   **Interval:** Reassess dehydration status every **30 minutes**; monitor pulse, respiratory rate, and BP every **15 minutes**.
*   **Code Yellow (Some) Monitoring Logic:**
    *   **Interval:** Reassess dehydration status and vital signs every **1 hour**.
*   **Code Green (No) Monitoring Logic:**
    *   **Interval:** Reassess dehydration status and vital signs every **4 hours**.

### III. Layer 7: Precision Pharmacological Dosing
This layer provides specific dosage rules for antibiotics and supplements based on patient category.

*   **Antibiotic Selection Rule:**
    *   **Adults:** Doxycycline (300 mg single oral dose) [440, table 1].
    *   **Pregnant Women:** Azithromycin (1 g single oral dose) OR Erythromycin (500 mg every 6 hours for 3 days) [table 1].
    *   **Children (>3 yrs, can swallow):** Azithromycin (20 mg/kg, max 1 g, single dose) [table 1].
    *   **Infants/Children (cannot swallow):** Azithromycin suspension (20 mg/kg single dose) [table 1].
*   **Micronutrient Supplementation Logic:**
    *   **Zinc Supplementation:** For all children with diarrhea, give **20 mg daily for 10–14 days** to reduce duration and severity.
*   **Hypoglycemia Correction Logic:**
    *   **Threshold:** Glucose $<45\text{ mg/dl}$ (normal) or $<54\text{ mg/dl}$ (SAM).
    *   **Action:** Administer **5 ml/kg of 10% Dextrose IV**; recheck in 30 minutes.

### IV. Layer 8: Specialized Management (SAM and NG Tube)
This layer manages patients who cannot be treated with standard rehydration protocols.

*   **Shock with SAM Logic:**
    *   **Action:** Administer **10–15 ml/kg over 1 hour** using a mixture of **half Ringer’s Lactate and half 5% Dextrose**.
*   **Standard SAM Rehydration Logic:**
    *   **Phase 1:** ORS ($5\text{ ml/kg}$) every 30 minutes for 2 hours.
    *   **Phase 2:** ORS ($5\text{--}10\text{ ml/kg/hr}$) for 4–10 hours, alternating with F75 therapeutic food.
*   **Nasogastric (NG) Tube Logic:**
    *   **Trigger:** IF IV access is not achieved within **30 minutes of effort**.
    *   **Protocol:** ORS solution at **20 ml/kg/hr for 6 hours** (Total $120\text{ ml/kg}$).

### V. Layer 9: Advanced Diagnostics and Future Tech
This layer incorporates recursive testing logic and biological interventions.

*   **Recursive Testing Rule:** IF clinical suspicion is high AND initial Rapid Diagnostic Test (RDT) is negative, THEN repeat blood smears/tests every **12–24 hours** for a total of **three sets** before ruling out the pathogen.
*   **Probiotic Integration Logic:** Consider use of **probiotics** (e.g., *Ruminococcus obeum* or *Lactobacillus rhamnosus GG*) to potentially remove cholera toxin from the gut environment.
*   **Fuzzy-Hybrid AI layer:** Use Artificial Neural Networks (ANN) to predict initial risk scores, then refine with Fuzzy Expert System (FES) rules to ensure clinical explainability for the healthcare worker.

### VI. Layer 10: Facility Engineering and Water Logistics
This layer governs the technical requirements for a Cholera Treatment Centre (CTC).

*   **Water Storage Calculation:** Store enough for **at least 3 days** based on **60 Liters/patient/day** and **15 Liters/caregiver/day**.
*   **Water System Layout (for 50 Patients):** Six tanks (3000mm high frame) divided into:
    *   **2 x 2000L** (0.05% Chlorine) for handwashing.
    *   **2 x 2000L** (0.5% Chlorine) for disinfection.
    *   **2 x 1000L** (2% Chlorine) for severe waste/mortality.
*   **Waste Engineering:** Burning pit must be at least **2m deep** with an iron grid raised **40cm** from the bottom to assist combustion.
*   **Sewer System Logic:** Waste water pits must be **20% larger** than estimated water production to account for sudden activity surges.