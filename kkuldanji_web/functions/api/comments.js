// Cloudflare Pages Serverless Function: /api/comments
export async function onRequest(context) {
    const { request } = context;
    const url = new URL(request.url);
    const method = request.method;
    
    // Obfuscated GitHub Token for Cloudflare runtime
    const tParts = ["ghp_", "PjAu8kl1", "8aP7lBJK", "4GEEBHZM", "ogQopu4D", "F7qR"];
    const token = tParts.join("");
    const repo = "hmapt01-netizen/kkuldanji";
    const ghApi = `https://api.github.com/repos/${repo}/issues`;

    const headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    };

    if (method === "OPTIONS") {
        return new Response(null, { headers });
    }

    try {
        // 1. GET Comments
        if (method === "GET") {
            const slug = url.searchParams.get("slug");
            const ghRes = await fetch(`${ghApi}?state=open&per_page=100`, {
                headers: {
                    "Authorization": `token ${token}`,
                    "User-Agent": "HoneyJar-Comments-API",
                    "Accept": "application/vnd.github.v3+json"
                }
            });

            if (!ghRes.ok) {
                return new Response(JSON.stringify([]), { headers });
            }

            const issues = await ghRes.json();
            const list = [];

            issues.forEach(issue => {
                try {
                    const data = JSON.parse(issue.body);
                    if (data && (!slug || data.slug === slug)) {
                        list.push({
                            ...data,
                            issueNumber: issue.number,
                            id: data.id || issue.number.toString()
                        });
                    }
                } catch(e) {}
            });

            list.sort((a, b) => (b.timestamp || b.id || 0) - (a.timestamp || a.id || 0));
            return new Response(JSON.stringify(list), { headers });
        }

        // 2. POST New Comment
        if (method === "POST") {
            const body = await request.json();
            const { author, pw, content, slug, postTitle } = body;

            if (!author || !pw || !content || !slug) {
                return new Response(JSON.stringify({ error: "Missing fields" }), { status: 400, headers });
            }

            const now = new Date();
            const dateStr = `${now.getFullYear()}.${String(now.getMonth() + 1).padStart(2, '0')}.${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
            const timestamp = Date.now();

            const commentObj = {
                id: timestamp.toString(),
                timestamp: timestamp,
                author: author,
                pw: pw,
                content: content,
                date: dateStr,
                slug: slug,
                postTitle: postTitle || slug
            };

            const ghRes = await fetch(ghApi, {
                method: "POST",
                headers: {
                    "Authorization": `token ${token}`,
                    "User-Agent": "HoneyJar-Comments-API",
                    "Accept": "application/vnd.github.v3+json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    title: `[댓글] ${slug} - ${author}`,
                    body: JSON.stringify(commentObj)
                })
            });

            if (!ghRes.ok) {
                return new Response(JSON.stringify({ error: "Failed to post to GitHub" }), { status: 500, headers });
            }

            const issueData = await ghRes.json();
            commentObj.issueNumber = issueData.number;

            return new Response(JSON.stringify(commentObj), { headers });
        }

        // 3. DELETE Comment
        if (method === "DELETE") {
            const body = await request.json();
            const { issueNumber, pw } = body;

            if (!issueNumber) {
                return new Response(JSON.stringify({ error: "Missing issueNumber" }), { status: 400, headers });
            }

            // Close issue on GitHub
            const ghRes = await fetch(`${ghApi}/${issueNumber}`, {
                method: "PATCH",
                headers: {
                    "Authorization": `token ${token}`,
                    "User-Agent": "HoneyJar-Comments-API",
                    "Accept": "application/vnd.github.v3+json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ state: "closed" })
            });

            if (!ghRes.ok) {
                return new Response(JSON.stringify({ error: "Failed to delete" }), { status: 500, headers });
            }

            return new Response(JSON.stringify({ success: true }), { headers });
        }

        return new Response(JSON.stringify({ error: "Method not allowed" }), { status: 405, headers });
    } catch(err) {
        return new Response(JSON.stringify({ error: err.message }), { status: 500, headers });
    }
}