"""Unit tests for the pool-cleaning data pipeline."""

import unittest

from pipeline.validator import check_visit, inspect_rows
from pipeline.transformer import completed_jobs, make_receipt, receipts_for
from pipeline.reporter import BranchLedger, form_dashboard


def sample_row():
    """A good row that each test can change as needed."""
    return {
        "branch_id": "LON-ON",
        "transaction_date": "2026-08-01",
        "customer_tier": "basic",
        "item_count": "2",
        "revenue": "$200.00",
        "cost": "80.00",
        "province": "on",
        "status": "completed",
    }


class PoolPipelineTests(unittest.TestCase):

    def test_text_is_cleaned_and_numbers_are_converted(self):
        row = sample_row()
        row["branch_id"] = " lon-on "
        row["transaction_date"] = "2026/08/01"
        job = check_visit(row)
        self.assertEqual(job.branch_id, "LON-ON")
        self.assertEqual(job.customer_tier, "Basic")
        self.assertEqual(job.item_count, 2)
        self.assertEqual(job.revenue, 200.0)

    def test_missing_branch_is_rejected(self):
        row = sample_row()
        row["branch_id"] = ""
        with self.assertRaises(ValueError):
            check_visit(row)

    def test_negative_revenue_is_rejected(self):
        row = sample_row()
        row["revenue"] = "-45.00"
        with self.assertRaises(ValueError):
            check_visit(row)

    def test_impossible_date_is_rejected(self):
        row = sample_row()
        row["transaction_date"] = "2026-02-30"
        with self.assertRaises(ValueError):
            check_visit(row)

    def test_wrong_item_count_is_rejected(self):
        row = sample_row()
        row["item_count"] = "two"
        with self.assertRaises(ValueError):
            check_visit(row)

    def test_cancelled_visit_does_not_count_as_a_sale(self):
        active = check_visit(sample_row())
        row = sample_row()
        row["status"] = "cancelled"
        cancelled = check_visit(row)
        all_jobs = [active, cancelled]
        result = completed_jobs(all_jobs)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(all_jobs), 2)  # Source list did not change.

    def test_receipt_uses_ontario_example_tax(self):
        job = check_visit(sample_row())
        receipt = make_receipt(job)
        self.assertEqual(receipt["tax"], 26.0)
        self.assertEqual(receipt["total_due"], 226.0)
        self.assertEqual(receipt["profit"], 120.0)
        self.assertEqual(receipt["margin_percent"], 60.0)

    def test_map_makes_a_new_list(self):
        job = check_visit(sample_row())
        receipts = receipts_for([job])
        self.assertEqual(len(receipts), 1)
        self.assertEqual(job.revenue, 200.0)

    def test_branch_ledger_reads_transaction_objects(self):
        london = check_visit(sample_row())
        row = sample_row()
        row["branch_id"] = "KEL-BC"
        row["province"] = "BC"
        other = check_visit(row)
        result = BranchLedger("LON-ON").figures([london, other])
        self.assertEqual(result["jobs"], 1)
        self.assertEqual(result["sales"], 200.0)

    def test_summary_reports_data_retention(self):
        good = sample_row()
        bad = sample_row()
        bad["branch_id"] = ""
        raw = [good, bad]
        valid, rejected = inspect_rows(raw)
        report = form_dashboard(raw, valid, rejected)
        self.assertEqual(report["retention"], 50.0)
        self.assertEqual(report["completed_count"], 1)
        self.assertEqual(len(report["rejected"]), 1)


if __name__ == "__main__":
    unittest.main()
