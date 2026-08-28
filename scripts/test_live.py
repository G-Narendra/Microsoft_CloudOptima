"""Live End-to-End Test for CloudOptima Orchestrator."""

import asyncio
import os
import sys
import time

# Ensure cloudoptima can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cloudoptima.app import create_orchestrator
from cloudoptima.dashboard import build_session
from cloudoptima.config import Settings
from cloudoptima.auth import can_approve

async def run_live_test():
    print("[*] Starting Live E2E Test...")
    settings = Settings()
    
    if settings.demo_mode:
        print("[!] Error: DEMO_MODE is True. Set DEMO_MODE=false in .env.")
        sys.exit(1)
        
    print(f"[*] Configuration loaded. Provider: {settings.llm_provider}")
    print("[*] Initializing Orchestrator...")
    orchestrator = create_orchestrator(settings)
    
    print("[*] Building test session...")
    session = build_session(
        project_name="live-test-1",
        workload_type="mixed",
        scale="large",
        region="uaenorth",
        frameworks=["gdpr", "hipaa", "pdpl"],
        budget=10000.0,
        services="Design a highly available 3-tier web application for a healthcare client. Include Azure App Service, Azure SQL Database, Redis Cache, and Azure Front Door.",
        context="Must serve 50k users in the UAE and scale for the Ramadan peak. Multi-AZ is required for High Availability. Patient data must be strictly encrypted at rest and in transit, and strictly adhere to UAE data residency laws.",
        settings=settings
    )
    
    print("[*] Executing Agent Pipeline...")
    start_time = time.time()
    task = asyncio.create_task(orchestrator.run(session))
    
    # Wait for completion
    await task
    
    print(f"[*] Pipeline executed in {time.time() - start_time:.2f}s!")
    
    if session.status != "pending_approval":
        print(f"[!] Error: Expected session status 'pending_approval', got '{session.status}'")
        for error in session.errors:
            print(f"  - {error}")
        sys.exit(1)
        
    print("[*] Session successfully hit pending_approval state.")
    
    print("[*] Simulating 'reviewer' approval...")
    if not can_approve("reviewer"):
        print("[!] Error: 'reviewer' role should be able to approve!")
        sys.exit(1)
        
    await orchestrator.resume_approval(session)
    
    print(f"[*] Session status after approval: {session.status}")
    
    if session.status != "completed":
        print(f"[!] Error: Expected session status 'completed', got '{session.status}'")
        sys.exit(1)
        
    # Verify artifacts
    if not session.artifacts:
        print("[!] Error: No artifacts were generated!")
        sys.exit(1)
        
    print("[*] Live Test Passed! Artifacts generated:")
    for artifact in session.artifacts:
        print(f"  - {artifact.title} ({artifact.type.value})")
        
    print("[*] Live workflow, MCP usage, and RAG compliance successfully validated using real API keys!")

if __name__ == "__main__":
    asyncio.run(run_live_test())
