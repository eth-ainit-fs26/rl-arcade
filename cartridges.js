/* cartridges.js : the course arcade registry (the single source of truth for content).
 *
 * Split into a FRONT SCREEN (headliners) and a THEORY GAMES bundle (the
 * concept visualizations that build intuition for the ideas we teach).
 *
 * INTEGRATOR: to add a game, edit ONLY this file (4 steps):
 *   1. add a GAMES entry   {name, href, acc, tag:"RL"|"BIZ", blurb}
 *   2. add its pixel sprite to SPRITES   (a grid of rows; PX maps each char to a colour, '.' = transparent)
 *   3. add the sprite's key to SPR        (SAME order/index as GAMES)
 *   4. add the game into VIEWS.extra (THEORY GAMES) or VIEWS.main (a front-screen headliner)
 * Counts (the "N IN 1" badge, the THEORY "+N" tag, the bundle blurb) auto-derive from these.
 *
 * The ANYMAL / CASINO / DARTS / SPOOKY HOUSE / MINIGOLF cartridges are the
 * course's own HTML visualizations (from eth-ainit-fs26/coding-exercises);
 * the rest are the shared business + RL games.
 *
 * index.html (the chrome + engine) consumes window.GAMES / SPRITES / PX / SPR / EXTRA / VIEWS.
 */
window.GAMES = [
  // front screen (headliners), in display order
  {name:"ANYMAL MDP",          href:"anymal-mdp/",         acc:"#60a5fa", tag:"RL",  blurb:"A robot dog roams a grid chasing treats. Name its state, moves, outcomes, and payoffs to see what every decision problem is made of."},
  {name:"REPAIR OR REPLACE",   href:"repair-or-replace/",  acc:"#9aa7ff", tag:"BIZ", blurb:"One van, four states of wear. Run it, shop it, or buy new: scrap it while it still starts, timing set by gamma."},
  {name:"LAST-MINUTE PRICING", href:"last-minute-pricing/",acc:"#ff8a3c", tag:"BIZ", blurb:"Perishable stock, a midnight deadline. Set a price each day; the revenue-management surface, learned by DP then SARSA."},
  {name:"RECYCLING ROBOT",     href:"recycling-robot/",    acc:"#4ecb8f", tag:"RL",  blurb:"A canister-collecting robot on a battery: search, wait, or recharge? The lever flips up the battery gauge, so a low battery means recharge before you strand."},
  {name:"POKEMON BATTLE",      href:"pokemon-battle/",     acc:"#ffe000", tag:"RL",  blurb:"A wild CHARMANDER appeared! The same RL lesson under a Gen-1 Red/Blue battle screen."},
  {name:"STALE BY SUNDOWN",    href:"stale-by-sundown/",   acc:"#ff7a59", tag:"BIZ", blurb:"Fresh stock spoils by sundown: hold, discount, or dump? The right call marches down the freshness tier (age, not stock, drives it)."},
  {name:"CRITICAL SPARE",      href:"critical-spare/",     acc:"#8aa0b8", tag:"BIZ", blurb:"One machine, one spare bin: run, order a spare, or replace? Pre-position the spare as the machine ages, before a failure strands you."},
  // theory games (the concept visualizations, from the course's coding-exercises)
  {name:"CASINO",              href:"casino/",             acc:"#fbbf24", tag:"RL",  blurb:"Five slot machines, hidden odds. Pull levers by hand, learn the best one, then let epsilon-greedy balance exploring against cashing in."},
  {name:"SPOOKY HOUSE",        href:"spooky-house/",       acc:"#c084fc", tag:"RL",  blurb:"A haunted grid of ghosts. Walk right or down to grab the most fright, then watch one recursion beat every brute force route."},
  {name:"DARTS IN THE DARK",   href:"darts/",              acc:"#38bdf8", tag:"RL",  blurb:"Throw darts at a bullseye you cannot see. Big misses, big corrections, then shrink your steps so the aim settles."},
  {name:"MINIGOLF",            href:"minigolf/",           acc:"#22c55e", tag:"RL",  blurb:"Aim your putt at a hidden hole, but the wind nudges every shot. One swing lies, so judge your force over many noisy tries."},
];

/* sprite key per game, SAME order as GAMES */
window.SPR=['robot','van','tag','robot2','pokeball','sun','crate','reel7','ghost','target','golf'];

/* palette: char -> colour ('.' = transparent) */
window.PX={'.':null,K:'#0b0b16',W:'#f4f6ff',R:'#ff4d5e',r:'#c0202e',G:'#6be24a',g:'#1f9a52',
  B:'#41a6ff',b:'#9aa7ff',Y:'#ffd23f',O:'#ff9a3c',P:'#b06bff',C:'#5ad0ff',S:'#c9cee6',s:'#6c7194',N:'#9a6a3c'};

/* one inline-SVG pixel sprite per game (plus qblock=THEORY bundle icon, dog=attract mascot) */
window.SPRITES={
  robot:[".....R.....",".....K.....","..KKKKKKK..","..KSSSSSK..","..KSSSSSK..",
         "..KCCSCCK..","..KSSSSSK..","..KSKKKSK..","..KKKKKKK..","...K...K..."],
  van:["...........","...KKKKKKK.","..KKWWKbbbK",".KbbbbbbbbK",".KbbbbbbbbK",
       ".KbbbbbbbbK",".KKKKKKKKK.","..KK...KK..","..KK...KK..","..........."],
  tag:["..KKKKKKK..",".KOOOKOOOK.",".KOOOOOOOK.",".KOYYYOOOK.",".KOYOOOOOK.",
       ".KOYYYOOOK.",".KOOOYOOOK.",".KOYYYOOOK.",".KOOOOOOOK.","..KKKKKKK.."],
  robot2:[".....K.....","...KKKKK...","..KGGGGGK..","..KCGGGCK..","..KGGGGGK..",
          "...KKKKK...","..KGGGGGK..","..KGGGGGK..","..KGGGGGK..","...K...K...","..........."],
  pokeball:["...KKKKK...",".KKRRRRRKK.",".KRRRRRRRK.","KRRRRRRRRRK","KRRRWWWRRRK",
            "KKKKWKWKKKK","KWWWWWWWWWK","KWWWWWWWWWK",".KWWWWWWWK.",".KKWWWWWKK.","...KKKKK..."],
  sun:["...........","....K.K....",".K..OOO..K.","...OOOOO...",".KKOOOOOKK.",
       "..OOOOOOO..","KKKKKKKKKKK","...........","...........","...........","..........."],
  crate:["KKKKKKKKKKK","KNNKNNNKNNK","KNNKNNNKNNK","KKKKKKKKKKK","KNKNNNNNKNK",
         "KNKNNNNNKNK","KKKKKKKKKKK","KNNKNNNKNNK","KNNKNNNKNNK","KKKKKKKKKKK","..........."],
  reel7:["..KKKKKKK..","..KYYYYYK..","..KRRRRRK..","..KYYYRYK..","..KYYYRYK..",
         "..KYYRYYK..","..KYYRYYK..","..KYRYYYK..","..KYYYYYK..","..KKKKKKK.."],
  ghost:["...KKKKK...","..KPPPPPK..",".KPPPPPPPK.",".KPWWPWWPK.",".KPWWPWWPK.",
         ".KPPPPPPPK.",".KPPPPPPPK.",".KPPPPPPPK.",".KPPPPPPPK.",".KP..P..PK."],
  target:["...........","...RRRRR...","..RWWWWWR..",".RWRRRRRWR.",".RWRWWWRWR.",
          ".RWRWRWRWR.",".RWRWWWRWR.",".RWRRRRRWR.","..RWWWWWR..","...RRRRR...","..........."],
  golf:["..KK.......","..KRKK.....","..KRRRKK...","..KRRRRRK..","..KRRRKK...",
        "..KRKK.....","..KK..KWK..","..K..gGGg..",".gKgGGGGGGg","gGKGKKKGGGg","gggKKKggggg"],
  qblock:["KKKKKKKKKKK","KYYYYYYYYYK","KYsYYYYYsYK","KYYYKKKYYYK","KYYKYYYKYYK",
          "KYYYYYKYYYK","KYYYYKYYYYK","KYYYYYYYYYK","KYYYYKYYYYK","KYsYYYYYsYK","KKKKKKKKKKK"],
  dog:["............KK",".KK........KSK",".KKKKKKKKKKSCK","KSSSSSSSSSSSSK",
       "KSSSSSSSSSSSK.","KSSSSSSSSSSSK.",".K.KK..KK.K...",".K.KK..KK.K..."]
};

/* attach each sprite key to its game */
window.GAMES.forEach((g,i)=>{ g.spr = window.SPR[i]; });

/* the THEORY GAMES bundle pseudo-cartridge (opens the sub-screen of concept visualizations) */
window.EXTRA = {name:"THEORY GAMES", isBundle:true, acc:"#ffd23f", spr:"qblock",
  blurb:"hands-on visualizations that build intuition for the core ideas. Press START to open."};

/* which cartridges are front-screen headliners vs in the THEORY GAMES bundle */
window.VIEWS = {
  main:[GAMES[0],GAMES[1],GAMES[2],GAMES[3],GAMES[4],GAMES[5],GAMES[6],EXTRA],
  extra:[GAMES[7],GAMES[8],GAMES[9],GAMES[10]]
};

/* counts auto-derive from the registry above */
window.EXTRA.tag = '+' + window.VIEWS.extra.length;
window.EXTRA.blurb = window.VIEWS.extra.length + ' theory games: ' + window.EXTRA.blurb;

/* Japanese strings (jp = name, jb = blurb), merged in by href. The start-screen
   日本語 toggle swaps the DOM names to jp and the info blurb to jb; the canvas
   draws them with the OS kana font (no kana webfont bundled). */
const JP = {
  'anymal-mdp/':         {jp:'アニマル MDP',       jb:'ロボット犬がごほうびを求めて格子を歩く。状態・行動・遷移・報酬という、あらゆる意思決定問題の四つの部品を体感しよう。'},
  'repair-or-replace/':  {jp:'修理か交換か',        jb:'一台のバン、四段階の摩耗。走らせる・整備する・買い替える。まだ動くうちに手放す見極めを、割引率ガンマが決める。'},
  'last-minute-pricing/':{jp:'直前の値付け',        jb:'売れ残る在庫と深夜の締め切り。毎日値段を決め、収益管理の地形を動的計画法とSARSAで学ぶ。'},
  'recycling-robot/':    {jp:'リサイクルロボット',  jb:'電池で動く回収ロボット。探す・待つ・充電する。電池が減ったら、立ち往生する前に充電へ。'},
  'pokemon-battle/':     {jp:'ポケモンバトル',      jb:'野生のヒトカゲがあらわれた！初代の対戦画面で学ぶ、同じ強化学習のレッスン。'},
  'stale-by-sundown/':   {jp:'日没までに',          jb:'生鮮品は日が暮れると傷む。保つ・値引き・処分する。正しい判断は鮮度の段階を下りていく。'},
  'critical-spare/':     {jp:'予備部品',            jb:'一台の機械、一つの予備在庫。走らせる・予備を注文・交換する。故障で止まる前に予備を備えよ。'},
  'casino/':             {jp:'カジノ',              jb:'五台のスロット、隠れた確率。手で回して当たりを学び、イプシロン貪欲法で探索と稼ぎを両立させる。'},
  'spooky-house/':       {jp:'お化け屋敷',          jb:'幽霊だらけの格子。右か下へ進んで怖さを最大にする。たった一つの再帰が総当たりに勝つ。'},
  'darts/':              {jp:'暗闇のダーツ',        jb:'見えない的にダーツを投げる。大きく外せば大きく直し、歩幅を縮めて狙いを落ち着かせる。'},
  'minigolf/':           {jp:'ミニゴルフ',          jb:'隠れたホールへパット。でも風が毎回ずらす。一打は嘘をつくから、ぶれる試行を重ねて力加減を見極めよう。'},
};
window.GAMES.forEach(g => { const j = JP[g.href]; if(j){ g.jp = j.jp; g.jb = j.jb; } });
window.EXTRA.jp = '理論ゲーム';
window.EXTRA.jb = '核心の考え方を体で掴むための実習ビジュアル。スタートを押して開く。';
