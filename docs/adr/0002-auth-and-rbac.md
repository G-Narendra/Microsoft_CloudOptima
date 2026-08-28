# ADR 0002: Authentication and RBAC via Entra ID

## Status
Accepted

## Context
The CloudOptima dashboard allows users to generate cloud architectures and provision infrastructure (e.g., Bicep templates). Without authentication and authorization, any user who accesses the dashboard can run expensive AI models, exhausting API credits, and potentially deploy unauthorized infrastructure. We need a robust identity and access management solution that meets enterprise standards.

## Decision
We will implement Authentication and Role-Based Access Control (RBAC) using **Microsoft Entra ID (OIDC)**.
- Streamlit's native OIDC integration (`st.login`, `st.user`) will be used to authenticate users against a registered Entra ID application.
- We will leverage Entra ID Security Groups to define roles (`ArchitectsGroup`, `AdminGroup`, `ReviewersGroup`).
- The dashboard will map these groups to application roles (`admin`, `reviewer`, `viewer`).
- A Human-in-the-Loop (HITL) gate will block artifact generation until a user with the `admin` or `reviewer` role explicitly approves the design.

## Consequences
- **Positive**: Secures the application against unauthorized use. Implements strict governance for infrastructure deployment. Leverages enterprise identity.
- **Negative**: Requires setting up an Entra ID App Registration, which adds complexity for local development. Handled by an `auth_enabled` toggle to bypass in local dev.
