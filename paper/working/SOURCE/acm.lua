-- ACM journal layout (JOURNAL_BUILD.py). Structure and presentation only; the words do not change.
-- 1. The first heading, byline and status line, the Abstract section and the Keywords line move into
--    the ACM title block. The byline's city, state and email fill ACM's author fields.
-- 2. Section numbers typed in headings, and "Table N." and "Figure N." typed in captions, are removed
--    because the template numbers them. JOURNAL_BUILD.py checks that the template's numbers equal the
--    removed ones, so cross-references in the text stay correct.
-- 3. Unnumbered level-4 headings and the declarations heading stay unnumbered.
-- 4. In anonymous mode, each entry of SOURCE/anonymize.txt is removed: "status:" removes the dated
--    status line under the byline; "block:" removes the paragraph
--    whose text starts with the entry; "text:" removes the exact text. Each entry must match once.
-- JOURNAL_BUILD.py compares the result with the source, word for word, and reports every difference.

local mode='preprint'
local removals={}

local function plain(x) return pandoc.utils.stringify(x) end

local function load_removals(path)
 local f=io.open(path,'r'); assert(f,'missing '..path)
 for line in f:lines() do
  local kind,body=line:match('^(%a+):%s(.+)$')
  if kind then
   assert(kind=='block' or kind=='text' or kind=='status','unknown removal kind: '..kind)
   table.insert(removals,{kind=kind,body=body,count=0})
  end
 end
 f:close()
end

function Meta(m)
 if m['acm-mode'] then mode=plain(m['acm-mode']) end
 assert(mode=='preprint' or mode=='anonymous','acm-mode must be preprint or anonymous')
 if mode=='anonymous' then load_removals(plain(m['anonymize'])) end
 return m
end

-- Remove one exact text from a paragraph's inlines. The text must lie on whole-word boundaries.
local function cut_text(inlines,target)
 for i=1,#inlines do
  local acc,j='',i
  while j<=#inlines and #acc<#target do
   local el=inlines[j]
   if el.t=='Space' or el.t=='SoftBreak' then acc=acc..' ' else acc=acc..plain(el) end
   j=j+1
  end
  if acc==target then
   local out,rest=pandoc.List(),pandoc.List()
   for k=1,i-1 do out:insert(inlines[k]) end
   for k=j,#inlines do rest:insert(inlines[k]) end
   -- Keep one space at the joint, none at either end.
   if #out>0 and out[#out].t=='Space' and (#rest==0 or rest[1].t=='Space') then out:remove(#out) end
   if #out==0 and #rest>0 and rest[1].t=='Space' then rest:remove(1) end
   out:extend(rest)
   return out,true
  end
 end
 return inlines,false
end

local function anonymize(b,is_status)
 if mode~='anonymous' or (b.t~='Para' and b.t~='Plain') then return b end
 if is_status then
  for _,r in ipairs(removals) do if r.kind=='status' then r.count=r.count+1; return nil end end
  return b
 end
 local text=plain(b)
 for _,r in ipairs(removals) do
  if r.kind=='block' and text:sub(1,#r.body)==r.body then r.count=r.count+1; return nil end
 end
 for _,r in ipairs(removals) do
  if r.kind=='text' then
   local new,hit=cut_text(b.content,r.body)
   if hit then r.count=r.count+1; b.content=new end
  end
 end
 return b
end

local function strip_prefix(inlines,pattern)
 -- Remove a typed number ("Table 4." or "Figure 2.") from the start of a bold caption title.
 local first=inlines[1]
 if first and first.t=='Strong' then
  local s=plain(first)
  local num=s:match(pattern)
  if num then
   local c=first.content
   -- c begins Str "Table", Space, Str "4."; drop those three and any following Space.
   c:remove(1); c:remove(1); c:remove(1)
   if c[1] and c[1].t=='Space' then c:remove(1) end
   return num
  end
 end
 return nil
end

local function widths_for(t)
 local n=#t.colspecs
 local s=plain(t)
 local w
 if n==10 then w={.44,.055,.055,.055,.055,.055,.055,.055,.055,.12}
 elseif n==4 and s:match('^Family') then w={.47,.11,.23,.19}
 elseif n==4 then w={.05,.30,.23,.42}
 elseif n==3 then w={.30,.34,.36}
 elseif n==2 then w={.25,.75} end
 if w then for i,x in ipairs(w) do t.colspecs[i][2]=x end end
end

local function tex_escape(s)
 return (s:gsub('[\\{}_#%%&$~^]',function(ch)
  if ch=='\\' then return [[\textbackslash{}]] elseif ch=='~' then return [[\textasciitilde{}]] elseif ch=='^' then return [[\textasciicircum{}]] end
  return '\\'..ch end))
end

function Pandoc(doc)
 local bs=doc.blocks
 local m=doc.meta
 Meta(m)
 -- Title block: heading, author, "City, State. Correspondence: email", status line.
 assert(bs[1].t=='Header' and bs[1].level==1,'first block must be the title')
 m.title=pandoc.MetaInlines(bs[1].content)
 local author=plain(bs[2])
 local city,state,email=plain(bs[3]):match('^(.-), (.-)%. Correspondence: (%S+)$')
 assert(city and state and email,'byline must read "City, State. Correspondence: email"')
 m['acm-author']=author; m['acm-city']=city; m['acm-state']=state; m['acm-email']=email
 m['acm-country']='USA'
 local status=bs[4]
 assert(bs[5].t=='Header' and plain(bs[5])=='Abstract','Abstract must follow the byline')
 local i=6
 local abstract=pandoc.List()
 while bs[i].t=='Para' and not plain(bs[i]):match('^Keywords:') do abstract:insert(bs[i]); i=i+1 end
 m.abstract=pandoc.MetaBlocks(abstract)
 local kw=bs[i].content; kw:remove(1); if kw[1].t=='Space' then kw:remove(1) end
 m.keywords=pandoc.MetaInlines(kw)
 i=i+1

 local out=pandoc.List()
 local first=anonymize(status,true)
 if first then out:insert(first) end
 while i<=#bs do
  local b=bs[i]
  local nxt=bs[i+1]
  local text=(b.t=='Para') and plain(b) or ''
  if b.t=='Header' then
   local s=plain(b)
   local num=s:match('^(%d+)%. ') or s:match('^(%d+%.%d+) ')
   if num then
    local c=b.content
    c:remove(1); if c[1] and c[1].t=='Space' then c:remove(1) end
    b.attributes['typed-number']=num
   else
    b.classes:insert('unnumbered')
   end
   -- The title is in the title block, so "##" is ACM's \section, "###" its \subsection.
   if FORMAT:match('latex') then b.level=b.level-1 end
   out:insert(b); i=i+1
  elseif text:match('^Table %d+%. ') and nxt and nxt.t=='Table' then
   local num=strip_prefix(b.content,'^Table (%d+)%.')
   assert(num,'table caption must start with bold "Table N."')
   widths_for(nxt)
   nxt.caption.long={pandoc.Plain(b.content)}
   nxt.attr.attributes['typed-number']=num
   local size=(#nxt.colspecs==10) and [[\begingroup\footnotesize]] or [[\begingroup\small]]
   out:insert(pandoc.RawBlock('latex',size)); out:insert(nxt); out:insert(pandoc.RawBlock('latex',[[\endgroup]]))
   i=i+2
  elseif text:match('^Figure %d+%. ') and nxt and nxt.t=='Para' and #nxt.content==1 and nxt.content[1].t=='Image' then
   local num=strip_prefix(b.content,'^Figure (%d+)%.')
   assert(num,'figure caption must start with bold "Figure N."')
   local img=nxt.content[1]
   img.src=img.src:gsub('%.svg$','.pdf'); img.attributes['width']='100%'
   local alt=plain(img.caption)
   -- In LaTeX the image is capped at three quarters of the text height, keeping its proportions.
   local pic=FORMAT:match('latex') and pandoc.RawBlock('latex','\\includegraphics[width=\\linewidth,height=0.75\\textheight,keepaspectratio]{'..img.src..'}')
             or pandoc.Plain({img})
   local fig=pandoc.Figure({pic,pandoc.RawBlock('latex','\\Description{'..tex_escape(alt)..'}')},
                           {long={pandoc.Plain(b.content)}},pandoc.Attr('',{},{{'typed-number',num}}))
   out:insert(fig)
   i=i+2
  else
   local r=anonymize(b)
   if r then out:insert(r) end
   i=i+1
  end
 end
 for _,r in ipairs(removals) do
  assert(r.count==1,'anonymize.txt entry matched '..r.count..' times: '..r.body)
 end
 doc.blocks=out
 return doc
end

-- Identifiers such as SIG-16 never break at their hyphen; short code with spaces stays on one line;
-- long hashes and paths may break. Same rules as layout.lua.
function Str(s)
 if not FORMAT:match('latex') then return nil end
 local pre,id,post=s.text:match('^([%(%[]*)(%u+%-%d+)(.*)$')
 if not id then return nil end
 while true do
  local more,rest=post:match('^(%-%d+)(.*)$')
  if not more then break end
  id=id..more; post=rest
 end
 local out=pandoc.List()
 if pre~='' then out:insert(pandoc.Str(pre)) end
 out:insert(pandoc.RawInline('latex','\\mbox{'..id..'}'))
 if post~='' then out:insert(pandoc.Str(post)) end
 return out
end
function Code(c)
 if not FORMAT:match('latex') then return nil end
 if c.text:find(' ',1,true) and (utf8.len(c.text) or 30)<30 then
  local tex=pandoc.write(pandoc.Pandoc({pandoc.Plain({c})}),'latex'):gsub('%s+$','')
  return pandoc.RawInline('latex','\\mbox{'..tex..'}')
 end
 if #c.text>30 and c.text:match('^[a-f0-9]+$') then
  return pandoc.RawInline('latex',[[\texttt{\seqsplit{]]..c.text..'}}')
 end
 return nil
end

return {{Pandoc=Pandoc},{Str=Str,Code=Code}}
