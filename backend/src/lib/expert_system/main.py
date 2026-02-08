"""
Medical Diagnostic Expert System - User Interface

Interactive console interface for the medical diagnosis expert system.
Allows users to input symptoms and receive diagnostic suggestions.
"""

from .diagnosis_engine import (
    MedicalDiagnosisEngine, run_diagnosis
)
from .facts import (
    Patient, Symptom, VitalSign, LabResult, DehydrationSign
)


def get_yes_no(prompt: str) -> bool:
    """Get yes/no input from user."""
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")


def get_choice(prompt: str, options: list) -> str:
    """Get choice from numbered options."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    while True:
        try:
            choice = int(input("Enter number: ").strip())
            if 1 <= choice <= len(options):
                return options[choice - 1]
        except ValueError:
            pass
        print(f"Please enter a number between 1 and {len(options)}")


def collect_patient_info() -> dict:
    """Collect patient demographics and history."""
    print("\n" + "="*50)
    print("PATIENT INFORMATION")
    print("="*50)
    
    patient = {}
    
    # Age
    while True:
        try:
            age = int(input("Patient age (years): ").strip())
            patient['age'] = age
            patient['is_child'] = age < 18
            break
        except ValueError:
            print("Please enter a valid number")
    
    # Pregnancy (if applicable)
    if age >= 12 and age <= 50:
        if get_yes_no("Is patient female?"):
            patient['is_pregnant'] = get_yes_no("Is patient pregnant?")
    
    # Travel/exposure history
    print("\n-- Exposure History --")
    patient['travel_endemic_area'] = get_yes_no("Recent travel to malaria/cholera/typhoid endemic area (within 30 days)?")
    patient['endemic_resident'] = get_yes_no("Does patient live in an endemic area?")
    patient['unsafe_water'] = get_yes_no("Consumed unboiled/untreated water recently?")
    patient['street_food'] = get_yes_no("Consumed raw street food recently?")
    patient['household_contact'] = get_yes_no("Contact with someone who has confirmed cholera/typhoid/malaria?")
    
    return patient


def collect_symptoms() -> list:
    """Collect symptom information."""
    print("\n" + "="*50)
    print("SYMPTOM ASSESSMENT")
    print("="*50)
    
    symptoms = []
    
    # --- FEVER ---
    print("\n-- Fever --")
    if get_yes_no("Does patient have fever?"):
        fever = {'name': 'fever', 'present': True}
        
        # Fever pattern
        pattern = get_choice(
            "What is the fever pattern?",
            ['continuous', 'cyclical (comes and goes)', 'stepladder (gradually increasing)', 'irregular', 'unknown']
        )
        if 'cyclical' in pattern:
            fever['pattern'] = 'cyclical'
        elif 'stepladder' in pattern:
            fever['pattern'] = 'stepladder'
        
        # Duration
        try:
            duration = input("Duration of fever in days (press Enter if unknown): ").strip()
            if duration:
                fever['duration_days'] = int(duration)
        except ValueError:
            pass
        
        symptoms.append(fever)
        
        # Check relative bradycardia (typhoid sign)
        if get_yes_no("Is heart rate slower than expected for the fever level (relative bradycardia)?"):
            symptoms.append({'name': 'relative_bradycardia', 'present': True})
    
    # --- CHILLS / SWEATING (Malaria paroxysm) ---
    print("\n-- Chills & Sweating --")
    if get_yes_no("Does patient have chills/rigors?"):
        symptoms.append({'name': 'chills', 'present': True})
    
    if get_yes_no("Does patient have profuse sweating episodes?"):
        symptoms.append({'name': 'sweating', 'present': True})
    
    # --- GASTROINTESTINAL ---
    print("\n-- Gastrointestinal Symptoms --")
    
    if get_yes_no("Does patient have diarrhea?"):
        diarrhea = {'name': 'diarrhea', 'present': True}
        
        # Severity
        severity = get_choice("Diarrhea severity:", ['mild (1-3 stools/day)', 'moderate (4-6 stools/day)', 'severe (>6 stools/day)'])
        if 'mild' in severity:
            diarrhea['severity'] = 'mild'
        elif 'moderate' in severity:
            diarrhea['severity'] = 'moderate'
        else:
            diarrhea['severity'] = 'severe'
        
        # Appearance (critical for cholera)
        appearance = get_choice(
            "Stool appearance:",
            ['rice-water (pale/milky with mucus flecks)', 'watery (clear/yellow)', 'bloody', 'mucoid', 'normal/formed']
        )
        if 'rice-water' in appearance:
            diarrhea['description'] = 'rice_water'
        elif 'watery' in appearance:
            diarrhea['description'] = 'watery'
        elif 'bloody' in appearance:
            diarrhea['description'] = 'bloody'
        
        symptoms.append(diarrhea)
    
    if get_yes_no("Does patient have vomiting?"):
        symptoms.append({'name': 'vomiting', 'present': True})
    
    if get_yes_no("Does patient have abdominal pain?"):
        pain = {'name': 'abdominal_pain', 'present': True}
        if get_yes_no("Is the abdominal pain severe?"):
            symptoms.append({'name': 'severe_abdominal_pain', 'present': True})
        symptoms.append(pain)
    
    if get_yes_no("Does patient have constipation?"):
        symptoms.append({'name': 'constipation', 'present': True})
    
    # --- TASTE (Malaria specific) ---
    print("\n-- Oral Symptoms --")
    if get_yes_no("Does patient report bitter taste in mouth?"):
        symptoms.append({'name': 'bitter_taste', 'present': True})
    
    # --- NEUROLOGICAL ---
    print("\n-- Neurological Symptoms --")
    if get_yes_no("Does patient have headache?"):
        symptoms.append({'name': 'headache', 'present': True})
    
    if get_yes_no("Does patient have altered consciousness (confusion, drowsiness)?"):
        symptoms.append({'name': 'altered_consciousness', 'present': True})
    
    if get_yes_no("Has patient had convulsions/seizures?"):
        symptoms.append({'name': 'convulsions', 'present': True})
    
    # --- MUSCULOSKELETAL ---
    print("\n-- Other Symptoms --")
    if get_yes_no("Does patient have body aches/muscle pain?"):
        symptoms.append({'name': 'body_aches', 'present': True})
    
    # --- SKIN ---
    if get_yes_no("Does patient have rose-colored spots on trunk (small pink macules)?"):
        symptoms.append({'name': 'rose_spots', 'present': True})
    
    # --- URINE ---
    if get_yes_no("Is patient's urine dark/cola-colored/bloody?"):
        urine = {'name': 'dark_urine', 'present': True}
        color = get_choice("Urine color:", ['dark yellow', 'brown/cola', 'red/bloody', 'black'])
        urine['description'] = color.split('/')[0]
        symptoms.append(urine)
    
    # --- DEHYDRATION ---
    print("\n-- Dehydration Assessment --")
    if get_yes_no("Does patient show signs of dehydration?"):
        dehydration = {'name': 'dehydration', 'present': True}
        severity = get_choice(
            "Dehydration severity:",
            ['mild (thirsty, slightly dry mouth)', 
             'moderate (very thirsty, dry mouth, decreased urine)',
             'severe (lethargic, sunken eyes, very dry, minimal urine)']
        )
        if 'mild' in severity:
            dehydration['severity'] = 'mild'
        elif 'moderate' in severity:
            dehydration['severity'] = 'moderate'
        else:
            dehydration['severity'] = 'severe'
        symptoms.append(dehydration)
    
    # --- ANEMIA ---
    if get_yes_no("Does patient appear pale/anemic?"):
        anemia = {'name': 'anemia', 'present': True}
        if get_yes_no("Is the pallor severe (very pale conjunctiva/palms)?"):
            anemia['severity'] = 'severe'
        symptoms.append(anemia)
    
    return symptoms


def collect_lab_results() -> list:
    """Collect available laboratory results."""
    print("\n" + "="*50)
    print("LABORATORY RESULTS (if available)")
    print("="*50)
    
    labs = []
    
    if not get_yes_no("Do you have any laboratory results?"):
        return labs
    
    # Malaria tests
    print("\n-- Malaria Tests --")
    if get_yes_no("Blood smear performed?"):
        result = get_choice("Blood smear result:", ['positive', 'negative', 'pending'])
        labs.append({'test': 'blood_smear', 'result': result})
    
    if get_yes_no("Malaria RDT performed?"):
        result = get_choice("Malaria RDT result:", ['positive', 'negative', 'pending'])
        labs.append({'test': 'rdt_malaria', 'result': result})
    
    # Cholera tests
    print("\n-- Cholera Tests --")
    if get_yes_no("Stool culture performed?"):
        result = get_choice("Stool culture result:", ['positive for Vibrio cholerae', 'negative', 'pending'])
        if 'positive' in result:
            labs.append({'test': 'stool_culture', 'result': 'positive', 'details': 'vibrio cholerae'})
        else:
            labs.append({'test': 'stool_culture', 'result': result.split()[0]})
    
    if get_yes_no("Cholera RDT performed?"):
        result = get_choice("Cholera RDT result:", ['positive', 'negative', 'pending'])
        labs.append({'test': 'rdt_cholera', 'result': result})
    
    # Typhoid tests
    print("\n-- Typhoid Tests --")
    if get_yes_no("Blood culture performed?"):
        result = get_choice("Blood culture result:", ['positive for Salmonella typhi', 'negative', 'pending'])
        if 'positive' in result:
            labs.append({'test': 'blood_culture', 'result': 'positive', 'details': 'salmonella typhi'})
        else:
            labs.append({'test': 'blood_culture', 'result': result.split()[0]})
    
    if get_yes_no("Typhidot RDT performed?"):
        result = get_choice("Typhidot result:", ['positive', 'negative', 'pending'])
        labs.append({'test': 'typhidot', 'result': result})
    
    if get_yes_no("Widal test performed?"):
        result = get_choice("Widal result:", ['positive (O-agglutinin ≥1:200)', 'positive (lower titer)', 'negative'])
        if '≥1:200' in result:
            labs.append({'test': 'widal', 'result': 'positive', 'details': '1:200'})
        elif 'positive' in result:
            labs.append({'test': 'widal', 'result': 'positive', 'details': 'low_titer'})
        else:
            labs.append({'test': 'widal', 'result': 'negative'})
    
    return labs


def display_results(results: dict):
    """Display diagnosis results."""
    print("\n" + "="*60)
    print("DIAGNOSTIC ASSESSMENT RESULTS")
    print("="*60)
    
    diagnoses = results.get('diagnoses', [])
    recommendations = results.get('recommendations', [])
    
    if not diagnoses:
        print("\n⚠ No diagnosis could be determined from the provided information.")
        print("Recommendation: Conduct further clinical assessment and laboratory tests.")
        return
    
    # Group diagnoses by confidence
    confirmed = [d for d in diagnoses if d.get('confidence') == 'confirmed']
    confident = [d for d in diagnoses if d.get('confidence') == 'confident']
    suspect = [d for d in diagnoses if d.get('confidence') == 'suspect']
    uncertain = [d for d in diagnoses if d.get('confidence') == 'uncertain']
    
    # Display confirmed diagnoses
    if confirmed:
        print("\n✓ CONFIRMED DIAGNOSIS:")
        for d in confirmed:
            print(f"  • {d['disease'].upper()}")
            print(f"    Reason: {d['reason']}")
    
    # Display confident diagnoses
    if confident:
        print("\n✓ LIKELY DIAGNOSIS (High Confidence):")
        for d in confident:
            print(f"  • {d['disease'].upper()}")
            print(f"    Reason: {d['reason']}")
    
    # Display suspect diagnoses
    if suspect:
        print("\n? SUSPECTED DIAGNOSIS (Needs Confirmation):")
        for d in suspect:
            print(f"  • {d['disease'].upper()}")
            print(f"    Reason: {d['reason']}")
            if d.get('recommendation'):
                print(f"    → {d['recommendation']}")
    
    # Display uncertain
    if uncertain and not (confirmed or confident):
        print("\n⚠ UNCERTAIN - Insufficient findings for confident diagnosis")
        for d in uncertain:
            print(f"  Note: {d['reason']}")
            if d.get('recommendation'):
                print(f"  → {d['recommendation']}")
    
    # Display urgent recommendations
    urgent_recs = [r for r in recommendations if r.get('type') == 'urgent']
    if urgent_recs:
        print("\n" + "!"*60)
        print("⚠⚠⚠ URGENT ACTIONS REQUIRED ⚠⚠⚠")
        print("!"*60)
        for r in urgent_recs:
            print(f"  {r['action']}")
    
    # Display differential notes
    diff_recs = [r for r in recommendations if r.get('type') == 'differential']
    if diff_recs:
        print("\n📋 Differential Diagnosis Notes:")
        for r in diff_recs:
            print(f"  • {r['note']}")
    
    print("\n" + "="*60)
    print("DISCLAIMER: This is a decision support tool only.")
    print("Clinical judgment and laboratory confirmation are required.")
    print("="*60)


def run_interactive():
    """Run the interactive diagnosis session."""
    print("\n" + "#"*60)
    print("#" + " "*58 + "#")
    print("#    MEDICAL DIAGNOSTIC EXPERT SYSTEM    #")
    print("#    Cholera | Malaria | Typhoid Fever   #")
    print("#" + " "*58 + "#")
    print("#"*60)
    
    print("\nThis system will help assess symptoms for:")
    print("  • Cholera")
    print("  • Malaria")
    print("  • Typhoid Fever")
    print("\nPlease answer the following questions about the patient.")
    
    # Collect information
    patient_info = collect_patient_info()
    symptoms = collect_symptoms()
    lab_results = collect_lab_results()
    
    # Run diagnosis
    print("\n\n⏳ Analyzing symptoms...")
    results = run_diagnosis(
        symptoms=symptoms,
        patient_info=patient_info,
        lab_results=lab_results
    )
    
    # Display results
    display_results(results)


def run_quick_test():
    """Run a quick test with predefined symptoms."""
    print("\n--- Quick Test Mode ---")
    
    # Test case: Classic malaria paroxysm
    print("\nTest Case 1: Cyclical fever + chills + sweating + endemic travel")
    results = run_diagnosis(
        symptoms=[
            {'name': 'fever', 'present': True, 'pattern': 'cyclical'},
            {'name': 'chills', 'present': True},
            {'name': 'sweating', 'present': True},
            {'name': 'headache', 'present': True}
        ],
        patient_info={'travel_endemic_area': True, 'age': 30}
    )
    display_results(results)
    
    print("\n" + "-"*60)
    
    # Test case: Cholera
    print("\nTest Case 2: Rice-water diarrhea + severe dehydration")
    results = run_diagnosis(
        symptoms=[
            {'name': 'diarrhea', 'present': True, 'description': 'rice_water', 'severity': 'severe'},
            {'name': 'dehydration', 'present': True, 'severity': 'severe'},
            {'name': 'vomiting', 'present': True}
        ],
        patient_info={'endemic_resident': True, 'unsafe_water': True, 'age': 25}
    )
    display_results(results)
    
    print("\n" + "-"*60)
    
    # Test case: Typhoid
    print("\nTest Case 3: Step-ladder fever + relative bradycardia + rose spots")
    results = run_diagnosis(
        symptoms=[
            {'name': 'fever', 'present': True, 'pattern': 'stepladder', 'duration_days': 7},
            {'name': 'relative_bradycardia', 'present': True},
            {'name': 'rose_spots', 'present': True},
            {'name': 'abdominal_pain', 'present': True}
        ],
        patient_info={'street_food': True, 'unsafe_water': True, 'age': 35}
    )
    display_results(results)
    
    print("\n" + "-"*60)
    
    # Test case: Uncertain
    print("\nTest Case 4: Non-specific fever only")
    results = run_diagnosis(
        symptoms=[
            {'name': 'fever', 'present': True},
            {'name': 'headache', 'present': True}
        ],
        patient_info={'age': 28}
    )
    display_results(results)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_quick_test()
    else:
        try:
            run_interactive()
        except KeyboardInterrupt:
            print("\n\nSession terminated by user.")
