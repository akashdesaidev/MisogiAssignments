# Task Definitions for Multi-Path Reasoning Pipeline

## Overview
This document defines the structured reasoning tasks used to evaluate the Tree-of-Thought + Self-Consistency pipeline. Each task requires multi-step reasoning and benefits from exploring multiple solution paths.

## Task Categories

### 1. Math Word Problems
**Domain**: Mathematical reasoning with real-world context
**Complexity**: Multi-step calculations with logical reasoning
**Key Challenges**:
- Extracting relevant numerical information
- Determining correct operation sequences
- Handling multiple solution approaches

**Example Problem**:
```
A bakery sells cookies in packages of 12 and muffins in packages of 8. 
If they sold 156 cookies and 144 muffins yesterday, and each cookie 
costs $0.75 while each muffin costs $1.25, what was their total revenue?
```

**Expected Solution Path**:
1. Calculate number of cookie packages: 156 ÷ 12 = 13 packages
2. Calculate number of muffin packages: 144 ÷ 8 = 18 packages
3. Calculate cookie revenue: 156 × $0.75 = $117
4. Calculate muffin revenue: 144 × $1.25 = $180
5. Total revenue: $117 + $180 = $297

---

### 2. Logic Puzzles
**Domain**: Logical deduction and constraint satisfaction
**Complexity**: Multi-constraint problems requiring systematic elimination
**Key Challenges**:
- Managing multiple constraints simultaneously
- Avoiding logical fallacies
- Systematic case analysis

**Example Problem**:
```
Five friends (Alice, Bob, Carol, David, Eve) sit in a row. 
Constraints:
- Alice sits next to Bob
- Carol doesn't sit at either end
- David sits to the left of Eve
- Bob doesn't sit next to Carol
Find all possible seating arrangements.
```

**Expected Solution Approach**:
1. Enumerate possible positions for each constraint
2. Apply constraint elimination systematically
3. Verify each potential solution against all constraints
4. List valid arrangements

---

### 3. Code Debugging
**Domain**: Software debugging and error analysis
**Complexity**: Multi-layered debugging requiring code understanding
**Key Challenges**:
- Understanding code intent vs. implementation
- Identifying multiple potential issues
- Proposing targeted fixes

**Example Problem**:
```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# This function sometimes crashes. Identify all issues and propose fixes.
```

**Expected Analysis**:
1. **Issue 1**: Division by zero when `numbers` is empty
2. **Issue 2**: No type checking for non-numeric inputs
3. **Issue 3**: Integer division issues in older Python versions
4. **Proposed fixes**: Input validation, exception handling, type hints

---

### 4. Planning Tasks
**Domain**: Sequential planning and resource optimization
**Complexity**: Multi-step planning with dependencies and constraints
**Key Challenges**:
- Managing task dependencies
- Optimizing resource allocation
- Handling temporal constraints

**Example Problem**:
```
Plan a 3-day conference with the following requirements:
- 5 keynote speakers (2 hours each)
- 12 workshop sessions (1.5 hours each)
- 3 panel discussions (1 hour each)
- Networking sessions between major events
- Speakers A and B cannot present on the same day
- Workshop topics must be spread across all days
- Each day should have 6-8 hours of content
```

**Expected Planning Process**:
1. Calculate total content hours and constraints
2. Distribute major events across days
3. Schedule workshops considering topic diversity
4. Insert networking sessions strategically
5. Validate all constraints are satisfied

---

### 5. Causal Reasoning
**Domain**: Cause-and-effect analysis in complex scenarios
**Complexity**: Multi-factor causation with indirect effects
**Key Challenges**:
- Distinguishing correlation from causation
- Identifying confounding variables
- Reasoning about chains of causation

**Example Problem**:
```
A company notices that their customer satisfaction scores dropped 
by 15% over the past quarter. During this period:
- They launched a new product line
- Customer service response time increased by 20%
- A competitor reduced their prices by 10%
- The company moved to a new office building
- Two senior customer service representatives left

Analyze the potential causes and their likely impact on satisfaction scores.
```

**Expected Analysis**:
1. **Direct causes**: Service response time, staff turnover
2. **Indirect causes**: New product line confusion, competitive pressure
3. **Unlikely causes**: Office move (unless affecting operations)
4. **Causal chains**: Staff departure → longer response times → lower satisfaction
5. **Quantitative estimation**: Relative impact of each factor

---

### 6. Resource Allocation
**Domain**: Optimization under constraints
**Complexity**: Multi-objective optimization with trade-offs
**Key Challenges**:
- Balancing competing objectives
- Working within resource constraints
- Evaluating trade-offs systematically

**Example Problem**:
```
A startup has $100,000 to allocate across:
- Product development (expected ROI: 3x over 2 years)
- Marketing (expected ROI: 2x over 1 year)
- Hiring (expected ROI: 4x over 3 years, but requires minimum $30k)
- Equipment (expected ROI: 1.5x over 5 years, enables other investments)

Determine optimal allocation strategy considering:
- Need for immediate cash flow
- Long-term growth potential
- Risk tolerance (conservative approach preferred)
```

**Expected Reasoning**:
1. Analyze ROI rates and time horizons
2. Consider interdependencies (equipment enabling other investments)
3. Factor in risk preferences and cash flow needs
4. Propose allocation with justification
5. Consider alternative scenarios

---

### 7. Ethical Dilemmas
**Domain**: Ethical reasoning and moral decision-making
**Complexity**: Multi-stakeholder scenarios with competing values
**Key Challenges**:
- Balancing different ethical frameworks
- Considering all stakeholder perspectives
- Reasoning about long-term consequences

**Example Problem**:
```
An AI company develops a facial recognition system that could:
- Help find missing children (high social benefit)
- Enable mass surveillance by governments (privacy concerns)
- Generate significant revenue for the company
- Potentially be misused by bad actors

The company must decide whether to:
1. Release the technology publicly
2. License only to verified organizations
3. Keep the technology internal
4. Discontinue development entirely

Analyze this decision from multiple ethical perspectives.
```

**Expected Analysis**:
1. **Stakeholder analysis**: Children/families, general public, company, governments
2. **Ethical frameworks**: Utilitarian, deontological, virtue ethics
3. **Risk assessment**: Potential benefits vs. harm
4. **Mitigation strategies**: Technical and policy safeguards
5. **Recommendation**: Balanced decision with ethical justification

---

## Evaluation Criteria

For each task type, solutions are evaluated on:

1. **Correctness**: Accuracy of final answer
2. **Reasoning Quality**: Logical coherence and completeness
3. **Path Diversity**: Exploration of multiple approaches
4. **Consistency**: Agreement across different reasoning paths
5. **Efficiency**: Resource usage and computational cost

## Task Complexity Scaling

Tasks are designed with multiple difficulty levels:
- **Basic**: Single-path solutions, clear constraints
- **Intermediate**: Multiple valid approaches, some ambiguity
- **Advanced**: Complex interdependencies, requires sophisticated reasoning

This structure allows for comprehensive evaluation of the multi-path reasoning pipeline across diverse domains and complexity levels. 