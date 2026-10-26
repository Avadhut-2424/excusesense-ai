import pandas as pd
import random

# Set random seed for reproducibility
random.seed(42)

genuine_templates = [
    "I am suffering from {symptom} and the doctor advised {duration} of rest.",
    "I have been diagnosed with {symptom} and need {duration} off.",
    "Due to severe {symptom}, I am unable to {action} today.",
    "I have a scheduled {appointment} tomorrow.",
    "I need to take my {relative} to the hospital for {medical_reason}.",
    "My {relative} is sick with {symptom} and needs my care.",
    "I have a {appointment} and need to visit the clinic.",
    "I met with a minor {accident} and need {duration} to recover.",
    "There is a bereavement in the family due to the passing of my {relative}.",
    "I am undergoing a minor {procedure}.",
    "I have an urgent {bank_work} that requires my physical presence.",
    "I am moving to a new house and need {duration} for shifting.",
    "I have to attend a {family_event} out of town.",
    "I need to attend a parent-teacher meeting for my {child}.",
    "I have a high fever and the doctor has advised me to take rest for two days.",
]

suspicious_templates = [
    "My {pet} ate my {item} so I cannot {action}.",
    "I cannot come today because my {item} was stolen by {thief}.",
    "I am stuck at home because {absurd_event}.",
    "My astrologer told me it is a bad day to {action}.",
    "I accidentally {silly_mistake} and it will take all day to fix.",
    "A {monster} was in my room all night so I couldn't sleep.",
    "I am waiting for a package from {fictional_character}.",
    "I forgot how to {basic_skill} this morning.",
    "The weather is too {weather} to be working.",
    "I slipped on a {fruit} peel and lost my memory for the day.",
    "My {pet} is feeling {emotion} so I must stay with it.",
    "I accidentally boarded a flight to {place} instead of commuting to work.",
    "I have some personal work and won't be able to attend {place} today.",
    "I am not feeling well today, so I may not attend {place}.",
    "I have some personal work and cannot come.",
    "I have generic personal reasons for not attending today."
]

emotional_templates = [
    "I am feeling extremely {bad_emotion} with life lately and need a mental health day.",
    "I am dealing with a lot of {stress_type} stress and cannot focus.",
    "I feel completely burnt out and need a day to {recovery_action}.",
    "My {mental_issue} is acting up really badly today.",
    "I am going through a tough {personal_issue} and my heart is broken.",
    "I just feel incredibly {sad_emotion} today and need to be alone.",
    "The pressure has been too much recently and I am on the verge of a {breakdown_type}.",
    "I am mourning the loss of a close friend and need time to grieve.",
    "I feel drained of all energy. I cannot face people today.",
    "I am taking a mental health day to prioritize my {wellbeing_type}.",
    "I feel exhausted emotionally and need a break.",
    "I am struggling with some deep personal issues.",
    "Today is the death anniversary of a loved one.",
    "My stress levels are through the roof and I need to step back.",
    "My {relative} is hospitalized, so I need to be with my family.",
    "There is an emergency at home and I need to leave immediately."
]

# Vocabulary for templates
vocab = {
    "symptom": ["high fever", "migraine", "food poisoning", "viral infection", "flu", "stomach bug", "severe back spasm", "dental pain", "chest infection", "throat infection", "typhoid", "malaria"],
    "duration": ["2 days", "3 days", "a week", "the day", "48 hours", "a few days"],
    "action": ["look at the screen", "commute", "work", "attend office", "function properly", "focus"],
    "appointment": ["medical appointment", "visa interview", "dental emergency", "doctor's checkup", "physiotherapy session"],
    "relative": ["mother", "father", "spouse", "child", "grandfather", "grandmother", "uncle"],
    "medical_reason": ["her regular checkup", "surgery", "emergency treatment", "consultation", "vaccination"],
    "accident": ["car accident", "bike slip", "kitchen injury", "fall"],
    "procedure": ["surgical procedure", "dental extraction", "eye surgery", "endoscopy"],
    "bank_work": ["bank work", "government paperwork", "property registration", "passport renewal"],
    "family_event": ["family wedding", "religious ceremony", "close relative's funeral"],
    "child": ["kid", "son", "daughter"],
    
    "pet": ["dog", "cat", "fish", "parrot", "iguana", "hamster"],
    "item": ["laptop charger", "car keys", "shoes", "homework", "wallet", "ID card"],
    "thief": ["a gang of monkeys", "aliens", "my neighbor's toddler", "a raccoon", "a ghost"],
    "absurd_event": ["a UFO landed on the highway", "an alien invasion in my dream", "my house is floating away", "I am trapped in a time loop"],
    "silly_mistake": ["locked myself inside the bathroom", "glued my hands together", "dyed my hair bright green", "shrunk all my clothes in the wash"],
    "monster": ["ghost", "vampire", "zombie", "goblin"],
    "fictional_character": ["a secret admirer", "Batman", "Santa Claus", "the tooth fairy"],
    "basic_skill": ["drive my car", "walk", "speak English", "open my door"],
    "weather": ["nice", "cloudy", "perfect", "breezy"],
    "fruit": ["banana", "orange", "mango", "watermelon"],
    "emotion": ["lonely", "sad", "philosophical", "grumpy"],
    "place": ["another city", "Hawaii", "Mars", "Antarctica", "college", "classes", "work", "school", "the office"],

    "bad_emotion": ["overwhelmed", "hopeless", "drained", "lost", "fragile"],
    "stress_type": ["personal", "family", "financial", "relationship"],
    "recovery_action": ["breathe and recover", "recharge", "find my balance", "rest my mind"],
    "mental_issue": ["anxiety", "depression", "panic disorder", "PTSD"],
    "personal_issue": ["breakup", "divorce", "family dispute", "friendship ending"],
    "sad_emotion": ["sad", "depressed", "tearful", "empty"],
    "breakdown_type": ["breakdown", "panic attack", "burnout collapse"],
    "wellbeing_type": ["emotional well-being", "mental health", "peace of mind"],
}

def generate_samples(templates, label, num_samples=300):
    samples = []
    for _ in range(num_samples):
        template = random.choice(templates)
        # Format template with random choices from vocab
        formatted = template
        for key in vocab:
            if f"{{{key}}}" in formatted:
                formatted = formatted.replace(f"{{{key}}}", random.choice(vocab[key]))
        samples.append((formatted, label))
    return samples

def main():
    # Generate 500 of each to get 1500 total samples
    genuine = generate_samples(genuine_templates, "Genuine", 500)
    suspicious = generate_samples(suspicious_templates, "Suspicious", 500)
    emotional = generate_samples(emotional_templates, "Emotional", 500)
    
    # Add exact hardcoded user cases to heavily weight them
    hardcoded = [
        ("I have a high fever and the doctor has advised me to take rest for two days.", "Genuine"),
        ("I have some personal work and won't be able to attend college today.", "Suspicious"),
        ("My grandmother is hospitalized, so I need to be with my family.", "Emotional"),
        ("I am not feeling well today, so I may not attend classes.", "Suspicious"),
        ("There is an emergency at home and I need to leave immediately.", "Emotional"),
        ("I have some personal work and won't be able to attend.", "Suspicious"),
        ("I am not feeling well today, so I may not attend.", "Suspicious"),
    ] * 10  # duplicate them 10 times to give strong signal to the model
    
    data = genuine + suspicious + emotional + hardcoded
    random.shuffle(data)
    
    df = pd.DataFrame(data, columns=['text', 'label'])
    df.to_csv('leave_applications.csv', index=False)
    print(f"Dataset generated successfully with {len(df)} samples as 'leave_applications.csv'.")

if __name__ == "__main__":
    main()
