import re

def process_input(user_id: str, input_text: str, is_query: bool = False):
    """
    Process input text for database storage/query.
    For now, using simple text cleaning instead of LLM to avoid timeouts.
    """
    # Simple text cleaning and normalization
    cleaned = input_text.strip()

    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)

    # Basic keyword extraction for queries (keep important terms)
    if is_query:
        # Remove common stop words and keep meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'}
        words = cleaned.lower().split()
        cleaned = ' '.join(word for word in words if word not in stop_words and len(word) > 2)

    return cleaned