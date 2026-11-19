# Craft fleet scorecard (Phase 0 baseline)

Generated (UTC): 2026-11-17T13:24:58Z. Source of truth for CRAFT_CONSOLIDATION_PLAN_2026-11 numbers.
Method: LOC = lines in non-target .rs; tests = regex count of #[test]/#[tokio::test] unless -ProbeTests with cargo ok;
stubs = literal marker counts (todo!/unimplemented!/TODO/stub-word); last_commit = local HEAD date (proxy for last push);
gh_kb = GitHub diskUsage KB; local_kb = sum of git-tracked worktree file sizes.

Totals: repos=77 with_git=72 without_git=5 rust=63 python=9 empty=5 ci=4 gitattributes=62 alpha=0 archived=0 loc_rs=432045 tests=2555

| repo | kind | git | loc_rs | tests | todo | unimpl | TODO | stub | branches | last_commit | release | pre | gh_kb | local_kb | ALPHA | CI | gitattr | archived | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aicraft | rust | yes | 1089 | 1(regex) | 0 | 0 | 0 | 2 | 1 | 2026-11-17 13:17:41 +0100 | n/a |  |  | 77.2 | - | - | yes | - |  |
| amazonshopcraft | rust | yes | 1162 | 1(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:17:44 +0100 | n/a |  |  | 638.9 | - | - | yes | - |  |
| appcraft | rust | yes | 3931 | 4(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:17:46 +0100 | n/a |  |  | 576 | - | - | yes | - |  |
| assetcraft | rust | yes | 4910 | 23(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:36 +0100 | n/a |  |  | 656.2 | - | - | yes | - |  |
| billcraft | rust | yes | 4225 | 6(regex) | 0 | 0 | 0 | 4 | 1 | 2026-11-17 13:17:48 +0100 | n/a |  |  | 315 | - | - | yes | - |  |
| bookcraft | rust | yes | 7101 | 46(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:17:51 +0100 | n/a |  |  | 927.9 | - | - | yes | - |  |
| bridgeclubcraft | rust | local | 2035 | 4(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:15:48 +0100 | n/a |  |  | 1794.8 | - | - | yes | - |  |
| buchcraft | rust | yes | 7093 | 28(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:32 +0100 | n/a |  |  | 2145.2 | - | - | yes | - |  |
| celcraft | rust | yes | 13559 | 54(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:17:54 +0100 | n/a |  |  | 6777.9 | - | - | yes | - |  |
| codercraft | rust | yes | 9365 | 21(regex) | 0 | 0 | 0 | 0 | 2 | 2026-11-17 13:17:56 +0100 | n/a |  |  | 1070.2 | - | - | yes | - |  |
| codercraft test | python | - |  | (none) |  |  |  |  |  |  | n/a |  |  |  | - | - | - | - | python-placeholder-candidate |
| containercraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:41:20 +0100 | n/a |  |  | 30.1 | - | - | - | - | python-placeholder-candidate |
| contractcraft | rust | yes | 5930 | 29(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:38 +0100 | n/a |  |  | 1172.5 | - | - | yes | - |  |
| craft-ai | rust | yes | 1445 | 12(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-14 21:37:03 +0100 | n/a |  |  | 59.3 | - | - | yes | - |  |
| craft-anything-demo | empty | - |  | (none) |  |  |  |  |  |  | n/a |  |  |  | - | - | - | - | no-code |
| craft-biz | rust | yes | 11800 | 65(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:25 +0100 | n/a |  |  | 520.5 | - | - | yes | - |  |
| craftcraft | rust | local | 717 | 5(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:21:57 +0100 | n/a |  |  | 182.4 | - | - | yes | - |  |
| craft-deck | mixed | yes | 40038 | 700(regex) | 0 | 0 | 0 | 0 | 2 | 2026-11-15 00:35:18 +0100 | n/a |  |  | 5234.6 | - | yes | - | - |  |
| craft-demo-20261112 | empty | - |  | (none) |  |  |  |  |  |  | n/a |  |  |  | - | - | - | - | no-code |
| craft-sandbox-vbox | rust | yes | 407 | 3(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-07 18:09:04 +0100 | n/a |  |  | 24.1 | - | - | yes | - |  |
| craft-showcase | mixed | yes | 2184 | 0(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:17:58 +0100 | n/a |  |  | 39274.6 | - | - | yes | - |  |
| craft-site-demo | empty | - |  | (none) |  |  |  |  |  |  | n/a |  |  |  | - | - | - | - | no-code |
| crochetcraft | rust | local | 1540 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:21:57 +0100 | n/a |  |  | 2399.4 | - | - | yes | - |  |
| databasecraft | rust | yes | 17858 | 38(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-15 23:16:26 +0100 | n/a |  |  | 1372.5 | - | - | yes | - |  |
| democraft-mcp | python | yes |  | (none) |  |  |  |  | 3 | 2026-11-07 18:08:55 +0100 | n/a |  |  | 10566.3 | - | yes | yes | - | python-placeholder-candidate |
| deskcraft | rust | yes | 5153 | 24(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:40 +0100 | n/a |  |  | 1144.6 | - | - | yes | - |  |
| devcraft | rust | yes | 10259 | 38(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:18:01 +0100 | n/a |  |  | 1718.5 | - | - | yes | - |  |
| digitalshopcraft | rust | yes | 1531 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:18:48 +0100 | n/a |  |  | 728.1 | - | - | yes | - |  |
| djcraft | rust | yes | 1032 | 3(regex) | 0 | 0 | 0 | 0 | 2 | 2026-11-17 13:18:51 +0100 | n/a |  |  | 415.2 | - | - | yes | - |  |
| doccraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:40:21 +0100 | n/a |  |  | 36.4 | - | - | - | - | python-placeholder-candidate |
| filecraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:40:26 +0100 | n/a |  |  | 39.7 | - | - | - | - | python-placeholder-candidate |
| formcraft | rust | yes | 2264 | 5(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:42 +0100 | n/a |  |  | 524.3 | - | - | yes | - |  |
| gaincraft | rust | yes | 9234 | 56(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:34 +0100 | n/a |  |  | 1374.5 | - | - | yes | - |  |
| gamecraft | rust | yes | 37738 | 258(regex) | 0 | 0 | 0 | 0 | 3 | 2026-11-12 19:40:04 +0100 | n/a |  |  | 34063.2 | - | - | yes | - |  |
| gamecraft-cli-wt | empty | - |  | (none) |  |  |  |  |  |  | n/a |  |  |  | - | - | - | - | no-code |
| giscraft | rust | yes | 16025 | 148(regex) | 0 | 0 | 0 | 2 | 1 | 2026-11-15 19:47:14 +0100 | n/a |  |  | 2707.5 | - | yes | yes | - |  |
| gitcraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:40:30 +0100 | n/a |  |  | 37.3 | - | - | - | - | python-placeholder-candidate |
| helmcraft | rust | yes | 4553 | 18(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:18:53 +0100 | n/a |  |  | 1425.2 | - | - | yes | - |  |
| hirecraft | rust | yes | 1655 | 5(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:18:56 +0100 | n/a |  |  | 214 | - | - | yes | - |  |
| homecraft | rust | yes | 25381 | 172(regex) | 0 | 0 | 0 | 5 | 1 | 2026-11-17 10:26:17 +0100 | n/a |  |  | 3595.7 | - | - | yes | - |  |
| horsecraft | rust | local | 1415 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:21:12 +0100 | n/a |  |  | 4953.3 | - | - | yes | - |  |
| kittycraft | rust | yes | 4886 | 6(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:18:58 +0100 | n/a |  |  | 2922.9 | - | - | yes | - |  |
| lenscraft | rust | local | 1903 | 27(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-14 20:45:50 +0100 | n/a |  |  | 123.5 | - | - | yes | - |  |
| lookcraft | rust | yes | 10102 | 85(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:19:01 +0100 | n/a |  |  | 3224.7 | - | yes | yes | - |  |
| makercraft | rust | yes | 3799 | 38(regex) | 0 | 0 | 0 | 1 | 1 | 2026-11-17 13:19:03 +0100 | n/a |  |  | 709 | - | - | yes | - |  |
| modcraft | rust | yes | 680 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:35:26 +0100 | n/a |  |  | 403.5 | - | - | - | - |  |
| moneycraft | rust | yes | 10588 | 13(regex) | 0 | 0 | 0 | 1 | 1 | 2026-11-12 19:40:25 +0100 | n/a |  |  | 1732.3 | - | - | yes | - |  |
| musiccraft | rust | yes | 6630 | 13(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:19:05 +0100 | n/a |  |  | 438.7 | - | - | yes | - |  |
| on-metacraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-10-31 03:09:58 +0100 | n/a |  |  | 3687.6 | - | - | - | - | python-placeholder-candidate |
| patterncraft | rust | yes | 8795 | 84(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:19:08 +0100 | n/a |  |  | 470.2 | - | - | yes | - |  |
| philosophercraft | rust | local | 1486 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:21:12 +0100 | n/a |  |  | 1384.7 | - | - | yes | - |  |
| puppycraft | rust | yes | 8589 | 9(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:19:58 +0100 | n/a |  |  | 4564.8 | - | - | yes | - |  |
| rentalshopcraft | rust | yes | 1259 | 1(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:20:00 +0100 | n/a |  |  | 675.3 | - | - | yes | - |  |
| revecraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:41:28 +0100 | n/a |  |  | 59 | - | - | - | - | python-placeholder-candidate |
| robotcraft | rust | yes | 5109 | 9(regex) | 0 | 0 | 0 | 1 | 1 | 2026-11-17 13:20:02 +0100 | n/a |  |  | 654.3 | - | - | yes | - |  |
| rsicraft | mixed | yes | 13808 | 47(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-14 23:47:46 +0100 | n/a |  |  | 4810 | - | - | yes | - |  |
| setupcraft | rust | local | 1006 | 3(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:21:57 +0100 | n/a |  |  | 138.4 | - | - | yes | - |  |
| shopcraft | rust | yes | 8949 | 27(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:20:05 +0100 | n/a |  |  | 689 | - | - | yes | - |  |
| smallvideocraft | empty | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:37:06 +0100 | n/a |  |  | 22.9 | - | - | - | - | no-code |
| speechcraft | rust | yes | 5595 | 20(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:20:07 +0100 | n/a |  |  | 606.9 | - | - | yes | - |  |
| spendcraft | rust | yes | 3297 | 8(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:20:10 +0100 | n/a |  |  | 404 | - | - | yes | - |  |
| splatcraft | mixed | yes | 11461 | 128(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-14 06:23:21 +0100 | n/a |  |  | 1444.8 | - | - | yes | - |  |
| sportscraft | rust | yes | 3916 | 30(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:20:12 +0100 | n/a |  |  | 656.7 | - | - | yes | - |  |
| stockcraft | rust | yes | 3508 | 10(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:20:15 +0100 | n/a |  |  | 765.1 | - | - | yes | - |  |
| studiocraft | rust | yes | 3699 | 17(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:20:17 +0100 | n/a |  |  | 573.6 | - | - | yes | - |  |
| subshopcraft | rust | yes | 1420 | 1(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:21:06 +0100 | n/a |  |  | 705.5 | - | - | yes | - |  |
| taskcraft | rust | yes | 9500 | 53(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 02:46:48 +0100 | n/a |  |  | 931.1 | - | - | yes | - |  |
| teamcraft | rust | yes | 7054 | 32(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:29 +0100 | n/a |  |  | 1369.2 | - | - | yes | - |  |
| ticketshopcraft | rust | yes | 1235 | 1(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:21:09 +0100 | n/a |  |  | 697.1 | - | - | yes | - |  |
| travelcraft | rust | yes | 12711 | 38(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-15 19:46:58 +0100 | n/a |  |  | 1075.5 | - | - | yes | - |  |
| virtucraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:41:24 +0100 | n/a |  |  | 319.1 | - | - | - | - | python-placeholder-candidate |
| vmcraft | rust | yes | 6718 | 34(regex) | 0 | 0 | 0 | 1 | 1 | 2026-11-17 13:21:11 +0100 | n/a |  |  | 645.5 | - | - | yes | - |  |
| webshopcraft | rust | yes | 1841 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:21:14 +0100 | n/a |  |  | 2741.7 | - | - | yes | - |  |
| wholesalecraft | rust | yes | 1873 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:21:16 +0100 | n/a |  |  | 731.6 | - | - | yes | - |  |
| wikicraft | rust | yes | 4165 | 6(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:43 +0100 | n/a |  |  | 592.8 | - | - | yes | - |  |
| wincraft | rust | yes | 6873 | 18(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:21:19 +0100 | n/a |  |  | 977.2 | - | - | yes | - |  |
| writercraft | rust | yes | 6961 | 16(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:21:21 +0100 | n/a |  |  | 784 | - | - | yes | - |  |
