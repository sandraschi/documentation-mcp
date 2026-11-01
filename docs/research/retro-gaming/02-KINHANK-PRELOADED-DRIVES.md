# 02 - Kinhank Preloaded Drives: Amazon Case Study (ASIN B09P36912T)

**Purpose:** Document the archetypal grey-market listing so the fleet has a worked example: what it is, why it infringes three times over, and why it stays up. Analyzed 2026-10-15, facts as listed that day.

## 1. The listing (facts)

* **Product:** "Kinhank 2TB Game Hard Drive, Built-in 120000+ Games, Batocera 33 System, External Hard Drive Compatible with Mac OS/Linux/Windows" - ASIN B09P36912T.
* **Claims:** 108 game collections + emulators pre-installed, 120,000+ games including 5,000+ 3D games. Compatible systems named: Sony PlayStation 2, PlayStation 3, PSP. Boot-via-BIOS USB drive, Batocera 33 (note: two major versions behind current 43.1).
* **Seller:** `yunsheng store` (3rd party), ships from Amazon Fulfillment ("Fulfilled by Amazon"). Price ~EUR 115.94 + shipping. Category filed under Sony PSP Consoles / external hard drives.
* **Evasion wording:** title says "Built-in 120000+ Games" but names no actual game; description says "Please contact us for a list of games" (moves the infringing manifest off-page). Filed as storage hardware, not software.
* **Kinhank's own site** (`kinhank-retrogame.com`) advertises the same: 120,000+ preloaded titles, 80+ emulators, "Supports adding your own games". Related SKUs: 500G/12TB drives, Super Console X / X2 Pro / Cube x3 boxes (EmuELEC-based).

## 2. Why it infringes three times over

1. **Game ROMs (mass copyright infringement).** 120,000 commercial games distributed without publisher licenses. Covers Nintendo, Sony, Sega, Microsoft, arcade (MAME) catalogs. Unit economics alone prove it: EUR 115 cannot license 120,000 commercial titles.
2. **Console BIOS files.** PS1/PS2/PSP emulation as advertised requires Sony BIOS dumps, which are separately copyrighted software Kinhank has no license to redistribute.
3. **Batocera's own license.** `wiki.batocera.org/license`: selling Batocera pre-installed on any machine, SD card, USB drive, or HDD is explicitly forbidden (libretro non-commercial components + project policy), *even before* any ROMs are added. Shipping it stuffed with copyrighted ROMs is called out as "illegal, strictly forbidden, and discouraged" by the Batocera team.

## 3. Why it stays on Amazon US (mechanics, not permission)

* **Marketplace + safe harbor.** Amazon is the platform/fulfiller, not the seller. Under DMCA-style safe harbor it reacts to takedown notices; it does not pre-vet what is on a 3rd-party USB HDD in its warehouse.
* **FBA laundering.** "Ships from Amazon" looks first-party but is just logistics. Amazon never opens the drive and audits 120k ROMs.
* **Keyword evasion.** No game titles, no "ROM" word, filed under hardware categories. Automated filters looking for "Mario ROM download" never fire.
* **Whack-a-mole economics.** Rights holders must find and report each ASIN individually (Amazon Brand Registry / infringement report). Banned seller reappears under a new store name; 800+ similar results exist for "preloaded emulator console" at any time.
* **Enforcement triage.** Nintendo sues strategically (RomUniverse $2.1M judgment, Yuzu $2.4M settlement, both precedent in Sources) to kill distribution hubs, not EUR-115 drop-shippers in Shenzhen. Most publishers never file at all.
* **Jurisdiction friction.** Seller entity is CN-based; a US/EU lawsuit costs more than the damages recoverable from one storefront.

## 4. Buyer-side reality

* **Prosecution risk for buyers: ~zero.** Enforcement targets distributors and profit-makers, not living-room buyers.
* **The goods are still infringing:** seizable by customs in transit, no valid warranty chain, no support from Batocera upstream (they explicitly refuse support for preloaded sellers' customers).
* **Quality/malware risk is the practical argument:** fake-capacity flash/HDDs are endemic in this segment, and boot partitions with bundled Windows "tools" have carried malware. You pay EUR 115 for a drive you cannot trust or update (Batocera 33 vs current 43.1).
* **120,000 is a padded number:** duplicates, regional clones, bad dumps, hacks, and unplayable filler inflate the count. The playable licensed-equivalent set is far smaller.

## 5. Fleet position

Do not buy, do not recommend, do not link as a source. The legal equivalent (doc 03) costs an empty drive + free software + your own dumps, performs better (current Batocera, not a 2-version-old image), and does not fund infringement. If a listing needs reporting, the path is the rights holder's Amazon infringement report, not ours to police.
