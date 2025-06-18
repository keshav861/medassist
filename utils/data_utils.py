import os
import json
from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader, DirectoryLoader

def load_medical_data():
    """
    Load medical data from the data directory.
    
    Returns:
        List of Document objects containing medical information
    """
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Check if data files exist, if not create them
    if not os.listdir(data_dir):
        create_sample_data(data_dir)
    
    # Load documents from data directory
    try:
        loader = DirectoryLoader(data_dir, glob="**/*.txt", loader_cls=TextLoader)
        documents = loader.load()
        return documents
    except Exception as e:
        print(f"Error loading documents: {e}")
        # Return empty list if loading fails
        return []

def create_sample_data(data_dir):
    """
    Create sample medical data files for the chatbot.
    
    Args:
        data_dir: Directory to save the data files
    """
    # Sample data about common symptoms and Biofina medications
    medical_data = {
        "common_symptoms.txt": """
# Common Symptoms and Possible Conditions

## Headache
Headaches can be caused by various factors including stress, dehydration, lack of sleep, or more serious conditions like migraines or high blood pressure.

## Fever
Fever is often a sign that your body is fighting an infection. Common causes include viral infections, bacterial infections, and inflammatory conditions.

## Cough
Coughing can be due to respiratory infections, allergies, asthma, or irritants in the air. Persistent coughs should be evaluated by a healthcare professional.

## Fatigue
Fatigue can result from lack of sleep, poor diet, stress, anemia, or underlying medical conditions like hypothyroidism or depression.

## Nausea
Nausea may be caused by digestive issues, food poisoning, motion sickness, pregnancy, or as a side effect of medications.

## Joint Pain
Joint pain can be due to injury, arthritis, autoimmune conditions, or overuse. Chronic joint pain should be evaluated by a doctor.

## Skin Rash
Skin rashes may result from allergic reactions, infections, autoimmune conditions, or contact with irritants.

## Dizziness
Dizziness can be caused by inner ear problems, low blood pressure, anemia, or neurological conditions.

## Shortness of Breath
Shortness of breath may indicate respiratory conditions, heart problems, anxiety, or physical exertion beyond one's capacity.

## Abdominal Pain
Abdominal pain can be due to digestive issues, menstrual cramps, kidney stones, appendicitis, or other internal conditions.
""",
        
        "biofina_medications.txt": """
# Biofina Pharmaceuticals Medications

## Biorelief (Paracetamol 500mg)
Indications: Mild to moderate pain relief, fever reduction
Dosage: 1-2 tablets every 4-6 hours as needed, not exceeding 8 tablets in 24 hours
Side effects: Rare when taken as directed; may include nausea, rash
Contraindications: Liver disease, alcoholism

## Inflacalm (Ibuprofen 400mg)
Indications: Pain relief, inflammation reduction, fever
Dosage: 1 tablet every 6-8 hours after food, not exceeding 3 tablets in 24 hours
Side effects: Stomach upset, heartburn, dizziness
Contraindications: Stomach ulcers, heart conditions, pregnancy (third trimester)

## Allerease (Cetirizine 10mg)
Indications: Allergies, hay fever, hives
Dosage: 1 tablet daily
Side effects: Drowsiness, dry mouth
Contraindications: Kidney disease (may require dose adjustment)

## Gastroguard (Omeprazole 20mg)
Indications: Acid reflux, heartburn, stomach ulcers
Dosage: 1 capsule daily before breakfast
Side effects: Headache, diarrhea, nausea
Contraindications: Liver disease (may require dose adjustment)

## Slumbersure (Melatonin 3mg)
Indications: Sleep difficulties, jet lag
Dosage: 1 tablet 30 minutes before bedtime
Side effects: Drowsiness, headache
Contraindications: Autoimmune disorders, depression

## Immunoboost (Vitamin C 1000mg + Zinc 15mg)
Indications: Immune system support, cold prevention
Dosage: 1 tablet daily
Side effects: Stomach upset at high doses
Contraindications: Kidney stones (high doses of Vitamin C)

## Flexocare (Glucosamine 500mg + Chondroitin 400mg)
Indications: Joint pain, osteoarthritis
Dosage: 2 capsules daily with food
Side effects: Mild stomach upset, nausea
Contraindications: Shellfish allergy (glucosamine often derived from shellfish)

## Cardioguard (Atorvastatin 10mg)
Indications: High cholesterol, cardiovascular disease prevention
Dosage: 1 tablet daily in the evening
Side effects: Muscle pain, liver enzyme elevation
Contraindications: Pregnancy, liver disease

## Diabecontrol (Metformin 500mg)
Indications: Type 2 diabetes management
Dosage: 1-2 tablets twice daily with meals
Side effects: Digestive upset, metallic taste
Contraindications: Kidney disease, heart failure

## Tensioease (Amlodipine 5mg)
Indications: High blood pressure, angina
Dosage: 1 tablet daily
Side effects: Ankle swelling, flushing, headache
Contraindications: Severe hypotension, heart failure
""",
        
        "medical_advice.txt": """
# Important Medical Advice

## When to Seek Medical Attention

### Seek Immediate Medical Attention If:
- Severe chest pain or pressure
- Difficulty breathing or shortness of breath
- Sudden severe headache
- Sudden confusion, trouble speaking, or understanding speech
- Sudden numbness or weakness, especially on one side of the body
- Severe abdominal pain
- Uncontrolled bleeding
- Severe burns or injuries
- Poisoning or overdose
- Suicidal thoughts

### Consult a Doctor Soon If:
- Fever above 39°C (102.2°F) that persists for more than two days
- Persistent cough lasting more than two weeks
- Unexplained weight loss
- Persistent or severe pain
- Unusual lumps or growths
- Changes in bowel or bladder habits
- Persistent fatigue
- Recurring infections

## Medication Safety Guidelines

- Always take medications as prescribed by your healthcare provider
- Do not stop taking prescribed medications without consulting your doctor
- Keep all medications out of reach of children
- Store medications according to instructions (some require refrigeration)
- Check expiration dates regularly
- Do not share prescription medications with others
- Inform your doctor about all medications you are taking, including over-the-counter drugs and supplements
- Be aware of potential drug interactions
- Report any unusual side effects to your healthcare provider

## Preventive Health Measures

- Schedule regular check-ups with your healthcare provider
- Stay up-to-date with recommended vaccinations
- Maintain a balanced diet rich in fruits, vegetables, and whole grains
- Exercise regularly (aim for at least 150 minutes of moderate activity per week)
- Get adequate sleep (7-9 hours for adults)
- Manage stress through relaxation techniques, mindfulness, or other methods
- Avoid tobacco and limit alcohol consumption
- Practice good hygiene, including regular handwashing
- Use sun protection when outdoors
- Stay hydrated by drinking plenty of water
"""
    }
    
    # Write sample data to files
    for filename, content in medical_data.items():
        file_path = os.path.join(data_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    # Create a JSON file with symptom-medication mappings
    symptom_medication_map = {
        "headache": ["Biorelief", "Inflacalm"],
        "fever": ["Biorelief", "Inflacalm"],
        "allergies": ["Allerease"],
        "acid reflux": ["Gastroguard"],
        "heartburn": ["Gastroguard"],
        "insomnia": ["Slumbersure"],
        "sleep problems": ["Slumbersure"],
        "cold": ["Immunoboost", "Biorelief"],
        "immune support": ["Immunoboost"],
        "joint pain": ["Flexocare", "Inflacalm"],
        "arthritis": ["Flexocare", "Inflacalm"],
        "high cholesterol": ["Cardioguard"],
        "diabetes": ["Diabecontrol"],
        "high blood pressure": ["Tensioease"],
        "hypertension": ["Tensioease"]
    }
    
    symptom_map_path = os.path.join(data_dir, "symptom_medication_map.json")
    with open(symptom_map_path, "w", encoding="utf-8") as f:
        json.dump(symptom_medication_map, f, indent=4)

def get_medication_for_symptom(symptom):
    """
    Get recommended medications for a specific symptom.
    
    Args:
        symptom: The symptom to look up
        
    Returns:
        List of recommended medications
    """
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    symptom_map_path = os.path.join(data_dir, "symptom_medication_map.json")
    
    try:
        with open(symptom_map_path, "r", encoding="utf-8") as f:
            symptom_medication_map = json.load(f)
        
        # Normalize symptom text for lookup
        symptom_lower = symptom.lower()
        
        # Find matching symptoms
        for key, medications in symptom_medication_map.items():
            if key in symptom_lower or symptom_lower in key:
                return medications
        
        # No exact match found
        return []
    except Exception as e:
        print(f"Error retrieving medication for symptom: {e}")
        return []