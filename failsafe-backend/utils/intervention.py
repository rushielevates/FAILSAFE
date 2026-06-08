def generate_intervention(risk_factors, risk_probability):
    """
    Generate personalized intervention plan based on risk factors.
    
    Returns a list of recommended actions.
    """
    interventions = []
    
    # Extract feature names that are risk factors
    risk_features = [f['feature'] for f in risk_factors if f['direction'] == 'risk']
    
    # ── Academic Interventions ──
    if 'G2' in risk_features or 'G1' in risk_features:
        interventions.append({
            "category": "Academic",
            "priority": "High",
            "action": "Schedule remedial classes in weak subjects",
            "detail": "Student's period grades (G1/G2) are low. Arrange extra tutoring sessions focusing on core subjects.",
            "timeline": "Start within 1 week"
        })
    
    if 'failures' in risk_features:
        interventions.append({
            "category": "Academic",
            "priority": "High",
            "action": "Assign academic mentor",
            "detail": "Student has history of class failures. Pair with a senior faculty mentor for weekly check-ins.",
            "timeline": "Start within 3 days"
        })
    
    if 'studytime' in risk_features:
        interventions.append({
            "category": "Academic",
            "priority": "Medium",
            "action": "Create structured study schedule",
            "detail": "Low study time detected. Help student create a daily study plan with specific goals.",
            "timeline": "Start within 1 week"
        })
    
    # ── Attendance Interventions ──
    if 'absences' in risk_features:
        interventions.append({
            "category": "Attendance",
            "priority": "High",
            "action": "Attendance monitoring program",
            "detail": "Student has high absenteeism. Implement daily attendance tracking and parent notification system.",
            "timeline": "Start immediately"
        })
    
    if 'traveltime' in risk_features:
        interventions.append({
            "category": "Attendance",
            "priority": "Low",
            "action": "Review transportation options",
            "detail": "Long commute may be affecting attendance. Explore school bus or carpool options.",
            "timeline": "Discuss within 2 weeks"
        })
    
    # ── Behavioral Interventions ──
    if 'Walc' in risk_features or 'Dalc' in risk_features:
        interventions.append({
            "category": "Behavioral",
            "priority": "High",
            "action": "Counselor referral for substance use",
            "detail": "Alcohol consumption patterns detected. Schedule confidential counseling session.",
            "timeline": "Start within 3 days"
        })
    
    if 'goout' in risk_features:
        interventions.append({
            "category": "Behavioral",
            "priority": "Medium",
            "action": "Balance social activities with academics",
            "detail": "High social activity may be impacting studies. Discuss time management strategies.",
            "timeline": "Discuss within 1 week"
        })
    
    if 'freetime' in risk_features:
        interventions.append({
            "category": "Behavioral",
            "priority": "Medium",
            "action": "Encourage structured extracurricular activities",
            "detail": "Excessive free time may indicate lack of engagement. Suggest joining clubs or sports.",
            "timeline": "Explore options within 2 weeks"
        })
    
    # ── Family & Social Interventions ──
    family_features = ['famsup', 'Pstatus', 'famrel']
    if any(f in risk_features for f in family_features):
        interventions.append({
            "category": "Family Support",
            "priority": "Medium",
            "action": "Schedule parent-teacher meeting",
            "detail": "Family factors may be affecting performance. Arrange meeting to discuss support strategies at home.",
            "timeline": "Schedule within 1 week"
        })
    
    if 'romantic' in risk_features:
        interventions.append({
            "category": "Social",
            "priority": "Low",
            "action": "Check-in on personal well-being",
            "detail": "Relationship status flagged as potential stressor. Offer pastoral care support.",
            "timeline": "Offer within 2 weeks"
        })
    
    # ── Health Interventions ──
    if 'health' in risk_features:
        interventions.append({
            "category": "Health",
            "priority": "Medium",
            "action": "Health check-up referral",
            "detail": "Health issues may be affecting academic performance. Refer to school health services.",
            "timeline": "Schedule within 1 week"
        })
    
    # ── General Interventions (always add based on risk level) ──
    if risk_probability > 80:
        interventions.insert(0, {
            "category": "Urgent",
            "priority": "Critical",
            "action": "Immediate intervention meeting",
            "detail": "Student is at critical risk of failure (>80%). Schedule emergency meeting with student, parents, and HOD within 24 hours.",
            "timeline": "Within 24 hours"
        })
    elif risk_probability > 50:
        interventions.insert(0, {
            "category": "Monitoring",
            "priority": "High",
            "action": "Weekly progress monitoring",
            "detail": "Student is at moderate risk. Assign faculty to track progress weekly for the next month.",
            "timeline": "Start immediately, review weekly"
        })
    
    # If no specific interventions matched, add general ones
    if len(interventions) == 0:
        interventions.append({
            "category": "General",
            "priority": "Low",
            "action": "Regular monitoring",
            "detail": "No specific risk factors identified. Continue standard academic monitoring.",
            "timeline": "Monthly check-ins"
        })
    
    return interventions


def generate_class_summary(students_results):
    """
    Generate summary recommendations for the entire class.
    """
    at_risk = [s for s in students_results if s['prediction'] == 'AT-RISK']
    safe = [s for s in students_results if s['prediction'] == 'SAFE']
    
    recommendations = []
    
    if len(at_risk) > len(students_results) * 0.3:
        recommendations.append({
            "level": "Class-wide",
            "action": "Conduct review session for entire class",
            "reason": f"{len(at_risk)} out of {len(students_results)} students are at risk (>30%)"
        })
    
    # Find common risk factors
    all_risk_features = []
    for student in at_risk:
        for factor in student.get('risk_factors', []):
            if factor['direction'] == 'risk':
                all_risk_features.append(factor['feature'])
    
    from collections import Counter
    common = Counter(all_risk_features).most_common(3)
    
    for feature, count in common:
        if count > len(at_risk) * 0.5:
            recommendations.append({
                "level": "Targeted",
                "action": f"Address common issue: {feature}",
                "reason": f"{count} at-risk students share this factor"
            })
    
    return {
        "class_summary": {
            "total": len(students_results),
            "at_risk": len(at_risk),
            "safe": len(safe),
            "recommendations": recommendations
        }
    }