function html(title, message) {
  return new Response(
    `<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
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
      headers: {
        "content-type": "text/html; charset=UTF-8"
      }
    }
  );
}

function randomState() {
  return crypto.randomUUID();
}

function getCookie(request, name) {
  const cookieHeader = request.headers.get("Cookie") || "";

  for (const part of cookieHeader.split(";")) {
    const [key, ...valueParts] = part.trim().split("=");

    if (key === name) {
      return decodeURIComponent(valueParts.join("="));
    }
  }

  return null;
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
      if (!env.TIKTOK_CLIENT_KEY || !env.TIKTOK_REDIRECT_URI) {
        return html(
          "Configuration Error",
          "TikTok OAuth environment variables are not configured."
        );
      }

      const state = randomState();

      const authUrl = new URL(
        "https://www.tiktok.com/v2/auth/authorize/"
      );

      authUrl.searchParams.set(
        "client_key",
        env.TIKTOK_CLIENT_KEY
      );

      authUrl.searchParams.set(
        "response_type",
        "code"
      );

      authUrl.searchParams.set(
        "scope",
        "user.info.basic,video.publish"
      );

      authUrl.searchParams.set(
        "redirect_uri",
        env.TIKTOK_REDIRECT_URI
      );

      authUrl.searchParams.set(
        "state",
        state
      );

      return new Response(null, {
        status: 302,
        headers: {
          "Location": authUrl.toString(),
          "Set-Cookie":
            `tiktok_oauth_state=${encodeURIComponent(state)}; Max-Age=600; Path=/; Secure; HttpOnly; SameSite=Lax`
        }
      });
    }

    if (url.pathname === "/auth/tiktok/callback") {
      const code = url.searchParams.get("code");
      const state = url.searchParams.get("state");
      const error = url.searchParams.get("error");
      const errorDescription =
        url.searchParams.get("error_description");

      if (error) {
        return html(
          "TikTok Authorization Error",
          errorDescription || error
        );
      }

      if (!code) {
        return html(
          "TikTok OAuth Error",
          "Missing authorization code."
        );
      }

      if (!state) {
        return html(
          "TikTok OAuth Error",
          "Missing OAuth state."
        );
      }

      const savedState = getCookie(
        request,
        "tiktok_oauth_state"
      );

      if (!savedState || savedState !== state) {
        return html(
          "TikTok OAuth Security Error",
          "Invalid OAuth state."
        );
      }

      if (
        !env.TIKTOK_CLIENT_KEY ||
        !env.TIKTOK_CLIENT_SECRET ||
        !env.TIKTOK_REDIRECT_URI
      ) {
        return html(
          "Configuration Error",
          "TikTok OAuth secrets are not configured."
        );
      }

      try {
        const tokenResponse = await fetch(
          "https://open.tiktokapis.com/v2/oauth/token/",
          {
            method: "POST",
            headers: {
              "Content-Type":
                "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
              client_key: env.TIKTOK_CLIENT_KEY,
              client_secret: env.TIKTOK_CLIENT_SECRET,
              code,
              grant_type: "authorization_code",
              redirect_uri: env.TIKTOK_REDIRECT_URI
            })
          }
        );

        const data = await tokenResponse.json();

        if (!tokenResponse.ok || data.error) {
          return new Response(
            JSON.stringify({
              ok: false,
              error:
                data.error ||
                "token_exchange_failed",
              error_description:
                data.error_description ||
                "TikTok token exchange failed."
            }),
            {
              status: 400,
              headers: {
                "content-type": "application/json"
              }
            }
          );
        }

        console.log(
          "TikTok OAuth token exchange succeeded.",
          JSON.stringify({
            open_id: data.open_id,
            scope: data.scope,
            expires_in: data.expires_in,
            refresh_expires_in:
              data.refresh_expires_in
          })
        );

        return new Response(
          null,
          {
            status: 302,
            headers: {
              "Location": "/?tiktok=connected",
              "Set-Cookie":
                "tiktok_oauth_state=; Max-Age=0; Path=/; Secure; HttpOnly; SameSite=Lax"
            }
          }
        );
      } catch (err) {
        return new Response(
          JSON.stringify({
            ok: false,
            error: "server_error",
            error_description: err.message
          }),
          {
            status: 500,
            headers: {
              "content-type": "application/json"
            }
          }
        );
      }
    }

    if (
      url.pathname === "/auth/instagram" ||
      url.pathname === "/auth/youtube" ||
      url.pathname === "/auth/facebook"
    ) {
      return html(
        "Coming Soon",
        "This platform adapter is not enabled yet."
      );
    }

    return new Response(
      "WaelAiStudio Cloudflare Worker Engine Gateway is Running...",
      {
        headers: {
          "content-type": "text/plain; charset=UTF-8"
        }
      }
    );
  }
};
