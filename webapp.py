import os
from flask import render_template, request, jsonify, abort
from telegram import Bot

def register_routes(app, sessions):

    @app.get("/capture/<sid>")
    def capture(sid):
        if sid not in sessions:
            abort(404)
        return render_template("index.html", sid=sid)

    @app.post("/upload/<sid>")
    def upload(sid):
        if sid not in sessions:
            abort(404)

        media = request.files.get("media")
        kind = request.form.get("kind")

        if not media or kind != "photo":
            return jsonify(ok=False, error="ملف غير صالح"), 400

        token = os.environ["BOT_TOKEN"]
        chat_id = sessions[sid]

        bot = Bot(token=token)
        awaitable = bot.send_photo(
            chat_id=chat_id,
            photo=media.stream,
            caption="صورة أرسلها الزائر بموافقته"
        )

        import asyncio
        asyncio.run(awaitable)

        return jsonify(ok=True)
