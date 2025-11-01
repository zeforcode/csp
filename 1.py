class Symptom:
    """Represents a medical symptom"""
    def __init__(self, name, severity=None):
        self.name = name
        self.severity = severity  # mild, moderate, severe
    
    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        if isinstance(other, Symptom):
            return self.name == other.name
        return self.name == other
    
    def __hash__(self):
        return hash(self.name)


class Disease:
    """Represents a disease with its characteristics"""
    def __init__(self, name, description, treatment):
        self.name = name
        self.description = description
        self.treatment = treatment
    
    def __str__(self):
        return self.name


class Rule:
    """Represents a diagnostic rule"""
    def __init__(self, conditions, conclusion, confidence):
        self.conditions = conditions  # List of symptoms
        self.conclusion = conclusion  # Disease
        self.confidence = confidence  # 0.0 to 1.0
    
    def matches(self, symptoms):
        """Check if all conditions are present in symptoms"""
        return all(cond in symptoms for cond in self.conditions)
    
    def __str__(self):
        cond_str = " AND ".join(str(c) for c in self.conditions)
        return f"IF {cond_str} THEN {self.conclusion} (confidence: {self.confidence})"


class KnowledgeBase:
    """Medical knowledge base with diseases and rules"""
    def __init__(self):
        self.diseases = {}
        self.rules = []
        self.symptoms_list = set()
        self._initialize_knowledge()
    
    def _initialize_knowledge(self):
        """Initialize diseases and diagnostic rules"""
        
        # Define diseases
        self.diseases["Common Cold"] = Disease(
            "Common Cold",
            "Viral infection of the upper respiratory tract",
            "Rest, fluids, over-the-counter cold medications, vitamin C"
        )
        
        self.diseases["Influenza"] = Disease(
            "Influenza (Flu)",
            "Viral infection affecting the respiratory system",
            "Antiviral medications, rest, fluids, fever reducers"
        )
        
        self.diseases["COVID-19"] = Disease(
            "COVID-19",
            "Coronavirus disease caused by SARS-CoV-2",
            "Isolation, rest, fluids, medical monitoring, oxygen therapy if needed"
        )
        
        self.diseases["Dengue"] = Disease(
            "Dengue Fever",
            "Mosquito-borne viral infection",
            "Rest, fluids, pain relievers (avoid aspirin), medical monitoring"
        )
        
        self.diseases["Malaria"] = Disease(
            "Malaria",
            "Parasitic infection transmitted by mosquitoes",
            "Antimalarial medications, supportive care, hospitalization if severe"
        )
        
        self.diseases["Typhoid"] = Disease(
            "Typhoid Fever",
            "Bacterial infection caused by Salmonella typhi",
            "Antibiotics, fluids, rest, proper nutrition"
        )
        
        self.diseases["Pneumonia"] = Disease(
            "Pneumonia",
            "Infection causing inflammation in the lungs",
            "Antibiotics, rest, fluids, oxygen therapy if needed"
        )
        
        self.diseases["Gastroenteritis"] = Disease(
            "Gastroenteritis",
            "Inflammation of the stomach and intestines",
            "Hydration, rest, bland diet, probiotics"
        )
        
        # Define symptoms
        symptoms = [
            "fever", "cough", "sore_throat", "runny_nose", "fatigue",
            "body_ache", "headache", "chills", "shortness_of_breath",
            "loss_of_taste", "loss_of_smell", "chest_pain", "high_fever",
            "joint_pain", "rash", "nausea", "vomiting", "diarrhea",
            "abdominal_pain", "muscle_pain", "weakness", "sweating"
        ]
        self.symptoms_list = set(symptoms)
        
        # Define diagnostic rules
        # Common Cold
        self.rules.append(Rule(
            ["runny_nose", "sore_throat", "cough"],
            "Common Cold",
            0.8
        ))
        
        self.rules.append(Rule(
            ["runny_nose", "sore_throat", "mild_fever", "fatigue"],
            "Common Cold",
            0.85
        ))
        
        # Influenza
        self.rules.append(Rule(
            ["high_fever", "body_ache", "fatigue", "cough"],
            "Influenza",
            0.85
        ))
        
        self.rules.append(Rule(
            ["fever", "headache", "muscle_pain", "chills", "fatigue"],
            "Influenza",
            0.8
        ))
        
        # COVID-19
        self.rules.append(Rule(
            ["fever", "cough", "shortness_of_breath"],
            "COVID-19",
            0.75
        ))
        
        self.rules.append(Rule(
            ["fever", "loss_of_taste", "loss_of_smell", "fatigue"],
            "COVID-19",
            0.9
        ))
        
        self.rules.append(Rule(
            ["fever", "cough", "fatigue", "body_ache"],
            "COVID-19",
            0.7
        ))
        
        # Dengue
        self.rules.append(Rule(
            ["high_fever", "severe_headache", "joint_pain", "rash"],
            "Dengue",
            0.85
        ))
        
        self.rules.append(Rule(
            ["fever", "body_ache", "nausea", "rash"],
            "Dengue",
            0.75
        ))
        
        # Malaria
        self.rules.append(Rule(
            ["high_fever", "chills", "sweating", "headache"],
            "Malaria",
            0.85
        ))
        
        self.rules.append(Rule(
            ["fever", "chills", "fatigue", "nausea"],
            "Malaria",
            0.75
        ))
        
        # Typhoid
        self.rules.append(Rule(
            ["high_fever", "abdominal_pain", "weakness", "headache"],
            "Typhoid",
            0.8
        ))
        
        self.rules.append(Rule(
            ["fever", "abdominal_pain", "diarrhea", "fatigue"],
            "Typhoid",
            0.75
        ))
        
        # Pneumonia
        self.rules.append(Rule(
            ["fever", "cough", "chest_pain", "shortness_of_breath"],
            "Pneumonia",
            0.85
        ))
        
        self.rules.append(Rule(
            ["high_fever", "cough", "fatigue", "chest_pain"],
            "Pneumonia",
            0.8
        ))
        
        # Gastroenteritis
        self.rules.append(Rule(
            ["nausea", "vomiting", "diarrhea", "abdominal_pain"],
            "Gastroenteritis",
            0.9
        ))
        
        self.rules.append(Rule(
            ["diarrhea", "abdominal_pain", "fever"],
            "Gastroenteritis",
            0.75
        ))


class ForwardChaining:
    """Forward chaining inference engine (data-driven)"""
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
    
    def diagnose(self, symptoms):
        """
        Perform diagnosis using forward chaining
        Returns list of (disease, confidence) tuples
        """
        diagnoses = {}
        
        # Check all rules
        for rule in self.kb.rules:
            if rule.matches(symptoms):
                disease = rule.conclusion
                confidence = rule.confidence
                
                # Update confidence if disease already diagnosed
                if disease in diagnoses:
                    # Take maximum confidence
                    diagnoses[disease] = max(diagnoses[disease], confidence)
                else:
                    diagnoses[disease] = confidence
        
        # Sort by confidence
        sorted_diagnoses = sorted(
            diagnoses.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_diagnoses


class BackwardChaining:
    """Backward chaining inference engine (goal-driven)"""
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
    
    def verify_disease(self, disease_name, symptoms):
        """
        Verify if symptoms support the diagnosis of a disease
        Returns (match, confidence, missing_symptoms)
        """
        relevant_rules = [r for r in self.kb.rules if r.conclusion == disease_name]
        
        best_match = 0
        best_confidence = 0
        best_missing = []
        
        for rule in relevant_rules:
            matched = sum(1 for cond in rule.conditions if cond in symptoms)
            total = len(rule.conditions)
            match_ratio = matched / total if total > 0 else 0
            
            if match_ratio > best_match:
                best_match = match_ratio
                best_confidence = rule.confidence * match_ratio
                best_missing = [c for c in rule.conditions if c not in symptoms]
        
        return best_match, best_confidence, best_missing
    
    def diagnose(self, symptoms, hypothesis=None):
        """
        Perform diagnosis using backward chaining
        If hypothesis provided, verify it. Otherwise, check all diseases.
        """
        if hypothesis:
            match, confidence, missing = self.verify_disease(hypothesis, symptoms)
            return [(hypothesis, confidence, missing)]
        
        results = []
        for disease_name in self.kb.diseases.keys():
            match, confidence, missing = self.verify_disease(disease_name, symptoms)
            if confidence > 0.5:  # Threshold
                results.append((disease_name, confidence, missing))
        
        # Sort by confidence
        results.sort(key=lambda x: x[1], reverse=True)
        return results


class MedicalExpertSystem:
    """Main expert system interface"""
    def __init__(self):
        self.kb = KnowledgeBase()
        self.forward_engine = ForwardChaining(self.kb)
        self.backward_engine = BackwardChaining(self.kb)
    
    def get_symptoms_from_user(self):
        """Interactive symptom collection"""
        print("\n" + "="*60)
        print("MEDICAL DIAGNOSIS EXPERT SYSTEM")
        print("="*60)
        print("\nAvailable symptoms:")
        print("-" * 60)
        
        symptoms_list = sorted(list(self.kb.symptoms_list))
        for i, symptom in enumerate(symptoms_list, 1):
            print(f"{i:2d}. {symptom.replace('_', ' ').title()}")
        
        print("\nEnter symptom numbers separated by commas (e.g., 1,5,7)")
        print("Or type symptom names separated by commas")
        user_input = input("\nYour symptoms: ").strip()
        
        symptoms = set()
        
        # Check if input is numbers
        if user_input.replace(',', '').replace(' ', '').isdigit():
            indices = [int(x.strip()) for x in user_input.split(',')]
            for idx in indices:
                if 1 <= idx <= len(symptoms_list):
                    symptoms.add(symptoms_list[idx - 1])
        else:
            # Input is symptom names
            input_symptoms = [s.strip().lower().replace(' ', '_') for s in user_input.split(',')]
            symptoms = set(s for s in input_symptoms if s in self.kb.symptoms_list)
        
        return symptoms
    
    def display_diagnosis(self, diagnoses, method="Forward Chaining"):
        """Display diagnosis results"""
        print("\n" + "="*60)
        print(f"DIAGNOSIS RESULTS ({method})")
        print("="*60)
        
        if not diagnoses:
            print("\n❌ No diagnosis could be made with the given symptoms.")
            print("   Please consult a medical professional.")
            return
        
        for i, result in enumerate(diagnoses, 1):
            if len(result) == 2:  # Forward chaining result
                disease_name, confidence = result
                missing = []
            else:  # Backward chaining result
                disease_name, confidence, missing = result
            
            disease = self.kb.diseases[disease_name]
            confidence_pct = confidence * 100
            
            print(f"\n{i}. {disease.name}")
            print(f"   Confidence: {confidence_pct:.1f}%")
            print(f"   Description: {disease.description}")
            
            if confidence_pct >= 70:
                print("   ✓ High confidence diagnosis")
            elif confidence_pct >= 50:
                print("   ⚠ Moderate confidence diagnosis")
            else:
                print("   ⚠ Low confidence diagnosis")
            
            if missing:
                print(f"   Missing symptoms: {', '.join(missing)}")
            
            print(f"   Recommended Treatment:")
            print(f"   {disease.treatment}")
        
        print("\n" + "="*60)
        print("⚠️  IMPORTANT DISCLAIMER")
        print("="*60)
        print("This is an educational expert system and NOT a substitute")
        print("for professional medical advice. Please consult a qualified")
        print("healthcare provider for proper diagnosis and treatment.")
        print("="*60)
    
    def run_forward_chaining(self, symptoms=None):
        """Run diagnosis with forward chaining"""
        if symptoms is None:
            symptoms = self.get_symptoms_from_user()
        
        print(f"\nSymptoms provided: {', '.join(sorted(symptoms))}")
        print("\nApplying Forward Chaining (Data-Driven Reasoning)...")
        
        diagnoses = self.forward_engine.diagnose(symptoms)
        self.display_diagnosis(diagnoses, "Forward Chaining")
        
        return diagnoses
    
    def run_backward_chaining(self, symptoms=None, hypothesis=None):
        """Run diagnosis with backward chaining"""
        if symptoms is None:
            symptoms = self.get_symptoms_from_user()
        
        print(f"\nSymptoms provided: {', '.join(sorted(symptoms))}")
        print("\nApplying Backward Chaining (Goal-Driven Reasoning)...")
        
        diagnoses = self.backward_engine.diagnose(symptoms, hypothesis)
        self.display_diagnosis(diagnoses, "Backward Chaining")
        
        return diagnoses
    
    def run_interactive(self):
        """Interactive mode with menu"""
        while True:
            print("\n" + "="*60)
            print("MEDICAL EXPERT SYSTEM - MAIN MENU")
            print("="*60)
            print("1. Diagnose using Forward Chaining")
            print("2. Diagnose using Backward Chaining")
            print("3. Run Test Cases")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                self.run_forward_chaining()
            elif choice == '2':
                self.run_backward_chaining()
            elif choice == '3':
                self.run_test_cases()
            elif choice == '4':
                print("\nThank you for using the Medical Expert System!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
    
    def run_test_cases(self):
        """Run predefined test cases"""
        print("\n" + "="*60)
        print("RUNNING TEST CASES")
        print("="*60)
        
        test_cases = [
            {
                "name": "Test Case 1: Common Cold",
                "symptoms": {"runny_nose", "sore_throat", "cough", "fatigue"},
                "expected": "Common Cold"
            },
            {
                "name": "Test Case 2: COVID-19",
                "symptoms": {"fever", "loss_of_taste", "loss_of_smell", "fatigue"},
                "expected": "COVID-19"
            },
            {
                "name": "Test Case 3: Dengue",
                "symptoms": {"high_fever", "severe_headache", "joint_pain", "rash"},
                "expected": "Dengue"
            },
            {
                "name": "Test Case 4: Pneumonia",
                "symptoms": {"fever", "cough", "chest_pain", "shortness_of_breath"},
                "expected": "Pneumonia"
            },
            {
                "name": "Test Case 5: Gastroenteritis",
                "symptoms": {"nausea", "vomiting", "diarrhea", "abdominal_pain"},
                "expected": "Gastroenteritis"
            }
        ]
        
        for test in test_cases:
            print(f"\n{'='*60}")
            print(f"{test['name']}")
            print(f"{'='*60}")
            print(f"Symptoms: {', '.join(sorted(test['symptoms']))}")
            print(f"Expected Diagnosis: {test['expected']}")
            
            # Test forward chaining
            diagnoses = self.forward_engine.diagnose(test['symptoms'])
            
            if diagnoses and diagnoses[0][0] == test['expected']:
                print(f"✓ PASSED - Diagnosed as {diagnoses[0][0]} (confidence: {diagnoses[0][1]*100:.1f}%)")
            else:
                actual = diagnoses[0][0] if diagnoses else "None"
                print(f"✗ FAILED - Diagnosed as {actual}")


# Main execution
def main():
    """Main function to run the expert system"""
    system = MedicalExpertSystem()
    
    # Option 1: Run interactive mode
    # system.run_interactive()
    
    # Option 2: Run test cases (for demonstration)
    system.run_test_cases()
    
    # Option 3: Run specific diagnosis
    print("\n\n" + "="*60)
    print("SAMPLE DIAGNOSIS")
    print("="*60)
    sample_symptoms = {"fever", "cough", "loss_of_taste", "fatigue"}
    system.run_forward_chaining(sample_symptoms)


if __name__ == "__main__":
    main()