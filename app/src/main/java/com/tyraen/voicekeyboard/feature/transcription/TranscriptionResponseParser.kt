package com.tyraen.voicekeyboard.feature.transcription

import org.json.JSONException
import org.json.JSONObject

/**
 * Normalises a transcription endpoint's response body into plain transcript text.
 *
 * Groq and OpenAI's `whisper-1` honour `response_format=text` and return the transcript as a
 * bare text body. Other OpenAI-compatible providers ignore that field and always answer with a
 * JSON object — Mistral (Voxtral) returns `{"text": "...", "language": ..., "segments": [...]}`,
 * and OpenAI's own `gpt-4o-transcribe` only supports JSON. Without this step those JSON bodies
 * were pasted verbatim into the text field.
 *
 * Strategy: if the body is a JSON object carrying a `text` field, use that field; otherwise treat
 * the whole body as plain text. A real transcript almost never looks like a `{"text": ...}` object,
 * and if parsing fails we fall back to the raw body, so nothing is lost for the text-mode providers.
 */
object TranscriptionResponseParser {

    fun extractText(rawBody: String): String {
        val trimmed = rawBody.trim()
        if (trimmed.startsWith("{")) {
            try {
                // Read the root "text" only, and only when it is an actual string. `opt` (not
                // `optString`) matters: on the device `optString` turns a JSON null into the
                // literal "null", and a missing/non-string field should fall back to the raw body.
                val text = JSONObject(trimmed).opt("text")
                if (text is String) {
                    return text.trim()
                }
            } catch (_: JSONException) {
                // Not JSON after all — fall through and use the body as plain text.
            }
        }
        return trimmed
    }
}
