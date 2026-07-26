# Apple publishing: App Store and distribution (May 2026)

Practical submission layer for iOS, iPadOS, macOS, and visionOS. For **install paths, marketplaces, IAP models, and commission**, start with **[ios/DISTRIBUTION_AND_MONETIZATION.md](../ios/DISTRIBUTION_AND_MONETIZATION.md)**.

---

## Accounts and costs

| Item | Cost | Notes |
|------|------|-------|
| **Apple Developer Program** | **$99 USD / year** | Required for TestFlight + App Store |
| **App Store listing** | Included | No per-app listing fee (unlike Steam Direct $100/title) |
| **TestFlight** | Included | Internal + external beta |

Free Apple ID alone: Xcode + Simulator + 7-day device installs only.

---

## Distribution channels

| Channel | Use |
|---------|-----|
| **App Store Connect** | Production releases, IAP configuration, analytics |
| **TestFlight** | Beta — internal (team) or external (public link, beta review) |
| **Xcode direct install** | Dev devices during agentic development |
| **Mac App Store** | macOS apps (same program) |
| **Notarized direct (macOS)** | DMG/pkg outside Mac App Store — enterprise or direct download |
| **EU alternative marketplaces** | Optional under DMA — extra signing/notarization rules; fleet default remains App Store |

---

## New project targets (2026)

- **Xcode 26.x** with **iOS 26** SDK for new apps (match `apple-test` scaffold)
- Older deployment targets allowed if supporting legacy devices — document minimum in App Store Connect

---

## Privacy and compliance

### Privacy manifest

Required when using certain APIs (UserDefaults, file timestamp, etc.) or third-party SDKs that require declarations.

- Doc: [Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files)
- VRM dance apps: declare network (Hub OAuth), file storage (VRM cache), Keychain

### App Privacy (Nutrition labels)

App Store Connect questionnaire — accurate data collection disclosure for Hub login, analytics, crash reporting.

### AI disclosure (2026)

- **Apple Intelligence / Foundation Models** in-app: follow Apple’s current guidelines
- **Third-party cloud LLMs** (OpenAI, Anthropic APIs in shipped app): disclose in privacy label + review notes
- **Xcode agentic coding** at dev time does not require disclosure in the shipped app

### VRoid Hub / user content

- Explain in review notes: app loads user-authorized Hub avatars
- Provide **sandbox Hub test account** for App Review if login-gated
- Respect per-model license metadata — commercial use flags in VRM

---

## In-App Purchase (StoreKit 2)

Configure in **App Store Connect** before implementation:

1. Create IAP products (consumable / non-consumable / subscription)
2. Add StoreKit configuration file in Xcode for Simulator testing
3. Use StoreKit 2 APIs in Swift
4. Submit IAP screenshots/metadata if required

Commission: **30%** standard; **15%** [Small Business Program](https://developer.apple.com/app-store/small-business-program/) if eligible.

Dance-app pattern: free app + consumable/non-consumable dance packs — see [DISTRIBUTION_AND_MONETIZATION.md](../ios/DISTRIBUTION_AND_MONETIZATION.md).

---

## Review workflow

1. Archive in Xcode (**Product → Archive**)
2. **Distribute App → App Store Connect**
3. Select build in Connect → add metadata → submit for review
4. Typical review: **24–48 hours** (varies)

Common rejection themes for avatar apps: missing login demo account, unclear IAP value, privacy label mismatch, copyrighted character content without rights.

---

## Agentic publishing (Xcode 26.3)

Agents can drive archive/upload steps when Xcode project is open and credentials configured — but **App Store Connect legal agreements** and **IAP business decisions** remain human.

See [development/AGENTIC_XCODE_26.md](../development/AGENTIC_XCODE_26.md).

---

## Deployment checklist

- [ ] Developer Program membership active
- [ ] Bundle ID + signing team in Xcode
- [ ] Privacy manifest + App Privacy questionnaire complete
- [ ] IAP products created (if monetizing)
- [ ] Hub OAuth redirect URI matches production bundle URL scheme
- [ ] TestFlight internal pass before external/public
- [ ] Review notes + demo account for gated features

---

## References

- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [App Store Connect Help](https://developer.apple.com/help/app-store-connect/)
- [StoreKit 2](https://developer.apple.com/documentation/storekit)
- [TestFlight Overview](https://developer.apple.com/testflight/)

---
*Last updated: 2026-05-28*
