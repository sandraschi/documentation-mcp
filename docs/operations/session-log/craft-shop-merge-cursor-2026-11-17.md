# Shop family merge, Cursor L-C, 2026-11-17

Status: the mode merge was committed locally as `8a1a6ca` on `shopcraft` `main` and was not pushed. A later same-day pass replaced the JSON pages. See `craft-shop-window-cursor-2026-11-17.md`. That later pass is uncommitted.

## What merged

Survivor: `shopcraft` on `main`. The other seven repos were read and not modified.

Each sibling's domain store, models, errors, host, and tests landed under `crates/shopcraft-core/src/modes/`:

| Mode | Source | Tool prefix |
|---|---|---|
| retail | existing shopcraft POS | `shop_*` and `retail_*` |
| web | webshopcraft | `webshop_*` |
| amazon | amazonshopcraft | `amazon_*` |
| subscription | subshopcraft | `sub_*` |
| digital | digitalshopcraft | `digital_*` |
| wholesale | wholesalecraft | `wholesale_*` |
| ticket | ticketshopcraft | `ticket_*` |
| rental | rentalshopcraft | `rental_*` |

One CLI: `shopcraft --mode <mode> status|seed|tool`. Retail keeps shift, checkout, storno, and Z-Bon. One MCP stdio server serves every prefix. The first egui pass left retail as the register and the other seven pages as a status dump. That dump was replaced later the same day.

## What dropped

`dist/` binaries and zips were not copied. Duplicate egui shells and duplicate CLI mains were not copied. No history rewrite.

## Tests

Before: shopcraft 1 `#[test]`; the seven siblings were 1 or 2 each (11 across the family).

After: `cargo test --workspace` 27 passed. `cargo clippy --workspace --all-targets --all-features -- -D warnings` clean.

CLI seed and status succeeded for all eight modes. `wholesale_quote` for B2B-1001 / WS-CER-01 qty 12 returned a Gold Net30 quote. MCP `initialize` plus `tools/list` included `retail_status`, `webshop_status`, `amazon_status`, `sub_status`, `digital_status`, `wholesale_status`, `ticket_status`, and `rental_book`.

Scorecard re-run 2026-11-17T13:24:58Z: shopcraft loc_rs 8949, tests 27(regex).

## Honest gaps

SEPA pain.008 XML is not generated. EU VAT OSS is a local rate table, not a filed return. Amazon repricing clamps a supplied competitor price. It does not call Amazon.

## Left for others

Opencode archives the seven siblings after the merge is pushed. `git filter-repo` on shopcraft `dist/` waits for Sandra. `8a1a6ca` is local only. The desk, web storefront, and photo work after that commit is still uncommitted.
