# Craft fleet scorecard (Phase 0 baseline)

Generated (UTC): 2026-11-18T21:41:09Z. Source of truth for CRAFT_CONSOLIDATION_PLAN_2026-11 numbers.
Method: LOC = lines in non-target .rs; tests = regex count of #[test]/#[tokio::test] unless -ProbeTests with cargo ok;
stubs = literal marker counts (todo!/unimplemented!/TODO/stub-word); last_commit = local HEAD date (proxy for last push);
gh_kb = GitHub diskUsage KB; local_kb = sum of git-tracked worktree file sizes.

Totals: repos=77 with_git=72 without_git=5 rust=62 python=9 empty=6 ci=4 gitattributes=62 alpha=0 archived=16 loc_rs=433452 tests=2561

| repo | kind | git | loc_rs | tests | todo | unimpl | TODO | stub | branches | last_commit | release | pre | gh_kb | local_kb | ALPHA | CI | gitattr | archived | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aicraft | rust | yes | 2534 | 13(regex) | 0 | 0 | 0 | 2 | 1 | 2026-11-18 22:36:04 +0100 | v0.1.0 | False | 37 | 136.4 | - | - | yes | no |  |
| amazonshopcraft | rust | yes | 1162 | 1(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 22:34:13 +0100 |  |  | 41587 | 636.1 | - | - | yes | yes |  |
| appcraft | rust | yes | 3931 | 4(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:17:46 +0100 | v0.1.0 | True | 9013 | 576 | - | - | yes | no |  |
| assetcraft | rust | yes | 4939 | 23(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 02:08:37 +0100 | v0.1.1 | False | 403 | 657.4 | - | - | yes | no |  |
| billcraft | rust | yes | 4241 | 6(regex) | 0 | 0 | 0 | 4 | 1 | 2026-11-18 02:08:37 +0100 | v0.1.0 | False | 178 | 315.9 | - | - | yes | no |  |
| bookcraft | rust | yes | 7101 | 46(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:17:51 +0100 | v0.5.0 | True | 10014 | 927.9 | - | - | yes | no |  |
| bridgeclubcraft | rust | local | 2035 | 4(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:15:48 +0100 | n/a |  |  | 1794.8 | - | - | yes | - |  |
| buchcraft | rust | yes | 7093 | 28(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:32 +0100 | v0.2.1 | False | 1183 | 2145.2 | - | - | yes | no |  |
| celcraft | rust | yes | 13559 | 54(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:17:54 +0100 | v1.5.2 | False | 6316 | 6777.9 | - | - | yes | no |  |
| codercraft | rust | yes | 9365 | 21(regex) | 0 | 0 | 0 | 0 | 2 | 2026-11-18 22:36:44 +0100 | v0.1.0 | True | 9710 | 1070.2 | - | - | yes | no |  |
| codercraft test | python | - |  | (none) |  |  |  |  |  |  | n/a |  |  |  | - | - | - | - | python-placeholder-candidate |
| containercraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:41:20 +0100 |  |  | 15 | 30.1 | - | - | - | yes | python-placeholder-candidate |
| contractcraft | rust | yes | 5930 | 29(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:38 +0100 | v0.2.0 | False | 678 | 1172.5 | - | - | yes | no |  |
| craft-ai | rust | yes | 1445 | 12(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 22:36:14 +0100 |  |  | 23 | 56.9 | - | - | yes | yes |  |
| craft-anything-demo | empty | - |  | (none) |  |  |  |  |  |  | n/a |  |  |  | - | - | - | - | no-code |
| craft-biz | rust | yes | 11849 | 65(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 02:08:36 +0100 |  |  | 241 | 522.4 | - | - | yes | no |  |
| craftcraft | rust | local | 717 | 5(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:21:57 +0100 | n/a |  |  | 182.4 | - | - | yes | - |  |
| craft-deck | mixed | yes | 40038 | 700(regex) | 0 | 0 | 0 | 0 | 2 | 2026-11-15 00:35:18 +0100 |  |  | 6272 | 5234.6 | - | yes | - | no |  |
| craft-demo-20261112 | empty | - |  | (none) |  |  |  |  |  |  | n/a |  |  |  | - | - | - | - | no-code |
| craft-sandbox-vbox | rust | yes | 407 | 3(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-07 18:09:04 +0100 |  |  | 12 | 24.1 | - | - | yes | no |  |
| craft-showcase | mixed | yes | 2184 | 0(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:17:58 +0100 |  |  | 17847 | 39274.5 | - | - | yes | no |  |
| craft-site-demo | empty | - |  | (none) |  |  |  |  |  |  | n/a |  |  |  | - | - | - | - | no-code |
| crochetcraft | rust | local | 1540 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:21:57 +0100 | n/a |  |  | 2399.4 | - | - | yes | - |  |
| databasecraft | rust | yes | 17858 | 38(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-15 23:16:26 +0100 | v0.5.0 v0.4.0 v0.3.0 v0.2.0 v0.1.0 | False False False False False | 9952 | 1372.5 | - | - | yes | no |  |
| democraft-mcp | python | yes |  | (none) |  |  |  |  | 3 | 2026-11-07 18:08:55 +0100 | v0.2.0-beta.2 v0.2.0-beta.1 v0.1.2-beta.1 | True True True | 11679 | 10566.3 | - | yes | yes | no | python-placeholder-candidate |
| deskcraft | rust | yes | 5153 | 24(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:40 +0100 | v0.2.0 | False | 676 | 1144.6 | - | - | yes | no |  |
| devcraft | rust | yes | 10259 | 38(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:18:01 +0100 | v0.2.0 v0.1.0 | False False | 1085 | 1718.5 | - | - | yes | no |  |
| digitalshopcraft | rust | yes | 1531 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 22:34:20 +0100 |  |  | 350 | 725.2 | - | - | yes | yes |  |
| djcraft | rust | yes | 1032 | 3(regex) | 0 | 0 | 0 | 0 | 2 | 2026-11-17 13:18:51 +0100 | v0.1.0 | True | 6030 | 415.2 | - | - | yes | no |  |
| doccraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:40:21 +0100 |  |  | 17 | 36.4 | - | - | - | yes | python-placeholder-candidate |
| filecraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:40:26 +0100 |  |  | 17 | 39.7 | - | - | - | yes | python-placeholder-candidate |
| formcraft | rust | yes | 2326 | 5(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 02:08:39 +0100 | v0.1.0 | False | 351 | 526.6 | - | - | yes | no |  |
| gaincraft | rust | yes | 9234 | 56(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:34 +0100 | v0.3.1 v0.3.0 | False False | 839 | 1374.5 | - | - | yes | no |  |
| gamecraft | rust | yes | 37738 | 258(regex) | 0 | 0 | 0 | 0 | 3 | 2026-11-12 19:40:04 +0100 | v0.14.0 | False | 29068 | 34063.2 | - | - | yes | no |  |
| gamecraft-cli-wt | empty | - |  | (none) |  |  |  |  |  |  | n/a |  |  |  | - | - | - | - | no-code |
| giscraft | rust | yes | 16025 | 148(regex) | 0 | 0 | 0 | 2 | 1 | 2026-11-15 19:47:14 +0100 | v0.2.1 v0.2.0 v0.1.0 | True True True | 4274 | 2709.3 | - | yes | yes | no |  |
| gitcraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:40:30 +0100 |  |  | 17 | 37.3 | - | - | - | yes | python-placeholder-candidate |
| helmcraft | rust | yes | 4590 | 18(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 02:08:40 +0100 | v0.1.0 | False | 1353 | 1906.9 | - | - | yes | no |  |
| hirecraft | rust | yes | 1664 | 5(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 02:08:39 +0100 | v0.1.0 | False | 120 | 214.5 | - | - | yes | no |  |
| homecraft | rust | yes | 25381 | 172(regex) | 0 | 0 | 0 | 5 | 1 | 2026-11-17 10:26:17 +0100 |  |  | 3120 | 3595.7 | - | - | yes | no |  |
| horsecraft | rust | local | 1415 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:21:12 +0100 | n/a |  |  | 4953.3 | - | - | yes | - |  |
| kittycraft | rust | yes | 4886 | 6(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:18:58 +0100 |  |  | 2494 | 2922.9 | - | - | yes | no |  |
| lenscraft | rust | local | 1903 | 27(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-14 20:45:50 +0100 | n/a |  |  | 123.5 | - | - | yes | - |  |
| lookcraft | rust | yes | 10102 | 85(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:19:01 +0100 | v0.1.0 | True | 1804 | 3224.7 | - | yes | yes | no |  |
| makercraft | rust | yes | 6646 | 40(regex) | 0 | 0 | 0 | 1 | 1 | 2026-11-17 13:19:03 +0100 | v0.1.0 | True | 543 | 757.4 | - | - | yes | no |  |
| modcraft | rust | yes | 680 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:35:26 +0100 | v0.1.0 | True | 5995 | 403.5 | - | - | - | yes |  |
| moneycraft | rust | yes | 10588 | 13(regex) | 0 | 0 | 0 | 1 | 1 | 2026-11-12 19:40:25 +0100 | v0.1.0 | True | 801 | 1732.3 | - | - | yes | no |  |
| musiccraft | empty | yes |  | (none) |  |  |  |  | 1 | 2026-11-18 22:37:17 +0100 |  |  | 135 | 15.4 | - | - | yes | no | no-code |
| on-metacraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-10-31 03:09:58 +0100 |  |  | 3505 | 3687.6 | - | - | - | no | python-placeholder-candidate |
| patterncraft | rust | yes | 8795 | 84(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:19:08 +0100 |  |  | 212 | 470.2 | - | - | yes | no |  |
| philosophercraft | rust | local | 1486 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:21:12 +0100 | n/a |  |  | 1384.7 | - | - | yes | - |  |
| puppycraft | rust | yes | 8589 | 9(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:19:58 +0100 |  |  | 3971 | 4564.8 | - | - | yes | no |  |
| rentalshopcraft | rust | yes | 1259 | 1(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 22:34:31 +0100 |  |  | 299 | 672.3 | - | - | yes | yes |  |
| revecraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:41:28 +0100 |  |  | 101 | 59 | - | - | - | yes | python-placeholder-candidate |
| robotcraft | rust | yes | 5109 | 9(regex) | 0 | 0 | 0 | 1 | 1 | 2026-11-17 13:20:02 +0100 | v0.3.0 v0.1.0 | False True | 8975 | 654.3 | - | - | yes | no |  |
| rsicraft | mixed | yes | 13808 | 47(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-14 23:47:46 +0100 | v0.3.1 v0.3.0 v0.2.0 | False False False | 7654 | 4810 | - | - | yes | no |  |
| setupcraft | rust | local | 1343 | 5(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 11:21:57 +0100 | n/a |  |  | 148.4 | - | - | yes | - |  |
| shopcraft | rust | yes | 12059 | 30(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 22:33:51 +0100 |  |  | 71785 | 3230.8 | - | - | yes | no |  |
| smallvideocraft | empty | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:37:06 +0100 |  |  | 16 | 22.9 | - | - | - | yes | no-code |
| speechcraft | rust | yes | 5595 | 20(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:20:07 +0100 | v0.1.0 | True | 8452 | 606.9 | - | - | yes | no |  |
| spendcraft | rust | yes | 3335 | 8(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 02:08:38 +0100 | v0.1.0 | False | 176 | 405.6 | - | - | yes | no |  |
| splatcraft | mixed | yes | 11461 | 128(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-14 06:23:21 +0100 | v0.1.0 | False | 1210 | 1444.8 | - | - | yes | no |  |
| sportscraft | rust | yes | 3916 | 30(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:20:12 +0100 | v0.2.0 | True | 426 | 656.7 | - | - | yes | no |  |
| stockcraft | rust | yes | 3508 | 10(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:20:15 +0100 |  |  | 384 | 765.1 | - | - | yes | no |  |
| studiocraft | rust | yes | 3699 | 17(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:20:17 +0100 | v0.1.0 | True | 10456 | 573.6 | - | - | yes | no |  |
| subshopcraft | rust | yes | 1420 | 1(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 22:34:17 +0100 |  |  | 329 | 702.6 | - | - | yes | yes |  |
| taskcraft | rust | yes | 9558 | 53(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 02:08:38 +0100 | v0.1.4 v0.1.3 | False True | 605 | 933.3 | - | - | yes | no |  |
| teamcraft | rust | yes | 7054 | 32(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:29 +0100 | v0.3.1 v0.3.0 | False False | 842 | 1369.2 | - | - | yes | no |  |
| ticketshopcraft | rust | yes | 1235 | 1(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 22:34:27 +0100 |  |  | 322 | 694.2 | - | - | yes | yes |  |
| travelcraft | rust | yes | 12711 | 38(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 22:36:45 +0100 | v0.2.0 v0.1.0 | True True | 14191 | 1075.5 | - | - | yes | no |  |
| virtucraft | python | yes |  | (none) |  |  |  |  | 1 | 2026-11-17 13:41:24 +0100 |  |  | 121 | 319.1 | - | - | - | yes | python-placeholder-candidate |
| vmcraft | rust | yes | 6718 | 34(regex) | 0 | 0 | 0 | 1 | 1 | 2026-11-17 13:21:11 +0100 |  |  | 315 | 645.5 | - | - | yes | no |  |
| webshopcraft | rust | yes | 1841 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 22:34:09 +0100 |  |  | 44392 | 2738.7 | - | - | yes | yes |  |
| wholesalecraft | rust | yes | 1873 | 2(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 22:34:24 +0100 |  |  | 337 | 728.6 | - | - | yes | yes |  |
| wikicraft | rust | yes | 4165 | 6(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-16 19:27:43 +0100 | v0.3.1 v0.3.0 v0.2.0 v0.1.0 | False False True True | 419 | 592.8 | - | - | yes | no |  |
| wincraft | rust | yes | 6873 | 18(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-17 13:21:19 +0100 |  |  | 482 | 977.2 | - | - | yes | no |  |
| writercraft | rust | yes | 6961 | 16(regex) | 0 | 0 | 0 | 0 | 1 | 2026-11-18 22:36:45 +0100 | v0.3.1 v0.1.0 | False True | 6121 | 784 | - | - | yes | no |  |
