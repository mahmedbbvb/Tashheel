// Vercel Serverless Function: Get/Delete Dental Anatomy Exam Results
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(204).end();

  const kvUrl = process.env.STORAGE_REST_API_URL || process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL || process.env.STORAGE_URL;
  const kvToken = process.env.STORAGE_REST_API_TOKEN || process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN || process.env.STORAGE_TOKEN;

  if (req.method === 'DELETE') {
    if (kvUrl && kvToken) {
      try {
        await fetch(kvUrl, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${kvToken}`, 'Content-Type': 'application/json' },
          body: JSON.stringify(["DEL", "tashheel_dental_exam_results"])
        });
      } catch (e) {}
    }
    return res.status(200).json({ success: true, message: 'تم مسح النتائج' });
  }

  if (req.method !== 'GET') return res.status(405).json({ error: 'Method Not Allowed' });

  try {
    if (kvUrl && kvToken) {
      const kvRes = await fetch(kvUrl, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${kvToken}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(["LRANGE", "tashheel_dental_exam_results", 0, -1])
      });
      if (kvRes.ok) {
        const json = await kvRes.json();
        const rawList = json.result || [];
        const results = rawList.map(item => {
          try { return typeof item === 'string' ? JSON.parse(item) : item; } catch (e) { return null; }
        }).filter(Boolean);
        return res.status(200).json(results);
      }
    }
    return res.status(200).json([]);
  } catch (error) {
    console.error('Error:', error);
    return res.status(500).json({ error: 'Failed: ' + error.message });
  }
}
