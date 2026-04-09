class KnowledgeBase:
    def __init__(self):
        self.rules = [
            {
                "id": 1,
                "conditions": {"fever": True, "cough": True, "sore_throat": True},
                "conclusion": "Flu",
                "confidence": 0.90
            },
            {
                "id": 2,
                "conditions": {"fever": True, "rash": True, "headache": True},
                "conclusion": "Dengue",
                "confidence": 0.85
            },
            {
                "id": 3,
                "conditions": {"cough": True, "shortness_of_breath": True, "chest_pain": True},
                "conclusion": "Pneumonia",
                "confidence": 0.88
            },
            {
                "id": 4,
                "conditions": {"sneezing": True, "runny_nose": True, "itchy_eyes": True},
                "conclusion": "Allergy",
                "confidence": 0.80
            },
            {
                "id": 5,
                "conditions": {"fever": True, "cough": True, "shortness_of_breath": True},
                "conclusion": "COVID-19",
                "confidence": 0.87
            },
            {
                "id": 6,
                "conditions": {"headache": True, "nausea": True, "sensitivity_to_light": True},
                "conclusion": "Migraine",
                "confidence": 0.85
            },
            {
                "id": 7,
                "conditions": {"fever": True, "vomiting": True, "diarrhea": True},
                "conclusion": "Gastroenteritis",
                "confidence": 0.82
            },
            {
                "id": 8,
                "conditions": {"sore_throat": True, "fever": True, "swollen_lymph_nodes": True},
                "conclusion": "Strep Throat",
                "confidence": 0.83
            },
        ]

        self.all_symptoms = [
            "fever", "cough", "sore_throat", "rash", "headache",
            "shortness_of_breath", "chest_pain", "sneezing", "runny_nose",
            "itchy_eyes", "nausea", "sensitivity_to_light", "vomiting",
            "diarrhea", "swollen_lymph_nodes"
        ]


class InferenceEngine:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def match_rules(self, facts):
        matched = []
        for rule in self.kb.rules:
            conditions = rule["conditions"]
            match_count = sum(1 for k, v in conditions.items() if facts.get(k) == v)
            total = len(conditions)
            match_ratio = match_count / total
            if match_ratio >= 0.66:
                adjusted_confidence = rule["confidence"] * match_ratio
                matched.append({
                    "conclusion": rule["conclusion"],
                    "confidence": round(adjusted_confidence, 2),
                    "matched": match_count,
                    "total": total
                })
        matched.sort(key=lambda x: x["confidence"], reverse=True)
        return matched

    def explain(self, facts, result):
        rule = next(
            (r for r in self.kb.rules if r["conclusion"] == result["conclusion"]), None
        )
        if not rule:
            return "No explanation available."
        lines = [f"Diagnosis: {result['conclusion']} (Confidence: {result['confidence']:.0%})"]
        lines.append("Matched symptoms:")
        for symptom, val in rule["conditions"].items():
            status = "✔" if facts.get(symptom) == val else "✘"
            lines.append(f"  {status} {symptom.replace('_', ' ').title()}")
        return "\n".join(lines)


class ExpertSystemShell:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb)
        self.facts = {}

    def greet(self):
        print("=" * 50)
        print("   Medical Diagnosis Expert System")
        print("=" * 50)
        print("Answer each symptom with y / n / skip\n")

    def collect_facts(self):
        for symptom in self.kb.all_symptoms:
            label = symptom.replace("_", " ").title()
            while True:
                ans = input(f"Do you have {label}? (y/n/skip): ").strip().lower()
                if ans == "y":
                    self.facts[symptom] = True
                    break
                elif ans == "n":
                    self.facts[symptom] = False
                    break
                elif ans == "skip":
                    break
                else:
                    print("  Please enter y, n, or skip.")

    def diagnose(self):
        results = self.engine.match_rules(self.facts)
        print("\n" + "=" * 50)
        if not results:
            print("No matching diagnosis found.")
            print("Please consult a doctor for further evaluation.")
            return

        print(f"Top Diagnosis: {results[0]['conclusion']}")
        print(f"Confidence   : {results[0]['confidence']:.0%}")
        print("\nExplanation:")
        print(self.engine.explain(self.facts, results[0]))

        if len(results) > 1:
            print("\nOther possible conditions:")
            for r in results[1:3]:
                print(f"  - {r['conclusion']} ({r['confidence']:.0%})")

        print("\n⚠ This is an expert system prototype. Always consult a medical professional.")
        print("=" * 50)

    def run(self):
        self.greet()
        self.collect_facts()
        self.diagnose()

        while True:
            again = input("\nRun again? (y/n): ").strip().lower()
            if again == "y":
                self.facts = {}
                self.collect_facts()
                self.diagnose()
            else:
                print("Goodbye!")
                break


if __name__ == "__main__":
    shell = ExpertSystemShell()
    shell.run()
