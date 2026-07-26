# XCGUI — DirectX GUI Framework for AHK v2

**Library:** `scriptlets/lib/XCGUI/XCGUI.ahk` (3302 lines)  
**Source:** [thqby/ahk2_lib](https://github.com/thqby/ahk2_lib) (MIT)  
**Based on:** [twgh/xcgui](https://github.com/twgh/xcgui) — DirectUI framework using DirectX 

## What It Is

XCGUI is a full GUI framework that replaces AHK's built-in `Gui()` with DirectX-rendered controls. It provides professional-looking, skinnable, hardware-accelerated UI elements that AHK's native GUI cannot match:

- Anti-aliased text and shapes
- CSS-like layout (flexbox, grids)
- Hardware-accelerated rendering (DirectX)
- Professional controls: tree view, list view, slider, progress bar, tab control, rich edit, etc.
- Skinning/theming support with XML styles

## When to Use It

| Use Case | AHK Gui() | XCGUI |
|----------|-----------|-------|
| Simple dialogs, message boxes | ✅ Best | ⚠️ Overkill |
| Game GUIs (our GdipHelper) | ✅ Fine | ⚠️ Extra dependency |
| Complex settings panels | ⚠️ Limited | ✅ Better |
| Data-heavy dashboards (tables, trees) | ⚠️ Painful | ✅ Native |
| Skinned/professional UI | ❌ No | ✅ DirectX |
| Cross-monitor DPI-aware | ⚠️ Partial | ✅ Full |

## Getting Started

XCGUI requires the `XCGUI.dll` binary. Download the latest release from [twgh/xcgui releases](https://github.com/twgh/xcgui/releases).

```autohotkey
#Include %A_ScriptDir%\lib\XCGUI\XCGUI.ahk

; Initialize
xcgui.XInitXCGUI()

; Create window
hWindow := xcgui.XWnd_Create(0, 0, 600, 400, "My XCGUI App", 0, 0)

; Add controls
hBtn := xcgui.XBtn_Create(20, 40, 100, 30, "Click Me", hWindow)
hEdit := xcgui.XEdit_Create(20, 80, 200, 24, "", hWindow)
hList := xcgui.XList_Create(20, 120, 300, 200, hWindow)

; Event handlers
xcgui.XEle_RegEventC(hBtn, xcgui.XE_BNCLICK, "OnButtonClick")

; Run
xcgui.XRunXCGUI()

OnButtonClick() {
    xcgui.XC_MessageBox("Button clicked!")
}
```

## Control Reference

### Window & Layout

| Function | Description |
|----------|-------------|
| `XInitXCGUI()` | Initialize XCGUI engine |
| `XRunXCGUI()` | Enter message loop |
| `XWnd_Create(x, y, w, h, title, style, exStyle)` | Create window |
| `XWnd_Show(hWindow, showFlag)` | Show/hide window |
| `XWnd_Close(hWindow)` | Close window |
| `XWnd_SetSize(hWindow, w, h)` | Resize window |
| `XWnd_SetBg(hWindow, color)` | Set background color |

### Basic Controls

| Function | Description |
|----------|-------------|
| `XBtn_Create(x, y, w, h, text, hParent)` | Button |
| `XEdit_Create(x, y, w, h, text, hParent)` | Text input |
| `XRichEdit_Create(x, y, w, h, text, hParent)` | Rich text editor |
| `XLabel_Create(x, y, w, h, text, hParent)` | Static label |
| `XComboBox_Create(x, y, w, h, hParent)` | Dropdown |
| `XCheckBox_Create(x, y, w, h, text, hParent)` | Checkbox |
| `XRadioButton_Create(x, y, w, h, text, hParent)` | Radio button |

### Data Controls

| Function | Description |
|----------|-------------|
| `XList_Create(x, y, w, h, hParent)` | List view (multi-column) |
| `XTree_Create(x, y, w, h, hParent)` | Tree view |
| `XListView_Create(x, y, w, h, hParent)` | Icon/thumbnail view |
| `XReport_Create(x, y, w, h, hParent)` | Report/grid view |
| `XProgressBar_Create(x, y, w, h, hParent)` | Progress bar |
| `XSlider_Create(x, y, w, h, hParent)` | Slider |

### Container Controls

| Function | Description |
|----------|-------------|
| `XTab_Create(x, y, w, h, hParent)` | Tab control |
| `XGroupBox_Create(x, y, w, h, text, hParent)` | Group box |
| `XScrollView_Create(x, y, w, h, hParent)` | Scrollable container |
| `XSplitter_Create(x, y, w, h, hParent)` | Splitter panel |

### Events

| Event Constant | Description |
|---------------|-------------|
| `XE_BNCLICK` | Button click |
| `XE_EDIT_CHANGE` | Edit text changed |
| `XE_LST_SELCHANGED` | List selection changed |
| `XE_TREE_SELCHANGED` | Tree selection changed |
| `XE_BNSTATE` | Checkbox/radio state change |
| `XE_SLIDER_CHANGED` | Slider value changed |
| `XE_TAB_SELCHANGED` | Tab selection changed |

```autohotkey
; Register event handler
xcgui.XEle_RegEventC(hControl, xcgui.XE_BNCLICK, "EventHandler")

; Event handler function — no parameters needed for simple cases
EventHandler() {
    MsgBox("Event fired!")
}
```

## Styling & Themes

XCGUI supports XML-based skinning. Controls can be styled with colors, fonts, borders, and background images.

```autohotkey
; Set control text color
xcgui.XBtn_SetTextColor(hBtn, xcgui.XRGB(255, 215, 0))

; Set control background
xcgui.XWnd_SetBg(hWindow, xcgui.XRGB(26, 26, 46))
```

## Comparison: AHK Gui vs XCGUI

```autohotkey
; === AHK native Gui() ===
myGui := Gui("+Resize", "Simple Form")
myGui.Add("Text", "x10 y10", "Name:")
myGui.Add("Edit", "x10 y30 w200")
myGui.Add("Button", "x10 y60 w80", "Submit")
myGui.Show()

; === XCGUI ===
xcgui.XInitXCGUI()
hWindow := xcgui.XWnd_Create(0, 0, 300, 200, "Simple Form")
xcgui.XLabel_Create(10, 10, 80, 24, "Name:", hWindow)
xcgui.XEdit_Create(10, 35, 200, 24, "", hWindow)
hBtn := xcgui.XBtn_Create(10, 70, 80, 30, "Submit", hWindow)
xcgui.XEle_RegEventC(hBtn, xcgui.XE_BNCLICK, "OnSubmit")
xcgui.XWnd_Show(hWindow)
xcgui.XRunXCGUI()
```

## Pros & Cons

**Pros:**
- Far richer control set than native AHK Gui
- Hardware-accelerated rendering
- Proper DPI scaling
- Skinnable
- Thread-safe (can update UI from other threads)

**Cons:**
- Requires separate `XCGUI.dll` binary (not pure AHK)
- Steeper learning curve
- Different event model from AHK
- 3300-line include file
- GUI code is not portable to non-Windows via Wine (DirectX dependency)

## Fleet Integration

The library is bundled at `autohotkey-test/scriptlets/lib/XCGUI/XCGUI.ahk`. The DLL is NOT bundled (gitignored) — download separately from the [XCGUI releases page](https://github.com/twgh/xcgui/releases).

For fleet game rendering, we use the minimal `GdipHelper.ahk` instead — XCGUI is better suited for settings panels, dashboards, and tools.
