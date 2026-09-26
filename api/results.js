// Vercel Serverless Function: Fetch Exam Results
export default async function handler(req, res) {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  // 1. If Vercel KV / Upstash Redis is connected
  const kvUrl = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
  const kvToken = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;

  if (req.method === 'DELETE') {
    if (kvUrl && kvToken) {
      try {
        await fetch(`${kvUrl}/del/tashheel_exam_results`, {
          headers: { Authorization: `Bearer ${kvToken}` }
        });
      } catch (e) {}
    }
    return res.status(200).json({ success: true, message: 'تم مسح النتائج' });
  }

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    if (kvUrl && kvToken) {
      const kvRes = await fetch(kvUrl, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${kvToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(["LRANGE", "tashheel_exam_results", 0, -1])
      });
      if (kvRes.ok) {
        const json = await kvRes.json();
        const rawList = json.result || [];
        const results = rawList.map(item => {
          try {
            return typeof item === 'string' ? JSON.parse(item) : item;
          } catch (e) {
            return null;
          }
        }).filter(Boolean);

        return res.status(200).json(results);
      }
    }

    // Default fallback if KV is not yet attached
    return res.status(200).json([]);
  } catch (error) {
    console.error('Error fetching results:', error);
    return res.status(500).json({ error: 'Failed to retrieve results: ' + error.message });
  }
}
