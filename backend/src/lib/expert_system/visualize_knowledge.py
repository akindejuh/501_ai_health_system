"""
Knowledge Graph Visualization for Medical Diagnostic Expert System.

Generates visual representations of the diagnostic rules and relationships.
Requires: pip install networkx matplotlib
"""

import inspect
from .diagnosis_engine import MedicalDiagnosisEngine


def extract_rules_info():
    """Extract rule information from the engine."""
    engine = MedicalDiagnosisEngine()
    rules = []
    
    # Get all methods with @Rule decorator
    for name, method in inspect.getmembers(engine, predicate=inspect.ismethod):
        if hasattr(method, '_wrapped'):  # This is a rule
            doc = method.__doc__ or name
            rules.append({
                'name': name,
                'description': doc.strip(),
                'salience': getattr(method, '_salience', 0)
            })
    
    return rules


def create_knowledge_graph():
    """Create a knowledge graph of the diagnostic system."""
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyBboxPatch
    except ImportError:
        print("Please install required packages: pip install networkx matplotlib")
        return
    
    G = nx.DiGraph()
    
    # Define nodes with categories
    # SYMPTOMS
    symptoms = {
        'fever': {'label': 'Fever', 'patterns': ['cyclical', 'stepladder', 'continuous']},
        'chills': {'label': 'Chills/Rigors'},
        'sweating': {'label': 'Profuse Sweating'},
        'diarrhea': {'label': 'Diarrhea', 'types': ['rice-water', 'watery', 'bloody']},
        'vomiting': {'label': 'Vomiting'},
        'dehydration': {'label': 'Dehydration', 'severity': ['mild', 'moderate', 'severe']},
        'headache': {'label': 'Headache'},
        'abdominal_pain': {'label': 'Abdominal Pain'},
        'constipation': {'label': 'Constipation'},
        'bitter_taste': {'label': 'Bitter Taste'},
        'rose_spots': {'label': 'Rose Spots'},
        'relative_bradycardia': {'label': 'Relative Bradycardia'},
        'altered_consciousness': {'label': 'Altered Consciousness'},
        'convulsions': {'label': 'Convulsions'},
        'dark_urine': {'label': 'Dark/Black Urine'},
        'anemia': {'label': 'Severe Anemia'},
    }
    
    # RISK FACTORS
    risk_factors = {
        'endemic_area': {'label': 'Endemic Area Travel/Residence'},
        'unsafe_water': {'label': 'Unsafe Water Consumption'},
        'street_food': {'label': 'Street Food Consumption'},
        'household_contact': {'label': 'Household Contact'},
    }
    
    # LAB TESTS
    lab_tests = {
        'blood_smear': {'label': 'Blood Smear', 'for': 'malaria'},
        'rdt_malaria': {'label': 'Malaria RDT', 'for': 'malaria'},
        'stool_culture': {'label': 'Stool Culture', 'for': 'cholera'},
        'rdt_cholera': {'label': 'Cholera RDT', 'for': 'cholera'},
        'blood_culture': {'label': 'Blood Culture', 'for': 'typhoid'},
        'typhidot': {'label': 'Typhidot RDT', 'for': 'typhoid'},
        'widal': {'label': 'Widal Test', 'for': 'typhoid'},
    }
    
    # DIAGNOSES
    diagnoses = {
        'cholera': {'label': 'CHOLERA', 'color': '#2196F3'},
        'malaria': {'label': 'MALARIA', 'color': '#F44336'},
        'typhoid': {'label': 'TYPHOID', 'color': '#FFC107'},
        'uncertain': {'label': 'UNCERTAIN', 'color': '#9E9E9E'},
    }
    
    # SEVERITY INDICATORS
    severity = {
        'cerebral_malaria': {'label': '⚠ Cerebral Malaria', 'urgent': True},
        'blackwater_fever': {'label': '⚠ Blackwater Fever', 'urgent': True},
        'intestinal_hemorrhage': {'label': '⚠ Intestinal Hemorrhage', 'urgent': True},
        'severe_dehydration': {'label': '⚠ Severe Dehydration', 'urgent': True},
    }
    
    # Add nodes
    for sym_id, sym_data in symptoms.items():
        G.add_node(f"S_{sym_id}", type='symptom', **sym_data)
    
    for rf_id, rf_data in risk_factors.items():
        G.add_node(f"R_{rf_id}", type='risk_factor', **rf_data)
    
    for lab_id, lab_data in lab_tests.items():
        G.add_node(f"L_{lab_id}", type='lab_test', **lab_data)
    
    for diag_id, diag_data in diagnoses.items():
        G.add_node(f"D_{diag_id}", type='diagnosis', **diag_data)
    
    for sev_id, sev_data in severity.items():
        G.add_node(f"SEV_{sev_id}", type='severity', **sev_data)
    
    # Add edges (diagnostic rules)
    # CHOLERA rules
    G.add_edge('S_diarrhea', 'D_cholera', rule='rice-water stool', confidence='confident', salience=90)
    G.add_edge('S_dehydration', 'D_cholera', rule='+ severe dehydration', confidence='confident', salience=90)
    G.add_edge('S_vomiting', 'D_cholera', rule='AWD + vomiting', confidence='suspect', salience=70)
    G.add_edge('R_endemic_area', 'D_cholera', rule='endemic exposure', confidence='suspect', salience=70)
    G.add_edge('R_unsafe_water', 'D_cholera', rule='unsafe water', confidence='suspect', salience=70)
    G.add_edge('L_stool_culture', 'D_cholera', rule='culture +ve', confidence='confirmed', salience=100)
    G.add_edge('L_rdt_cholera', 'D_cholera', rule='RDT +ve', confidence='confident', salience=95)
    G.add_edge('S_dehydration', 'SEV_severe_dehydration', rule='severe dehydration')
    
    # MALARIA rules
    G.add_edge('S_fever', 'D_malaria', rule='cyclical fever', confidence='confident', salience=90)
    G.add_edge('S_chills', 'D_malaria', rule='+ chills (paroxysm)', confidence='confident', salience=90)
    G.add_edge('S_sweating', 'D_malaria', rule='+ sweating (paroxysm)', confidence='confident', salience=90)
    G.add_edge('S_bitter_taste', 'D_malaria', rule='bitter taste', confidence='confident', salience=80)
    G.add_edge('S_headache', 'D_malaria', rule='nonspecific', confidence='suspect', salience=65)
    G.add_edge('R_endemic_area', 'D_malaria', rule='endemic travel', confidence='suspect', salience=65)
    G.add_edge('L_blood_smear', 'D_malaria', rule='smear +ve', confidence='confirmed', salience=100)
    G.add_edge('L_rdt_malaria', 'D_malaria', rule='RDT +ve', confidence='confident', salience=95)
    G.add_edge('S_altered_consciousness', 'SEV_cerebral_malaria', rule='danger sign')
    G.add_edge('S_convulsions', 'SEV_cerebral_malaria', rule='danger sign')
    G.add_edge('S_dark_urine', 'SEV_blackwater_fever', rule='hemoglobinuria')
    G.add_edge('S_anemia', 'D_malaria', rule='severe anemia', confidence='differential')
    
    # TYPHOID rules
    G.add_edge('S_fever', 'D_typhoid', rule='stepladder fever', confidence='confident', salience=90)
    G.add_edge('S_relative_bradycardia', 'D_typhoid', rule='+ bradycardia', confidence='confident', salience=90)
    G.add_edge('S_rose_spots', 'D_typhoid', rule='rose spots', confidence='confident', salience=90)
    G.add_edge('S_abdominal_pain', 'D_typhoid', rule='+ abdominal pain', confidence='suspect', salience=70)
    G.add_edge('S_constipation', 'D_typhoid', rule='altered bowel', confidence='suspect', salience=70)
    G.add_edge('S_headache', 'D_typhoid', rule='+ headache', confidence='suspect', salience=50)
    G.add_edge('R_unsafe_water', 'D_typhoid', rule='fecal-oral route', confidence='suspect', salience=50)
    G.add_edge('R_street_food', 'D_typhoid', rule='contaminated food', confidence='suspect', salience=50)
    G.add_edge('L_blood_culture', 'D_typhoid', rule='culture +ve', confidence='confirmed', salience=100)
    G.add_edge('L_typhidot', 'D_typhoid', rule='typhidot +ve', confidence='confident', salience=85)
    G.add_edge('L_widal', 'D_typhoid', rule='widal ≥1:200', confidence='suspect', salience=75)
    G.add_edge('D_typhoid', 'SEV_intestinal_hemorrhage', rule='complication')
    
    # UNCERTAIN
    G.add_edge('S_fever', 'D_uncertain', rule='fever only', confidence='uncertain', salience=10)
    G.add_edge('S_diarrhea', 'D_uncertain', rule='non-specific diarrhea', confidence='uncertain', salience=10)
    
    return G


def visualize_graph(G, output_file='knowledge_graph.png'):
    """Visualize the knowledge graph."""
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        print("Please install: pip install networkx matplotlib")
        return
    
    plt.figure(figsize=(20, 16))
    
    # Define positions using multipartite layout
    # Group nodes by type
    symptoms = [n for n in G.nodes() if n.startswith('S_')]
    risk_factors = [n for n in G.nodes() if n.startswith('R_')]
    lab_tests = [n for n in G.nodes() if n.startswith('L_')]
    diagnoses = [n for n in G.nodes() if n.startswith('D_')]
    severity = [n for n in G.nodes() if n.startswith('SEV_')]
    
    # Manual positioning
    pos = {}
    
    # Symptoms on the left
    for i, node in enumerate(symptoms):
        pos[node] = (0, len(symptoms) - i)
    
    # Risk factors
    for i, node in enumerate(risk_factors):
        pos[node] = (1.5, len(symptoms) - len(risk_factors)//2 + i - len(risk_factors)//2)
    
    # Lab tests
    for i, node in enumerate(lab_tests):
        pos[node] = (3, len(symptoms) - len(lab_tests)//2 + i - len(lab_tests)//2)
    
    # Diagnoses in the center-right
    for i, node in enumerate(diagnoses):
        pos[node] = (5, len(symptoms)//2 + 2 - i * 2)
    
    # Severity on the far right
    for i, node in enumerate(severity):
        pos[node] = (7, len(symptoms)//2 + 1.5 - i * 1.5)
    
    # Node colors
    color_map = []
    for node in G.nodes():
        if node.startswith('S_'):
            color_map.append('#81D4FA')  # Light blue for symptoms
        elif node.startswith('R_'):
            color_map.append('#A5D6A7')  # Light green for risk factors
        elif node.startswith('L_'):
            color_map.append('#CE93D8')  # Light purple for lab tests
        elif node.startswith('D_'):
            data = G.nodes[node]
            color_map.append(data.get('color', '#BDBDBD'))
        elif node.startswith('SEV_'):
            color_map.append('#FF8A65')  # Orange for severity
        else:
            color_map.append('#BDBDBD')
    
    # Node sizes
    node_sizes = []
    for node in G.nodes():
        if node.startswith('D_'):
            node_sizes.append(3000)
        elif node.startswith('SEV_'):
            node_sizes.append(2000)
        else:
            node_sizes.append(1500)
    
    # Draw the graph
    labels = {node: G.nodes[node].get('label', node.split('_', 1)[1]) for node in G.nodes()}
    
    # Draw edges with different colors based on confidence
    edge_colors = []
    edge_styles = []
    for u, v, data in G.edges(data=True):
        confidence = data.get('confidence', '')
        if confidence == 'confirmed':
            edge_colors.append('#4CAF50')  # Green
        elif confidence == 'confident':
            edge_colors.append('#2196F3')  # Blue
        elif confidence == 'suspect':
            edge_colors.append('#FF9800')  # Orange
        else:
            edge_colors.append('#9E9E9E')  # Gray
    
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=node_sizes, alpha=0.9)
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True, 
                           arrowsize=15, alpha=0.7, connectionstyle="arc3,rad=0.1")
    
    # Add edge labels for rule names
    edge_labels = {(u, v): data.get('rule', '') for u, v, data in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6, alpha=0.8)
    
    # Add legend
    legend_elements = [
        plt.scatter([], [], c='#81D4FA', s=150, marker='o', label='Symptoms'),
        plt.scatter([], [], c='#A5D6A7', s=150, marker='o', label='Risk Factors'),
        plt.scatter([], [], c='#CE93D8', s=150, marker='o', label='Lab Tests'),
        plt.scatter([], [], c='#2196F3', s=200, marker='o', label='Cholera'),
        plt.scatter([], [], c='#F44336', s=200, marker='o', label='Malaria'),
        plt.scatter([], [], c='#FFC107', s=200, marker='o', label='Typhoid'),
        plt.scatter([], [], c='#FF8A65', s=150, marker='o', label='Severity/Urgent'),
    ]
    
    plt.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    plt.title('Medical Diagnostic Expert System - Knowledge Graph\n'
              'Edge colors: Green=Confirmed, Blue=Confident, Orange=Suspect, Gray=Other',
              fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Knowledge graph saved to: {output_file}")
    plt.show()


def print_rules_summary():
    """Print a text-based summary of all rules."""
    print("\n" + "="*70)
    print("MEDICAL DIAGNOSTIC EXPERT SYSTEM - RULES SUMMARY")
    print("="*70)
    
    rules_by_disease = {
        'CHOLERA': [
            ('Rice-water stool', 'CONFIDENT', 90, 'Pathognomonic'),
            ('Rice-water stool + Severe dehydration', 'CONFIDENT + SEVERE', 90, 'Pathognomonic'),
            ('Watery diarrhea + Vomiting + Endemic', 'SUSPECT', 70, 'Needs culture/RDT'),
            ('Stool culture +ve V.cholerae', 'CONFIRMED', 100, 'Gold standard'),
            ('Cholera RDT +ve', 'CONFIDENT', 95, 'Crystal VC'),
        ],
        'MALARIA': [
            ('Cyclical fever + Chills + Sweating', 'CONFIDENT', 90, 'Classic paroxysm'),
            ('Fever + Bitter taste + Endemic travel', 'CONFIDENT', 80, 'High diagnostic weight'),
            ('Fever + Nonspecific Sx + Endemic', 'SUSPECT', 65, 'Needs blood smear/RDT'),
            ('Blood smear +ve Plasmodium', 'CONFIRMED', 100, 'Gold standard'),
            ('Malaria RDT +ve', 'CONFIDENT', 95, 'pLDH/HRP2'),
            ('Altered consciousness / Convulsions', 'CEREBRAL MALARIA', 100, 'URGENT: IV Artesunate'),
            ('Dark/Black urine', 'BLACKWATER FEVER', 95, 'URGENT: Hemoglobinuria'),
        ],
        'TYPHOID': [
            ('Stepladder fever + Relative bradycardia', 'CONFIDENT', 90, 'Pathognomonic'),
            ('Rose spots + Fever', 'CONFIDENT', 90, 'Highly specific'),
            ('Fever ≥5 days + Abdominal pain', 'SUSPECT', 70, 'Needs blood culture'),
            ('Fever + Headache + Unsafe water/food', 'SUSPECT', 50, 'Consider Widal'),
            ('Blood culture +ve S.typhi', 'CONFIRMED', 100, 'Gold standard'),
            ('Typhidot +ve + Fever', 'CONFIDENT', 85, '95-97% sensitivity'),
            ('Widal ≥1:200 + Fever', 'SUSPECT', 75, '14% false positive rate'),
            ('Melena / Bloody stool', 'INTESTINAL HEMORRHAGE', 100, 'URGENT: Surgical referral'),
        ],
        'UNCERTAIN': [
            ('Fever only', 'UNCERTAIN', 10, 'Recommend lab tests'),
            ('Non-specific diarrhea', 'UNCERTAIN', 10, 'Consider other GI causes'),
        ]
    }
    
    for disease, rules in rules_by_disease.items():
        print(f"\n{'─'*70}")
        print(f"  {disease}")
        print(f"{'─'*70}")
        for symptom_combo, confidence, salience, note in rules:
            print(f"  IF: {symptom_combo}")
            print(f"     → {confidence} (salience: {salience}) | {note}")
    
    print(f"\n{'='*70}")
    print("CONFIDENCE LEVELS:")
    print("  ★ CONFIRMED  - Laboratory-confirmed diagnosis")
    print("  ✓ CONFIDENT  - High clinical certainty (pathognomonic signs)")
    print("  ? SUSPECT    - Probable, needs confirmation")
    print("  ⚠ UNCERTAIN  - Insufficient findings, recommend testing")
    print("="*70)


def generate_mermaid_diagram():
    """Generate Mermaid diagram code for the knowledge graph."""
    mermaid = """
```mermaid
flowchart LR
    subgraph INPUT["📋 INPUT"]
        SYMPTOMS[Symptoms]
        PATIENT[Patient History]
        LABS[Lab Results]
    end

    subgraph CHOLERA["🔵 CHOLERA"]
        C1[Rice-water stool] -->|pathognomonic| C_CONF[✓ Confident]
        C2[AWD + Vomiting + Endemic] -->|suspect| C_SUSP[? Suspect]
        C3[Stool Culture +ve] -->|gold standard| C_CONFIRM[★ Confirmed]
        C4[Severe Dehydration] -->|urgent| C_SEV[⚠ Plan C]
    end

    subgraph MALARIA["🔴 MALARIA"]
        M1[Cyclical Fever + Chills + Sweating] -->|paroxysm| M_CONF[✓ Confident]
        M2[Fever + Bitter Taste] -->|specific| M_CONF2[✓ Confident]
        M3[Blood Smear +ve] -->|gold standard| M_CONFIRM[★ Confirmed]
        M4[Altered Consciousness] -->|danger| M_SEV[⚠ Cerebral]
        M5[Dark Urine] -->|danger| M_SEV2[⚠ Blackwater]
    end

    subgraph TYPHOID["🟡 TYPHOID"]
        T1[Stepladder Fever + Bradycardia] -->|pathognomonic| T_CONF[✓ Confident]
        T2[Rose Spots] -->|specific| T_CONF2[✓ Confident]
        T3[Blood Culture +ve] -->|gold standard| T_CONFIRM[★ Confirmed]
        T4[Prolonged Fever + Abd Pain] -->|suspect| T_SUSP[? Suspect]
        T5[Melena/GI Bleed] -->|danger| T_SEV[⚠ Hemorrhage]
    end

    subgraph UNCERTAIN["⚪ UNCERTAIN"]
        U1[Fever Only] -->|insufficient| UNC[? Need Tests]
        U2[Non-specific Diarrhea] -->|insufficient| UNC
    end

    SYMPTOMS --> C1 & C2 & M1 & M2 & T1 & T2 & T4 & U1 & U2
    PATIENT --> C2 & M1
    LABS --> C3 & M3 & T3

    style CHOLERA fill:#e3f2fd
    style MALARIA fill:#ffebee  
    style TYPHOID fill:#fff9c4
    style UNCERTAIN fill:#f5f5f5
```
"""
    print(mermaid)
    
    # Save to file
    with open('knowledge_graph.md', 'w', encoding='utf-8') as f:
        f.write("# Medical Diagnostic Expert System - Knowledge Graph\n\n")
        f.write(mermaid)
    print("\nMermaid diagram saved to: knowledge_graph.md")


if __name__ == "__main__":
    import sys
    
    print("Medical Diagnostic Expert System - Knowledge Visualization")
    print("-" * 50)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--text':
            print_rules_summary()
        elif sys.argv[1] == '--mermaid':
            generate_mermaid_diagram()
        elif sys.argv[1] == '--graph':
            G = create_knowledge_graph()
            if G:
                visualize_graph(G)
    else:
        print("\nUsage:")
        print("  python visualize_knowledge.py --text     # Print rules summary")
        print("  python visualize_knowledge.py --mermaid  # Generate Mermaid diagram")
        print("  python visualize_knowledge.py --graph    # Generate PNG graph (requires networkx, matplotlib)")
        print("\nRunning all visualizations...")
        print_rules_summary()
        generate_mermaid_diagram()
        
        # Try to create graph
        try:
            G = create_knowledge_graph()
            if G:
                visualize_graph(G)
        except Exception as e:
            print(f"\nNote: Could not generate PNG graph: {e}")
            print("Install requirements with: pip install networkx matplotlib")
