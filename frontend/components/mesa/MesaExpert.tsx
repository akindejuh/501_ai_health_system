"use client";

/**
 * MESA Expert System Component
 * Rule-based diagnostic interface with structured input
 */

import { useState } from "react";
import { useMesaStore } from "@/lib/api/stores/mesaStore";
import type {
  Symptom,
  SymptomInfo,
  LabTestType,
  LabResultValue,
  DehydrationSignType,
  DiagnosisConfidence,
} from "@/lib/api/types/mesa.types";
import { cn } from "@/lib/utils";

/* ----------------------------- SUB-COMPONENTS ----------------------------- */

function SymptomSelector() {
  const { availableSymptoms, selectedSymptoms, addSymptom, removeSymptom, updateSymptom } =
    useMesaStore();
  const [expandedSymptom, setExpandedSymptom] = useState<string | null>(null);

  const handleSymptomToggle = (symptom: SymptomInfo) => {
    const isSelected = selectedSymptoms.some((s) => s.name === symptom.name);
    if (isSelected) {
      removeSymptom(symptom.name);
    } else {
      addSymptom({ name: symptom.name, present: true });
    }
  };

  const getSelectedSymptom = (name: string): Symptom | undefined =>
    selectedSymptoms.find((s) => s.name === name);

  return (
    <div className="mesa-expert-section">
      <h3 className="mesa-expert-section-title">
        <span className="mesa-expert-section-icon">🩺</span>
        Symptoms
      </h3>
      <p className="mesa-expert-section-desc">
        Select all symptoms the patient is experiencing
      </p>
      <div className="mesa-symptom-grid">
        {availableSymptoms.map((symptom) => {
          const isSelected = selectedSymptoms.some((s) => s.name === symptom.name);
          const selected = getSelectedSymptom(symptom.name);
          const hasOptions = symptom.options !== null;
          const isExpanded = expandedSymptom === symptom.name;

          return (
            <div
              key={symptom.name}
              className={cn("mesa-symptom-card", isSelected && "selected")}
            >
              <button
                onClick={() => handleSymptomToggle(symptom)}
                className="mesa-symptom-main"
              >
                <div className="mesa-symptom-checkbox">
                  {isSelected && (
                    <svg viewBox="0 0 24 24" fill="currentColor">
                      <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
                    </svg>
                  )}
                </div>
                <div className="mesa-symptom-info">
                  <span className="mesa-symptom-name">{symptom.display_name}</span>
                  <span className="mesa-symptom-desc">{symptom.description}</span>
                </div>
              </button>

              {isSelected && hasOptions && (
                <button
                  onClick={() => setExpandedSymptom(isExpanded ? null : symptom.name)}
                  className="mesa-symptom-expand"
                >
                  <svg
                    viewBox="0 0 24 24"
                    className={cn("mesa-symptom-chevron", isExpanded && "expanded")}
                  >
                    <path
                      fill="currentColor"
                      d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"
                    />
                  </svg>
                </button>
              )}

              {isSelected && hasOptions && isExpanded && (
                <div className="mesa-symptom-options">
                  {symptom.options?.severity && (
                    <div className="mesa-symptom-option">
                      <label className="mesa-option-label">Severity</label>
                      <div className="mesa-option-buttons">
                        {symptom.options.severity.map((sev) => (
                          <button
                            key={sev}
                            onClick={() => updateSymptom(symptom.name, { severity: sev })}
                            className={cn(
                              "mesa-option-btn",
                              selected?.severity === sev && "active"
                            )}
                          >
                            {sev}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {symptom.options?.pattern && (
                    <div className="mesa-symptom-option">
                      <label className="mesa-option-label">Pattern</label>
                      <div className="mesa-option-buttons">
                        {symptom.options.pattern.map((pat) => (
                          <button
                            key={pat}
                            onClick={() => updateSymptom(symptom.name, { pattern: pat })}
                            className={cn(
                              "mesa-option-btn",
                              selected?.pattern === pat && "active"
                            )}
                          >
                            {pat}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="mesa-symptom-option">
                    <label className="mesa-option-label">Duration (days)</label>
                    <input
                      type="number"
                      min="1"
                      value={selected?.duration_days || ""}
                      onChange={(e) =>
                        updateSymptom(symptom.name, {
                          duration_days: parseInt(e.target.value) || undefined,
                        })
                      }
                      className="mesa-option-input"
                      placeholder="Number of days"
                    />
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function PatientInfoForm() {
  const { patientInfo, setPatientInfo } = useMesaStore();

  return (
    <div className="mesa-expert-section">
      <h3 className="mesa-expert-section-title">
        <span className="mesa-expert-section-icon">👤</span>
        Patient Information
      </h3>
      <p className="mesa-expert-section-desc">
        Provide additional context about the patient (optional)
      </p>
      <div className="mesa-patient-grid">
        <div className="mesa-patient-field">
          <label className="mesa-field-label">Age</label>
          <input
            type="number"
            min="0"
            max="120"
            value={patientInfo.age || ""}
            onChange={(e) =>
              setPatientInfo({ age: parseInt(e.target.value) || undefined })
            }
            className="mesa-field-input"
            placeholder="Years"
          />
        </div>

        <div className="mesa-patient-toggles">
          {[
            { key: "is_child", label: "Is Child (<18)", icon: "👶" },
            { key: "is_pregnant", label: "Is Pregnant", icon: "🤰" },
            { key: "travel_endemic_area", label: "Recent Travel to Endemic Area", icon: "✈️" },
            { key: "endemic_resident", label: "Lives in Endemic Area", icon: "🏠" },
            { key: "unsafe_water", label: "Consumed Untreated Water", icon: "💧" },
            { key: "street_food", label: "Consumed Raw Street Food", icon: "🍜" },
            { key: "household_contact", label: "Contact with Confirmed Case", icon: "🏥" },
          ].map(({ key, label, icon }) => (
            <button
              key={key}
              onClick={() =>
                setPatientInfo({
                  [key]: !patientInfo[key as keyof typeof patientInfo],
                })
              }
              className={cn(
                "mesa-toggle-btn",
                patientInfo[key as keyof typeof patientInfo] && "active"
              )}
            >
              <span className="mesa-toggle-icon">{icon}</span>
              <span className="mesa-toggle-label">{label}</span>
              <span className="mesa-toggle-indicator" />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

function LabResultsForm() {
  const { labResults, addLabResult, removeLabResult } = useMesaStore();
  const [selectedTest, setSelectedTest] = useState<LabTestType | "">("");
  const [selectedResult, setSelectedResult] = useState<LabResultValue>("positive");

  const labTests: { test: LabTestType; label: string; disease: string }[] = [
    { test: "blood_smear", label: "Blood Smear", disease: "Malaria" },
    { test: "rdt_malaria", label: "RDT Malaria", disease: "Malaria" },
    { test: "stool_culture", label: "Stool Culture", disease: "Cholera" },
    { test: "rdt_cholera", label: "RDT Cholera", disease: "Cholera" },
    { test: "blood_culture", label: "Blood Culture", disease: "Typhoid" },
    { test: "widal", label: "Widal Test", disease: "Typhoid" },
    { test: "typhidot", label: "Typhidot", disease: "Typhoid" },
  ];

  const handleAddResult = () => {
    if (!selectedTest) return;
    addLabResult({ test: selectedTest, result: selectedResult });
    setSelectedTest("");
  };

  return (
    <div className="mesa-expert-section">
      <h3 className="mesa-expert-section-title">
        <span className="mesa-expert-section-icon">🧪</span>
        Lab Results
      </h3>
      <p className="mesa-expert-section-desc">
        Add any available laboratory test results (optional)
      </p>

      <div className="mesa-lab-input">
        <select
          value={selectedTest}
          onChange={(e) => setSelectedTest(e.target.value as LabTestType)}
          className="mesa-lab-select"
        >
          <option value="">Select a test...</option>
          {labTests
            .filter((t) => !labResults.some((r) => r.test === t.test))
            .map((t) => (
              <option key={t.test} value={t.test}>
                {t.label} ({t.disease})
              </option>
            ))}
        </select>
        <select
          value={selectedResult}
          onChange={(e) => setSelectedResult(e.target.value as LabResultValue)}
          className="mesa-lab-select result"
        >
          <option value="positive">Positive</option>
          <option value="negative">Negative</option>
          <option value="pending">Pending</option>
        </select>
        <button
          onClick={handleAddResult}
          disabled={!selectedTest}
          className="mesa-lab-add-btn"
        >
          Add
        </button>
      </div>

      {labResults.length > 0 && (
        <div className="mesa-lab-results">
          {labResults.map((result) => {
            const testInfo = labTests.find((t) => t.test === result.test);
            return (
              <div key={result.test} className="mesa-lab-result-card">
                <div className="mesa-lab-result-info">
                  <span className="mesa-lab-result-name">{testInfo?.label}</span>
                  <span
                    className={cn("mesa-lab-result-value", result.result)}
                  >
                    {result.result}
                  </span>
                </div>
                <button
                  onClick={() => removeLabResult(result.test)}
                  className="mesa-lab-result-remove"
                >
                  ×
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function DehydrationAssessment() {
  const { dehydrationSigns, addDehydrationSign, removeDehydrationSign } = useMesaStore();

  const signs: {
    sign: DehydrationSignType;
    label: string;
    findings: { value: string; label: string; severity: string }[];
  }[] = [
    {
      sign: "mental_state",
      label: "Mental State",
      findings: [
        { value: "alert", label: "Alert", severity: "none" },
        { value: "restless", label: "Restless/Irritable", severity: "some" },
        { value: "lethargic", label: "Lethargic/Unconscious", severity: "severe" },
      ],
    },
    {
      sign: "eyes",
      label: "Eyes",
      findings: [
        { value: "normal", label: "Normal", severity: "none" },
        { value: "sunken", label: "Sunken", severity: "some" },
      ],
    },
    {
      sign: "skin_pinch",
      label: "Skin Pinch",
      findings: [
        { value: "normal", label: "Goes back quickly", severity: "none" },
        { value: "slow", label: "Goes back slowly", severity: "some" },
        { value: "very_slow", label: "Goes back very slowly", severity: "severe" },
      ],
    },
    {
      sign: "thirst",
      label: "Thirst",
      findings: [
        { value: "drinks_normally", label: "Drinks normally", severity: "none" },
        { value: "drinks_eagerly", label: "Drinks eagerly", severity: "some" },
        { value: "unable_to_drink", label: "Unable to drink", severity: "severe" },
      ],
    },
  ];

  const getSignValue = (signType: DehydrationSignType) =>
    dehydrationSigns.find((s) => s.sign === signType)?.finding;

  return (
    <div className="mesa-expert-section">
      <h3 className="mesa-expert-section-title">
        <span className="mesa-expert-section-icon">💧</span>
        Dehydration Assessment (WHO)
      </h3>
      <p className="mesa-expert-section-desc">
        Assess dehydration level using WHO guidelines (optional)
      </p>

      <div className="mesa-dehydration-grid">
        {signs.map(({ sign, label, findings }) => (
          <div key={sign} className="mesa-dehydration-card">
            <h4 className="mesa-dehydration-label">{label}</h4>
            <div className="mesa-dehydration-options">
              {findings.map(({ value, label: findingLabel, severity }) => {
                const isSelected = getSignValue(sign) === value;
                return (
                  <button
                    key={value}
                    onClick={() => {
                      if (isSelected) {
                        removeDehydrationSign(sign);
                      } else {
                        addDehydrationSign({ sign, finding: value });
                      }
                    }}
                    className={cn(
                      "mesa-dehydration-btn",
                      isSelected && "selected",
                      severity
                    )}
                  >
                    {findingLabel}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function DiagnosisResults() {
  const { diagnosisResult, clearDiagnosis } = useMesaStore();

  if (!diagnosisResult) return null;

  const getConfidenceConfig = (confidence: DiagnosisConfidence) => {
    const configs = {
      confirmed: { color: "confirmed", icon: "✅", label: "Confirmed" },
      confident: { color: "confident", icon: "🟢", label: "High Confidence" },
      suspect: { color: "suspect", icon: "🟡", label: "Suspected" },
      uncertain: { color: "uncertain", icon: "🔴", label: "Uncertain" },
    };
    return configs[confidence];
  };

  return (
    <div className="mesa-diagnosis-results">
      <div className="mesa-diagnosis-header">
        <h3 className="mesa-diagnosis-title">
          <span className="mesa-diagnosis-icon">📊</span>
          Diagnosis Results
        </h3>
        <button onClick={clearDiagnosis} className="mesa-diagnosis-clear">
          Clear & Start Over
        </button>
      </div>

      {/* Diagnoses */}
      <div className="mesa-diagnoses">
        {diagnosisResult.diagnoses.map((diagnosis, index) => {
          const config = getConfidenceConfig(diagnosis.confidence);
          return (
            <div key={index} className={cn("mesa-diagnosis-card", config.color)}>
              <div className="mesa-diagnosis-card-header">
                <span className="mesa-diagnosis-disease">
                  {diagnosis.disease.replace(/_/g, " ")}
                </span>
                <span className={cn("mesa-diagnosis-confidence", config.color)}>
                  {config.icon} {config.label}
                </span>
              </div>
              <p className="mesa-diagnosis-reason">{diagnosis.reason}</p>
              {diagnosis.recommendation && (
                <p className="mesa-diagnosis-recommendation">
                  💡 {diagnosis.recommendation}
                </p>
              )}
            </div>
          );
        })}
      </div>

      {/* Dehydration Level */}
      {diagnosisResult.dehydration_level !== "none" && (
        <div
          className={cn(
            "mesa-dehydration-result",
            diagnosisResult.dehydration_level
          )}
        >
          <span className="mesa-dehydration-result-label">Dehydration Level:</span>
          <span className="mesa-dehydration-result-value">
            {diagnosisResult.dehydration_level.toUpperCase()}
          </span>
          <span className="mesa-treatment-plan">
            WHO Treatment Plan {diagnosisResult.treatment_plan}
          </span>
        </div>
      )}

      {/* Recommendations */}
      {diagnosisResult.recommendations.length > 0 && (
        <div className="mesa-recommendations">
          <h4 className="mesa-recommendations-title">Recommendations</h4>
          <ul className="mesa-recommendations-list">
            {diagnosisResult.recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Disclaimer */}
      <div className="mesa-disclaimer">
        <span className="mesa-disclaimer-icon">⚠️</span>
        <p>{diagnosisResult.disclaimer}</p>
      </div>
    </div>
  );
}

/* ----------------------------- MAIN COMPONENT ----------------------------- */

export function MesaExpert() {
  const { selectedSymptoms, runDiagnosis, isLoading, error, diagnosisResult } =
    useMesaStore();

  return (
    <div className="mesa-expert">
      {diagnosisResult ? (
        <DiagnosisResults />
      ) : (
        <>
          <SymptomSelector />
          <PatientInfoForm />
          <LabResultsForm />
          <DehydrationAssessment />

          {error && (
            <div className="mesa-expert-error">
              <span className="mesa-expert-error-icon">⚠️</span>
              <span>{error}</span>
            </div>
          )}

          <div className="mesa-expert-actions">
            <div className="mesa-expert-summary">
              <span className="mesa-expert-summary-count">
                {selectedSymptoms.length} symptom
                {selectedSymptoms.length !== 1 ? "s" : ""} selected
              </span>
            </div>
            <button
              onClick={runDiagnosis}
              disabled={selectedSymptoms.length === 0 || isLoading}
              className="mesa-diagnose-btn"
            >
              {isLoading ? (
                <>
                  <span className="mesa-btn-spinner" />
                  Analyzing...
                </>
              ) : (
                <>
                  <span className="mesa-btn-icon">🔬</span>
                  Run Diagnosis
                </>
              )}
            </button>
          </div>
        </>
      )}
    </div>
  );
}
