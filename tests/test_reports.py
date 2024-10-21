import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.reports import save_report_to_file_decorator, spending_by_category, spending_by_weekday, spending_by_workday


class TestReports(unittest.TestCase):
    def setUp(self) -> None:
        self.transactions = pd.DataFrame(
            {
                "Дата операции": ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05"],
                "Категория": ["Category1", "Category2", "Category1", "Category2", "Category1"],
                "Сумма операции": [100, 200, 300, 400, 500],
            }
        )
        self.transactions["Дата операции"] = pd.to_datetime(self.transactions["Дата операции"])

    def test_spending_by_category(self) -> None:
        report = spending_by_category(self.transactions, "Category1")
        self.assertIsInstance(report, pd.DataFrame)
        self.assertGreaterEqual(report.shape[0], 0)  # Check if the report has at least one row

    def test_spending_by_weekday(self) -> None:
        report = spending_by_weekday(self.transactions)
        self.assertIsInstance(report, pd.DataFrame)
        self.assertGreaterEqual(report.shape[0], 0)  # Check if the report has at least one row

    def test_spending_by_workday(self) -> None:
        report = spending_by_workday(self.transactions, "01.01.2022")
        self.assertIsInstance(report, pd.DataFrame)
        self.assertGreaterEqual(report.shape[0], 0)

    @patch("src.reports.save_report_to_file")
    def test_save_report_to_file_decorator(self, mock_save_report_to_file: MagicMock) -> None:
        report = spending_by_category(self.transactions, "Category1")
        save_report_to_file_decorator("spending_by_category.json")(lambda x: x)(report)
        mock_save_report_to_file.assert_called_once_with(report, "spending_by_category.json")


if __name__ == "__main__":
    unittest.main()
