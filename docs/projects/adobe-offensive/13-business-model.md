# 13 - Business Model: Free Beer Apps, Metered Clouds

Date: 2026-10-11. Sources: getartcraft.com/pricing and /apps (read live),
GitHub API on org storytold (56 repos), artcraft PR #2043. Provider API list
prices quoted from memory are marked UNVERIFIED.

## 1. Two product lines, only one touches the cloud

| | Crafting Apps (PhotoCraft, VectorCraft, FilmCraft, LightCraft, PdfCraft, EffectCraft, DesignCraft, plus wordcraft, gridcraft, deckcraft, cadcraft, soundcraft repos) | ArtCraft (app.getartcraft.com + Tauri desktop) |
|---|---|---|
| What | Native Rust reimplementations of Adobe / Microsoft / Autodesk / Avid apps | AI generation studio, ~62 models |
| AI | **None from the cloud.** PhotoCraft page: offline, "On-device selection ... runs on your machine, not someone else's server" | Nano Banana 1/2/Pro, GPT-Image, Seedance, Kling, Veo, Suno, Hunyuan 3D, Marble, ... |
| Price | Free, MIT OR Apache-2.0 | Free with BYO keys/subscriptions, or credits |
| Job | Attention, trust, contributor funnel (see 11) | Revenue |

Correction to the common framing ("the apps use tons of cloud models"): the
Craft apps, as shipped, do not. The cloud bill and the revenue both sit in
ArtCraft. Reported plan (Reddit, see 01): bundle the ArtCraft model IDE inside
the Crafts later. Watch for that; it would turn every Craft install into a
credit funnel.

## 2. Licensing state (changed 2026-10-10)

- **Core artcraft relicensed from WIP Fair Source to MIT OR Apache-2.0**,
  PR #2043 "Relicense ArtCraft under MIT OR Apache-2.0", merged
  2026-10-10T08:14Z, "matching PhotoCraft, LightCraft, and the other craft"
  repos. Files 01/02/06 of this section predate this and are corrected by
  erratum.
- GitHub API 2026-10-11: every craft repo reports Apache-2.0 (dual MIT/Apache in
  the files). Exceptions: `artcraft-services` NOASSERTION, `artcraftx` and some
  infra repos no license. **The hosted backend is the remaining non-open asset.**
- Implication: the code is no longer a moat or an acquisition asset. Anyone can
  fork everything. What is ownable is the brand (NOTICE reserves name + logos),
  the hosted services, the paying customer base, the community, and the people.
  This is central to the trajectory analysis in 15.

## 3. Pricing page, observed 2026-10-11

Banner: "LIMITED-TIME OFFER - Save 20% on every plan ... ENDS SOON". Toggle
yearly (2 months free) / monthly. Trust row: cancel anytime, Stripe checkout,
**credits refunded if a generation fails**, "open source - yours forever".

| Plan | Yearly $/mo (list monthly) | Credits/mo | $/credit (yearly) |
|---|---|---|---|
| Basic | $8 ($10) | 1,000 | 0.0080 |
| Pro (most popular) | $28 ($35) | 3,750 | 0.0075 |
| Max (best value) | $48 ($60) | 6,600 | 0.0073 |
| Enterprise | custom | bespoke allocation | - (secure models, SLAs, custom integrations) |

Plus one-time credit packs that never expire (sign-in required to see prices).
Footnote, verbatim intent: usable without paying, bring your own compute and
third-party subscriptions, "we hope you'll subscribe".

### Implied per-generation prices (from the "~N per month" lines)

| Model | Credits per unit | $ at Basic yearly | Provider list price (UNVERIFIED, from memory) |
|---|---|---|---|
| Nano Banana image | ~4 | ~$0.032 | ~$0.039 (Gemini 2.5 Flash Image) |
| GPT-Image-1.5 image | ~5 | ~$0.040 | varies by size/quality |
| Nano Banana Pro image | ~15 | ~$0.12 | ~$0.13 to 0.14 at 1K/2K |
| Nano Banana Pro 4K | ~30 | ~$0.24 | ~$0.24 |
| Seedance 2.0 video | ~16 / s | ~$0.13 / s | unknown |
| Kling 3.0 Pro video | ~22 / s | ~$0.18 / s | unknown |

Reading: the credit prices sit at or near public API list prices, possibly
below on Nano Banana Pro. Gross margin per generation is thin or negative at
list. The money must come from:

1. **Breakage**: unused monthly credits. Classic subscription economics. (Packs
   never expire, so packs carry no breakage; they are goodwill.)
2. **Annual prepay float** plus urgency ("20% off, ends soon").
3. **Wholesale/aggregator rates** below list that BYOK users cannot get.
4. **Enterprise**: the only line with obvious margin (bespoke allocation,
   "secure models", SLAs).
5. Strategic, not P&L: users, data on what creators generate, distribution.

The "refund on failure" line is a pointed jab at competitors who charge for
failed generations. Cheap for him (providers often do not bill failures
either), high trust value.

## 4. The model in one sentence

Blender-style free core, Canva-Affinity-style paid AI layer, Obsidian-style
"we hope you subscribe" honesty, with no lock-in because BYOK is always allowed.
The sustainability bet is that convenience + bundled pricing + goodwill beats
the BYOK leak.

Precedent (verified 2026-10-11): Canva bought Serif/Affinity in March 2024
(~$380M reported, never confirmed) and on 2025-10-30 merged the apps into one
desktop app, "completely free, forever", offline-capable, with Canva AI
features (Generative Fill/Expand) behind a paid Canva plan. Same shape: free
pro desktop apps, paid AI. Difference: Affinity stayed closed source.

## 5. Risks to the model

- **Subsidy durability.** If credits are at list, a usage spike from 114k
  stars worth of attention is a cost spike, not a profit spike. Watch for
  quiet credit-per-generation increases or model removals.
- **Local generation commoditizes the paid layer.** Wan / FLUX / Hunyuan on a
  4090 for zero marginal cost. BYOK + local is promised; the more it works, the
  less the credits sell. (Our comfyops/videogen fleet is exactly that threat.)
- **Provider dependence.** Google (Nano Banana), ByteDance (Seedance), Kuaishou
  (Kling) can reprice or cut access. Seedance being a ByteDance model is also a
  geopolitical exposure for a US company.
- **Brand dilution.** The tagline "The open-source studio for controllable AI
  image and video" sits in the footer of offline Adobe-clone pages. Two
  audiences (AI creators, anti-AI Adobe refugees) with opposite instincts. The
  anti-AI crowd is a real slice of the jubilant Adobe-haters (see 15 section 1).
- **Relicensing removes leverage.** With everything MIT/Apache, a well-funded
  fork (or an AI lab) can ship the same apps with its own credits. The only
  defense is velocity + community + brand.

## 6. What the fleet takes from this

- If we ever charge for anything: free FOSS core, BYOK always, optional
  convenience credits priced near cost, margin from breakage/prepay/enterprise.
  Never gate the tool, meter the cloud.
- Publish credit-to-unit tables like his ("~250 Nano Banana images"). Users
  understand images and seconds, not credits.
- "Refunded on failure" is the right default for any metered agent operation.
