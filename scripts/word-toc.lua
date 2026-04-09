-- Lua filter to create clickable TOC using hyperlinks (not field codes)
-- This creates a TOC that is:
-- - Clickable (uses internal hyperlinks)
-- - No popups (no field codes)
-- - Static (no update required)
--
-- How it works:
-- 1. Collects all headings during first pass
-- 2. Generates TOC with hyperlinks to heading bookmarks
-- 3. Pandoc automatically creates bookmarks for headings

local headings = {}
local defined = false

-- First pass: collect all headings
function Header(el)
    -- Store heading info
    table.insert(headings, {
        level = el.level,
        text = pandoc.utils.stringify(el.content),
        identifier = el.identifier
    })
    return el
end

-- Generate TOC block with hyperlinks
function generate_toc()
    local toc_items = {}
    
    -- TOC title
    table.insert(toc_items, pandoc.Header(1, pandoc.Str("Table of Contents")))
    
    -- Build bullet list for TOC
    local items = {}
    for _, h in ipairs(headings) do
        if h.level <= 3 then  -- Only include H1-H3
            -- Create hyperlink to the heading's bookmark
            local link = pandoc.Link(
                pandoc.Str(h.text),
                "#" .. h.identifier,
                "",
                pandoc.Attr("", {}, {})
            )
            
            -- Create list item with proper indentation via nested lists
            local item = pandoc.Plain({link})
            
            if h.level == 1 then
                table.insert(items, {item})
            elseif h.level == 2 then
                -- Indent level 2
                if #items > 0 then
                    local last = items[#items]
                    if type(last) == "table" and #last > 0 then
                        table.insert(last, pandoc.BulletList({{item}}))
                    end
                else
                    table.insert(items, {item})
                end
            elseif h.level == 3 then
                -- Indent level 3 (nested deeper)
                table.insert(items, {pandoc.Plain({pandoc.Str("    "), link})})
            end
        end
    end
    
    -- Simpler approach: flat list with indentation markers
    local flat_items = {}
    for _, h in ipairs(headings) do
        if h.level <= 3 then
            local indent = string.rep("    ", h.level - 1)
            local link = pandoc.Link(
                pandoc.Str(h.text),
                "#" .. h.identifier
            )
            table.insert(flat_items, {pandoc.Plain({pandoc.Str(indent), link})})
        end
    end
    
    table.insert(toc_items, pandoc.BulletList(flat_items))
    table.insert(toc_items, pandoc.HorizontalRule())
    
    return toc_items
end

-- Insert TOC at document start
function Pandoc(doc)
    if #headings > 0 then
        local toc = generate_toc()
        for i = #toc, 1, -1 do
            table.insert(doc.blocks, 1, toc[i])
        end
    end
    return doc
end

return {
    {Header = Header},  -- First pass: collect headings
    {Pandoc = Pandoc}   -- Second pass: insert TOC
}
