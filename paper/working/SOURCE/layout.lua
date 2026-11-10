-- Numbering (10 November 2026): manuscript Tables 1 to 3 and Figures 2 and 3 moved to the supplement as Tables
-- S1.1, S3.1, S4.1 and Figures S3.1, S4.1. Manuscript Table 3 below is the Section 8.3 table (formerly 6) and
-- Figure 2 the Section 7 figure (formerly 4). Later the same day the Section 7 table moved to the supplement as
-- Table S7.1, so the Section 8.3 table is now manuscript Table 2; comments that say Table 3 mean that table.
-- Presentation only. Scientific text, citations and table values are unchanged.
-- Captioned tables and figures are set as top-placed floats, so following text fills the page and each
-- caption stays with its table or image. Figure 2 is the exception: it is placed at the bottom of a page
-- or on a float page, so it cannot print above the Section 7 heading or its callout. Table S9.1 is taller
-- than a page, so it is set as two floats: its caption with the first row at the bottom of a page, then
-- the other rows as "Table S9.1 (continued)" on the float page that follows, so no text falls between
-- them. Table 3 directly follows its Section 8.3 heading. A reservation for the heading and the whole
-- table (about 432pt) left most of a page empty when the heading fell low on a page, so Table 3 is a
-- float that prints where it occurs if it fits ([!ht]); \suppressfloats[t] before it keeps it from the
-- top of its heading's page, so otherwise it prints at the top of the next page and the 8.3 text fills
-- the space before it. Table S6.1 also follows its heading and is nearly a page tall. The S6 heading
-- starts a new page (\clearpage), and Table S6.1 is a top-only float: the \suppressfloats after the
-- heading then acts on the heading's own page, so the table prints at the top of the next page and the
-- S6 text fills the heading's page. In the PDF only, Tables S1.1 and S4.1 formerly followed the paragraphs that cite
-- them; the former Table 1 also followed \suppressfloats[t] and, like Table 3, prints where it occurs if it fits ([!ht]),
-- otherwise at the top of a later page, after the Section 2.4 heading and its callout. The two uncaptioned tables, the query-interface table in S4 and
-- the SDK-file table in S5, are set in place after their lead-ins, each after a space reservation; the
-- taller query-interface table may break between rows, with its header repeated. The Section 4.2
-- lead-in that ends in a colon reserves room for its whole planes list, so it shares a page with the
-- list; Figure 1 follows the list in the source. Short inline code containing spaces cannot break
-- across lines (BUILD.py also turns off hyphenation in the monospace font), and signal and mechanism
-- identifiers such as SIG-16 cannot break at their hyphen.
-- INPLACE lists captioned tables set in place after a reservation of their rendered extent, from
-- heading to bottom rule, plus the space above a heading and a margin. No table uses it at present.
local INPLACE={}
function Table(t)
 local n=#t.colspecs
 local s=pandoc.utils.stringify(t)
 local widths
 if n==10 then widths={.44,.055,.055,.055,.055,.055,.055,.055,.055,.12}
 elseif n==5 and s:match('SDK file') then widths={.11,.23,.10,.36,.20}
 elseif n==5 then widths={.22,.07,.14,.17,.40}
 elseif n==4 and s:match('^Family') then widths={.47,.11,.23,.19}
 elseif n==4 then widths={.05,.30,.23,.42}
 elseif n==3 and s:match('^Requirement') then widths={.15,.53,.32}
 elseif n==3 then widths={.30,.34,.36}
 elseif n==2 and s:match('^Disposition') then widths={.20,.80}
 elseif n==2 then widths={.25,.75} end
 if widths then for i,w in ipairs(widths) do t.colspecs[i][2]=w end end
 if FORMAT:match('latex') then local sz=(n==10 or s:match('^Requirement') or s:match('^SDK file')) and [[\begingroup\footnotesize]] or [[\begingroup\small]]; if s:match('^Store or shared requirement') then sz=[[\begingroup\small\renewcommand{\arraystretch}{1.04}]] end; return {pandoc.RawBlock('latex',sz),t,pandoc.RawBlock('latex',[[\endgroup]])} end
 return t
end
local function table_key(text)
 return text:match('^Table (S%d+%.%d+)%.') or text:match('^Table (%d+)%.')
end
function Para(p)
 if not FORMAT:match('latex') then return p end
 local text=pandoc.utils.stringify(p)
 -- Keep the query-interface lead-in with the header and first rows of its table (Blocks()).
 if text:match('^The query interface must show') then
  return {pandoc.RawBlock('latex',[[\Needspace{150pt}]]),p}
 end
 -- Keep the Section 4.2 lead-in that ends in a colon on one page with its whole planes list (about
 -- 150pt measured), so Figure 1, which follows the list, cannot fall between the lead-in and the list.
 if text:match('^The architecture separates three logical layers') then
  return {pandoc.RawBlock('latex',[[\Needspace{170pt}]]),p}
 end
 -- Keep the SDK-file lead-in with its three-row table (set in place in Blocks()). The table is
 -- set in footnote size with a one-line header, so the four-line lead-in and the table need 120pt.
 if text:match('^File A is') then
  return {pandoc.RawBlock('latex',[[\Needspace{120pt}]]),p}
 end
 -- An in-place captioned table reserves room for its caption and rows; a heading directly
 -- before it emits the reservation first (Blocks()), so heading and table stay together.
 local key=table_key(text)
 if key and INPLACE[key] then
  return {pandoc.RawBlock('latex','\\Needspace{'..INPLACE[key]..'}'),p}
 end
 return p
end
local function to_tabular(tbl)
 local tex=pandoc.write(pandoc.Pandoc({tbl}),'latex')
 tex=tex:gsub('\\begin{longtable}%[%]','\\begin{tabular}',1)
 local a,b=tex:find('\\endhead',1,true)
 local c,d=tex:find('\\endlastfoot',1,true)
 local e=tex:find('\\end{longtable}',1,true)
 assert(a and c and e,'unexpected longtable structure')
 return tex:sub(1,a-1)..tex:sub(d+1,e-1)..tex:sub(b+1,c-1)..'\\end{tabular}'
end
local function latex_of(block)
 return pandoc.write(pandoc.Pandoc({block}),'latex')
end
-- Tables 1 and 3 (PDF only): emit each float directly after the paragraph that cites it, so the float
-- can be placed near its citation rather than flushed by the barrier before the next section.
-- Without this, the former Table 3 took a float page after the end of Section 5 and the barrier before
-- Section 6 can leave the last lines of Section 5 alone on a page.
local function advance_table(bs,num,cite)
 for j=1,#bs-3 do
  if bs[j].t=='Para' and pandoc.utils.stringify(bs[j]):match('^Table '..num..'%.') and bs[j+2].t=='Table' then
   for k=j-1,1,-1 do
    if bs[k].t=='Para' and pandoc.utils.stringify(bs[k]):match(cite) then
     local held={bs[j],bs[j+1],bs[j+2],bs[j+3]}
     local out=pandoc.List()
     for m=1,#bs do
      if m<j or m>j+3 then out:insert(bs[m]) end
      if m==k then for _,x in ipairs(held) do out:insert(x) end end
     end
     return out
    end
   end
  end
 end
 return bs
end
-- Copy a table, keeping only body rows first..last.
local function rows_of(tbl,first,last)
 local c=tbl:clone()
 local bodies=c.bodies
 bodies[1].body=pandoc.List({table.unpack(tbl.bodies[1].body,first,last)})
 c.bodies=bodies
 return c
end
function Blocks(bs)
 if not FORMAT:match('latex') then return bs end
 local out=pandoc.List()
 local i=1
 while i<=#bs do
  local b=bs[i]
  local nxt=bs[i+1]
  local text=(b.t=='Para') and pandoc.utils.stringify(b) or ''
  local key=table_key(text)
  if key and key~='S9.1' and nxt and nxt.t=='RawBlock' and nxt.text:match('^\\begingroup') and bs[i+2] and bs[i+2].t=='Table' and bs[i+3] and bs[i+3].t=='RawBlock' then
   local size=nxt.text:gsub('^\\begingroup','')
   if INPLACE[key] then
    -- In-place captioned table: caption and rows set where they occur, after the reservation from Para().
    out:insert(pandoc.RawBlock('latex',latex_of(b)..'\\par\\smallskip\n{'..size..'\n'..to_tabular(bs[i+2])..'\n}\\par'))
   else
    -- Captioned table: a top-placed float with its caption above the rows.
    -- Table S6.1 is top-only ([t]) so that it never forms a float page of its own.
    local place=(key=='S2.1') and '[htp]' or (key=='S6.1') and '[t]' or (key=='2') and '[!ht]' or '[tp]'
    -- Table S4.1 fills a float page exactly, so it omits the small skip below its caption and, in Table(),
    -- sets its rows with a slightly smaller array stretch (1.04) than the other tables.
    local skip=(key=='S4.1') and '' or '\\smallskip'
    -- The former Table 1 was emitted after the Section 2.4 paragraph that cites it, below a level-3 heading that
    -- does not suppress top floats, so it could print at the top of that page, above the heading.
    -- \suppressfloats[t] before it keeps it from that page's top. Like Table 3 it is [!ht], so it prints
    -- below its citing paragraph if it fits there; a top-only placement left most of a page empty before
    -- the Section 3 barrier once Section 2.3 grew (29 October 2026).
    -- Table 3 ([!ht]) prints directly below its heading if it fits there; the same suppression keeps it
    -- from the top of the heading's page, so otherwise it moves to the top of the next page.
    local pre=(key=='2') and '\\suppressfloats[t]\n' or ''
    out:insert(pandoc.RawBlock('latex',pre..'\\begin{table}'..place..'\n'..latex_of(b)..'\\par'..skip..'\n{'..size..'\n'..to_tabular(bs[i+2])..'\n}\n\\end{table}'))
   end
   i=i+4
  elseif key=='S9.1' and nxt and nxt.t=='RawBlock' and nxt.text:match('^\\begingroup') and bs[i+2] and bs[i+2].t=='Table' and bs[i+3] and bs[i+3].t=='RawBlock' then
   -- Table S9.1 is taller than a page and its rows cannot break, so it is set as two floats: the caption
   -- with the first row at the bottom of a page ([!b]), then the remaining rows under "Table S9.1
   -- (continued)". The continuation fills a page, too tall for a top float above text, so [!tp] lets it
   -- take the float page that follows. The two parts then meet across one page break with no text between.
   local size=nxt.text:gsub('^\\begingroup','')
   local n=#bs[i+2].bodies[1].body
   assert(n==3,'Table S9.1 should have three rows')
   out:insert(pandoc.RawBlock('latex','\\begin{table}[!b]\n'..latex_of(b)..'\\par\\smallskip\n{'..size..'\n'..to_tabular(rows_of(bs[i+2],1,1))..'\n}\n\\end{table}'))
   out:insert(pandoc.RawBlock('latex','\\begin{table}[!tp]\n\\textbf{Table S9.1 (continued).}\\par\\smallskip\n{'..size..'\n'..to_tabular(rows_of(bs[i+2],2,n))..'\n}\n\\end{table}'))
   i=i+4
  elseif text:match('^File A is') and nxt and nxt.t=='RawBlock' and nxt.text:match('^\\begingroup') and bs[i+2] and bs[i+2].t=='Table' and bs[i+3] and bs[i+3].t=='RawBlock' then
   -- Uncaptioned SDK-file table: set in place after its lead-in, as a non-floating tabular, so it
   -- stays next to the text that explains it. The reservation emitted by Para() keeps the lead-in
   -- and all three rows on one page.
   local size=nxt.text:gsub('^\\begingroup','')
   out:insert(pandoc.RawBlock('latex',latex_of(b)..'\\par\\smallskip\n{'..size..'\n'..to_tabular(bs[i+2])..'\n}\\par'))
   i=i+4
  elseif text:match('^The query interface must show') and nxt and nxt.t=='RawBlock' and nxt.text:match('^\\begingroup') and bs[i+2] and bs[i+2].t=='Table' and bs[i+3] and bs[i+3].t=='RawBlock' then
   -- Uncaptioned query-interface table: set in place after its lead-in as a longtable, so it never
   -- interrupts the preceding paragraph. It is taller than the space usually left on its page, so it
   -- may break between rows, with its header repeated; the reservation emitted by Para() keeps the
   -- lead-in with the header and first rows.
   out:insert(b); out:insert(nxt); out:insert(bs[i+2]); out:insert(bs[i+3])
   i=i+4
  elseif (text:match('^Figure %d%.') or text:match('^Figure S%d+%.%d+%.')) and nxt and nxt.t=='Para' and #nxt.content==1 and nxt.content[1].t=='Image' then
   -- Figure: a top-placed float with its caption above the image. Figure 2 directly follows the
   -- Section 7 heading and its callout, so it is placed at the bottom of a page or on a float page.
   -- The ! lets it use more than the default 30 percent bottom area, which it needs; nothing else
   -- is placed at the bottom of a page.
   local place=text:match('^Figure 2%.') and '[!bp]' or '[tp]'
   out:insert(pandoc.RawBlock('latex','\\begin{figure}'..place))
   out:insert(b); out:insert(nxt)
   out:insert(pandoc.RawBlock('latex','\\end{figure}'))
   i=i+2
  elseif b.t=='Header' and b.level<=2 then
   -- Keep each numbered section's floats inside it: flush pending floats before the heading
   -- and forbid a top float above the heading on its own page. The S6 heading starts a new page
   -- (\clearpage also flushes floats), so the \suppressfloats after it acts on the heading's own page.
   if b.level==2 and pandoc.utils.stringify(b):match('^S6%.') then
    out:insert(pandoc.RawBlock('latex','\\clearpage'))
   else
    out:insert(pandoc.RawBlock('latex','\\FloatBarrier'))
   end
   if nxt and nxt.t=='RawBlock' and nxt.text:match('^\\[Nn]eedspace') then out:insert(nxt); i=i+1 end
   if b.level==1 then
    -- Document title: ragged right without hyphenation, so lines break between words.
    out:insert(pandoc.RawBlock('latex',[[\begingroup\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000]]))
    out:insert(b); out:insert(pandoc.RawBlock('latex',[[\endgroup]]))
   else
    out:insert(b)
   end
   out:insert(pandoc.RawBlock('latex','\\suppressfloats[t]')); i=i+1
  elseif b.t=='Header' and nxt and nxt.t=='RawBlock' and nxt.text:match('^\\[Nn]eedspace') then
   -- Keep a heading with the reservation that follows it: emit the reservation first.
   out:insert(nxt); out:insert(b); i=i+2
  elseif b.t=='Para' and #b.content==1 and b.content[1].t=='Strong' and nxt and nxt.t=='BulletList' then
   -- Keep a bold label with the list it introduces.
   out:insert(pandoc.RawBlock('latex',[[\needspace{4\baselineskip}]])); out:insert(b); i=i+1
  else
   out:insert(b); i=i+1
  end
 end
 return out
end
function Image(i)
 if FORMAT:match('latex') then i.src=i.src:gsub('%.svg$','.pdf'); i.attributes['width']='86%' end
 return i
end
function Str(s)
 -- Signal and mechanism identifiers, such as SIG-16 or PAY-05, are lookup keys, so the PDF never
 -- breaks them at their hyphen. The identifier is boxed; leading and trailing punctuation stays outside.
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
 -- Short code containing spaces, such as inline arithmetic, is set as one unbreakable unit.
 if FORMAT:match('latex') and c.text:find(' ',1,true) and (utf8.len(c.text) or 30)<30 then
  local tex=pandoc.write(pandoc.Pandoc({pandoc.Plain({c})}),'latex'):gsub('%s+$','')
  return pandoc.RawInline('latex','\\mbox{'..tex..'}')
 end
 if FORMAT:match('latex') and #c.text>30 and c.text:match('^[a-f0-9]+$') then
  return pandoc.RawInline('latex',[[\texttt{\seqsplit{]]..c.text..'}}')
 end
 if FORMAT:match('latex') and #c.text>30 and c.text:match('/') then
  local esc=c.text:gsub('[\\{}_#%%&$~^]',function(ch)
   if ch=='\\' then return [[\textbackslash{}]] elseif ch=='~' then return [[\textasciitilde{}]] elseif ch=='^' then return [[\textasciicircum{}]] end
   return '\\'..ch end)
  esc=esc:gsub('/','/\\allowbreak ')
  return pandoc.RawInline('latex','\\texttt{'..esc..'}')
 end
 return c
end
