// Vercel Serverless Function: Save Exam Result
export default async function handler(req, res) {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try {
        body = JSON.parse(body);
      } catch (e) {
        return res.status(400).json({ error: 'Invalid JSON body' });
      }
    }

    if (!body || !body.name || body.score === undefined) {
      return res.status(400).json({ error: 'Name and score are required' });
    }

    // Prepare complete record
    const record = {
      id: body.id || 'res_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5),
      name: String(body.name).trim(),
      score: Number(body.score),
      total: Number(body.total) || 20,
      percentage: Number(body.percentage) || Math.round((Number(body.score) / (Number(body.total) || 20)) * 100),
      wrongQuestions: Array.isArray(body.wrongQuestions) ? body.wrongQuestions : [],
      wrongDetails: Array.isArray(body.wrongDetails) ? body.wrongDetails : [],
      date: body.date || new Date().toLocaleString('ar-EG', { timeZone: 'Africa/Cairo' }),
      timestamp: body.timestamp || Date.now()
    };

    // 1. If Vercel KV / Upstash Redis is connected in Vercel project
    const kvUrl = process.env.STORAGE_REST_API_URL || 
                  process.env.KV_REST_API_URL || 
                  process.env.UPSTASH_REDIS_REST_URL ||
                  process.env.STORAGE_URL;

    const kvToken = process.env.STORAGE_REST_API_TOKEN || 
                    process.env.KV_REST_API_TOKEN || 
                    process.env.UPSTASH_REDIS_REST_TOKEN ||
                    process.env.STORAGE_TOKEN;

    if (kvUrl && kvToken) {
      try {
        const pushRes = await fetch(kvUrl, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${kvToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(["LPUSH", "tashheel_exam_results", JSON.stringify(record)])
        });

        if (pushRes.ok) {
          return res.status(200).json({
            success: true,
            storage: 'vercel_kv',
            message: 'تم حفظ النتيجة في Vercel KV السحابي بنجاح',
            data: record
          });
        }
      } catch (kvErr) {
        console.error('KV Save Error:', kvErr);
      }
    }

    // 2. Return record so client can persist in localStorage & downloadable results.json
    return res.status(200).json({
      success: true,
      storage: 'client_sync',
      message: 'تم استلام النتيجة وتسجيلها بنجاح',
      data: record
    });

  } catch (error) {
    console.error('Error in save-result handler:', error);
    return res.status(500).json({ error: 'Server error: ' + error.message });
  }
}
