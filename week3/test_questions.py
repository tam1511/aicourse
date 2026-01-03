"""
Test questions for Korea Study RAG evaluation.
Each test has: question, expected keywords, reference answer, and category.
Based on actual knowledge base content.
"""

from pydantic import BaseModel, Field
from typing import List
import json


class TestQuestion(BaseModel):
    """A test question for evaluating the RAG system."""
    question: str = Field(description="The question to ask")
    keywords: List[str] = Field(description="Keywords that should appear in retrieved chunks")
    reference_answer: str = Field(description="The correct/ideal answer")
    category: str = Field(description="Question type: company_info, employee_info, school_info, visa_info, complex")


# Create test questions based on your knowledge base
TEST_QUESTIONS = [
    # === COMPANY INFO (8 questions) ===
    TestQuestion(
        question="Korea Study được thành lập năm nào?",
        keywords=["2018", "thành lập", "năm"],
        reference_answer="Korea Study Consultant Center được thành lập vào năm 2018 với sứ mệnh kết nối các bạn trẻ Việt Nam với hệ thống giáo dục chất lượng cao của Hàn Quốc.",
        category="company_info"
    ),
    TestQuestion(
        question="Văn phòng Korea Study ở đâu?",
        keywords=["Lotte Center", "Hà Nội", "Bitexco", "TP.HCM", "Seoul"],
        reference_answer="Korea Study có trụ sở chính tại tầng 12, Tòa nhà Lotte Center, 54 Liễu Giai, Ba Đình, Hà Nội. Chi nhánh TP.HCM ở tầng 8, Tòa nhà Bitexco, 2 Hải Triều, Quận 1. Văn phòng đại diện Seoul ở Gangnam-gu.",
        category="company_info"
    ),
    TestQuestion(
        question="Tỷ lệ đậu visa của Korea Study là bao nhiêu?",
        keywords=["98.5%", "tỷ lệ", "visa", "thành công"],
        reference_answer="Tỷ lệ đậu visa của Korea Study là 98.5% trong 5 năm qua, đây là một trong những tỷ lệ cao nhất trong ngành tư vấn du học Hàn Quốc.",
        category="company_info"
    ),
    TestQuestion(
        question="Korea Study có bao nhiêu trường đối tác?",
        keywords=["50", "68", "trường đối tác", "đại học"],
        reference_answer="Korea Study là đối tác chính thức với hơn 50 trường đại học Hàn Quốc (theo trang about) và 68 trường theo thống kê tích lũy (theo trang overview).",
        category="company_info"
    ),
    TestQuestion(
        question="Hotline của Korea Study là gì?",
        keywords=["1900-6789", "hotline", "liên hệ"],
        reference_answer="Hotline của Korea Study là 1900-6789, hoạt động 24/7 để hỗ trợ khách hàng.",
        category="company_info"
    ),
    TestQuestion(
        question="Korea Study có những dịch vụ gì?",
        keywords=["tư vấn", "chọn trường", "visa", "học bổng", "hỗ trợ"],
        reference_answer="Korea Study cung cấp các dịch vụ: tư vấn chọn trường và ngành học, hỗ trợ chuẩn bị hồ sơ, xin visa du học, dạy tiếng Hàn, hỗ trợ học bổng, và dịch vụ hỗ trợ sau khi đến Hàn Quốc.",
        category="company_info"
    ),
    TestQuestion(
        question="Giờ làm việc của Korea Study?",
        keywords=["8:00", "18:00", "Thứ 2", "Chủ nhật"],
        reference_answer="Korea Study làm việc từ 8:00-18:00 thứ 2 đến thứ 6, thứ 7 từ 8:00-17:00, và chủ nhật từ 9:00-16:00.",
        category="company_info"
    ),
    TestQuestion(
        question="Korea Study đã hỗ trợ bao nhiêu học sinh?",
        keywords=["2000", "2156", "học sinh", "hỗ trợ"],
        reference_answer="Korea Study đã hỗ trợ hơn 2,000 học sinh (theo trang about) hoặc 2,156 học sinh theo thống kê tích lũy từ 2018-2023 (theo trang overview).",
        category="company_info"
    ),
    
    # === EMPLOYEE INFO (7 questions) ===
    TestQuestion(
        question="Bà Lan là ai?",
        keywords=["Nguyễn Thị Lan", "CEO", "Giám đốc", "Yonsei"],
        reference_answer="Bà Nguyễn Thị Lan là Giám Đốc Điều Hành (CEO) của Korea Study Consultant Center. Bà tốt nghiệp Thạc sĩ Quản trị Kinh doanh từ Đại học Yonsei và có hơn 15 năm kinh nghiệm trong lĩnh vực tư vấn du học.",
        category="employee_info"
    ),
    TestQuestion(
        question="Bà Lan có trình độ tiếng Hàn như thế nào?",
        keywords=["TOPIK 6", "thành thạo", "tiếng Hàn"],
        reference_answer="Bà Nguyễn Thị Lan có trình độ tiếng Hàn thành thạo với chứng chỉ TOPIK Level 6, ngoài ra bà còn thông thạo tiếng Anh với IELTS 8.0.",
        category="employee_info"
    ),
    TestQuestion(
        question="Alex Kim làm việc ở phòng ban nào?",
        keywords=["Alex Kim", "Phòng Tư vấn Đại học", "tư vấn viên"],
        reference_answer="Alex Kim làm việc tại Phòng Tư vấn Đại học với chức danh Tư Vấn Viên Giáo Dục Hàn Quốc Cấp Cao. Anh có 7 năm kinh nghiệm và chuyên về các trường top như SKY.",
        category="employee_info"
    ),
    TestQuestion(
        question="Alex Kim tốt nghiệp trường nào?",
        keywords=["Seoul National", "Thạc sĩ", "Hankuk University"],
        reference_answer="Alex Kim có Thạc sĩ Giáo dục Quốc tế từ Seoul National University (2015) và Cử nhân Ngôn ngữ Việt Nam từ Hankuk University of Foreign Studies (2013).",
        category="employee_info"
    ),
    TestQuestion(
        question="Michael Lee chuyên về lĩnh vực gì?",
        keywords=["Michael Lee", "visa", "xuất nhập cảnh", "D-2", "D-4"],
        reference_answer="Michael Lee là Điều Phối Viên Xử Lý Visa với 8 năm kinh nghiệm. Anh chuyên xử lý các loại visa D-2, D-4, D-4-1 và các trường hợp visa phức tạp hoặc bị từ chối.",
        category="employee_info"
    ),
    TestQuestion(
        question="Tỷ lệ đậu visa của Michael Lee là bao nhiêu?",
        keywords=["99.1%", "Michael Lee", "visa", "cao nhất"],
        reference_answer="Tỷ lệ đậu visa của Michael Lee là 99.1%, cao nhất trong công ty. Anh đã xử lý thành công 1,200+ hồ sơ visa và giải quyết 50+ trường hợp visa bị từ chối.",
        category="employee_info"
    ),
    TestQuestion(
        question="Liên hệ Alex Kim như thế nào?",
        keywords=["alex.kim@koreastudyvn.com", "024", "3935-2468"],
        reference_answer="Có thể liên hệ Alex Kim qua email alex.kim@koreastudyvn.com, điện thoại (024) 3935-2468 ext 101, hoặc Zalo 0901-234-568. Giờ tư vấn từ thứ 2-7 (8:00-18:00).",
        category="employee_info"
    ),
    
    # === SCHOOL INFO (10 questions) ===
    TestQuestion(
        question="Seoul National University ở đâu?",
        keywords=["Seoul National", "SNU", "Gwanak-gu", "Seoul"],
        reference_answer="Seoul National University (SNU) nằm tại 1 Gwanak-ro, Gwanak-gu, Seoul 08826. Đây là trường đại học hàng đầu Hàn Quốc, được thành lập năm 1946.",
        category="school_info"
    ),
    TestQuestion(
        question="SNU ranking bao nhiêu?",
        keywords=["Seoul National", "Top 1", "Top 30", "ranking"],
        reference_answer="Seoul National University xếp hạng Top 1 tại Hàn Quốc và Top 30-40 trên thế giới. Đây là trường đại học uy tín nhất Hàn Quốc.",
        category="school_info"
    ),
    TestQuestion(
        question="Học phí tại SNU là bao nhiêu?",
        keywords=["4,188,000", "4,776,000", "KRW", "học phí", "SNU"],
        reference_answer="Học phí tại SNU cho sinh viên quốc tế: Khoa Nhân văn/Xã hội là 4,188,000 KRW/học kỳ (~$3,200), Khoa Tự nhiên/Kỹ thuật là 4,776,000 KRW/học kỳ (~$3,650), và Khoa Y là 5,652,000 KRW/học kỳ (~$4,300).",
        category="school_info"
    ),
    TestQuestion(
        question="Yonsei University thuộc liên minh nào?",
        keywords=["SKY", "Seoul National", "Korea", "Yonsei"],
        reference_answer="Yonsei University thuộc liên minh 'SKY' (Seoul National, Korea, Yonsei) - 3 trường đại học hàng đầu Hàn Quốc. Yonsei được thành lập năm 1885.",
        category="school_info"
    ),
    TestQuestion(
        question="Yonsei có mấy campus?",
        keywords=["Sinchon", "Songdo", "Wonju", "Seoul", "Incheon"],
        reference_answer="Yonsei University có 3 campus: Sinchon (Seoul), Songdo (Incheon), và Wonju. Campus chính ở Sinchon, Seoul.",
        category="school_info"
    ),
    TestQuestion(
        question="UIC là gì?",
        keywords=["Underwood International College", "UIC", "tiếng Anh", "Yonsei"],
        reference_answer="UIC (Underwood International College) là chương trình đặc biệt tại Yonsei giảng dạy 100% bằng tiếng Anh, tập trung vào giáo dục liberal arts với các ngành như Quan hệ quốc tế, Kinh tế học quốc tế.",
        category="school_info"
    ),
    TestQuestion(
        question="Yêu cầu TOPIK cho SNU là gì?",
        keywords=["TOPIK", "Level 4", "Level 5-6", "tiếng Hàn"],
        reference_answer="Yêu cầu tiếng Hàn cho SNU là TOPIK Level 4+ (khuyến khích Level 5-6) cho sinh viên quốc tế. Ngoài ra cần TOEFL iBT 88+ hoặc IELTS 6.5+ cho tiếng Anh.",
        category="school_info"
    ),
    TestQuestion(
        question="Yonsei Business School ranking thế nào?",
        keywords=["Yonsei Business School", "Top 1", "AACSB", "EQUIS"],
        reference_answer="Yonsei Business School xếp hạng Top 1 tại Hàn Quốc và được công nhận bởi AACSB và EQUIS. Đây là khoa kinh doanh uy tín nhất Hàn Quốc.",
        category="school_info"
    ),
    TestQuestion(
        question="Chi phí sinh hoạt tại Seoul là bao nhiêu?",
        keywords=["ký túc xá", "600,000", "300,000", "ăn uống", "KRW"],
        reference_answer="Chi phí sinh hoạt tại Seoul: ký túc xá 600,000-1,200,000 KRW/tháng, ăn uống 300,000-600,000 KRW/tháng, giao thông 100,000-150,000 KRW/tháng.",
        category="school_info"
    ),
    TestQuestion(
        question="Tỷ lệ việc làm sau tốt nghiệp SNU là bao nhiêu?",
        keywords=["95%", "việc làm", "Samsung", "LG", "Hyundai"],
        reference_answer="Tỷ lệ việc làm trong vòng 6 tháng sau tốt nghiệp SNU là 95%+. Mức lương khởi điểm 35-50 triệu KRW/năm. Top employers gồm Samsung, LG, Hyundai, SK Group.",
        category="school_info"
    ),
    
    # === VISA INFO (8 questions) ===
    TestQuestion(
        question="Visa D-2 là gì?",
        keywords=["D-2", "student visa", "cử nhân", "thạc sĩ", "tiến sĩ"],
        reference_answer="Visa D-2 là loại visa du học dành cho sinh viên quốc tế theo học các chương trình cấp bằng chính thức tại Hàn Quốc, bao gồm cử nhân (4 năm), thạc sĩ (2 năm), và tiến sĩ (3-4 năm).",
        category="visa_info"
    ),
    TestQuestion(
        question="Thời hạn visa D-2 là bao lâu?",
        keywords=["2 năm", "gia hạn", "thời hạn"],
        reference_answer="Visa D-2 được cấp tối đa 2 năm cho lần đầu và có thể gia hạn theo thời gian học tập. Thời gian xử lý hồ sơ là 5-10 ngày làm việc.",
        category="visa_info"
    ),
    TestQuestion(
        question="Cần bao nhiêu tiền để xin visa D-2?",
        keywords=["20,000 USD", "tài chính", "chứng minh"],
        reference_answer="Cần chứng minh tài chính tối thiểu 20,000 USD với tài khoản ngân hàng có số dư ổn định trong 6 tháng. Có thể dùng bảo lãnh tài chính từ gia đình nếu cần.",
        category="visa_info"
    ),
    TestQuestion(
        question="Giấy tờ nào cần thiết để xin visa D-2?",
        keywords=["đơn xin visa", "hộ chiếu", "giấy nhập học", "bằng tốt nghiệp", "chứng minh tài chính"],
        reference_answer="Giấy tờ bắt buộc gồm: đơn xin visa (Form 34), hộ chiếu còn hạn 6 tháng, ảnh 3.5x4.5cm, giấy nhập học, bằng tốt nghiệp và bảng điểm có công chứng, chứng minh tài chính, và giấy khám sức khỏe.",
        category="visa_info"
    ),
    TestQuestion(
        question="Có được làm thêm với visa D-2 không?",
        keywords=["làm thêm", "20 giờ", "bán thời gian", "xin phép"],
        reference_answer="Với visa D-2, sinh viên được phép làm việc bán thời gian tối đa 20 giờ/tuần sau khi xin phép. Không được làm việc toàn thời gian.",
        category="visa_info"
    ),
    TestQuestion(
        question="Lệ phí visa D-2 là bao nhiêu?",
        keywords=["60 USD", "lệ phí", "phí visa"],
        reference_answer="Lệ phí visa D-2 là 60 USD. Ngoài ra còn các chi phí khác như phí dịch thuật (50-100 USD), công chứng (30-50 USD), khám sức khỏe (50-100 USD).",
        category="visa_info"
    ),
    TestQuestion(
        question="Yêu cầu TOPIK cho visa D-2?",
        keywords=["TOPIK", "Level 3", "tiếng Hàn"],
        reference_answer="Yêu cầu TOPIK Level 3 trở lên cho visa D-2, một số trường có thể yêu cầu Level 4-6. Chương trình giảng dạy bằng tiếng Anh có thể không yêu cầu TOPIK.",
        category="visa_info"
    ),
    TestQuestion(
        question="Mất bao lâu để xử lý visa D-2?",
        keywords=["5-10 ngày", "xử lý", "thời gian"],
        reference_answer="Thời gian xử lý visa D-2 là 5-10 ngày làm việc sau khi nộp hồ sơ đầy đủ tại Lãnh sự quán/Đại sứ quán Hàn Quốc. Nên nộp hồ sơ sớm 2-3 tháng trước khi nhập học.",
        category="visa_info"
    ),
    
    # === COMPLEX QUESTIONS (7 questions) ===
    TestQuestion(
        question="Tôi muốn học tại Yonsei Business School, cần chuẩn bị gì và ai có thể giúp?",
        keywords=["Yonsei Business School", "GMAT", "TOEFL", "Alex Kim", "tư vấn"],
        reference_answer="Để vào Yonsei Business School cần: bằng cử nhân GPA 3.0+, GMAT/GRE, TOEFL iBT 88+ hoặc IELTS 6.5+. Học phí MBA khoảng 12,000,000 KRW/học kỳ. Alex Kim, tư vấn viên cấp cao tại Phòng Tư vấn Đại học, chuyên về các trường top như Yonsei và có thể hỗ trợ bạn.",
        category="complex"
    ),
    TestQuestion(
        question="Chi phí toàn bộ để học tại SNU và xin visa là bao nhiêu?",
        keywords=["học phí", "4,188,000", "chi phí sinh hoạt", "visa", "60 USD"],
        reference_answer="Chi phí học tại SNU: học phí 4,188,000-5,652,000 KRW/học kỳ tùy ngành, chi phí sinh hoạt khoảng 1,000,000-2,000,000 KRW/tháng. Chi phí visa: lệ phí 60 USD, dịch thuật 50-100 USD, công chứng 30-50 USD, khám sức khỏe 50-100 USD. Tổng cộng cần chuẩn bị khoảng 20,000-25,000 USD/năm.",
        category="complex"
    ),
    TestQuestion(
        question="Tôi muốn xin học bổng và visa D-2, quy trình như thế nào?",
        keywords=["học bổng", "KGSP", "visa D-2", "hồ sơ", "timeline"],
        reference_answer="Quy trình: (1) Xin học bổng trước (KGSP hoặc học bổng trường), (2) Nhận thư nhập học và thư học bổng, (3) Chuẩn bị hồ sơ visa D-2 với chứng minh tài chính 20,000 USD, (4) Nộp hồ sơ visa, (5) Nhận visa sau 5-10 ngày. Korea Study có dịch vụ hỗ trợ học bổng miễn phí và tỷ lệ đậu học bổng 45%.",
        category="complex"
    ),
    TestQuestion(
        question="So sánh SNU và Yonsei về ranking và học phí?",
        keywords=["SNU", "Yonsei", "ranking", "Top 1", "Top 3", "học phí"],
        reference_answer="SNU xếp Top 1 Hàn Quốc và Top 30-40 thế giới, học phí 4,188,000-5,652,000 KRW/học kỳ. Yonsei xếp Top 3 Hàn Quốc và Top 80 thế giới, học phí 4,305,000-6,804,000 KRW/học kỳ. SNU uy tín hơn nhưng cạnh tranh cao hơn. Yonsei có nhiều chương trình tiếng Anh hơn như UIC.",
        category="complex"
    ),
    TestQuestion(
        question="Bà Lan có kinh nghiệm gì và học trường nào?",
        keywords=["Nguyễn Thị Lan", "Yonsei", "MBA", "15 năm", "CEO"],
        reference_answer="Bà Nguyễn Thị Lan là CEO của Korea Study, có 15 năm kinh nghiệm tư vấn du học. Bà tốt nghiệp MBA từ Đại học Yonsei (2010) và Cử nhân Quan hệ Quốc tế từ Đại học Ngoại thương (2005). Bà từng sống và làm việc tại Hàn Quốc 8 năm, thông thạo tiếng Hàn (TOPIK 6) và tiếng Anh (IELTS 8.0).",
        category="complex"
    ),
    TestQuestion(
        question="Tôi bị từ chối visa, ai có thể giúp và làm gì?",
        keywords=["Michael Lee", "visa bị từ chối", "appeal", "50+ trường hợp"],
        reference_answer="Michael Lee, Điều Phối Viên Xử Lý Visa, chuyên giải quyết các trường hợp visa bị từ chối với tỷ lệ thành công cao. Anh đã xử lý thành công 50+ trường hợp appeal. Quy trình: (1) Phân tích lý do từ chối, (2) Bổ sung giấy tờ cần thiết, (3) Viết thư giải trình, (4) Nộp lại hồ sơ appeal. Liên hệ: michael.lee@koreastudyvn.com hoặc 0912-345-678.",
        category="complex"
    ),
    TestQuestion(
        question="Dịch vụ của Korea Study bao gồm những gì và giá bao nhiêu?",
        keywords=["tư vấn", "visa", "học bổng", "5,000,000", "3,000,000", "miễn phí"],
        reference_answer="Korea Study cung cấp: (1) Tư vấn chọn trường - miễn phí cơ bản, 2,000,000 VNĐ chuyên sâu, (2) Hỗ trợ hồ sơ - 5,000,000-8,000,000 VNĐ, (3) Xin visa - 3,000,000 VNĐ, (4) Học tiếng Hàn - 1,500,000 VNĐ/tháng, (5) Hỗ trợ học bổng - miễn phí (chỉ thu phí khi đậu), (6) Hỗ trợ tại Hàn Quốc - 500,000-3,000,000 VNĐ.",
        category="complex"
    ),
]


def save_tests_to_jsonl(filename: str = "tests.jsonl"):
    """Save test questions to JSONL file."""
    with open(filename, 'w', encoding='utf-8') as f:
        for test in TEST_QUESTIONS:
            f.write(test.model_dump_json() + '\n')
    print(f"Saved {len(TEST_QUESTIONS)} test questions to {filename}")


def load_tests_from_jsonl(filename: str = "tests.jsonl") -> List[TestQuestion]:
    """Load test questions from JSONL file."""
    tests = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            tests.append(TestQuestion(**data))
    return tests


def print_test_summary():
    """Print summary of test questions by category."""
    from collections import Counter
    categories = Counter([t.category for t in TEST_QUESTIONS])
    
    print("\n=== Test Question Summary ===")
    print(f"Total: {len(TEST_QUESTIONS)} questions\n")
    for category, count in categories.items():
        print(f"{category}: {count} questions")


if __name__ == "__main__":
    # Save tests to file
    save_tests_to_jsonl()
    
    # Print summary
    print_test_summary()
    
    # Show example
    print("\n=== Example Test Question ===")
    example = TEST_QUESTIONS[0]
    print(f"Question: {example.question}")
    print(f"Category: {example.category}")
    print(f"Keywords: {example.keywords}")
    print(f"Reference: {example.reference_answer}")