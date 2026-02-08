Based on the sources, here is a third layer of logic for your knowledge engine, incorporating advanced diagnostic criteria, specific treatment protocols for severe cases, and management of chronic carriage that were not detailed in the previous trees.

### **I. Layer 1: Pathogen and Strain Identification Logic**
The system must distinguish between the primary causative agent and its variants, as this affects epidemiological tracking and resistance expectations.
*   **Rule - Pathogen Distinction:** IF (Infection = Enteric Fever):
    *   **Check** for *Salmonella enterica* serotype **Typhi** (most common).
    *   **OR Check** for serovars **Paratyphi A, B, or C**.
*   **Rule - Incubation Period Variance:** IF (Exposure to contaminated food/water), THEN expected onset is between **6–30 days** (range can be 1–14 days in some clinical settings).

### **II. Layer 2: Advanced Diagnostic Culture Hierarchy**
This layer addresses scenarios where initial blood cultures are inconclusive or the patient has already begun antibiotic therapy.
*   **Rule - Culture Sensitivity:** 
    *   **IF (Blood Culture)**, THEN Sensitivity = **40–80%**.
    *   **IF (Bone Marrow Culture)**, THEN Sensitivity = **80–95%**; **Note:** This remains positive even after 5 days of pre-treatment with antibiotics.
*   **Rule - Isolate Requirements:** IF (Culture = Positive), THEN Action = Perform **Antimicrobial Susceptibility Testing (AST)** to identify resistance patterns (e.g., MDR strains).

### **III. Layer 3: Endemic-Specific Serological Refinement**
In endemic regions, standard Widal thresholds may be insufficient due to high background antibody levels.
*   **Rule - Endemic Widal Thresholds:** IF (Area = High Endemicity), THEN consider indicative titers to be:
    *   **O-agglutinin** $\geq 1:200$.
    *   **H-agglutinin** $\geq 1:100$.
*   **Rule - Serological Pitfall Filter:** IF (Widal = Positive), CHECK for **Vaccination History**; prior typhoid vaccination can cause significant false-positive titers.

### **IV. Layer 4: Severe Disease and Encephalopathy Protocol**
Specific pharmacological dosing is required for patients exhibiting neurological complications or shock.
*   **Rule - Dexamethasone Dosing:** IF (Diagnosis = Severe Typhoid) AND (Symptoms = **Encephalopathy, Shock, or DIC**):
    *   **ACTION:** Administer **Dexamethasone** at **3 mg/kg** initial dose.
    *   **Follow-up:** **1 mg/kg** every 6 hours for **48 hours**.
*   **Rule - MDR Treatment:** IF (Suspected Multidrug-Resistance), THEN Treatment = **IV Ceftriaxone** at **50–75 mg/kg/day** for 10–14 days.

### **V. Layer 5: Chronic Carriage and Eradication Logic**
Chronic carriers (shedding bacteria for $> 1$ year) require extended therapy to prevent community spread.
*   **Rule - Chronic Carrier Eradication:** IF (Patient = Asymptomatic Shedder) AND (Confirmed *S. Typhi* in stool):
    *   **TREATMENT OPTION 1:** **Ciprofloxacin** (750 mg) twice daily for **14–28 days**.
    *   **TREATMENT OPTION 2:** **Norfloxacin** (400 mg) twice daily for **14–28 days**.

### **VI. Layer 6: Pediatric Differentiating Criteria**
*   **Rule - Pediatric Vulnerability:** Assign higher diagnostic weight to Typhoid in children **15 years of age and younger** in urban areas.
*   **Rule - Clinical "Look-Alike" Safety Net:** IF (Fever + Headaches + Muscle/Joint Pain), ALWAYS screen for **Leptospirosis** if the patient has had direct contact with water contaminated by animal waste.