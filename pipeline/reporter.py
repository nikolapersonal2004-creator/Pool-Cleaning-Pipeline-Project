"""Put the cleaned pool-cleaning information into a readable report."""

from pipeline.transformer import completed_jobs, receipts_for


class BranchLedger:
    """Work out the total sales for one branch using TransactionRecord objects."""

    def __init__(self, branch_code):
        self.branch_code = branch_code

    def figures(self, jobs):
        # List comprehension selects only jobs from this branch.
        my_jobs = [job for job in jobs if job.branch_id == self.branch_code]
        sales = round(sum(job.revenue for job in my_jobs), 2)
        costs = round(sum(job.cost for job in my_jobs), 2)

        return {
            "branch": self.branch_code,
            "jobs": len(my_jobs),
            "sales": sales,
            "profit": round(sales - costs, 2),
        }


def form_dashboard(raw_rows, valid_jobs, rejected_rows):
    """Collect business totals and information about data quality."""
    finished = completed_jobs(valid_jobs)
    receipts = receipts_for(finished)

    # Build a list of branch names without adding duplicates.
    branch_names = []
    for job in finished:
        if job.branch_id not in branch_names:
            branch_names.append(job.branch_id)

    by_branch = []
    for name in branch_names:
        ledger = BranchLedger(name)  # Our second class works with job objects.
        by_branch.append(ledger.figures(finished))

    # Find the branch with the largest completed sales total.
    leader = None
    for branch in by_branch:
        if leader is None or branch["sales"] > leader["sales"]:
            leader = branch

    # Nested loops count and total each customer plan.
    by_tier = {}
    for tier in ("Basic", "Plus", "Commercial"):
        tier_jobs = []
        for job in finished:
            if job.customer_tier == tier:
                tier_jobs.append(job)
        by_tier[tier] = {
            "jobs": len(tier_jobs),
            "sales": round(sum(job.revenue for job in tier_jobs), 2),
        }

    if len(raw_rows) > 0:
        retention = round(len(valid_jobs) / len(raw_rows) * 100, 1)
    else:
        retention = 0.0

    sales_total = round(sum(row["sales"] for row in receipts), 2)
    profit_total = round(sum(row["profit"] for row in receipts), 2)
    if sales_total > 0:
        overall_margin = round(profit_total / sales_total * 100, 1)
    else:
        overall_margin = 0.0

    return {
        "source_count": len(raw_rows),
        "accepted_count": len(valid_jobs),
        "rejected": rejected_rows,
        "retention": retention,
        "completed_count": len(finished),
        "service_count": sum(job.item_count for job in finished),
        "gross_sales": sales_total,
        "estimated_profit": profit_total,
        "profit_margin_percent": overall_margin,
        "taxes": round(sum(row["tax"] for row in receipts), 2),
        "sales_with_tax": round(sum(row["total_due"] for row in receipts), 2),
        "leader": leader,
        "branches": by_branch,
        "tiers": by_tier,
    }


def show_dashboard(summary):
    """Print the results in the terminal."""
    print("=" * 52)
    print("      POOL CLEANING - OPERATIONS REPORT")
    print("=" * 52)
    print("Records received:       ", summary["source_count"])
    print("Records accepted:       ", summary["accepted_count"])
    print("Records rejected:       ", len(summary["rejected"]))
    print("Clean record rate:      ", str(summary["retention"]) + "%")
    print("Completed jobs:         ", summary["completed_count"])
    print("Services completed:     ", summary["service_count"])
    print("-" * 52)
    print(f"Sales before tax:        ${summary['gross_sales']:,.2f}")
    print(f"Estimated profit:        ${summary['estimated_profit']:,.2f}")
    print(f"Estimated profit margin: {summary['profit_margin_percent']}%")
    print(f"Calculated sales tax:    ${summary['taxes']:,.2f}")
    print(f"Sales including tax:     ${summary['sales_with_tax']:,.2f}")

    print("\nBRANCH PERFORMANCE")
    for branch in summary["branches"]:
        print(f"  {branch['branch']:<9} {branch['jobs']:>2} jobs   ${branch['sales']:>8,.2f}")

    if summary["leader"] is not None:
        print("Highest sales branch:   ", summary["leader"]["branch"])

    print("\nCUSTOMER PLAN BREAKDOWN")
    for name, values in summary["tiers"].items():
        print(f"  {name:<12} {values['jobs']:>2} jobs   ${values['sales']:>8,.2f}")

    print("\nREJECTED ROWS")
    if summary["rejected"]:
        for issue in summary["rejected"]:
            print("  - " + issue)
    else:
        print("  None")

    print("\nNote: All data is fictional; tax rates are example values.")
