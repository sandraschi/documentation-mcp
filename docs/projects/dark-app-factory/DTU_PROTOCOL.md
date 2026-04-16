# Digital Twin Universe (DTU) Protocol

The **Digital Twin Universe** is a local-first mock server pattern that enables the **Satisficer (Judge)** to audit applications without external dependencies.

## 1. The Pattern
Industrial Digital Twins are virtual replicas of physical assets. In DAF, the DTU is a virtual replica of the **Entire Internet Economy** (Stripe, Discord, Auth, Email).

## 2. Environment Var Injection
The `Plumber` specialist is mandated to read API base URLs from environment variables rather than hardcoding.
- **Production**: `STRIPE_API_URL=https://api.stripe.com`
- **Testing**: `STRIPE_API_URL=http://localhost:8001/stripe`

### Supported Mocks
- **Stripe**: `/stripe/v1/payment_intents` (Always succeeds).
- **Auth**: `/auth/login` (Returns valid mock JWT).
- **Email/SMS**: `/email/send` (Logs request, returns success).
- **AI**: `/ai/generate` (Mock LLM response for testing flow).

## 3. Auditing with the Satisficer
When the `Satisficer` (Judge) boots the app via Playwright:
1. It starts the DTU on port 8001.
2. It injects the `DTU_URL` into the app's environment.
3. It performs UI actions (e.g., "Click Pay").
4. The app calls `localhost:8001/stripe`.
5. DTU logs the call and returns 200 OK.
6. The Judge queries `localhost:8001/dtu/log` to verify that the pay attempt actually happened.

## 4. Benefit
- **Zero Cost**: No real API tokens burned during build-loops.
- **Zero Friction**: Tests pass even on a plane (offline).
- **Zero Risk**: No chance of accidentally hitting a production endpoint.
