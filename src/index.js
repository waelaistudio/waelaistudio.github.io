const TIKTOK_CLIENT_KEY = "sbawrto8glrbd2mt2h";
const TIKTOK_REDIRECT_URI =
  "https://waelaistudio-github-io.mohamedenwael3.workers.dev/auth/tiktok/callback";

function html(title, message) {
  return new Response(
    `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title}</title>
<style>
body{font-family:Arial,sans-serif;max-width:720px;margin:60px auto;padding:20px;line-height:1.6}
</style>
</head>
<body>
<h1>${title}</h1>
<p>${message}</p>
</body>
</html>`,
    {
      headers: { "content-type": "text/html; charset=UTF-8" }
    }
  );
}

function randomState() {
  return crypto.randomUUID();
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/health") {
      return Response.json({
        ok: true,
        service: "WaelAiStudio Worker",
        tiktok: "oauth-ready"
      });
    }

    if (url.pathname === "/auth/tiktok") {
      const state = randomState();

      const authUrl = new URL(
        "https://www.tiktok.com/v2/auth/authorize/"
      );

      authUrl.searchParams.set("client_key", TIKTOK_CLIENT_KEY);
      authUrl.searchParams.set("response_type", "code");
      authUrl.searchParams.set("scope", "user.info.basic,video.publish");
      authUrl.searchParams.set("redirect_uri", TIKTOK_REDIRECT_URI);
      authUrl.searchParams.set("state", state);

      return new Response(null, {
        status: 302,
        headers: {
          Location: authUrl.toString(),
          "Set-Cookie": `tiktok_oauth_state=${state}; Max-Age=600; Path=/; Secure; HttpOnly; SameSite=Lax`
        }
      });
    }

    if (url.pathname === "/auth/tiktok/callback") {
      const error = url.searchParams.get("error");
      const errorDescription = url.searchParams.get("error_description");

      if (error) {
        return html(
          "TikTok Authorization Failed",
          `${error}: ${errorDescription || "Authorization was not completed."}`
        );
      }

      const code = url.searchParams.get("code");
      const returnedState = url.searchParams.get("state");

      if (!code || !returnedState) {
        return html(
          "TikTok OAuth Error",
          "Missing authorization code or state."
        );
      }

      const cookies = request.headers.get("Cookie") || "";
      const match = cookies.match(
        /(?:^|;\s*)tiktok_oauth_state=([^;]+)/
      );

      const savedState = match ? decodeURIComponent(match[1]) : null;

      if (!savedState || savedState !== returnedState) {
        return html(
          "TikTok OAuth Error",
          "Invalid OAuth state. The authorization request could not be verified."
        );
      }

      if (!env.TIKTOK_CLIENT_SECRET) {
        return html(
          "TikTok OAuth Configuration Error",
          "TIKTOK_CLIENT_SECRET is not configured in Cloudflare."
        );
      }

      const tokenResponse = await fetch(
        "https://open.tiktokapis.com/v2/oauth/token/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded"
          },
          body: new URLSearchParams({
            client_key: TIKTOK_CLIENT_KEY,
            client_secret: env.TIKTOK_CLIENT_SECRET,
            code,
            grant_type: "authorization_code",
            redirect_uri: TIKTOK_REDIRECT_URI
          })
        }
      );

      const tokenData = await tokenResponse.json();

      if (!tokenResponse.ok || tokenData.error) {
        return Response.json(
          {
            ok: false,
            service: "WaelAiStudio Worker",
            step: "tiktok_token_exchange",
            error: tokenData
          },
          { status: 502 }
        );
      }

      return html(
        "TikTok Connected",
        `Authorization succeeded.<br><br>
         Granted scopes: ${tokenData.scope || "not returned"}<br><br>
         The access token was received server-side and was not displayed.`
      );
    }

    return env.ASSETS.fetch(request);
  }
};
