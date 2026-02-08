This logic tree incorporates detailed epidemiological, host-specific, microbiological, and operational data for cholera management that were absent from the previous triage-focused tree.

### I. Pre-Clinical Filter: Epidemiology and Host Risk Factors
This layer identifies high-risk individuals and environmental triggers before symptoms appear.

*   **Node 1: Environmental Risk Factors (Trigger Points)**
    *   **IF** Water temperature $\approx 30^{\circ}C$ AND Salinity $\approx 15\%$ AND $pH \approx 8.5 \rightarrow$ **High Bacterial Proliferation Risk**.
    *   **IF** Rainy/Monsoon season (in regions like the Bengal Delta) $\rightarrow$ **High Outbreak Probability**.
*   **Node 2: Host Biological Susceptibility**
    *   **Rule A (Blood Group):** IF Blood Group is O $\rightarrow$ **Increased risk of severe disease**.
    *   **Rule B (Gastric Acidity):** IF patient uses proton pump inhibitors/antacids OR has a history of gastrectomy $\rightarrow$ **Increased susceptibility (lowered infectious dose threshold)**.
    *   **Rule C (Micronutrients):** IF Retinol (Vitamin A) deficiency exists $\rightarrow$ **Increased clinical risk**.
*   **Node 3: Temporal Logic**
    *   **Incubation Rule:** Symptoms manifest between **12 hours and 5 days** post-ingestion.

### II. Advanced Clinical Logic: Variants and Pathophysiology
This layer identifies non-standard presentations and specific physiological excretion rates.

*   **Decision Node: Standard AWD vs. "Cholera Sicca"**
    *   **IF** Fluid accumulates in the intestinal lumen AND circulatory collapse/death occurs **WITHOUT diarrhea** $\rightarrow$ **Diagnosis: Cholera Sicca**.
*   **Pathophysiological Rate Monitoring (Excretion Logic)**
    *   **Adult Rule:** Monitor for stool output up to **1 Liter per hour**.
    *   **Pediatric Rule:** Monitor for excretion rates of **10–20 ml/kg/hr**.
*   **Bacteriological Lifecycle Logic**
    *   **Hyperinfectious Window:** Freshly shed stool is hyperinfectious for the first **24 hours** in the environment.

### III. Laboratory and Microbiological Intelligence
This layer refines the diagnosis using biotype, serotype, and specific testing sensitivities.

*   **Node 1: Serogroup and Biotype Classification**
    *   **IF** *V. cholerae* O1 $\rightarrow$ Classify as **Classical** (1st–6th pandemics) or **El Tor** (7th pandemic).
    *   **IF** *V. cholerae* O139 $\rightarrow$ Emerged 1992; restricted primarily to the Indian subcontinent.
*   **Node 2: Rapid Diagnostic Test (RDT) Selection**
    *   **IF** Outbreak involves both O1 and O139 $\rightarrow$ Use **Crystal VC** (97% sensitivity).
    *   **IF** Only O1 is predominant $\rightarrow$ Use **Cholkit** (higher specificity at 90%).
*   **Node 3: Differential Weighting (Tie-Breakers)**
    *   **IF** Fever is continuous ($104^{\circ}F$) AND joint pain is severe ("breakbone") $\rightarrow$ **Weight for Dengue**.
    *   **IF** Fever is cyclical with chills/sweats AND anemia is present $\rightarrow$ **Weight for Malaria**.

### IV. Operational and Logistics Logic (Facility Management)
This layer governs the engineering and maintenance of a Cholera Treatment Centre (CTC).

*   **Rule 1: Zonation Logic**
    *   **Green Zone:** Administrative, stores, and kitchen; casual clothes allowed.
    *   **Red Zone:** Treatment and recovery; mandatory uniforms, boots, and gloves.
    *   **Buffer Zone:** Double-fence strip separating Red and Green zones to prevent vector movement.
*   **Rule 2: Specific Disinfection Protocols**
    *   **0.05% Chlorine:** Handwashing, dishes, and laundry rinsing.
    *   **0.2% Chlorine:** Floors (3 times daily), beds, and footbaths.
    *   **2% Chlorine:** Feces/vomit (pour 1/2 cup into bucket when 2/3 full) and **Dead Body management**.
*   **Rule 3: Mortality Protocol (Dead Body Management)**
    *   **Action A:** Plug mouth and anus with cotton soaked in **2% chlorine**.
    *   **Action B:** Bandage head so the mouth remains shut.
    *   **Action C:** Burial at least **50m** from water sources and **1.5m** deep.

### V. Prevention and Global Strategy Logic
This layer guides long-term immunization and elimination targets.

*   **Vaccine Selection Matrix**
    *   **IF** Mass campaign in endemic area $\rightarrow$ Use **Shanchol** or **Euvichol** (two doses 14 days apart).
    *   **IF** Travel to endemic zone (Adults) $\rightarrow$ Use **Vaxchora** (live attenuated, single dose).
*   **Herd Immunity Logic**
    *   **Calculation:** 50% OCV coverage predicts a **93% prevention rate** of total infections.
*   **Elimination Strategy (Roadmap 2030)**
    *   **Target:** 90% mortality reduction in **47 endemic countries**.