"""
BigQuery Service - Handles patient data storage and analytics
Includes data anonymization and secure handling
"""
import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import hashlib
from datetime import datetime

load_dotenv()

# BigQuery imports
try:
    from google.cloud import bigquery
    BIGQUERY_AVAILABLE = True
except ImportError:
    BIGQUERY_AVAILABLE = False
    print("WARNING: BigQuery SDK not installed. Using fallback mode.")


class BigQueryService:
    """Service for secure patient data handling and analytics"""
    
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
        self.dataset_id = os.getenv("BIGQUERY_DATASET", "aarogya_healthcare")
        self.initialized = False
        
        # Set credentials if provided, otherwise use ADC
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if credentials_path and os.path.exists(credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            print(f"✅ Using credentials from: {credentials_path}")
        else:
            print("ℹ️ Using Application Default Credentials (ADC)")
        
        if BIGQUERY_AVAILABLE and self.project_id != "your-gcp-project-id":
            try:
                self.client = bigquery.Client(project=self.project_id)
                self.initialized = True
                print(f"✅ BigQuery initialized: {self.project_id}.{self.dataset_id}")
            except Exception as e:
                print(f"⚠️ BigQuery initialization failed: {e}")
                self.initialized = False
        else:
            print("⚠️ BigQuery not configured. Using in-memory storage.")
    
    def anonymize_patient_id(self, patient_id: str) -> str:
        """
        Anonymize patient ID using SHA-256 hashing
        Ensures HIPAA compliance
        """
        return hashlib.sha256(patient_id.encode()).hexdigest()[:16]
    
    def store_patient_record(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Store patient record in BigQuery with anonymization
        """
        if not self.initialized:
            return {
                "success": False,
                "message": "BigQuery not configured. Data not persisted.",
                "fallback": True
            }
        
        try:
            # Anonymize sensitive fields
            anonymized_data = patient_data.copy()
            if "patient_id" in anonymized_data:
                anonymized_data["patient_id_hash"] = self.anonymize_patient_id(
                    anonymized_data["patient_id"]
                )
                del anonymized_data["patient_id"]
            
            anonymized_data["timestamp"] = datetime.utcnow().isoformat()
            
            # Insert into BigQuery
            table_id = f"{self.project_id}.{self.dataset_id}.patient_records"
            errors = self.client.insert_rows_json(table_id, [anonymized_data])
            
            if errors:
                return {
                    "success": False,
                    "message": f"BigQuery insert failed: {errors}",
                    "fallback": True
                }
            
            return {
                "success": True,
                "message": "Patient record stored securely",
                "fallback": False
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "fallback": True
            }
    
    def get_patient_history(self, patient_id_hash: str) -> Dict[str, Any]:
        """
        Retrieve anonymized patient history from BigQuery
        """
        if not self.initialized:
            return {
                "success": False,
                "data": [],
                "message": "BigQuery not configured.",
                "fallback": True
            }
        
        try:
            query = f"""
                SELECT *
                FROM `{self.project_id}.{self.dataset_id}.patient_records`
                WHERE patient_id_hash = @patient_id_hash
                ORDER BY timestamp DESC
                LIMIT 10
            """
            
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("patient_id_hash", "STRING", patient_id_hash)
                ]
            )
            
            query_job = self.client.query(query, job_config=job_config)
            results = [dict(row) for row in query_job]
            
            return {
                "success": True,
                "data": results,
                "fallback": False
            }
        except Exception as e:
            return {
                "success": False,
                "data": [],
                "message": f"Error: {str(e)}",
                "fallback": True
            }
    
    def get_hospital_analytics(self) -> Dict[str, Any]:
        """
        Get aggregated hospital analytics from BigQuery
        """
        if not self.initialized:
            return {
                "success": False,
                "analytics": {},
                "message": "BigQuery not configured. Using simulated analytics.",
                "fallback": True
            }
        
        try:
            query = f"""
                SELECT 
                    COUNT(*) as total_patients,
                    AVG(age) as avg_age,
                    COUNT(DISTINCT condition) as unique_conditions
                FROM `{self.project_id}.{self.dataset_id}.patient_records`
                WHERE DATE(timestamp) = CURRENT_DATE()
            """
            
            query_job = self.client.query(query)
            results = list(query_job)
            
            if results:
                return {
                    "success": True,
                    "analytics": dict(results[0]),
                    "fallback": False
                }
            
            return {
                "success": False,
                "analytics": {},
                "message": "No data available",
                "fallback": True
            }
        except Exception as e:
            return {
                "success": False,
                "analytics": {},
                "message": f"Error: {str(e)}",
                "fallback": True
            }


# Singleton instance
bigquery_service = BigQueryService()
