from app.models.session import CandidateProfile, CandidateAnalysis

def analyze_candidate(candidate: CandidateProfile) -> CandidateAnalysis:
    passed_days = []
    failed_days = []
    skipped_days = []
    attempt_counts = {}

    for mission in candidate.missions:
        day = mission.day
        if mission.attempts is not None:
            attempt_counts[day] = mission.attempts

        if mission.skipped:
            skipped_days.append(day)
        elif mission.passed:
            passed_days.append(day)
        else:
            failed_days.append(day)

    return CandidateAnalysis(
        candidate=candidate,
        passed_days=passed_days,
        failed_days=failed_days,
        skipped_days=skipped_days,
        attempt_counts=attempt_counts
    )
