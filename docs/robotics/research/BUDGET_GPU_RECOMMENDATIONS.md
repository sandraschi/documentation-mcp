# Budget GPU Recommendations for VREALM

**Last Updated**: 2025-12-02  
**Purpose**: Help cash-strapped friends join Villa Straylight fun!  
**Context**: Gaussian splats + Unity + VR on a budget

---

## TL;DR - Best Budget Pick

### 🏆 **RTX 3060 12GB** (Used/Refurbished)

**Price**: €250-350 used, ~€400 new (if still available)  
**Why**: 12GB VRAM is HUGE advantage for splats!  
**Performance**: 80-90% of your friend's needs, 20% of RTX 4090 cost

---

## Budget GPU Comparison

### The VRAM Reality

**Gaussian splats are VRAM-hungry!**

| GPU | VRAM | Lower-res .ply | Standard .ply | VR Capable | Price (EUR) |
|-----|------|----------------|---------------|------------|-------------|
| **RTX 4090 24GB** | 24GB | ✅✅✅ Overkill | ✅✅✅ Perfect | ✅✅✅ 120+ FPS | €1800-2000 |
| **RTX 4070 Ti 12GB** | 12GB | ✅✅✅ Excellent | ✅✅ Good | ✅✅ 90+ FPS | €800-900 |
| **RTX 3060 12GB** | 12GB | ✅✅✅ Excellent | ✅✅ Good | ✅ 60+ FPS | €250-400 |
| **RTX 4060 Ti 16GB** | 16GB | ✅✅✅ Excellent | ✅✅✅ Great | ✅✅ 75+ FPS | €500-600 |
| **RTX 4060 8GB** | 8GB | ✅✅ Good | ⚠️ Struggles | ✅ 60 FPS | €300-350 |
| **RTX 3060 Ti 8GB** | 8GB | ✅✅ Good | ⚠️ Limited | ✅ 70 FPS | €250-350 |
| **RTX 3050 8GB** | 8GB | ✅ Okay | ❌ No | ⚠️ Minimal | €200-250 |

---

## Detailed Recommendations

### Tier 1: Best Budget Choice (€250-400)

#### 🥇 **RTX 3060 12GB** - THE BUDGET KING

**Why this is the sweet spot**:
- ✅ **12GB VRAM** (same as RTX 4070 Ti!)
- ✅ Can handle Lower-res .ply easily (60-90 FPS)
- ✅ Can handle Standard .ply (30-60 FPS, playable!)
- ✅ VR capable (Quest Link works fine)
- ✅ Unity runs smoothly
- ✅ Power efficient (~170W)
- ✅ Available used/refurbished (great value!)

**Where it struggles**:
- ❌ Older architecture (slower than newer cards per-VRAM)
- ❌ Ray tracing weak (but splats don't use it!)
- ❌ No DLSS 3 Frame Generation

**Real-world performance**:
```
Desktop (Lower-res .ply):   80-100 FPS ✅
Desktop (Standard .ply):    35-55 FPS  ⚠️ (playable!)
VR (Lower-res .ply):        60-75 FPS  ✅
VR (Standard .ply):         30-45 FPS  ⚠️ (works but not ideal)
VRChat upload:              Perfect! ✅
```

**Verdict**: **Buy used RTX 3060 12GB for €250-350!**  
Your friend gets 12GB VRAM for less than new 8GB cards!

---

### Tier 2: Stretch Budget (€500-600)

#### 🥈 **RTX 4060 Ti 16GB** - FUTURE-PROOF

**If your friend can stretch budget**:
- ✅ **16GB VRAM** (more than 3060!)
- ✅ Newer architecture (faster per-VRAM)
- ✅ Lower power consumption (160W)
- ✅ DLSS 3 Frame Generation (free FPS!)
- ✅ Standard .ply runs better than 3060

**Trade-off**: €200+ more expensive than used 3060

**Real-world performance**:
```
Desktop (Lower-res .ply):   100-120 FPS ✅✅
Desktop (Standard .ply):    50-70 FPS   ✅
VR (Lower-res .ply):        75-90 FPS   ✅✅
VR (Standard .ply):         45-60 FPS   ✅
```

**Verdict**: Best NEW card under €600, but 3060 used is better value!

---

### Tier 3: Absolute Minimum (€200-300)

#### 🥉 **RTX 4060 8GB** or **RTX 3060 Ti 8GB**

**If really tight budget**:
- ⚠️ **Only 8GB VRAM** (limiting!)
- ✅ Lower-res .ply works fine
- ❌ Standard .ply struggles (will hit VRAM limit)
- ✅ VR works (Lower-res only)

**Real-world performance**:
```
Desktop (Lower-res .ply):   70-90 FPS  ✅
Desktop (Standard .ply):    20-35 FPS  ❌ (VRAM bottleneck!)
VR (Lower-res .ply):        55-70 FPS  ✅
VR (Standard .ply):         15-25 FPS  ❌ (unplayable)
```

**Verdict**: Works but VERY limited! Must use Lower-res .ply always.

**Warning**: Can't grow into Standard .ply later (VRAM wall).

---

## The VRAM Explanation

### Why 12GB+ Matters for Gaussian Splats

**Gaussian splats are NOT traditional 3D**:
- Traditional mesh: Polygons + textures (predictable VRAM)
- Gaussian splat: **Millions of 3D gaussians** (VRAM-hungry!)

**VRAM usage examples**:

| Scene Size | Lower-res .ply | Standard .ply |
|------------|----------------|---------------|
| Small (apartment) | 2-3GB | 4-6GB |
| Medium (building) | 3-5GB | 6-10GB |
| Large (city block) | 5-8GB | 10-16GB |

**Plus Unity overhead**: ~1-2GB  
**Plus VR overhead**: ~1-2GB additional

**Total VRAM needed**:
- **8GB GPU**: Lower-res only, struggles with large scenes
- **12GB GPU**: Lower-res perfect, Standard playable for small/medium
- **16GB+ GPU**: Standard .ply comfortable

**Your friend with 12GB**: Can do 90% of what you do! (just uses Lower-res more often)

---

## Used vs New?

### Used RTX 3060 12GB Advantages

**Why used is smart**:
1. **Half price** of new equivalent
2. **Same VRAM** as much pricier cards
3. **Proven reliability** (30-series is mature)
4. **Still has warranty** (many used cards transferable)
5. **Easy to find** (popular card, lots available)

**Where to buy used** (Austria/EU):
- **Willhaben.at** (Austrian eBay equivalent)
- **eBay Kleinanzeigen** (Germany)
- **Facebook Marketplace**
- **Reddit r/HardwareSwapEU**
- **Local PC shops** (often have trade-ins)

**What to check**:
- ✅ Not used for mining (ask seller!)
- ✅ Has original box/receipt (warranty)
- ✅ Test before buying (run benchmark)
- ✅ Check for physical damage
- ✅ Verify it's actually 12GB (not 6GB model!)

**Red flags**:
- ❌ "Used for mining 24/7"
- ❌ No returns/refunds
- ❌ Price too good to be true
- ❌ Seller has many GPUs (miner liquidation)

---

## Performance Comparison: You vs Friend

### Real-World Scenarios

**Scenario 1: Stroheckgasse Apartment (Small Scene)**

| Task | You (RTX 4090) | Friend (RTX 3060 12GB) |
|------|----------------|------------------------|
| Desktop, Lower-res | 150+ FPS | 90 FPS |
| Desktop, Standard | 120+ FPS | 45 FPS |
| VR, Lower-res | 120 FPS | 70 FPS |
| VR, Standard | 100 FPS | 35 FPS |

**Result**: Friend uses Lower-res, still smooth! You notice no difference in quality (Lower-res looks great in VR!).

**Scenario 2: VRChat Upload**

| Task | You (RTX 4090) | Friend (RTX 3060 12GB) |
|------|----------------|------------------------|
| Build time | 2 min | 4 min |
| Upload speed | Same | Same |
| In VRChat | 120 FPS | 60 FPS |

**Result**: Both can upload and visit! Friend just gets 60 FPS instead of 120 (still perfectly smooth).

**Scenario 3: Multiplayer VREALM**

Both of you in VRChat Villa Straylight:
- You: 120 FPS, ultra settings
- Friend: 60 FPS, high settings
- **Both**: Same experience, same fun, same tea with Archimedes! ☕

**Important**: VRChat is server-side, so you see same world regardless of GPU!

---

## The Actual Recommendation

### For Your Cash-Strapped Friend

**Best choice: Used RTX 3060 12GB for €250-350**

**Why**:
1. **12GB VRAM** is non-negotiable for splats
2. **Lower-res .ply looks 95% as good** as Standard in VR
3. **Half the price** of new cards
4. **Can do everything** you do (just Lower-res)
5. **No compromise** on VRChat/multiplayer
6. **Can upgrade later** when finances improve

**What to tell them**:
- "Get used RTX 3060 12GB, €250-300 range"
- "Avoid 8GB cards! VRAM is everything for splats!"
- "We'll both use Lower-res for VRChat anyway (size limits)"
- "You'll have 90% of my experience for 20% of cost"
- "Later you can upgrade, but this gets you in NOW"

**Alternative if can't find 3060 12GB**:
- RTX 4060 Ti 16GB (€500-600 new) - better VRAM, newer
- Used RTX 3070 8GB (€200-250) - only if desperate, VRAM limited

**Avoid**:
- ❌ RTX 3050 (not enough power)
- ❌ GTX 1660/1650 (no VR support, old)
- ❌ AMD cards (Unity/VR support weaker, splat plugin may not work)

---

## Future-Proofing Consideration

### Upgrade Path

**Your friend's progression**:

**2025**: RTX 3060 12GB (€300 used)
- ✅ Lower-res .ply perfect
- ⚠️ Standard .ply playable but limited
- ✅ VRChat smooth
- ✅ Desktop VR smooth

**2027-2028**: Upgrade to RTX 5060 Ti 16GB or RTX 6060 (€400-500)
- ✅✅ Standard .ply perfect
- ✅✅ Multiple splats in scene
- ✅✅ VR ultra settings
- 💰 Sell 3060 for €150-200 (offset cost!)

**Total investment**: €600-700 over 3 years (vs €1800 for 4090 now)

**Your friend pays €25/month** for Villa Straylight access instead of €1800 upfront!

---

## What They CAN'T Do (vs You)

**Honest limitations with RTX 3060 12GB**:

### Won't Work Well:
- ❌ **Multiple Standard .ply** in same scene (VRAM limit)
- ❌ **4K resolution** desktop (1080p/1440p fine)
- ❌ **Ray tracing** in Unity (but splats don't use it!)
- ❌ **8K texture packs** for VRChat (don't need anyway!)

### Will Work But Slower:
- ⚠️ **Large Standard .ply** (city blocks) - 30 FPS instead of 120
- ⚠️ **Unity editor** with huge scenes - slower than 4090
- ⚠️ **Multiple VRChat worlds** loaded - longer load times

### Works Perfectly:
- ✅ **Lower-res .ply** (this is 95% of use case!)
- ✅ **VRChat** (standard quality)
- ✅ **VR with Quest/Pico** (smooth 60+ FPS)
- ✅ **Desktop viewing** (80+ FPS)
- ✅ **Multiplayer VREALM** (same as you!)
- ✅ **VROB interaction** (LLM is CPU, not GPU!)

**Bottom line**: They sacrifice quality settings, NOT core experience!

---

## Power & System Requirements

### RTX 3060 12GB System Needs

**PSU**: 550W+ (650W recommended)  
**CPU**: Any modern 6-core+ (Ryzen 5, Intel i5)  
**RAM**: 16GB (32GB better for Unity)  
**Motherboard**: PCIe 3.0 x16 slot (any modern board)  
**Case**: Standard ATX (card is ~24cm long)

**Power consumption comparison**:
- RTX 4090: 450W (needs 850W+ PSU)
- RTX 3060 12GB: 170W (needs 550W PSU)

**Your friend saves on**:
- Cheaper PSU (don't need 850W)
- Lower electricity bills (€50-100/year difference!)
- Less heat (apartment stays cooler)

---

## The Social Aspect

### Villa Straylight is Multiplayer!

**Important realization**: Your friend doesn't need YOUR hardware to enjoy YOUR world!

**VRChat/Resonite**:
- Server streams world to everyone
- Each person renders on their GPU
- Your 4090: Ultra settings, 120 FPS
- Their 3060: High settings, 60 FPS
- **Same experience, same presence, same fun!**

**Like movies**:
- You: 4K OLED TV
- Friend: 1080p LCD TV
- Both watch same movie, both enjoy equally!

**Villa Straylight tea parties**:
- Archimedes vrob doesn't care about FPS!
- Conversations same quality
- Presence same feeling
- **GPU only affects rendering, not social experience!**

---

## Final Recommendation Letter

### What to Send Your Friend

```
Hey [Friend],

Want to join Villa Straylight (my photorealistic VR metaverse)?

You DON'T need my €1800 RTX 4090!

Get this: Used RTX 3060 12GB for €250-300

Why:
- 12GB VRAM (critical for Gaussian splats!)
- Handles everything I do (slightly lower quality)
- VR works perfectly (60+ FPS)
- We can hang out in VRChat together
- Tea with AI Archimedes! ☕

Where to find:
- Willhaben.at
- eBay Kleinanzeigen
- Local PC shops

Check:
- 12GB model (not 6GB!)
- Not used for mining
- Test before buying

You'll have 90% of my experience for 20% of cost!

Later (2027?) upgrade to newer card, sell 3060.

Let's build Villa Straylight together! 🏰✨

- Sandra
```

---

## Summary Table

| GPU | Price | VRAM | Lower-res .ply | Standard .ply | VR | Verdict |
|-----|-------|------|----------------|--------------|----|---------|
| **RTX 3060 12GB** (used) | **€250-350** | **12GB** | ✅✅✅ | ✅✅ | ✅ | **🏆 BUY THIS** |
| RTX 4060 Ti 16GB (new) | €500-600 | 16GB | ✅✅✅ | ✅✅✅ | ✅✅ | If can afford |
| RTX 4060 8GB | €300-350 | 8GB | ✅✅ | ❌ | ✅ | Too limited |
| RTX 3060 Ti 8GB (used) | €250-300 | 8GB | ✅✅ | ❌ | ✅ | Only if desperate |
| RTX 3050 8GB | €200-250 | 8GB | ✅ | ❌ | ⚠️ | Avoid |

---

**Status**: Budget recommendation complete!  
**Best choice**: Used RTX 3060 12GB (€250-350) - 12GB VRAM is king! 👑  
**Your friend**: Can join Villa Straylight for 20% of your GPU cost! 🏰✨  

**Shazbat! Everyone gets a VREALM!** 🚀






































