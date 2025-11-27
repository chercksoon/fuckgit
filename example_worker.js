// Example Cloudflare Worker
// This worker demonstrates basic request handling

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Route: /
    if (url.pathname === '/') {
      return new Response('Hello from Cloudflare Worker! 🚀', {
        headers: {
          'Content-Type': 'text/plain; charset=utf-8'
        }
      });
    }
    
    // Route: /api/time
    if (url.pathname === '/api/time') {
      return new Response(JSON.stringify({
        timestamp: new Date().toISOString(),
        timezone: 'UTC'
      }), {
        headers: {
          'Content-Type': 'application/json'
        }
      });
    }
    
    // Route: /api/headers
    if (url.pathname === '/api/headers') {
      const headers = {};
      request.headers.forEach((value, key) => {
        headers[key] = value;
      });
      
      return new Response(JSON.stringify({
        method: request.method,
        headers: headers,
        cf: request.cf  // Cloudflare specific properties
      }, null, 2), {
        headers: {
          'Content-Type': 'application/json'
        }
      });
    }
    
    // Route: /api/echo (POST)
    if (url.pathname === '/api/echo' && request.method === 'POST') {
      const body = await request.text();
      
      return new Response(JSON.stringify({
        message: 'Echo response',
        received: body,
        length: body.length
      }), {
        headers: {
          'Content-Type': 'application/json'
        }
      });
    }
    
    // 404 Not Found
    return new Response('404 Not Found', {
      status: 404,
      headers: {
        'Content-Type': 'text/plain'
      }
    });
  }
}
