from datetime import datetime
from typing import Dict


class ReportModel:

    @staticmethod
    def create_report_document(report_data: Dict) -> Dict:

        total_cases = (
            report_data["diarrhea_cases"] +
            report_data["fever_cases"] +
            report_data["vomiting_cases"] +
            report_data["jaundice_cases"]
        )

        return {
            "village": report_data["village"],
            "diarrhea_cases": report_data["diarrhea_cases"],
            "fever_cases": report_data["fever_cases"],
            "vomiting_cases": report_data["vomiting_cases"],
            "jaundice_cases": report_data["jaundice_cases"],
            "total_cases": total_cases,
            "water_source_condition": report_data["water_source_condition"],
            "risk_factors": report_data["risk_factors"],
            "timestamp": datetime.utcnow()
        }

    @staticmethod
    def sanitize_report_output(report_doc: Dict) -> Dict:
        """Remove Mongo internal fields"""
        report_doc.pop("_id", None)
        return report_doc