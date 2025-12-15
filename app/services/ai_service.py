import os
import openai
from flask import current_app

class AIService:
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def format_post_content(self, raw_content, context=None):
        """
        Gửi nội dung thô lên OpenAI để format lại thành HTML đẹp.
        Nếu không có API Key, trả về nội dung giả lập.
        """
        if not self.client:
            return self._mock_format(raw_content)

        try:
            prompt = f"""
            You are a professional editor for a Christian blog named "Spiritual Feed".
            Your task is to rewrite and format the following raw content into structured, beautiful HTML.
            
            Guidelines:
            1. Use <h2> and <h3> for headings.
            2. Use <p> for paragraphs. Break long text into readable chunks.
            3. Use <blockquote> for any Bible verses, quotes, or key takeaways.
            4. Use <ul> or <ol> for lists.
            5. Highlight important phrases with <strong> or <em>.
            6. Do NOT return <html>, <head>, or <body> tags. Return only the body content.
            7. Suggest places for images by inserting comments like <!-- IMG: [Description] -->.
            
            Raw Content:
            {raw_content}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo", # Hoặc gpt-4o nếu có budget
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            current_app.logger.error(f"OpenAI API Error: {e}")
            return f"<p>Error generating AI content: {str(e)}</p><hr>{raw_content}"

    def _mock_format(self, raw_content):
        """
        Giả lập response nếu chưa có API Key.
        """
        return f"""
        <!-- MOCK AI RESPONSE (No API Key found) -->
        <h2>Giới Thiệu</h2>
        <p>{raw_content[:200]}...</p>
        
        <blockquote>
            "Đây là một câu trích dẫn giả lập từ AI. Hãy cấu hình OPENAI_API_KEY để dùng thật."
        </blockquote>
        
        <h3>Nội Dung Chính</h3>
        <p>Hệ thống AI sẽ tự động phân tích văn bản của bạn và chia nhỏ thành các đoạn văn dễ đọc. Nó cũng sẽ thêm các định dạng như <strong>in đậm</strong> hoặc <em>in nghiêng</em> để làm nổi bật ý chính.</p>
        
        <ul>
            <li>Ý chính 1: Tự động format.</li>
            <li>Ý chính 2: Tiết kiệm thời gian.</li>
            <li>Ý chính 3: Giao diện đẹp mắt.</li>
        </ul>
        
        <p>{raw_content}</p>
        """

# Singleton instance
ai_service = AIService()
