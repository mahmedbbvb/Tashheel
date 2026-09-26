const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 3000;
const ROOT_DIR = __dirname;
const RESULTS_FILE = path.join(ROOT_DIR, 'results.json');

// Ensure results.json exists
if (!fs.existsSync(RESULTS_FILE)) {
  fs.writeFileSync(RESULTS_FILE, JSON.stringify([], null, 2), 'utf8');
}

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.mp3': 'audio/mpeg',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  // API: Get Results
  if (pathname === '/api/results' && req.method === 'GET') {
    fs.readFile(RESULTS_FILE, 'utf8', (err, data) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Failed to read results file' }));
        return;
      }
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(data || '[]');
    });
    return;
  }

  // API: Save Exam Result
  if (pathname === '/api/save-result' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const resultItem = JSON.parse(body);
        if (!resultItem.name || resultItem.score === undefined) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Invalid result format: name and score are required' }));
          return;
        }

        // Add server metadata
        resultItem.id = resultItem.id || 'res_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5);
        resultItem.timestamp = resultItem.timestamp || Date.now();
        resultItem.date = resultItem.date || new Date().toLocaleString('ar-EG', { timeZone: 'Africa/Cairo' });

        let currentResults = [];
        try {
          const raw = fs.readFileSync(RESULTS_FILE, 'utf8');
          currentResults = JSON.parse(raw);
          if (!Array.isArray(currentResults)) currentResults = [];
        } catch (e) {
          currentResults = [];
        }

        currentResults.push(resultItem);

        fs.writeFileSync(RESULTS_FILE, JSON.stringify(currentResults, null, 2), 'utf8');

        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({
          success: true,
          message: 'تم حفظ النتيجة بنجاح في ملف results.json',
          totalRecords: currentResults.length,
          data: resultItem
        }));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Invalid JSON payload: ' + err.message }));
      }
    });
    return;
  }

  // API: Clear Results
  if (pathname === '/api/results' && req.method === 'DELETE') {
    fs.writeFileSync(RESULTS_FILE, '[]', 'utf8');
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ success: true, message: 'تم مسح النتائج' }));
    return;
  }

  // Serve Static Files
  let filePath = path.join(ROOT_DIR, pathname === '/' ? 'index.html' : pathname);

  // Security: prevent directory traversal
  if (!filePath.startsWith(ROOT_DIR)) {
    res.writeHead(403);
    res.end('Forbidden');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      // Check if it's a directory and has index.html
      if (stats && stats.isDirectory()) {
        filePath = path.join(filePath, 'index.html');
      } else {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('404: الملف غير موجود');
        return;
      }
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    fs.readFile(filePath, (readErr, content) => {
      if (readErr) {
        res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('خطأ في قراءة الملف');
        return;
      }
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    });
  });
});

server.listen(PORT, () => {
  console.log(`\n======================================================`);
  console.log(`🚀 خادم منصة تسهيل التعليمية يعمل بنجاح!`);
  console.log(`🌐 رابط المنصة الرئيسي:   http://localhost:${PORT}/`);
  console.log(`📝 رابط امتحان الفسيولوجي: http://localhost:${PORT}/physiology_lecture_1_quiz.html`);
  console.log(`📊 رابط نتائج الامتحانات:  http://localhost:${PORT}/results.html`);
  console.log(`💾 ملف حفظ النتائج:       ${RESULTS_FILE}`);
  console.log(`======================================================\n`);
});
