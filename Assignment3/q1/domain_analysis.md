# Domain Analysis: Medical Q&A Assistant

## 🏥 Domain Overview

The medical domain is chosen for its critical importance and unique challenges in LLM applications. Medical information systems require:

- **High Accuracy**: Incorrect medical information can have serious consequences
- **Transparency**: Clear reasoning and source attribution
- **Caution**: Appropriate disclaimers and uncertainty handling
- **Comprehensibility**: Complex medical concepts explained clearly

## 🎯 Representative User Tasks

### 1. Symptom Analysis and Differential Diagnosis

**Description**: Users describe symptoms and seek potential diagnoses or conditions to consider.

**Example Query**: "I have been experiencing persistent headaches, nausea, and sensitivity to light for the past 3 days. What could be causing these symptoms?"

**Challenges**:

- Multiple possible diagnoses
- Need for careful qualification of suggestions
- Avoiding definitive diagnosis without examination

### 2. Medical Term and Concept Explanation

**Description**: Users need clear explanations of medical terminology, procedures, or conditions.

**Example Query**: "What is atrial fibrillation and how does it affect the heart?"

**Challenges**:

- Balancing technical accuracy with understandability
- Providing comprehensive yet concise explanations
- Using appropriate analogies and examples

### 3. Treatment and Medication Information

**Description**: Users seek information about treatments, medications, side effects, and care instructions.

**Example Query**: "What are the common side effects of metformin and how should it be taken?"

**Challenges**:

- Providing accurate dosage and safety information
- Emphasizing the need for professional medical advice
- Handling individual variation in treatment responses

## 🧠 Domain-Specific Reasoning Requirements

### Medical Reasoning Patterns

1. **Differential Diagnosis**: Considering multiple possible explanations
2. **Risk Stratification**: Evaluating urgency and severity
3. **Evidence-Based Reasoning**: Referencing medical knowledge
4. **Uncertainty Management**: Acknowledging limitations

### Safety Considerations

- Always include medical disclaimers
- Emphasize consulting healthcare professionals
- Avoid definitive diagnoses
- Handle emergency situations appropriately

## 📊 Expected Challenges

### 1. Hallucination Risks

- **Medication dosages**: Incorrect dosing information
- **Rare conditions**: Overconfident diagnosis of uncommon diseases
- **Treatment protocols**: Outdated or incorrect procedures

### 2. Ambiguity Handling

- **Vague symptoms**: Non-specific complaints
- **Multiple conditions**: Overlapping symptom patterns
- **Context missing**: Insufficient patient information

### 3. Ethical Considerations

- **Scope of practice**: Not providing medical diagnosis
- **Liability concerns**: Clear disclaimers about limitations
- **Privacy**: Handling sensitive health information

## 🎯 Success Metrics

### Accuracy Metrics

- Factual correctness of medical information
- Appropriate uncertainty expression
- Relevant differential considerations

### Safety Metrics

- Presence of appropriate disclaimers
- Avoidance of definitive diagnoses
- Proper emergency situation handling

### Usability Metrics

- Clarity of explanations
- User comprehension
- Actionable recommendations

## 🔧 Domain-Specific Prompt Engineering Strategies

### 1. Medical Disclaimers

All responses should include appropriate medical disclaimers and recommendations to consult healthcare professionals.

### 2. Structured Medical Reasoning

Prompts should encourage systematic thinking following medical reasoning patterns.

### 3. Uncertainty Acknowledgment

Responses should appropriately express confidence levels and acknowledge limitations.

### 4. Patient Safety Focus

Prompts should prioritize patient safety and appropriate medical care seeking behavior.
