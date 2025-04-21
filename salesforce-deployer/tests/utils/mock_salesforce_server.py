#!/usr/bin/env python3
"""
Mock Salesforce API server for testing Salesforce Schema Deployer
without connecting to a real Salesforce organization.
"""

import json
import os
import sys
import argparse
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, Any, List, Optional, Tuple
import threading
import uuid
import re

class MockSalesforceState:
    """Represents the state of the mock Salesforce org."""
    
    def __init__(self):
        """Initialize the mock state with default values."""
        self.api_version = "54.0"
        self.objects = {}  # Custom objects
        self.fields = {}   # Custom fields by object
        self.workflows = {}  # Workflow rules
        self.deployment_ids = {}  # Deployment IDs to status mapping
        
        # Simulate standard objects
        self.standard_objects = ["Account", "Contact", "Opportunity", "Case", "User"]
        for obj in self.standard_objects:
            self.objects[obj] = {
                "name": obj,
                "label": obj,
                "isCustom": False
            }
            self.fields[obj] = {}
        
        # Session information
        self.access_token = f"00D{uuid.uuid4().hex[:15]}!{uuid.uuid4().hex[:65]}"
        self.instance_url = "https://mock-instance.salesforce.com"
        self.token_timestamp = time.time()
        self.token_lifetime = 7200  # 2 hours
    
    def is_token_valid(self) -> bool:
        """Check if the access token is still valid."""
        return (time.time() - self.token_timestamp) < self.token_lifetime
    
    def refresh_token(self) -> None:
        """Generate a new access token."""
        self.access_token = f"00D{uuid.uuid4().hex[:15]}!{uuid.uuid4().hex[:65]}"
        self.token_timestamp = time.time()
    
    def start_deployment(self, metadata: Dict[str, Any]) -> str:
        """Start a new deployment and return the deployment ID."""
        deployment_id = uuid.uuid4().hex
        self.deployment_ids[deployment_id] = {
            "status": "InProgress",
            "startTime": time.time(),
            "metadata": metadata,
            "messages": []
        }
        return deployment_id
    
    def complete_deployment(self, deployment_id: str, success: bool = True) -> None:
        """Mark a deployment as complete."""
        if deployment_id in self.deployment_ids:
            self.deployment_ids[deployment_id]["status"] = "Succeeded" if success else "Failed"
            self.deployment_ids[deployment_id]["endTime"] = time.time()
            
            if success:
                # Actually apply the changes to our mock state
                metadata = self.deployment_ids[deployment_id]["metadata"]
                self._apply_metadata_changes(metadata)
                self.deployment_ids[deployment_id]["messages"].append({
                    "type": "Info",
                    "message": "Deployment completed successfully"
                })
            else:
                self.deployment_ids[deployment_id]["messages"].append({
                    "type": "Error",
                    "message": "Deployment failed due to validation errors"
                })
    
    def _apply_metadata_changes(self, metadata: Dict[str, Any]) -> None:
        """Apply metadata changes to the mock state."""
        # Process custom objects
        if "objects" in metadata:
            for obj in metadata["objects"]:
                obj_name = obj["name"]
                self.objects[obj_name] = obj
                
                # Initialize fields for this object if needed
                if obj_name not in self.fields:
                    self.fields[obj_name] = {}
                
                # Process fields for this object
                if "fields" in obj:
                    for field in obj["fields"]:
                        field_name = field["name"]
                        self.fields[obj_name][field_name] = field
        
        # Process workflows
        if "workflows" in metadata:
            for workflow in metadata["workflows"]:
                wf_name = workflow["name"]
                self.workflows[wf_name] = workflow

class MockSalesforceHandler(BaseHTTPRequestHandler):
    """HTTP request handler for mock Salesforce API."""
    
    # Class variable to store the shared state
    state = None
    
    def log_message(self, format, *args):
        """Override to customize logging."""
        sys.stderr.write(f"[MockSF] {self.client_address[0]} - {format % args}\n")
    
    def _send_json_response(self, data: Dict[str, Any], status: int = 200) -> None:
        """Send a JSON response with the given status code."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _parse_json_request(self) -> Dict[str, Any]:
        """Parse the JSON request body."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests."""
        # OAuth token endpoint
        if self.path == "/services/oauth2/token":
            self._handle_oauth_token()
        # Metadata API deploy endpoint
        elif self.path.startswith("/services/data/v") and "/metadata/deployments" in self.path:
            self._handle_metadata_deploy()
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_GET(self):
        """Handle GET requests."""
        # Deployment status endpoint
        deployment_pattern = r"/services/data/v.+/metadata/deployments/([a-z0-9]+)"
        match = re.match(deployment_pattern, self.path)
        if match:
            deployment_id = match.group(1)
            self._handle_deployment_status(deployment_id)
        # Describe API
        elif "/sobjects/" in self.path and "/describe" in self.path:
            self._handle_object_describe()
        # API versions
        elif self.path == "/services/data/":
            self._handle_api_versions()
        else:
            self.send_error(404, "Endpoint not found")
    
    def _handle_oauth_token(self):
        """Handle OAuth token request."""
        try:
            data = self._parse_json_request()
            grant_type = data.get("grant_type")
            
            if grant_type == "password":
                # Username/password flow
                username = data.get("username")
                password = data.get("password")
                client_id = data.get("client_id")
                client_secret = data.get("client_secret")
                
                # In a real implementation, validate these credentials
                # For mock, accept anything that's not empty
                if username and password and client_id:
                    self.state.refresh_token()
                    response = {
                        "access_token": self.state.access_token,
                        "instance_url": self.state.instance_url,
                        "id": f"{self.state.instance_url}/id/00D000000000123ABC/005000000000123ABC",
                        "token_type": "Bearer",
                        "issued_at": str(int(self.state.token_timestamp * 1000))
                    }
                    self._send_json_response(response)
                else:
                    self._send_json_response({
                        "error": "invalid_grant",
                        "error_description": "Invalid username, password, security token, or user locked out."
                    }, 400)
            else:
                self._send_json_response({
                    "error": "unsupported_grant_type",
                    "error_description": "grant type not supported"
                }, 400)
        except Exception as e:
            self._send_json_response({
                "error": "server_error",
                "error_description": str(e)
            }, 500)
    
    def _handle_metadata_deploy(self):
        """Handle metadata deployment request."""
        try:
            # Validate authorization header
            auth_header = self.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                self._send_json_response({
                    "error": "invalid_session_id",
                    "error_description": "Session expired or invalid"
                }, 401)
                return
            
            token = auth_header[7:]  # Remove 'Bearer ' prefix
            if token != self.state.access_token or not self.state.is_token_valid():
                self._send_json_response({
                    "error": "invalid_session_id",
                    "error_description": "Session expired or invalid"
                }, 401)
                return
            
            # Process the deployment request
            data = self._parse_json_request()
            metadata = data.get("metadata", {})
            
            # Start a deployment and return the ID
            deployment_id = self.state.start_deployment(metadata)
            
            # Simulate async deployment - complete it in a background thread
            def complete_deployment():
                time.sleep(2)  # Simulate processing time
                
                # Simple validation
                success = True
                for obj in metadata.get("objects", []):
                    if not obj.get("name") or not obj.get("label"):
                        success = False
                        break
                
                self.state.complete_deployment(deployment_id, success)
            
            threading.Thread(target=complete_deployment).start()
            
            # Return the deployment ID
            self._send_json_response({
                "id": deployment_id,
                "status": "InProgress",
                "startTime": self.state.deployment_ids[deployment_id]["startTime"],
                "done": False
            })
        except Exception as e:
            self._send_json_response({
                "error": "server_error",
                "error_description": str(e)
            }, 500)
    
    def _handle_deployment_status(self, deployment_id: str):
        """Handle deployment status check."""
        try:
            # Validate authorization
            auth_header = self.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                self._send_json_response({
                    "error": "invalid_session_id",
                    "error_description": "Session expired or invalid"
                }, 401)
                return
            
            token = auth_header[7:]  # Remove 'Bearer ' prefix
            if token != self.state.access_token or not self.state.is_token_valid():
                self._send_json_response({
                    "error": "invalid_session_id",
                    "error_description": "Session expired or invalid"
                }, 401)
                return
            
            # Check if the deployment exists
            if deployment_id not in self.state.deployment_ids:
                self._send_json_response({
                    "error": "not_found",
                    "error_description": f"Deployment {deployment_id} not found"
                }, 404)
                return
            
            # Return the deployment status
            deployment = self.state.deployment_ids[deployment_id]
            done = deployment["status"] in ["Succeeded", "Failed", "Canceled"]
            
            response = {
                "id": deployment_id,
                "status": deployment["status"],
                "startTime": deployment["startTime"],
                "done": done
            }
            
            if done:
                response["endTime"] = deployment.get("endTime")
                response["success"] = deployment["status"] == "Succeeded"
                response["messages"] = deployment["messages"]
            
            self._send_json_response(response)
        except Exception as e:
            self._send_json_response({
                "error": "server_error",
                "error_description": str(e)
            }, 500)
    
    def _handle_object_describe(self):
        """Handle object describe request."""
        try:
            # Extract object name from URL
            match = re.search(r"/sobjects/([^/]+)/describe", self.path)
            if not match:
                self._send_json_response({
                    "error": "not_found",
                    "error_description": "Object not found"
                }, 404)
                return
            
            obj_name = match.group(1)
            
            # Check if the object exists
            if obj_name not in self.state.objects:
                self._send_json_response({
                    "error": "not_found",
                    "error_description": f"Object {obj_name} not found"
                }, 404)
                return
            
            # Build the describe response
            obj = self.state.objects[obj_name]
            fields = self.state.fields.get(obj_name, {})
            
            response = {
                "name": obj["name"],
                "label": obj["label"],
                "fields": [
                    {
                        "name": field_name,
                        "label": field.get("label", field_name),
                        "type": field.get("type", "String"),
                        "custom": field_name.endswith("__c"),
                        "nillable": not field.get("required", False)
                    } for field_name, field in fields.items()
                ]
            }
            
            self._send_json_response(response)
        except Exception as e:
            self._send_json_response({
                "error": "server_error",
                "error_description": str(e)
            }, 500)
    
    def _handle_api_versions(self):
        """Handle API versions request."""
        versions = [
            {"version": "54.0", "label": "Winter '22", "url": "/services/data/v54.0"},
            {"version": "53.0", "label": "Summer '21", "url": "/services/data/v53.0"},
            {"version": "52.0", "label": "Spring '21", "url": "/services/data/v52.0"}
        ]
        self._send_json_response(versions)


def run_server(port: int = 8000):
    """Run the mock Salesforce server."""
    server_address = ('', port)
    
    # Create shared state
    MockSalesforceHandler.state = MockSalesforceState()
    
    httpd = HTTPServer(server_address, MockSalesforceHandler)
    print(f"Starting mock Salesforce server on port {port}...")
    print(f"Mock instance URL: {MockSalesforceHandler.state.instance_url}")
    print(f"Initial access token: {MockSalesforceHandler.state.access_token}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a mock Salesforce API server for testing")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    
    run_server(args.port)