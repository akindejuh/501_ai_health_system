This final layer of logic for your knowledge engine incorporates specific statistical probabilities, refined clinical timing, and cross-reactivity rules found in the sources that were not explicitly detailed in the previous five trees.

### **I. Layer 1: Prior Probability and Co-infection Logic**
The system should adjust its initial hypothesis based on the known prevalence of co-infections in tropical regions.
*   **Rule - Malaria-Typhoid Co-infection Baseline:** IF (Malaria = Confirmed), THEN the system must assign a **3.9% to 6.7%** prior probability weight to a concurrent **Typhoid Fever** infection.
*   **Rule - Occupational Risk Filter:** IF (Occupation = High Exposure; e.g., street food vendor or sanitation worker), THEN assign an additional **$+10\%$** probability weight.

### **II. Layer 2: Differentiating Tie-Breakers (Exclusionary Weights)**
These rules provide "negative weights" to help the engine rule out Typhoid when symptoms overlap with Dengue.
*   **Rule - Retro-orbital Pain Exclusion:** IF (Headache = Present) AND (Pain Location = **Retro-orbital/Behind the eyes**), THEN weight for Typhoid = **0**, weight for Dengue = **Maximum (+5)**.
*   **Rule - Joint Pain Severity:** IF (Joint/Body Pain = **Intense "Breakbone"**), THEN prioritize Dengue; IF (Joint/Body Pain = **Mild/Aching**), THEN maintain Typhoid as a candidate.

### **III. Layer 3: Refined Temporal Staging (Week 3 Outcomes)**
While previous trees mentioned complications, this layer adds the specific multi-organ progression logic for the third week.
*   **Rule - Stage III Progression:** IF (Fever Duration = **15–21 Days**) AND (Clinical Condition = Worsening), THEN check for:
    *   **Intestinal Perforation** (Trigger: Acute guarding/rigidity).
    *   **Intestinal Bleeding** (Trigger: Melena).
    *   **Multi-Organ Dysfunction Syndrome (MODS)** (Trigger: Hypotension + Oliguria).

### **IV. Layer 4: Advanced Serological Reliability Metrics**
The engine should utilize these specific accuracy percentages to calculate its "Diagnostic Confidence Score."
*   **Rule - Single-Tube Widal Success Rate:** In clinical modeling, a single-tube Widal test correctly identifies **74%** of blood-culture positive cases when optimal cut-offs are utilized.
*   **Rule - Cross-Reactivity Filter:** IF (Widal = Positive), the system must query for other recent infections; titers may be elevated due to cross-reactions with **non-typhi *Salmonella* species**.

### **V. Layer 5: Clinical Linguistic Markers**
Specific physical descriptors can serve as low-level triggers for the inference engine.
*   **Rule - Linguistic Descriptor:** IF (Patient reports **"Bitterness in the mouth"** OR **"Sour lips"**), THEN increase the importance weight of the febrile illness module.
*   **Rule - Apparent vs. Real Severity:** IF (Dehydration = Absent) AND (Vomiting = Severe), THEN trigger a **Differential Safety Net** to rule out food poisoning or viral gastroenteritis instead of Typhoid.

### **VI. Layer 6: Shedding and Carrier Refinement**
*   **Rule - Shedder Classification:** IF (Stool Culture = Positive) AND (Duration = **Week 3 of illness**), THEN classify the patient as a **Confirmed Shedder** (Immediate precursor to chronic carrier logic).

(NO MORE RULES)