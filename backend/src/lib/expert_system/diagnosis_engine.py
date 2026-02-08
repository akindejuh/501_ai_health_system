"""
Medical Diagnostic Expert System Engine.

This module contains the main KnowledgeEngine with diagnostic rules
for cholera, malaria, and typhoid fever based on clinical guidelines.
"""

from experta import (
    KnowledgeEngine, Rule, DefFacts, Fact,
    AND, OR, NOT, AS, MATCH,
    L, W, P
)

from .facts import (
    Patient, Symptom, VitalSign, DehydrationSign,
    LabResult, DehydrationLevel, SeverityIndicator,
    Diagnosis, TreatmentPlan
)


class MedicalDiagnosisEngine(KnowledgeEngine):
    """
    Expert system for diagnosing cholera, malaria, and typhoid fever.
    
    Usage:
        engine = MedicalDiagnosisEngine()
        engine.reset()
        engine.declare(Symptom(name='fever', present=True, pattern='cyclical'))
        engine.declare(Symptom(name='chills', present=True))
        engine.run()
        print(engine.get_diagnoses())
    """
    
    def __init__(self):
        super().__init__()
        self.diagnoses = []
        self.recommendations = []
    
    @DefFacts()
    def initial_facts(self):
        """Declare initial state."""
        yield Fact(diagnosis_complete=False)
    
    def get_diagnoses(self):
        """Return all diagnoses made by the engine."""
        return self.diagnoses
    
    def get_recommendations(self):
        """Return all recommendations."""
        return self.recommendations

    # =========================================================================
    # DEHYDRATION CLASSIFICATION (WHO Protocol)
    # =========================================================================
    
    @Rule(
        OR(
            DehydrationSign(sign='mental_state', finding='lethargic'),
            DehydrationSign(sign='mental_state', finding='unconscious')
        ),
        DehydrationSign(sign='eyes', finding='sunken'),
        DehydrationSign(sign='skin_pinch', finding=P(lambda x: x in ['very_slow', '>2_seconds']))
    )
    def severe_dehydration(self):
        """Classify severe dehydration - Plan C."""
        self.declare(DehydrationLevel(level='severe', treatment_plan='C'))
        self.declare(SeverityIndicator(
            indicator='severe_dehydration',
            action='IV_rehydration_urgent'
        ))
    
    @Rule(
        OR(
            DehydrationSign(sign='mental_state', finding='restless'),
            DehydrationSign(sign='mental_state', finding='irritable')
        ),
        DehydrationSign(sign='thirst', finding='drinks_eagerly'),
        DehydrationSign(sign='skin_pinch', finding='slow'),
        NOT(DehydrationLevel(level='severe'))
    )
    def some_dehydration(self):
        """Classify some dehydration - Plan B."""
        self.declare(DehydrationLevel(level='some', treatment_plan='B'))
    
    @Rule(
        DehydrationSign(sign='mental_state', finding='alert'),
        DehydrationSign(sign='thirst', finding='drinks_normally'),
        DehydrationSign(sign='skin_pinch', finding='normal'),
        NOT(DehydrationLevel(level=W()))
    )
    def no_dehydration(self):
        """Classify no dehydration - Plan A."""
        self.declare(DehydrationLevel(level='none', treatment_plan='A'))

    # =========================================================================
    # CHOLERA RULES
    # =========================================================================
    
    @Rule(
        Symptom(name='diarrhea', present=True, description='rice_water'),
        Symptom(name='dehydration', present=True, severity='severe'),
        salience=90
    )
    def cholera_confident_ricewater(self):
        """Rice-water stool + severe dehydration = pathognomonic for cholera."""
        diag = Diagnosis(
            disease='cholera',
            confidence='confident',
            reason='rice-water stool with severe dehydration (pathognomonic)',
            severity='severe'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'cholera',
            'confidence': 'confident',
            'reason': 'Rice-water stool with severe dehydration is pathognomonic for cholera'
        })
    
    @Rule(
        Symptom(name='diarrhea', present=True, description='rice_water'),
        NOT(Symptom(name='dehydration', present=True, severity='severe')),
        salience=85
    )
    def cholera_confident_ricewater_only(self):
        """Rice-water stool alone is highly specific for cholera."""
        diag = Diagnosis(
            disease='cholera',
            confidence='confident',
            reason='rice-water stool (pathognomonic appearance)',
            severity='uncomplicated'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'cholera',
            'confidence': 'confident',
            'reason': 'Rice-water stool is pathognomonic for cholera'
        })
    
    @Rule(
        Symptom(name='diarrhea', present=True, severity=P(lambda x: x in ['moderate', 'severe'])),
        Symptom(name='diarrhea', present=True, description=P(lambda x: x in ['watery', 'acute_watery', None])),
        Symptom(name='vomiting', present=True),
        OR(
            Patient(endemic_resident=True),
            Patient(unsafe_water=True)
        ),
        NOT(Diagnosis(disease='cholera')),
        salience=70
    )
    def cholera_suspect_awd_endemic(self):
        """Acute watery diarrhea + vomiting + endemic exposure = suspect cholera."""
        diag = Diagnosis(
            disease='cholera',
            confidence='suspect',
            reason='acute watery diarrhea with vomiting in endemic area',
            recommendation='Confirm with stool culture or RDT (Crystal VC)'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'cholera',
            'confidence': 'suspect',
            'reason': 'Acute watery diarrhea with vomiting in endemic area/unsafe water exposure'
        })
    
    @Rule(
        LabResult(test='stool_culture', result='positive', details=P(lambda x: 'vibrio' in x.lower() if x else False)),
        salience=100
    )
    def cholera_confirmed_culture(self):
        """Positive stool culture for V. cholerae = confirmed."""
        diag = Diagnosis(
            disease='cholera',
            confidence='confirmed',
            reason='Vibrio cholerae isolated on stool culture'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'cholera',
            'confidence': 'confirmed',
            'reason': 'Laboratory confirmed: V. cholerae isolated on stool culture'
        })
    
    @Rule(
        LabResult(test='rdt_cholera', result='positive'),
        salience=95
    )
    def cholera_confirmed_rdt(self):
        """Positive cholera RDT."""
        if not any(d['disease'] == 'cholera' and d['confidence'] == 'confirmed' for d in self.diagnoses):
            diag = Diagnosis(
                disease='cholera',
                confidence='confident',
                reason='Positive cholera rapid diagnostic test'
            )
            self.declare(diag)
            self.diagnoses.append({
                'disease': 'cholera',
                'confidence': 'confident',
                'reason': 'Positive cholera RDT'
            })

    # =========================================================================
    # MALARIA RULES
    # =========================================================================
    
    @Rule(
        Symptom(name='fever', present=True, pattern='cyclical'),
        Symptom(name='chills', present=True),
        Symptom(name='sweating', present=True),
        salience=90
    )
    def malaria_confident_paroxysm(self):
        """Classic malarial paroxysm: cyclical fever + chills + sweating."""
        diag = Diagnosis(
            disease='malaria',
            confidence='confident',
            reason='classic malarial paroxysm (cyclical fever, chills, sweating)'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'malaria',
            'confidence': 'confident',
            'reason': 'Classic malarial paroxysm: cyclical fever with chills followed by sweating'
        })
    
    @Rule(
        Symptom(name='fever', present=True),
        Symptom(name='bitter_taste', present=True),
        Patient(travel_endemic_area=True),
        NOT(Diagnosis(disease='malaria')),
        salience=80
    )
    def malaria_confident_bitter_taste(self):
        """Fever + bitter taste + endemic exposure - high diagnostic weight."""
        diag = Diagnosis(
            disease='malaria',
            confidence='confident',
            reason='fever with bitter taste in mouth (highly suggestive) + endemic exposure'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'malaria',
            'confidence': 'confident',
            'reason': 'Fever with bitter taste in mouth is highly suggestive of malaria'
        })
    
    @Rule(
        Symptom(name='fever', present=True),
        OR(
            Symptom(name='chills', present=True),
            Symptom(name='headache', present=True),
            Symptom(name='body_aches', present=True)
        ),
        Patient(travel_endemic_area=True),
        NOT(Diagnosis(disease='malaria')),
        salience=65
    )
    def malaria_suspect_endemic_fever(self):
        """Fever with nonspecific symptoms + endemic area = suspect malaria."""
        diag = Diagnosis(
            disease='malaria',
            confidence='suspect',
            reason='fever with nonspecific symptoms in endemic area',
            recommendation='Confirm with blood smear or malaria RDT'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'malaria',
            'confidence': 'suspect',
            'reason': 'Fever with nonspecific symptoms in traveler from endemic area'
        })
    
    @Rule(
        LabResult(test='blood_smear', result='positive'),
        salience=100
    )
    def malaria_confirmed_smear(self):
        """Positive blood smear = confirmed malaria."""
        diag = Diagnosis(
            disease='malaria',
            confidence='confirmed',
            reason='Plasmodium parasites seen on blood smear'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'malaria',
            'confidence': 'confirmed',
            'reason': 'Laboratory confirmed: Plasmodium parasites on blood smear'
        })
    
    @Rule(
        LabResult(test='rdt_malaria', result='positive'),
        NOT(LabResult(test='blood_smear')),
        salience=95
    )
    def malaria_confirmed_rdt(self):
        """Positive malaria RDT."""
        diag = Diagnosis(
            disease='malaria',
            confidence='confident',
            reason='Positive malaria rapid diagnostic test'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'malaria',
            'confidence': 'confident',
            'reason': 'Positive malaria RDT'
        })
    
    # Severe malaria indicators
    @Rule(
        OR(
            Diagnosis(disease='malaria'),
            Symptom(name='fever', present=True)
        ),
        OR(
            Symptom(name='altered_consciousness', present=True),
            Symptom(name='convulsions', present=True),
            Symptom(name='prostration', present=True)
        ),
        salience=100
    )
    def severe_malaria_cerebral(self):
        """Cerebral malaria indicators - urgent referral."""
        self.declare(SeverityIndicator(
            indicator='cerebral_malaria',
            disease='malaria',
            action='urgent_referral_IV_artesunate'
        ))
        self.recommendations.append({
            'type': 'urgent',
            'action': 'URGENT: Possible cerebral malaria. Immediate referral for IV Artesunate.'
        })
    
    @Rule(
        OR(
            Diagnosis(disease='malaria'),
            Symptom(name='fever', present=True)
        ),
        Symptom(name='dark_urine', present=True, description=P(lambda x: x in ['black', 'cola', 'red'] if x else False)),
        salience=95
    )
    def severe_malaria_blackwater(self):
        """Blackwater fever - hemoglobinuria."""
        self.declare(SeverityIndicator(
            indicator='blackwater_fever',
            disease='malaria',
            action='urgent_referral'
        ))
        self.recommendations.append({
            'type': 'urgent',
            'action': 'URGENT: Possible blackwater fever (hemoglobinuria). Immediate referral.'
        })

    # =========================================================================
    # TYPHOID FEVER RULES
    # =========================================================================
    
    @Rule(
        Symptom(name='fever', present=True, pattern='stepladder'),
        Symptom(name='relative_bradycardia', present=True),
        NOT(Diagnosis(disease='typhoid')),
        salience=90
    )
    def typhoid_confident_stepladder_bradycardia(self):
        """Step-ladder fever + relative bradycardia = pathognomonic for typhoid."""
        diag = Diagnosis(
            disease='typhoid',
            confidence='confident',
            reason='step-ladder fever pattern with relative bradycardia (pathognomonic)'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'typhoid',
            'confidence': 'confident',
            'reason': 'Step-ladder fever with relative bradycardia is pathognomonic for typhoid'
        })
    
    @Rule(
        Symptom(name='rose_spots', present=True),
        Symptom(name='fever', present=True),
        NOT(Diagnosis(disease='typhoid')),
        salience=90
    )
    def typhoid_confident_rose_spots(self):
        """Rose spots + fever = highly specific for typhoid."""
        diag = Diagnosis(
            disease='typhoid',
            confidence='confident',
            reason='rose spots on trunk with fever (highly specific)'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'typhoid',
            'confidence': 'confident',
            'reason': 'Rose spots (pink macules on trunk) are highly specific for typhoid fever'
        })
    
    @Rule(
        Symptom(name='fever', present=True, duration_days=P(lambda x: x and x >= 5)),
        Symptom(name='abdominal_pain', present=True),
        OR(
            Symptom(name='constipation', present=True),
            Symptom(name='diarrhea', present=True)
        ),
        NOT(Diagnosis(disease='typhoid')),
        salience=70
    )
    def typhoid_suspect_prolonged_fever(self):
        """Prolonged fever (>=5 days) + abdominal symptoms = suspect typhoid."""
        diag = Diagnosis(
            disease='typhoid',
            confidence='suspect',
            reason='prolonged fever with abdominal pain and altered bowel habits',
            recommendation='Confirm with blood culture (gold standard) or Typhidot RDT'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'typhoid',
            'confidence': 'suspect',
            'reason': 'Prolonged fever (>=5 days) with abdominal pain'
        })
    
    @Rule(
        Symptom(name='fever', present=True),
        Symptom(name='headache', present=True),
        OR(
            Patient(unsafe_water=True),
            Patient(street_food=True)
        ),
        NOT(Diagnosis(disease='typhoid')),
        NOT(Diagnosis(disease='malaria')),
        salience=50
    )
    def typhoid_suspect_exposure(self):
        """Fever + headache + contaminated food/water exposure."""
        diag = Diagnosis(
            disease='typhoid',
            confidence='suspect',
            reason='fever with headache and contaminated food/water exposure',
            recommendation='Consider blood culture or Widal test'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'typhoid',
            'confidence': 'suspect',
            'reason': 'Fever with headache and history of unsafe water/street food consumption'
        })
    
    @Rule(
        LabResult(test='blood_culture', result='positive', details=P(lambda x: 'salmonella' in x.lower() if x else False)),
        salience=100
    )
    def typhoid_confirmed_culture(self):
        """Positive blood culture for S. typhi = confirmed."""
        diag = Diagnosis(
            disease='typhoid',
            confidence='confirmed',
            reason='Salmonella typhi isolated on blood culture'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'typhoid',
            'confidence': 'confirmed',
            'reason': 'Laboratory confirmed: S. typhi isolated on blood culture'
        })
    
    @Rule(
        LabResult(test='typhidot', result='positive'),
        Symptom(name='fever', present=True),
        salience=85
    )
    def typhoid_confident_typhidot(self):
        """Positive Typhidot with fever."""
        if not any(d['disease'] == 'typhoid' and d['confidence'] in ['confirmed', 'confident'] for d in self.diagnoses):
            diag = Diagnosis(
                disease='typhoid',
                confidence='confident',
                reason='Positive Typhidot RDT with fever'
            )
            self.declare(diag)
            self.diagnoses.append({
                'disease': 'typhoid',
                'confidence': 'confident',
                'reason': 'Positive Typhidot RDT (95-97% sensitivity)'
            })
    
    @Rule(
        LabResult(test='widal', result='positive', details=P(lambda x: '1:200' in x or '1:320' in x or '1:400' in x if x else False)),
        Symptom(name='fever', present=True),
        NOT(Diagnosis(disease='typhoid', confidence='confirmed')),
        salience=75
    )
    def typhoid_suspect_widal(self):
        """Positive Widal with significant titer."""
        if not any(d['disease'] == 'typhoid' and d['confidence'] == 'confirmed' for d in self.diagnoses):
            diag = Diagnosis(
                disease='typhoid',
                confidence='suspect',
                reason='Widal test positive with significant O-agglutinin titer',
                recommendation='Consider blood culture for confirmation (14% false positive rate with Widal)'
            )
            self.declare(diag)
            self.diagnoses.append({
                'disease': 'typhoid',
                'confidence': 'suspect',
                'reason': 'Widal positive (note: 14% false positive rate, may cross-react with malaria)'
            })
    
    # Severe typhoid / complications
    @Rule(
        Diagnosis(disease='typhoid'),
        OR(
            Symptom(name='melena', present=True),
            Symptom(name='bloody_stool', present=True),
            Symptom(name='severe_abdominal_pain', present=True)
        ),
        salience=100
    )
    def typhoid_complication_hemorrhage(self):
        """Intestinal hemorrhage or perforation risk."""
        self.declare(SeverityIndicator(
            indicator='intestinal_complication',
            disease='typhoid',
            action='urgent_surgical_referral'
        ))
        self.recommendations.append({
            'type': 'urgent',
            'action': 'URGENT: Possible intestinal hemorrhage/perforation. Immediate surgical referral.'
        })

    # =========================================================================
    # UNCERTAINTY / NO CLEAR DIAGNOSIS
    # =========================================================================
    
    @Rule(
        Symptom(name='fever', present=True),
        NOT(Diagnosis(disease=W())),
        salience=10
    )
    def fever_uncertain(self):
        """Fever present but no specific diagnosis made."""
        diag = Diagnosis(
            disease='uncertain',
            confidence='uncertain',
            reason='fever present but insufficient specific findings',
            recommendation='Recommend: blood smear, malaria RDT, blood culture, and clinical reassessment'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'uncertain',
            'confidence': 'uncertain',
            'reason': 'Fever present but symptoms do not clearly match cholera, malaria, or typhoid patterns',
            'recommendation': 'Blood smear, malaria RDT, blood culture recommended. Reassess in 24 hours.'
        })
    
    @Rule(
        Symptom(name='diarrhea', present=True),
        NOT(Symptom(name='diarrhea', description='rice_water')),
        NOT(Diagnosis(disease=W())),
        salience=10
    )
    def diarrhea_uncertain(self):
        """Diarrhea without rice-water appearance and no other diagnosis."""
        diag = Diagnosis(
            disease='uncertain',
            confidence='uncertain',
            reason='diarrhea present but not cholera-specific (no rice-water stool)',
            recommendation='Consider stool culture, assess for other causes (viral, bacterial gastroenteritis)'
        )
        self.declare(diag)
        self.diagnoses.append({
            'disease': 'uncertain',
            'confidence': 'uncertain',
            'reason': 'Diarrhea present but does not have cholera-specific features',
            'recommendation': 'Stool culture recommended. Consider other causes of gastroenteritis.'
        })

    # =========================================================================
    # DIFFERENTIAL DIAGNOSIS TIE-BREAKERS
    # =========================================================================
    
    @Rule(
        Symptom(name='fever', present=True, pattern='cyclical'),
        Symptom(name='constipation', present=True),
        salience=75
    )
    def differential_favor_typhoid_over_malaria(self):
        """Constipation with fever favors typhoid over malaria."""
        self.recommendations.append({
            'type': 'differential',
            'note': 'Constipation with fever favors typhoid over malaria'
        })
    
    @Rule(
        Symptom(name='fever', present=True),
        Symptom(name='anemia', present=True, severity='severe'),
        salience=75
    )
    def differential_favor_malaria_anemia(self):
        """Severe anemia with fever favors malaria."""
        self.recommendations.append({
            'type': 'differential',
            'note': 'Severe anemia with fever strongly favors malaria'
        })


def run_diagnosis(symptoms: list, patient_info: dict = None, lab_results: list = None,
                  dehydration_signs: list = None) -> dict:
    """
    Convenience function to run the diagnostic engine.
    
    Args:
        symptoms: List of dicts with symptom info
            e.g., [{'name': 'fever', 'present': True, 'pattern': 'cyclical'}]
        patient_info: Dict with patient demographics
            e.g., {'travel_endemic_area': True, 'age': 25}
        lab_results: List of dicts with lab results
            e.g., [{'test': 'rdt_malaria', 'result': 'positive'}]
        dehydration_signs: List of dicts with dehydration assessment
            e.g., [{'sign': 'skin_pinch', 'finding': 'slow'}]
    
    Returns:
        Dict with diagnoses and recommendations
    """
    engine = MedicalDiagnosisEngine()
    engine.reset()
    
    # Declare patient info
    if patient_info:
        engine.declare(Patient(**patient_info))
    
    # Declare symptoms
    for symptom in symptoms:
        engine.declare(Symptom(**symptom))
    
    # Declare lab results
    if lab_results:
        for lab in lab_results:
            engine.declare(LabResult(**lab))
    
    # Declare dehydration signs
    if dehydration_signs:
        for sign in dehydration_signs:
            engine.declare(DehydrationSign(**sign))
    
    # Run the inference engine
    engine.run()
    
    return {
        'diagnoses': engine.get_diagnoses(),
        'recommendations': engine.get_recommendations()
    }
