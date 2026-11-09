from backend.app.services.indicators import INDICATORS


def calculate_evaluation(scores_source) -> dict:
    """
    Given a score source (dict, Pydantic-validated dict, or Starlette FormData)
    mapping indicator item IDs (e.g. "c1", "m2") to scores 1-4, computes the
    per-domain averages, composite index, percentage, and predicate.

    Missing scores fall back to 1 (BB).
    """
    domain_scores = {domain: [] for domain in INDICATORS}
    scores_dict = {}

    for domain_name, domain_data in INDICATORS.items():
        for item in domain_data["items"]:
            score_val = scores_source.get(item["id"])
            score_int = int(score_val) if score_val is not None else 1
            scores_dict[item["id"]] = score_int
            domain_scores[domain_name].append(score_int)

    domain_averages = {
        domain: (sum(vals) / len(vals) if vals else 1.0)
        for domain, vals in domain_scores.items()
    }

    # Composite Index: simple average, all domains equally weighted
    composite_index = round(sum(domain_averages.values()) / len(domain_averages), 2)

    # Percentage Index: (Index - 1) / 3 * 100
    index_percentage = round(((composite_index - 1.0) / 3.0) * 100.0, 1)
    index_percentage = max(index_percentage, 0.0)

    # Predicate: 1.0-1.49 BB, 1.5-2.49 MB, 2.5-3.49 BSH, 3.5-4.0 BSB
    if composite_index >= 3.50:
        predicate = "BSB"
    elif composite_index >= 2.50:
        predicate = "BSH"
    elif composite_index >= 1.50:
        predicate = "MB"
    else:
        predicate = "BB"

    return {
        "scores": scores_dict,
        "avg_cognitive": domain_averages["cognitive"],
        "avg_motoric": domain_averages["motoric"],
        "avg_language": domain_averages["language"],
        "avg_social": domain_averages["social"],
        "avg_independence": domain_averages["independence"],
        "composite_index": composite_index,
        "index_percentage": index_percentage,
        "predicate": predicate,
    }
