package com.tyraen.voicekeyboard.feature.transcription

import org.junit.Assert.assertEquals
import org.junit.Test

class TranscriptionResponseParserTest {

    @Test fun `plain text body is returned unchanged`() {
        assertEquals("Привет, как дела?", TranscriptionResponseParser.extractText("Привет, как дела?"))
    }

    @Test fun `plain text body is trimmed`() {
        assertEquals("Hello world", TranscriptionResponseParser.extractText("  Hello world\n"))
    }

    @Test fun `mistral json object exposes the text field`() {
        val body = """
            {"model":"voxtral-mini-2507","text":"Съешь ещё этих булок","language":"ru","segments":[],"usage":{"prompt_tokens":4}}
        """.trimIndent()
        assertEquals("Съешь ещё этих булок", TranscriptionResponseParser.extractText(body))
    }

    @Test fun `openai json object exposes the text field`() {
        assertEquals("Hello there", TranscriptionResponseParser.extractText("""{"text":"Hello there"}"""))
    }

    @Test fun `json text field is trimmed`() {
        assertEquals("padded", TranscriptionResponseParser.extractText("""{"text":"  padded  "}"""))
    }

    @Test fun `empty text field yields empty string`() {
        assertEquals("", TranscriptionResponseParser.extractText("""{"text":""}"""))
    }

    @Test fun `json null text field falls back to the raw body`() {
        val body = """{"text":null}"""
        assertEquals(body, TranscriptionResponseParser.extractText(body))
    }

    @Test fun `non-string text field falls back to the raw body`() {
        val body = """{"text":42}"""
        assertEquals(body, TranscriptionResponseParser.extractText(body))
    }

    @Test fun `json object without a text field falls back to the raw body`() {
        val body = """{"error":{"message":"bad request"}}"""
        assertEquals(body, TranscriptionResponseParser.extractText(body))
    }

    @Test fun `malformed json starting with brace falls back to the raw body`() {
        val body = "{not really json"
        assertEquals(body, TranscriptionResponseParser.extractText(body))
    }

    @Test fun `transcript that merely contains a brace stays plain text`() {
        val body = "the config uses {curly} braces"
        assertEquals(body, TranscriptionResponseParser.extractText(body))
    }
}
