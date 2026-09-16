import unittest
from register_post import validate_body_style

BODY='<blockquote class="lead-quote-card">quote</blockquote><nav class="toc-box"><strong>목차</strong><ul><li>section</li></ul></nav>'+''.join('<h2>section</h2><figure class="post-img-wrap"><img src="photo.jpg"><figcaption>Photo description</figcaption></figure>' for _ in range(5))
class BodyStyle(unittest.TestCase):
    def test_existing_structure(self):validate_body_style(BODY)
    def test_summary_without_attribution(self):
        validate_body_style(BODY.replace('<blockquote', '<div').replace('</blockquote>', '</div>'))
    def test_plain_quote(self):
        with self.assertRaises(ValueError):validate_body_style(BODY.replace('lead-quote-card',''))
    def test_missing_toc_label(self):
        with self.assertRaises(ValueError):validate_body_style(BODY.replace('<strong>목차</strong>',''))
    def test_missing_caption(self):
        with self.assertRaises(ValueError):validate_body_style(BODY.replace('<figcaption>Photo description</figcaption>',''))
    def test_photo_after_paragraph(self):
        with self.assertRaises(ValueError):validate_body_style(BODY.replace('</h2>','</h2><p>paragraph</p>'))
if __name__=='__main__':unittest.main()
