# Shop window, web storefront, photos, 2026-11-17

Status: uncommitted on `shopcraft` `main`, on top of local commit `8a1a6ca` (ahead of origin by 1). Not pushed.

## What changed

The egui window no longer dumps JSON for the seven non-retail modes. Each shop lists its own rows and runs the store calls the CLI already had: order, pay, ship, reprice, subscribe, license, quote, ticket, rental.

**Shop > Mode** switches the shop. The left sidebar is that shop's sections. Retail sections are Stats, Register, Catalog, Hours, Calendar, Roster, and Shift. Hours, calendar days, and employees are rows in `retail.db`. Seed demo writes a standard week, three December 2026 exceptions, and three employees.

**Shop > Open webshop**, and the same button on the Web stats page, copies `storefront\` into `%LOCALAPPDATA%\shopcraft\web-storefront`, writes `catalog.js` from the live web database, and opens `index.html`.

Product cards and the hero use six photos in `storefront\assets\`. They are not the old generated SVG drawings. Search, bag, and theme controls are still small icons.

Amazon orders can be listed (`AmazonStore::list_orders`). `cargo test --workspace` was 28 passed before the photo-path edit. After the retail floor tables, `cargo test -p shopcraft-core --lib` was 29 passed, including `floor_hours_calendar_and_roster`. Hours, calendar, and roster are store methods on the retail desk. They are not MCP tools.

## Honest gaps

- Browser checkout does not insert a web order. The desk does.
- Shop stock and stockcraft stock are different databases. The shop writes `channel.sale_committed`, `channel.return_restocked`, and `channel.stock_reserved` into the stockcraft bus inbox. Stockcraft rejects those kinds. Reorder is `stock_reorder_plan` plus `stock_receive` in stockcraft.
- No chat dock. `chat_panel` is empty.
- SEPA pain.008 XML is not written. EU VAT OSS is not filed. Amazon repricing does not call Amazon.
- `dist\shopcraft-app.exe` is still the 16 November binary.

## Docs

`shopcraft\README.md` and `shopcraft\AGENTS.md` match this window, including Shop > Mode, the per-shop sidebar, and the retail hours, calendar, and roster tables. The earlier merge log no longer says the other pages are a status dump.
