from PIL import Image, ImageDraw, ImageFont
import os, math

W=H=1024
PAPER='#f4f0e7'; INK='#17212b'; MUTED='#59636b'; RED='#b43831'; LINE='#c9c2b6'; WHITE='#fffdf8'; NAVY='#153149'
im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im)
SANS='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; SER='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'; ITAL='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
def font(sz,path=SANS): return ImageFont.truetype(path,sz)
def txt(x,y,s,sz=12,fill=INK,path=SANS): d.text((x,y),s,font=font(sz,path),fill=fill)
def rounded(box,r=9,fill=WHITE,outline=LINE,w=1): d.rounded_rectangle(box,r,fill=fill,outline=outline,width=w)
def wrap(s,f,maxw):
    words=s.split(); lines=[]; cur=''
    for word in words:
        t=(cur+' '+word).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    return lines
def fit_lines(s,path,size,minsize,maxw,maxlines):
    while size>=minsize:
        f=font(size,path); lines=wrap(s,f,maxw)
        if len(lines)<=maxlines:return f,lines
        size-=1
    f=font(minsize,path); lines=wrap(s,f,maxw)[:maxlines]
    return f,lines
def draw_lines(x,y,lines,f,fill,lh=None):
    lh=lh or int(f.size*1.2)
    for i,line in enumerate(lines): d.text((x,y+i*lh),line,font=f,fill=fill)

regions=['N. America','Latin America','Europe','Middle East','Africa','South Asia','East & SE Asia','Oceania','Global']
colors={'N. America':'#39728a','Latin America':'#bd713e','Europe':'#4b6e55','Middle East':'#b9483d','Africa':'#aa7a31','South Asia':'#765a9a','East & SE Asia':'#315b9b','Oceania':'#25847d','Global':'#555b64'}
# story number -> region (all 38, region categories sum to 38)
rmap={1:'N. America',2:'East & SE Asia',3:'South Asia',4:'Africa',5:'Europe',6:'Europe',7:'Europe',8:'Africa',9:'Middle East',10:'Middle East',11:'Middle East',12:'East & SE Asia',13:'South Asia',14:'Oceania',15:'Middle East',16:'N. America',17:'N. America',18:'N. America',19:'Oceania',20:'East & SE Asia',21:'Africa',22:'Latin America',23:'South Asia',24:'Middle East',25:'Middle East',26:'Europe',27:'Europe',28:'Europe',29:'Europe',30:'Latin America',31:'N. America',32:'N. America',33:'East & SE Asia',34:'N. America',35:'N. America',36:'Global',37:'Europe',38:'Global'}

# Top identity strip
d.rectangle((0,0,W,31),fill=NAVY)
txt(24,7,'THE WORLD IN ONE DAY',12,'#fffdf8',BOLD)
txt(475,8,'38 STORIES  ·  10 REGIONS  ·  ALL FIRST REPORTED WEDNESDAY 25 NOVEMBER 2026',9,'#e6e5df',BOLD)
txt(24,38,'Wednesday 25 November 2026',40,INK,SER)
txt(26,87,'TARIFFS PROPOSED · ASIAN CHIP STOCKS SLIDE · PAKISTAN JOINS TIANGONG',14,RED,ITAL)
# region bar
counts={r:sum(1 for v in rmap.values() if v==r) for r in regions}
txt(24,115,'REGION',9,MUTED,BOLD)
labels=['N. America','Latin America','Europe','Middle East','Africa','South Asia','East & SE Asia','Oceania','Global']
# give every region a minimum width, then distribute remaining width by count
x=24; y=131; total=976; minimum=88
extra=total-minimum*len(regions)
weights=sum(counts.values())
widths={r:minimum+extra*counts[r]/weights for r in regions}
for r in regions:
    ww=widths[r]
    d.rectangle((x,y,x+ww-2,y+31),fill=colors[r])
    lab=f'{r}  {counts[r]}'
    f=font(9,BOLD)
    txt(x+5,y+9,lab,9,'white',BOLD)
    x+=ww
txt(24,168,'THE DAY IN SIX FIGURES',9,MUTED,BOLD)
figs=[('-6.2%','KOSPI CLOSE'),('14','ECONOMIES IN US TARIFF PLAN'),('1st','FOREIGN ASTRONAUT ON TIANGONG'),('+26%','UK ENERGY CAP FROM JAN'),('31','KILLED IN CAIRO TANKER BLAST'),('4.3%','US Q3 GDP, REVISED')]
for i,(big,small) in enumerate(figs):
    x=24+i*163
    rounded((x,182,x+155,219),6,WHITE,LINE)
    txt(x+8,183,big,17,RED,SER)
    smf,sml=fit_lines(small,BOLD,7,6,139,2); draw_lines(x+8,203,sml,smf,INK,8)

# Heroes: cards with custom illustrations
def ship_icon(x,y,w,h):
    # sea, hull, containers, crane and hanging tariff tag
    d.rectangle((x,y+h-22,x+w,y+h),fill='#d8e5e6')
    d.polygon([(x+12,y+h-26),(x+w-15,y+h-26),(x+w-31,y+h-8),(x+27,y+h-8)],fill='#203e55')
    for j,c in enumerate(['#be573d','#d69b45','#49798a','#d7ba77']):
        xx=x+28+j*34
        d.rectangle((xx,y+h-59,xx+30,y+h-28),fill=c,outline=WHITE,width=1)
        d.line((xx+7,y+h-55,xx+7,y+h-32),fill='#f0d8b8',width=1)
    d.line((x+134,y+12,x+134,y+45),fill=INK,width=2); d.line((x+134,y+12,x+185,y+12),fill=INK,width=2)
    d.line((x+178,y+12,x+178,y+35),fill=RED,width=2)
    d.polygon([(x+165,y+35),(x+191,y+35),(x+187,y+57),(x+169,y+57)],fill=RED)
    txt(x+169,y+39,'20%',8,'white',BOLD)
def chart_icon(x,y,w,h):
    rounded((x+8,y+8,x+w-8,y+h-8),6,'#fbfaf5','#d9d2c8')
    # descending market bars
    vals=[31,25,29,20,14,9,5]; xx=x+20
    for i,v in enumerate(vals):
        yy=y+21+(35-v)
        d.rectangle((xx+i*25,yy,xx+13+i*25,y+58),fill='#c84c43')
    pts=[(x+18,y+20),(x+45,y+25),(x+70,y+31),(x+95,y+36),(x+120,y+44),(x+146,y+50),(x+173,y+58)]
    d.line(pts,fill=RED,width=3)
    txt(x+14,y+66,'KOSPI  −6.16%',10,INK,BOLD)
    txt(x+14,y+80,'SK hynix −11.05%  ·  Samsung −9.87%',8,MUTED,BOLD)
def space_icon(x,y,w,h):
    # star field, earth limb, station, rocket
    for sx,sy in [(18,17),(69,12),(144,22),(195,12),(220,49),(83,62)]: d.ellipse((x+sx,y+sy,x+sx+2,y+sy+2),fill='#71859a')
    d.ellipse((x+156,y+48,x+225,y+116),fill='#1c6684')
    d.arc((x+149,y+43,x+230,y+124),180,275,fill='#7ac0c5',width=3)
    # station panels + module
    d.rectangle((x+41,y+38,x+92,y+55),fill='#c5d5db',outline=INK,width=1)
    d.rectangle((x+52,y+32,x+81,y+61),fill='#e9e5d8',outline=INK,width=1)
    d.rectangle((x+27,y+35,x+40,y+58),fill='#366f9c'); d.rectangle((x+93,y+35,x+106,y+58),fill='#366f9c')
    # rocket
    d.polygon([(x+133,y+26),(x+144,y+11),(x+155,y+26),(x+153,y+62),(x+135,y+62)],fill='#f4f0e7',outline=INK)
    d.polygon([(x+135,y+52),(x+126,y+65),(x+137,y+61)],fill=RED); d.polygon([(x+153,y+52),(x+162,y+65),(x+151,y+61)],fill=RED)
    d.ellipse((x+140,y+33,x+149,y+42),fill='#39728a')
    # flags
    # recognizable Pakistan and China flags, with captions
    d.line((x+114,y+2,x+114,y+28),fill=INK,width=2); d.rectangle((x+116,y+3,x+154,y+25),fill='#168b59'); d.rectangle((x+116,y+3,x+124,y+25),fill='#fffdf8')
    d.ellipse((x+131,y+7,x+147,y+23),fill='#fffdf8'); d.ellipse((x+136,y+5,x+150,y+21),fill='#168b59')
    d.polygon([(x+141,y+7),(x+143,y+12),(x+148,y+12),(x+144,y+15),(x+146,y+20),(x+141,y+17),(x+137,y+20),(x+139,y+15),(x+135,y+12),(x+140,y+12)],fill='#fffdf8')
    txt(x+118,y+27,'PAKISTAN',6,NAVY,BOLD)
    d.line((x+168,y+2,x+168,y+28),fill=INK,width=2); d.rectangle((x+170,y+3,x+208,y+25),fill='#de2910')
    d.polygon([(x+177,y+6),(x+179,y+10),(x+183,y+10),(x+180,y+12),(x+181,y+16),(x+177,y+14),(x+174,y+16),(x+175,y+12),(x+172,y+10),(x+176,y+10)],fill='#ffde00')
    for sx,sy in [(187,6),(193,10),(193,17),(187,21)]: d.ellipse((x+sx,y+sy,x+sx+3,y+sy+3),fill='#ffde00')
    txt(x+174,y+27,'CHINA',6,NAVY,BOLD)
    txt(x+43,y+65,'SHENZHOU-24',7,NAVY,BOLD); txt(x+170,y+100,'TIANGONG',7,WHITE,BOLD)
heroes=[
(1,'WASHINGTON / TRADE','OFFICIAL','US proposes new tariffs on 14 economies','Up to 20% China and Singapore, 35% Vietnam, 25% India, 15% EU and Japan. Proposals open for comment, not yet in force.','Proposals could reshape trade across 14 economies.','ship'),
(2,'SEOUL / MARKETS','REPORTED','AI doubts sink Asian chip stocks: Kospi -6.2%','Kospi fell 6.16% to 4,697.51, wiping out Tuesday’s +6.3% Huang rally. Goldman and Morgan Stanley cut chip targets.','A sharp reversal hit the region’s leading chip shares.','chart'),
(3,'JIUQUAN, CHINA / SPACE','OFFICIAL','Pakistani becomes first foreigner aboard China’s space station','Shenzhou-24 docked with Muhammad Zeeshan Ali, 40, and Chinese crew Tang Hongbo and Wu Yi; stay: 5–10 days.','Pakistan’s first astronaut joined the Tiangong crew.','space')]
for i,(num,place,status,head,sub,why,kind) in enumerate(heroes):
    x=24+i*328; y=228; w=314; h=230
    rounded((x,y,x+w,y+h),10,WHITE,LINE)
    d.rectangle((x+1,y+1,x+w-1,y+4),fill=colors[rmap[num]])
    # illustrative inset
    d.rectangle((x+10,y+11,x+w-10,y+111),fill='#edf0ec')
    if kind=='ship':ship_icon(x+10,y+11,w-20,100)
    elif kind=='chart':chart_icon(x+10,y+11,w-20,100)
    else:space_icon(x+10,y+11,w-20,100)
    txt(x+12,y+117,place,9,colors[rmap[num]],BOLD)
    tagw=68 if status=='OFFICIAL' else 72
    rounded((x+w-tagw-10,y+114,x+w-10,y+132),5,'#e8ece8',None)
    txt(x+w-tagw-5,y+117,status,8,INK,BOLD)
    f,ls=fit_lines(head,SER,14,12,w-24,2); draw_lines(x+12,y+139,ls,f,INK,int(f.size*1.15))
    subf,sls=fit_lines(sub,SANS,9,8,w-24,2); draw_lines(x+12,y+174,sls,subf,MUTED,11)
    txt(x+12,y+199,'WHY IT MATTERS',7,RED,BOLD)
    wf,wls=fit_lines(why,BOLD,8,7,w-24,2); draw_lines(x+12,y+209,wls,wf,INK,9)

# Secondary story tiles 4-15
secondary=[
(4,'CAIRO, EGYPT','REPORTED','Fuel tanker blast kills 31 in Cairo','25 injured after tanker exploded on Ring Road.','blast'),
(5,'UKRAINE','REPORTED','Russian strikes kill 5, cut power in 5 regions','Zaporizhzhia plant ran on diesel, its 17th outage in 2026.','power'),
(6,'SAMARA, RUSSIA','REPORTED','Ukrainian drones hit two Rosneft refineries','Syzran and Kuibyshev ablaze; Russia says 145 drones downed.','fire'),
(7,'LONDON','OFFICIAL','UK energy price cap to rise 26% in January','Ofgem: typical annual bill £1,723 → £2,166 from 1 Jan.','bill'),
(8,'CAPE TOWN','OFFICIAL','Court sets aside Phala Phala report','Court: not a finding on Ramaphosa’s conduct.','gavel'),
(9,'JERUSALEM','REPORTED','Judges urge prosecutors to drop Netanyahu case','Court cast doubt on Case 4000; Netanyahu says trial “must end”.','court'),
(10,'SAUDI ARABIA','CLAIM','Houthis claim drone attack on Saudi refinery','Saudi Arabia says four drones were downed.','drone'),
(11,'HORMUZ','CLAIM','Iran says two tankers hit mines in Hormuz','IRGC Navy says ships caught fire on an “unauthorised route”.','ship'),
(12,'WEST JAVA','REPORTED','Flooded gold mine: 9 dead, 17 trapped','River floods illegal shafts in West Java.','flood'),
(13,'DHAKA','OFFICIAL','Garment minimum wage raised to Tk 17,000','Up from Tk 12,500; unions demand Tk 18,000.','worker'),
(14,'CANBERRA','OFFICIAL','Solomon Islands names Australia security partner','Leaders sign treaty after ending 2022 China pact.','pact'),
(15,'GAZA CITY','REPORTED','Israeli strike kills Hamas official and family','Wife and two daughters killed in Shati camp; 7 more in other strikes.','blast')]

def icon(x,y,k):
    # simple, legible line-art pictograms in a 27px circle
    d.ellipse((x,y,x+28,y+28),fill='#f0e8dc',outline='#d5cabb')
    cx=x+14; cy=y+14
    if k in ('blast','fire'):
        d.polygon([(cx-7,cy+7),(cx-6,cy-1),(cx-2,cy+2),(cx,cy-9),(cx+3,cy-2),(cx+8,cy-5),(cx+6,cy+7)],fill=RED)
    elif k in ('power','worker'):
        d.line((cx,cy-10,cx-5,cy+1,cx+1,cy+1,cx-2,cy+10),fill=NAVY,width=2)
    elif k in ('ship','flood'):
        d.polygon([(cx-10,cy+2),(cx+10,cy+2),(cx+6,cy+8),(cx-6,cy+8)],fill='#39728a'); d.line((cx-10,cy+11,cx+10,cy+11),fill='#39728a',width=1)
    elif k in ('gavel','court'):
        d.line((cx-7,cy+7,cx+7,cy-7),fill=NAVY,width=3); d.rectangle((cx-8,cy-8,cx-1,cy-4),fill=RED); d.rectangle((cx+2,cy+4,cx+9,cy+8),fill=RED)
    elif k=='drone':
        d.line((cx-8,cy,cx+8,cy),fill=NAVY,width=2); d.line((cx,cy-2,cx,cy+8),fill=NAVY,width=2); d.ellipse((cx-10,cy-4,cx-5,cy+1),outline=RED); d.ellipse((cx+5,cy-4,cx+10,cy+1),outline=RED)
    else:
        d.rectangle((cx-8,cy-5,cx+8,cy+6),outline=NAVY,width=2); d.line((cx-4,cy-7,cx+4,cy-7),fill=RED,width=2)

for idx,item in enumerate(secondary):
    num,place,status,head,sub,k=item; col=idx%6; row=idx//6
    x=24+col*163; y=466+row*78; w=155; h=76
    rounded((x,y,x+w,y+h),7,WHITE,LINE)
    d.ellipse((x+7,y+6,x+25,y+24),fill=colors[rmap[num]])
    nf=font(9,BOLD); nw=d.textlength(str(num),font=nf); d.text((x+16-nw/2,y+8),str(num),font=nf,fill='white')
    icon(x+31,y+4,k)
    # location and compact colour-coded status pill
    pillcol={'OFFICIAL':'#94cda4','REPORTED':'#9fc4df','CLAIM':'#efb2a5'}[status]
    pillw={'OFFICIAL':48,'REPORTED':54,'CLAIM':38}[status]
    short_places={4:'CAIRO',5:'UKRAINE',6:'SAMARA',7:'LONDON',8:'CAPE TOWN',9:'JERUSALEM',10:'SAUDI',11:'HORMUZ',12:'WEST JAVA',13:'DHAKA',14:'CANBERRA',15:'GAZA'}
    place=short_places[num]
    draw_lines(x+64,y+3,[place],font(9,BOLD),colors[rmap[num]])
    rounded((x+64,y+17,x+64+pillw,y+30),5,pillcol,None)
    tw=d.textlength(status,font=font(8,BOLD)); txt(x+64+(pillw-tw)/2,y+19,status,8,INK,BOLD)
    hf,hls=fit_lines(head,SER,10,8,w-14,2); draw_lines(x+7,y+29,hls,hf,INK,int(hf.size*1.1))
    sf,sls=fit_lines(sub,SANS,8,7,w-14,2); draw_lines(x+7,y+53,sls,sf,MUTED,9)

# lower zone map left; list right
# map panel
rounded((24,624,384,900),9,'#e9eee9',LINE)
txt(36,632,'WHERE IT HAPPENED',10,INK,BOLD)
# simplified world map silhouettes, enlarged into the available map area
# North America, South America, Europe/Africa, Asia, Australia
d.polygon([(36,692),(59,670),(101,667),(131,679),(123,701),(107,710),(95,738),(76,735),(65,716),(47,710)],fill='#c3d0c8',outline='#80918a')
d.polygon([(101,741),(124,749),(133,766),(127,787),(119,802),(112,832),(101,820),(95,793),(88,770)],fill='#c3d0c8',outline='#80918a')
d.polygon([(199,686),(224,679),(247,686),(255,699),(241,709),(228,705),(217,718),(204,706)],fill='#c3d0c8',outline='#80918a')
d.polygon([(219,710),(245,708),(257,728),(252,755),(241,778),(231,803),(220,789),(215,759),(209,734)],fill='#c3d0c8',outline='#80918a')
d.polygon([(252,686),(289,674),(339,686),(359,704),(345,722),(314,718),(304,738),(284,731),(274,710),(256,710)],fill='#c3d0c8',outline='#80918a')
d.polygon([(266,684),(284,674),(302,680),(307,691),(294,697),(288,711),(274,707)],fill='#c3d0c8',outline='#80918a')
d.ellipse((319,779,355,801),fill='#c3d0c8',outline='#80918a')
# numbered region-colored map pins for stories represented (all 38 using clustered coordinates)
coords={
1:(53,700),16:(72,696),17:(91,700),18:(52,714),31:(96,716),34:(67,729),35:(43,711),
22:(87,751),30:(101,768),
5:(145,699),6:(157,706),7:(173,697),9:(184,706),26:(151,715),27:(165,714),28:(177,714),29:(142,706),32:(184,696),37:(158,697),
4:(151,736),8:(171,746),21:(157,756),
10:(194,720),11:(180,729),15:(191,735),24:(174,725),25:(193,708),
13:(205,729),23:(199,742),3:(208,719),
2:(222,700),12:(238,711),20:(218,724),33:(239,729),
14:(235,759),19:(246,772),
36:(136,687),38:(151,681)
}
for n,(px,py) in coords.items():
    # cluster offsets, connected back to the approximate region position
    spread={6:(151,692),7:(178,690),9:(191,700),26:(143,722),27:(171,724),28:(182,711),29:(137,700),37:(163,688),10:(201,713),11:(181,738),15:(202,742),24:(169,733),25:(199,704),13:(211,737),23:(207,751),3:(216,714),2:(230,692),12:(249,706),20:(216,736),33:(247,735),5:(131,744),32:(141,754),4:(152,768),8:(177,778),21:(198,770)}
    leader=None
    if n in spread:
        ox,oy=px,py; px,py=spread[n]; leader=(ox,oy,px,py)
    px=36+(px-42)*1.55; py=667+(py-688)*1.48
    if leader:
        ax,ay,bx,by=leader
        d.line((36+(ax-42)*1.55,667+(ay-688)*1.48,px,py),fill='#718078',width=1)
    c=colors[rmap[n]]
    d.ellipse((px-7,py-7,px+7,py+7),fill=c,outline=WHITE,width=1)
    nf=font(8,BOLD); tw=d.textlength(str(n),font=nf); d.text((px-tw/2,py-4),str(n),font=nf,fill='white')
txt(35,844,'Numbered pins match stories 1–38',8,MUTED)
# legend row in 2 lines
legend=[('N. Am.','N. America'),('Lat. Am.','Latin America'),('Europe','Europe'),('M. East','Middle East'),('Africa','Africa'),('S. Asia','South Asia'),('E/SE Asia','East & SE Asia'),('Oceania','Oceania'),('Global','Global')]
for i,(lab,r) in enumerate(legend):
    xx=35+(i%3)*105; yy=858+(i//3)*12
    d.ellipse((xx,yy+2,xx+6,yy+8),fill=colors[r]); txt(xx+8,yy,lab,8,MUTED)

# 23 compact numbered headlines in two columns
# concise, source wording retained; location in bold label
stories=[
('Washington','Q3 GDP growth revised up to 4.3%'),('Washington','Jobless claims fall to 189,000, 4-month low'),('New York','Dow +0.3% to 50,183; Nasdaq -0.6%'),('Sydney',"Australia's inflation jumps to 4.9%"),('Kuala Lumpur','Regulator sues Google for RM600m over YouTube'),('Ed Damazin, Sudan','RSF drones kill at least 19'),('Cartagena, Colombia','All 76 supermarket hostages freed'),('Karachi','Building collapse kills 3, injures 14'),('Baghdad','Court backs federal control of Kurdish oil'),('Hasakah, Syria','IS suicide bomber kills 2'),('Athens','General strike halts ferries, metro, flights'),('Brussels','EU, UK fine fragrance makers over €570m'),('Berlin','Merz defends tighter 2027 budget'),('Warsaw','Poland plans no-fly zone on Ukraine border'),('Brasília','Brazil recalls ambassador to Argentina'),('Mexico City','Sheinbaum protests to US over deported TV host'),('Madrid','Kilmar Abrego Garcia arrives after leaving US'),('Cambodia','Biggest-ever drill with China begins'),('Iowa, US','Army detonates 5 tons of unstable explosive'),('Mississippi, US','Plane crash kills family of 6'),('Space',"ESA's Hera images DART's stadium-sized crater"),('Football','Brugge 0-3 Liverpool; Lille 2-1 Bayern'),('UN','47,000 women killed by partners or relatives in 2025')]
rounded((398,624,1000,900),9,'#faf8f2',LINE)
txt(412,633,'ALSO ON WEDNESDAY 25 NOVEMBER',11,INK,BOLD)
for i,(place,body) in enumerate(stories):
    col=i//8; row=i%8
    x=412+col*194; y=652+row*30
    label=place+': '; lf=font(9,BOLD); bodyf=font(9,SANS)
    prefix=f'{i+16}. '
    room1=182-d.textlength(prefix,font=font(9,BOLD))-d.textlength(label,font=lf)
    words=body.split(); first=''
    while words:
        candidate=(first+' '+words[0]).strip()
        if d.textlength(candidate,font=bodyf)>room1: break
        first=candidate; words.pop(0)
    second=' '.join(words)
    assert first and (not second or d.textlength(second,font=bodyf)<=162), f'item {i+16} exceeds two lines'
    d.text((x,y),prefix,font=font(9,BOLD),fill=RED)
    px=x+d.textlength(prefix,font=font(9,BOLD)); d.text((px,y),label,font=lf,fill=INK)
    d.text((px+d.textlength(label,font=lf),y),first,font=bodyf,fill=MUTED)
    if second:
        d.text((x+20,y+12),second,font=bodyf,fill=MUTED)
    measured_height=23 if second else 12
    assert measured_height<=29 and y+measured_height<900, f'item {i+16} exceeds its column box'

# Date check + status/source footer
d.rectangle((24,910,1000,1016),fill=NAVY)
txt(38,918,'DATE CHECK',10,'#f0c76f',BOLD)
check='Every story happened or was first reported on Wednesday 25 November 2026. Left out as earlier news: Huang’s return to Nvidia (Mon 23 Nov), Huawei’s US conviction (Tue 24 Nov), CAS restoring Senegal’s AFCON title (Tue 24 Nov). Not yet: US Thanksgiving (Thu 26 Nov), UK price cap takes effect (1 Jan).'
f,ls=fit_lines(check,SANS,10,9,840,2); draw_lines(140,918,ls,f,'#fffdf8',12)
# status key and source line
# status tags
txt(38,968,'STATUS',9,'#f0c76f',BOLD)
for x,label,col in [(93,'OFFICIAL · authority’s own words','#94cda4'),(285,'REPORTED · 2+ major outlets','#9fc4df'),(477,'CLAIM · one side’s account','#efb2a5')]:
    rounded((x,970,x+7,977),3,col,None); txt(x+10,967,label,9,'#fffdf8',BOLD)
txt(38,990,'Sources: USTR, Ofgem, CMSA, BEA, ABS, Reuters, AP, AFP, BBC, Al Jazeera, Yonhap, Xinhua, News24, Times of Israel',9,'#d9e0e2',BOLD)

os.makedirs(os.path.dirname(os.path.abspath(__file__)),exist_ok=True)
out=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'entry.png')
im.save(out,'PNG',optimize=True)
print(f'wrote {out}: {os.path.getsize(out)} bytes')
