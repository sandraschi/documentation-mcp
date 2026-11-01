# SQL for Relational Truth: The SOTA 2026 Standard

**Standard**: PostgreSQL 16+ (Mandatory)
**Context**: "ACID Guarantees"
**Role**: Primary Data Store / Analytical Engine / Vector DB (`pgvector`)
**Linting**: `sqlfluff`

> [!IMPORTANT]
> **"Butter bei die Fische"**: This document serves as the **Single Source of Truth** for SQL usage within the Antigravity ecosystem. It integrates global knowledge (Wikipedia) with specific local operational standards (SOTA 2026).

---

## 📑 Table of Contents

1.  [Executive Summary](#executive-summary)
2.  [The Antigravity SQL Standard](#the-antigravity-sql-standard)
    *   [CTEs (Common Table Expressions)](#ctes-common-table-expressions)
    *   [JSONB (Schemaless Documents)](#jsonb-schemaless-documents)
    *   [Window Functions](#window-functions)
3.  [Global Context: SQL Evolution](#global-context-sql-evolution)
    *   [History: Edgar F. Codd (1970)](#history-edgar-f-codd-1970)
    *   [The NoSQL War & Resulting Convergence](#the-nosql-war--resulting-convergence)
4.  [Fleet Integration Patterns](#fleet-integration-patterns)
    *   [TimescaleDB (Telemetry)](#timescaledb-telemetry)
    *   [PostGIS (Geospatial)](#postgis-geospatial)
    *   [pgvector (Semantic Search)](#pgvector-semantic-search)
5.  [Advanced Patterns](#advanced-patterns)
    *   [Recursive Queries (Graph Traversal)](#recursive-queries-graph-traversal)
    *   [Lateral Joins](#lateral-joins)
    *   [Materialized Views](#materialized-views)
6.  [Security Best Practices](#security-best-practices)
7.  [Reference Material](#reference-material)

---

## 1. Executive Summary

In the **Antigravity Fleet**, SQL is the **Store of Record**.
For 99% of data that matters (user accounts, billing, robot inventory), we trust PostgreSQL.
It is the boring solution that lets us sleep at night.

**Why SQL for SOTA 2026?**
-   **Reliability**: ACID transactions mean we don't lose data when power fails.
-   **Flexibility**: JSONB allows us to store unstructured robot logs alongside structured metadata.
-   **Ecosystem**: PostGIS handles our maps. `pgvector` handles our LLM embeddings. One database to rule them all.

---

## 2. The Antigravity SQL Standard

### CTEs (Common Table Expressions)

We ban nested subqueries. They are unreadable.
Use `WITH` clauses to build logic step-by-step.

```sql
WITH robot_stats AS (
    SELECT robot_id, AVG(battery_level) as avg_bat
    FROM telemetry
    WHERE timestamp > NOW() - INTERVAL '1 hour'
    GROUP BY robot_id
)
SELECT * FROM robots
JOIN robot_stats ON robots.id = robot_stats.robot_id
WHERE avg_bat < 20;
```

### JSONB (Schemaless Documents)

Use `jsonb` (binary JSON) for high-performance indexing of unstructured data.
Use `@>` (contains) operator.

```sql
SELECT * FROM sensors
WHERE payload @> '{"type": "lidar", "status": "error"}';
```

### Window Functions

Calculate moving averages or dense ranks without leaving the database.

```sql
SELECT 
    timestamp,
    battery_level,
    AVG(battery_level) OVER (
        PARTITION BY robot_id 
        ORDER BY timestamp 
        ROWS BETWEEN 10 PRECEDING AND CURRENT ROW
    ) as moving_avg
FROM telemetry;
```

---

## 3. Global Context: SQL Evolution

*(Ingested from Wikipedia Research)*

### History: Edgar F. Codd (1970)
Based on relational algebra. Codd's paper "A Relational Model of Data for Large Shared Data Banks" changed the world.
Standardized by ANSI in 1986.

### The NoSQL War & Resulting Convergence
In the 2010s, NoSQL (Mongo, Cassandra) rose due to scale issues.
SQL databases responded by adding JSON support (JSONB) and sharding features.
Today, Postgres creates a "NewSQL" reality: Scalable AND Relational.

---

## 4. Fleet Integration Patterns

### TimescaleDB (Telemetry)

We use the TimescaleDB extension on Postgres to handle time-series data (robot sensor logs). It partitions data automatically by time.

### PostGIS (Geospatial)

The gold standard for maps.
`ST_DWithin(robot_loc, target_loc, 10.0)` determines if a robot has reached its goal.

### pgvector (Semantic Search)

We store embeddings of robot camera frames in Postgres.
`ORDER BY embedding <-> query_embedding LIMIT 5` finds visually similar scenarios.

---

## 5. Advanced Patterns

### Recursive Queries (Graph Traversal)

Used for traversing hierarchical structures (like component parts lists).

```sql
WITH RECURSIVE parts_tree AS (
    SELECT id, parent_id, name FROM parts WHERE id = 1
    UNION ALL
    SELECT p.id, p.parent_id, p.name 
    FROM parts p
    JOIN parts_tree t ON p.parent_id = t.id
)
SELECT * FROM parts_tree;
```

### Lateral Joins

Apply a subquery for each row. Powerful for "top-N-per-category" queries.

```sql
SELECT robots.name, latest_log.msg
FROM robots
LEFT JOIN LATERAL (
    SELECT msg FROM logs WHERE robot_id = robots.id ORDER BY time DESC LIMIT 1
) AS latest_log ON true;
```

---

## 6. Security Best Practices

1.  **SQL Injection**: NEVER assemble SQL strings. Always use parameterized queries (`$1`, `$2`).
2.  **Least Privilege**: The application user should not be `postgres` superuser. It should only have `SELECT, INSERT, UPDATE` on specific tables.

---

## 7. Reference Material

-   [PostgreSQL Documentation](https://www.postgresql.org/docs/)
-   [Use The Index, Luke](https://use-the-index-luke.com/)
-   [PostGIS Manual](https://postgis.net/documentation/)

---

**Maintainer:** Sandra S.
**Last Updated:** 2026-02-13
**Status**: SOTA 2026 Compliant
