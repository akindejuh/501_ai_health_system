This logic tree incorporates specific clinical details, diagnostic nuances, and weighted probability rules found in the sources that were not explicitly detailed in the previous general tree.

### **I. Layer 1: Epidemiological and Risk Filtering**
Before clinical symptoms are weighted, the knowledge engine must assess the environmental "Catalyst Factors" that increase the prior probability of Typhoid.
*   **IF (Travel History = Recent visit to endemic region)** AND **(Sanitation Access = Poor)**:
    *   **THEN** Assign $+15\%$ to base probability.
*   **IF (Food Exposure = Recent ingestion of raw street foods or unboiled water)**:
    *   **THEN** Assign $+10\%$ to base probability.
*   **IF (Biological History = *H. pylori* infection OR Gastrectomy)**:
    *   **THEN** Increase susceptibility weight (Lower infectious dose requirement).

### **II. Layer 2: Expanded Symptomatic Rules (Fuzzy Integration)**
These rules address specific symptoms and temporal patterns identified in more detailed diagnostic models.
*   **Rule - Fever Onset:** IF (Fever Pattern = Step-ladder/Gradual rise daily), THEN weight for **Week 1 Typhoid** is maximum.
*   **Rule - Respiratory Clues:** IF (Persistent non-productive cough) AND (Night sweats), THEN add secondary weight for Typhoid (Differential from Malaria).
*   **Rule - Gastrointestinal Sequence:** 
    *   IF (Duration $< 7$ days) AND (Constipation), THEN increase probability.
    *   IF (Duration $> 10$ days) AND (Watery Diarrhea), THEN increase probability.
*   **Rule - Mental State:** IF (Fever plateaus at $40^{\circ}C$) AND (Mental status = Stupor/Confusion), THEN classify as **Typhoid Encephalopathy** (Week 2/3 Marker).

### **III. Layer 3: Laboratory Integration and Reliability Logic**
This layer handles the high rate of uncertainty in common serological tests.
*   **Rule - CBC Logic:** IF (White Blood Cell Count = Low/Leukopenia) AND (Platelet Count = Low/Thrombocytopenia), THEN clinical suspicion of Typhoid increases.
*   **Rule - Widal "Rule-Out" Power:** IF (Widal Test = Negative), THEN probability of Typhoid is $\approx 1.1\%$ (High Negative Predictive Value of $98.9\%$).
*   **Rule - Widal Reliability Filter:** IF (Widal = Positive), THEN check for "Confounding Factors":
    *   IF (Patient had prior Typhoid vaccine) OR (Recent Malaria infection), THEN reduce Widal weight by $50\%$ (Risk of False Positive).
*   **Rule - Confirmatory Paired Sera:** IF (Initial Titer is borderline) AND (Repeat Titer shows 4-fold rise after 7 days), THEN Diagnosis = **Confirmed Enteric Fever**.

### **IV. Layer 4: Mathematical Probability Calculation**
The engine can utilize the "Probability Disease" formula provided in the source for more precise scoring:
*   **Formula:** $P(d) = \frac{(\sum S_{i}W_{i} - \sum(S_{major})_{j}(W_{max})_{j}) - Min_{th}}{Max_{th} - Min_{th}} \times 100\%$
    *   $S_{i} = 1$ if symptom selected, $0$ if not.
    *   $W_{i} = $ Weight assigned to symptom.
    *   $Min_{th}/Max_{th} = $ System thresholds for "Mild" to "Very Severe".

### **V. Layer 5: Management of Chronic Carriage**
If the patient is in the recovery stage (Week 4+) but remains a shedder.
*   **IF (Diagnosis = Recovery Stage)** AND **(Stool Culture = Positive for *S. Typhi*)**:
    *   **THEN** Action = **Eradication Therapy**.
    *   **TREATMENT:** Oral **Ciprofloxacin** (750mg BD) OR **Norfloxacin** (400mg BD) for **14–28 days**.

### **VI. Layer 6: Critical Complication Monitoring (Week 3 Logic)**
*   **IF (Abdominal Exam = Guarding/Rigidity)** OR **(Stool = Melena/Black tarry)**:
    *   **THEN** Complication = **Intestinal Perforation/Hemorrhage** (Peyer's patch necrosis).
    *   **ACTION:** IMMEDIATE surgical referral and cessation of oral intake.