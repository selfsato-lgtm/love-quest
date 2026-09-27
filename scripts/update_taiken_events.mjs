// 体験型デート向けイベントを、Claude(Web検索ツール)でキュレーションして data/taiken_events.json を更新する。
// GitHub Actionsの定期実行から呼ばれる。ANTHROPIC_API_KEY が必要。
import { readFile, writeFile } from 'node:fs/promises';

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) { console.error('ANTHROPIC_API_KEY が未設定です'); process.exit(1); }

const OUT = 'data/taiken_events.json';
const now = new Date();
const jst = new Date(now.getTime() + 9 * 3600 * 1000);
const todayStr = jst.toISOString().slice(0, 10);
const months = Array.from({ length: 4 }, (_, i) => {
  const d = new Date(Date.UTC(jst.getUTCFullYear(), jst.getUTCMonth() + i, 1));
  return `${d.getUTCFullYear()}年${d.getUTCMonth() + 1}月`;
}).join('、');

const prompt = `今日は${todayStr}です。東京・首都圏で、今日から先の約4か月(${months})に開催される
「デートに使える体験型イベント」を、次の情報源を検索して最大30件キュレーションしてください。
情報源: ウォーカープラス(walkerplus.com)、東京ウォーカー、るるぶ&more.(rurubu.jp)、プラスウォーカー等の公的・大手メディア。

選定基準: 謎解き/脱出ゲーム、プラネタリウム、没入型アート・展示、ワークショップ(陶芸・料理等)、
イルミネーション・季節イベント、街歩き型企画など、二人で一緒に「やる/体験する」ものを優先。
すでに終了したもの、大人数向けのもの、日付や場所が確認できないものは除外。

出力は次のJSON配列のみ(前後に説明文や\`\`\`を付けない)。各要素:
{"id":"英数字の一意ID","title":"イベント名","area":"エリア(駅名や区)","start":"YYYY-MM-DD","end":"YYYY-MM-DD または null",
 "summary":"60字程度の要約","tags":["謎解き"等を1〜3個","プラネタリウム","展示","体験型","室内","昼","夜","無料","写真映え"などから選ぶ],
 "dateTip":"デートで誘う時の一言アドバイス(40字程度)","url":"検索で実際に確認できたイベント詳細ページのURL(https)","source":"情報源名"}
URLは必ず検索結果で実在を確認したものだけを使い、推測で作らないこと。`;

const res = await fetch('https://api.anthropic.com/v1/messages', {
  method: 'POST',
  headers: { 'x-api-key': apiKey, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
  body: JSON.stringify({
    model: 'claude-sonnet-4-5',
    max_tokens: 16000,
    messages: [{ role: 'user', content: prompt }],
    tools: [{ type: 'web_search_20250305', name: 'web_search', max_uses: 12, user_location: { type: 'approximate', country: 'JP' } }],
  }),
});
if (!res.ok) { console.error('API error', res.status, await res.text()); process.exit(1); }
const data = await res.json();
const text = (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('\n');

const m = text.match(/\[[\s\S]*\]/);
if (!m) { console.error('JSON配列が見つかりません:', text.slice(0, 500)); process.exit(1); }
let items;
try { items = JSON.parse(m[0]); } catch (e) { console.error('JSONパース失敗:', e.message); process.exit(1); }

const dateOk = s => s === null || (typeof s === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(s) && !isNaN(new Date(s)));
const seen = new Set();
const events = items.filter(e =>
  e && e.title && e.area && e.summary && typeof e.url === 'string' && e.url.startsWith('https://') &&
  dateOk(e.start ?? null) && dateOk(e.end ?? null) && !(e.end && e.end < todayStr) &&
  !seen.has(e.url) && seen.add(e.url)
).map((e, i) => ({
  id: String(e.id || `ev-${i}`), title: e.title, area: e.area, start: e.start ?? null, end: e.end ?? null,
  summary: e.summary, tags: Array.isArray(e.tags) ? e.tags.slice(0, 3) : [], dateTip: e.dateTip || '',
  url: e.url, source: e.source || '',
}));

// 取得結果が極端に少ない場合は、既存データを壊さないよう更新しない
if (events.length < 8) { console.error(`有効なイベントが${events.length}件のみのため更新をスキップ`); process.exit(1); }

let prevNote = '';
try { prevNote = JSON.parse(await readFile(OUT, 'utf8')).note || ''; } catch {}
await writeFile(OUT, JSON.stringify({ updatedAt: todayStr, note: prevNote, events }, null, 2) + '\n');
console.log(`更新完了: ${events.length}件 (${todayStr})`);
