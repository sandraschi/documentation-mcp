# Arazzo Specification (1.0.1) - Overview

**Standard:** Arazzo Specification  
**Version:** 1.0.1  
**Release Date:** January 2025  
**Domain:** API Workflow Orchestration  

---

## 📖 Introduction

The Arazzo Specification is an OpenAPI Initiative standard designed to describe **workflow sequences**—chains of API calls that achieve a specific business objective. While the OpenAPI Specification (OAS) excels at documenting individual endpoints, Arazzo provides the "choreography script" for how those endpoints interact.

In the MCP ecosystem, Arazzo acts as the glue that transforms a collection of individual tools into deterministic, reliable agentic workflows.

## 🏗️ Core Components

### 1. Arazzo Description
A document (YAML or JSON) that defines the workflows. It must specify the `arazzo` version (e.g., `1.0.1`).

### 2. Source Descriptions
References to external API definitions (typically OpenAPI files) or other Arazzo documents. This allows workflows to reuse existing schemas and operation IDs.

### 3. Workflows
The high-level use cases. Each workflow contains:
- **Inputs**: JSON schemas for initial data.
- **Steps**: An ordered list of activities.
- **Outputs**: Results of the workflow.

### 4. Steps
Individual actions within a workflow. A step can:
- Call an API operation (defined in a Source Description).
- Reference another local or external workflow.
- Execute conditional logic (success/failure actions).

## 🚀 Key Features (v1.0.1)

- **Dynamic Parameters**: Pass data between steps using expressions (e.g., `$outputs.step1.id`).
- **Success/Failure Actions**: Define branching logic based on response codes or content.
- **Language Agnostic**: Workflows can be executed by any engine (e.g., `arazzo-runner`).
- **AI-Ready**: Designed to be both human-readable and machine-readable, making it ideal for LLM-based agents.

## 🛠️ Tooling Ecosystem

- **[arazzo-runner](https://github.com/AdrianMachado/arazzo-runner)**: Official Python library and CLI for executing workflows.
- **[arazzo-engine](https://github.com/jentic/arazzo-engine)**: Comprehensive implementation including a runner and an AI-powered workflow generator.

---

## 🎓 Relevance to MCP

MCP servers provide tools. Arazzo provides the **sequences** for those tools. By exposing Arazzo descriptions, an MCP server can teach an agent exactly how to perform complex tasks (e.g., "Create a Unity scene, import an avatar, and start an animation") without relying on fragile prompts.
