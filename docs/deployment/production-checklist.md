# Production Deployment Checklist

**Last Updated:** 2025-12-04

Complete checklist before deploying MCP servers to production.

---

## 🔒 Security

- [ ] HTTPS/TLS enabled with valid certificate
- [ ] API authentication implemented
- [ ] Rate limiting configured
- [ ] Input validation on all tools
- [ ] Secrets stored in environment variables (not code)
- [ ] CORS configured properly
- [ ] Firewall rules in place
- [ ] Dependencies updated to latest secure versions

---

## 📊 Monitoring

- [ ] Health check endpoint implemented
- [ ] Readiness probe configured
- [ ] Prometheus metrics exposed
- [ ] Logging configured
- [ ] Error tracking setup (Sentry, etc.)
- [ ] Alerts configured for critical issues

---

## 🧪 Testing

- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Load testing completed
- [ ] Security scanning done
- [ ] Manual testing in staging environment

---

## 🐳 Infrastructure

- [ ] Docker image built and tested
- [ ] Container health checks configured
- [ ] Resource limits set (CPU, memory)
- [ ] Restart policy configured
- [ ] Backup strategy in place
- [ ] Rollback plan documented

---

## 📝 Documentation

- [ ] README updated
- [ ] API documentation complete
- [ ] Deployment guide written
- [ ] Runbook for common issues
- [ ] Contact information for on-call

---

→ See [README.md](README.md) for complete deployment guide

