"""Create new lists with calculations. Original transactions stay unchanged."""


# Example rates used only for the fictional assignment data.
REGIONAL_TAX = {"ON": 0.13, "BC": 0.12, "AB": 0.05}


def completed_jobs(records):
    """Keep jobs that actually went ahead."""
    return list(filter(lambda job: job.active, records))


def make_receipt(job):
    """Calculate the financial figures for one completed service job."""
    tax = round(job.revenue * REGIONAL_TAX[job.province], 2)
    profit = round(job.revenue - job.cost, 2)

    if job.revenue > 0:
        margin = round(profit / job.revenue * 100, 1)
    else:
        margin = 0.0

    return {
        "branch": job.branch_id,
        "sales": job.revenue,
        "tax": tax,
        "total_due": round(job.revenue + tax, 2),
        "profit": profit,
        "margin_percent": margin,
    }


def receipts_for(jobs):
    """Use map to calculate a new receipt for every completed job."""
    return list(map(make_receipt, jobs))
