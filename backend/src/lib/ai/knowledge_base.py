"""
Knowledge Base for Medical Expert System.

Loads and indexes raw knowledge markdown files for retrieval during AI chat.
Provides simple keyword-based retrieval (can be upgraded to embeddings later).
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict, Set


@dataclass
class KnowledgeChunk:
    """A chunk of knowledge from a markdown file."""
    disease: str
    source_file: str
    title: str
    content: str
    keywords: Set[str]
    
    def to_dict(self):
        return {
            "disease": self.disease,
            "source_file": self.source_file,
            "title": self.title,
            "content": self.content,
        }


# Medical keywords for matching
SYMPTOM_KEYWORDS = {
    "fever", "chills", "sweating", "diarrhea", "vomiting", "headache",
    "abdominal", "pain", "nausea", "fatigue", "weakness", "dehydration",
    "constipation", "bloody", "watery", "rice-water", "stool", "urine",
    "dark", "jaundice", "rash", "spots", "rose", "bradycardia", "pulse",
    "consciousness", "confusion", "seizure", "convulsion", "coma",
    "anemia", "pallor", "splenomegaly", "hepatomegaly", "enlarged",
}

SEVERITY_KEYWORDS = {
    "severe", "mild", "moderate", "complicated", "uncomplicated",
    "urgent", "emergency", "critical", "danger", "warning",
}

TREATMENT_KEYWORDS = {
    "treatment", "therapy", "medication", "antibiotic", "antimalarial",
    "rehydration", "ors", "iv", "oral", "injection", "dose", "dosage",
    "primaquine", "artemisinin", "act", "ciprofloxacin", "azithromycin",
    "doxycycline", "quinine", "artesunate",
}

DIAGNOSTIC_KEYWORDS = {
    "diagnosis", "diagnostic", "test", "laboratory", "lab", "smear",
    "blood", "culture", "rdt", "rapid", "widal", "microscopy",
    "sensitivity", "specificity", "positive", "negative",
}


class KnowledgeBase:
    """
    Knowledge base that loads and indexes medical knowledge from markdown files.
    
    Usage:
        kb = KnowledgeBase()
        kb.load()
        context = kb.get_relevant_context(["fever", "chills"], ["malaria"])
    """
    
    def __init__(self, knowledge_dir: Optional[str] = None):
        if knowledge_dir is None:
            # Default to the raw_knowledge directory
            base_dir = Path(__file__).parent.parent / "expert_system" / "raw_knowledge"
            self.knowledge_dir = base_dir
        else:
            self.knowledge_dir = Path(knowledge_dir)
        
        self.chunks: List[KnowledgeChunk] = []
        self.diseases: Set[str] = set()
        self._loaded = False
    
    def load(self) -> None:
        """Load and index all knowledge files."""
        if self._loaded:
            return
            
        if not self.knowledge_dir.exists():
            raise FileNotFoundError(f"Knowledge directory not found: {self.knowledge_dir}")
        
        # Iterate through disease folders
        for disease_dir in self.knowledge_dir.iterdir():
            if disease_dir.is_dir() and not disease_dir.name.startswith("_"):
                disease_name = disease_dir.name.replace("_", " ").title()
                self.diseases.add(disease_name)
                
                # Load each markdown file
                for md_file in disease_dir.glob("*.md"):
                    self._load_file(md_file, disease_name)
        
        self._loaded = True
    
    def _load_file(self, filepath: Path, disease: str) -> None:
        """Load and chunk a single markdown file."""
        content = filepath.read_text(encoding="utf-8")
        
        # Split by headers (## or ###)
        sections = re.split(r'\n(?=#{2,3}\s)', content)
        
        for section in sections:
            if not section.strip():
                continue
            
            # Extract title from first line if it's a header
            lines = section.strip().split("\n")
            title_match = re.match(r'^#{2,3}\s*(.+)', lines[0])
            title = title_match.group(1) if title_match else "General"
            
            # Extract keywords from content
            keywords = self._extract_keywords(section.lower())
            
            chunk = KnowledgeChunk(
                disease=disease,
                source_file=filepath.name,
                title=title,
                content=section.strip(),
                keywords=keywords,
            )
            self.chunks.append(chunk)
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract relevant medical keywords from text."""
        words = set(re.findall(r'\b\w+\b', text))
        
        keywords = set()
        keywords.update(words & SYMPTOM_KEYWORDS)
        keywords.update(words & SEVERITY_KEYWORDS)
        keywords.update(words & TREATMENT_KEYWORDS)
        keywords.update(words & DIAGNOSTIC_KEYWORDS)
        
        return keywords
    
    def get_relevant_context(
        self,
        symptoms: List[str] = None,
        diseases: List[str] = None,
        query: str = None,
        max_chunks: int = 5,
    ) -> List[Dict]:
        """
        Retrieve relevant knowledge chunks based on symptoms, diseases, or query.
        
        Args:
            symptoms: List of symptom names to match
            diseases: List of disease names to prioritize
            query: Free-text query to match keywords
            max_chunks: Maximum number of chunks to return
            
        Returns:
            List of relevant knowledge chunks as dicts
        """
        if not self._loaded:
            self.load()
        
        # Build search keywords
        search_keywords = set()
        
        if symptoms:
            for symptom in symptoms:
                search_keywords.update(symptom.lower().replace("_", " ").split())
        
        if query:
            query_words = set(re.findall(r'\b\w+\b', query.lower()))
            search_keywords.update(query_words & (
                SYMPTOM_KEYWORDS | SEVERITY_KEYWORDS | TREATMENT_KEYWORDS | DIAGNOSTIC_KEYWORDS
            ))
        
        # Normalize disease names for matching
        target_diseases = set()
        if diseases:
            for d in diseases:
                target_diseases.add(d.lower().replace("_", " ").title())
        
        # Score and rank chunks
        scored_chunks = []
        for chunk in self.chunks:
            score = 0
            
            # Disease match bonus
            if target_diseases and chunk.disease in target_diseases:
                score += 10
            
            # Keyword overlap score
            if search_keywords:
                overlap = len(chunk.keywords & search_keywords)
                score += overlap * 2
            
            if score > 0:
                scored_chunks.append((score, chunk))
        
        # Sort by score descending
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        # Return top chunks
        return [chunk.to_dict() for _, chunk in scored_chunks[:max_chunks]]
    
    def get_disease_summary(self, disease: str) -> str:
        """Get a summary of knowledge for a specific disease."""
        if not self._loaded:
            self.load()
        
        disease_normalized = disease.lower().replace("_", " ").title()
        
        relevant_chunks = [
            chunk for chunk in self.chunks 
            if chunk.disease == disease_normalized
        ]
        
        if not relevant_chunks:
            return f"No knowledge available for {disease}"
        
        # Combine first few chunks as summary
        summaries = []
        for chunk in relevant_chunks[:3]:
            summaries.append(f"### {chunk.title}\n{chunk.content[:500]}...")
        
        return "\n\n".join(summaries)
    
    def get_all_diseases(self) -> List[str]:
        """Return list of all diseases in the knowledge base."""
        if not self._loaded:
            self.load()
        return sorted(list(self.diseases))


# Global instance for reuse
_knowledge_base: Optional[KnowledgeBase] = None


def get_knowledge_base() -> KnowledgeBase:
    """Get or create the global knowledge base instance."""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
        _knowledge_base.load()
    return _knowledge_base
