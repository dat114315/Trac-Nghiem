import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Đề Kiểm Tra Trắc Nghiệm Máy Gấp AOQI",
    page_icon="📋",
    layout="centered"
)

# Initialize Session State
if 'started' not in st.session_state:
    st.session_state.started = False
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'employee_name' not in st.session_state:
    st.session_state.employee_name = ""
if 'employee_id' not in st.session_state:
    st.session_state.employee_id = ""
if 'finished' not in st.session_state:
    st.session_state.finished = False

# 50 Questions bám sát tài liệu gốc
QUESTIONS = [
    # === PHẦN 1: QUY TẮC VÀ TRẬT TỰ TRONG CÔNG TY (5 câu) ===
    {
        "id": 1,
        "category": "Quy tắc & Trật tự Công ty",
        "question": "Theo quy tắc nơi làm việc, độ tuổi tối thiểu đối với nhân viên mới vào Công Ty là bao nhiêu?",
        "options": [
            "A. Từ đủ 15 tuổi trở lên",
            "B. Từ đủ 16 tuổi trở lên",
            "C. Từ đủ 18 tuổi trở lên",
            "D. Không quy định độ tuổi tối thiểu nếu có người bảo lãnh"
        ],
        "answer": "B. Từ đủ 16 tuổi trở lên",
        "explanation": "Theo Điều 12 (khoản 1): 'Nhân viên mới vào Công Ty phải từ đủ 16 tuổi trở lên, sức khỏe tốt và có chứng từ hợp pháp...'"
    },
    {
        "id": 2,
        "category": "Quy tắc & Trật tự Công ty",
        "question": "Hành vi nào sau đây là ĐÚNG khi ra vào công ty qua cổng từ an ninh?",
        "options": [
            "A. Chui hoặc nhảy qua cổng từ nếu quên thẻ để tiết kiệm thời gian",
            "B. Sử dụng thẻ của đồng nghiệp cùng phòng để quẹt giùm",
            "C. Quẹt thẻ của mình tại cổng từ an ninh; trường hợp quên thẻ thì thông báo cho bảo vệ để được hỗ trợ",
            "D. Đi qua lối dành cho phương tiện giao thông để tránh ùn tắc"
        ],
        "answer": "C. Quẹt thẻ của mình tại cổng từ an ninh; trường hợp quên thẻ thì thông báo cho bảo vệ để được hỗ trợ",
        "explanation": "Theo Điều 12 (khoản 2): 'Nhân viên được yêu cầu quẹt thẻ của mình tại cổng từ an ninh. Trường hợp không mang thẻ, thông báo cho bảo vệ trực tại cổng từ để được hỗ trợ. Nghiêm cấm sử dụng thẻ người khác, nhảy/chui qua cổng...'"
    },
    {
        "id": 3,
        "category": "Quy tắc & Trật tự Công ty",
        "question": "Nhân viên khối Sản xuất trực tiếp được quy định quẹt thẻ chấm công tại địa điểm nào?",
        "options": [
            "A. Bất kỳ máy chấm công nào đặt tại công ty",
            "B. Máy chấm công ở cổng bảo vệ chính",
            "C. Máy chấm công lắp đặt ở lối vào phân xưởng các tầng, làm việc tầng nào chỉ được quẹt thẻ tại tầng đó",
            "D. Quẹt thẻ qua ứng dụng điện thoại cá nhân"
        ],
        "answer": "C. Máy chấm công lắp đặt ở lối vào phân xưởng các tầng, làm việc tầng nào chỉ được quẹt thẻ tại tầng đó",
        "explanation": "Theo Điều 12 (khoản 4): 'Nhân viên thuộc khối Sản xuất trực tiếp quẹt thẻ chấm công được lắp đặt ở lối vào phân xưởng các tầng. Nhân viên làm việc tầng nào chỉ được quẹt thẻ tại máy chấm công tầng đó.'"
    },
    {
        "id": 4,
        "category": "Quy tắc & Trật tự Công ty",
        "question": "Việc quẹt thẻ chấm công hộ người khác hoặc nhờ người khác quẹt hộ sẽ bị xử lý như thế nào?",
        "options": [
            "A. Chỉ bị nhắc nhở nếu vi phạm lần đầu",
            "B. Bị trừ 50% lương của ngày chấm công hộ",
            "C. Được chấp nhận nếu có sự đồng ý bằng miệng của đồng nghiệp",
            "D. Tuyệt đối bị nghiêm cấm và bị áp dụng hình thức xử lý kỷ luật phù hợp"
        ],
        "answer": "D. Tuyệt đối bị nghiêm cấm và bị áp dụng hình thức xử lý kỷ luật phù hợp",
        "explanation": "Theo Điều 12 (khoản 8): 'Nhân viên tuyệt đối không được nhờ Nhân viên khác quẹt thẻ chấm công hộ hoặc quẹt thẻ chấm công hộ Nhân viên khác... Các trường hợp vi phạm sẽ bị áp dụng hình xử lý kỷ luật phù hợp.'"
    },
    {
        "id": 5,
        "category": "Quy tắc & Trật tự Công ty",
        "question": "Quy định về việc sử dụng điện thoại cá nhân trong giờ làm việc của nhân viên được nêu thế nào?",
        "options": [
            "A. Được sử dụng thoải mái nếu đã hoàn thành định mức ca",
            "B. Nhân viên không được sử dụng điện thoại cho nhu cầu cá nhân trong giờ làm việc tại khu vực Sản xuất hoặc nhà kho",
            "C. Chỉ được dùng điện thoại để nhắn tin, cấm gọi điện thoại cá nhân",
            "D. Được sử dụng điện thoại khi máy gấp đang tự động chạy mà không có lỗi"
        ],
        "answer": "B. Nhân viên không được sử dụng điện thoại cho nhu cầu cá nhân trong giờ làm việc tại khu vực Sản xuất hoặc nhà kho",
        "explanation": "Theo Điều 13 (khoản 3): 'Nhân viên không được phép sử dụng điện thoại cho nhu cầu cá nhân trong giờ làm việc tại khu vực Sản xuất hoặc nhà kho.'"
    },

    # === PHẦN 2: AN TOÀN LAO ĐỘNG, VỆ SINH LAO ĐỘNG (5 câu) ===
    {
        "id": 6,
        "category": "An toàn & Vệ sinh Lao động",
        "question": "Khi muốn thực hiện vệ sinh hoặc sửa chữa máy gấp nhãn AOQI, người vận hành phải tuân thủ nguyên tắc an toàn nào?",
        "options": [
            "A. Vừa cho máy chạy chậm (inch mode) vừa dùng khăn lau lô gấp",
            "B. Phải tắt máy, khoá máy và gắn thẻ (LOTO) hoặc chuyển về chế độ chạy từng nấc bằng tay (jog/Inch mode)",
            "C. Chỉ cần bấm nút dừng tạm thời trên màn hình điều khiển là có thể sửa chữa",
            "D. Nhờ một người khác đứng canh nút nguồn rồi tiến hành lau chùi"
        ],
        "answer": "B. Phải tắt máy, khoá máy và gắn thẻ (LOTO) hoặc chuyển về chế độ chạy từng nấc bằng tay (jog/Inch mode)",
        "explanation": "Theo SOP AOQI mục 8.1.1: 'Khi cần làm vệ sinh hoặc sửa chữa máy, phải tắt máy, khoá máy và gắn thẻ (LOTO) hay chuyển về chế độ chạy từng nấc bằng tay (jog/Inch mode).'"
    },
    {
        "id": 7,
        "category": "An toàn & Vệ sinh Lao động",
        "question": "Quy định nào sau đây là ĐÚNG về việc nghỉ ngơi của nhân viên trong khuôn viên nhà máy?",
        "options": [
            "A. Được phép nằm nghỉ tại các lối đi sạch sẽ trong giờ giải lao",
            "B. Nhân viên không được phép nằm trong khuôn viên nhà máy ngay cả trong giờ nghỉ giải lao",
            "C. Được nằm nghỉ bên cạnh máy của mình nếu máy đang dừng bảo trì",
            "D. Được phép mang võng xếp vào lắp ở góc xưởng để nằm nghỉ trưa"
        ],
        "answer": "B. Nhân viên không được phép nằm trong khuôn viên nhà máy ngay cả trong giờ nghỉ giải lao",
        "explanation": "Theo Điều 14 (khoản 4) về An toàn lao động: 'Nhân viên không được phép nằm trong khuôn viên nhà máy ngay cả trong giờ nghỉ giải lao.'"
    },
    {
        "id": 8,
        "category": "An toàn & Vệ sinh Lao động",
        "question": "Khi phát hiện các nguy cơ gây tai nạn lao động hoặc bệnh nghề nghiệp, người vận hành phải làm gì?",
        "options": [
            "A. Tự ý tháo gỡ phụ tùng máy này lắp sang máy khác để khắc phục",
            "B. Tiếp tục làm việc bình thường và đợi đến hết ca báo cáo sau",
            "C. Báo cáo ngay cho cấp giám sát/quản lý hay phòng EHS để kịp thời giải quyết",
            "D. Chia sẻ lên nhóm mạng xã hội của phân xưởng để mọi người cùng tránh"
        ],
        "answer": "C. Báo cáo ngay cho cấp giám sát/quản lý hay phòng EHS để kịp thời giải quyết",
        "explanation": "Theo Điều 14 (khoản 8) và SOP mục 8.1.1: 'Báo cáo ngay cho cấp giám sát/quản lý hay phòng EHS ngay khi phát hiện các nguy cơ gây tai nạn lao động hay bệnh nghề nghiệp.'"
    },
    {
        "id": 9,
        "category": "An toàn & Vệ sinh Lao động",
        "question": "Quy định vệ sinh thiết bị trước và sau khi làm việc được thực hiện như thế nào?",
        "options": [
            "A. Chỉ cần vệ sinh vào ngày cuối tuần hoặc khi máy quá dơ",
            "B. Chỉ vệ sinh sau khi kết thúc ca làm việc, đầu ca không cần làm",
            "C. Trước và sau khi làm việc phải vệ sinh thiết bị, máy móc sạch sẽ; khi rời khỏi vị trí làm việc bắt buộc phải tắt máy",
            "D. Để máy tự chạy chế độ tự động làm sạch không cần vệ sinh thủ công"
        ],
        "answer": "C. Trước và sau khi làm việc phải vệ sinh thiết bị, máy móc sạch sẽ; khi rời khỏi vị trí làm việc bắt buộc phải tắt máy",
        "explanation": "Theo Điều 15 (khoản 1) về Vệ sinh lao động: 'Trước và sau khi làm việc phải vệ sinh thiết bị, máy móc, phương tiện cho sạch sẽ... rời khỏi vị trí làm việc phải tắt máy.'"
    },
    {
        "id": 10,
        "category": "An toàn & Vệ sinh Lao động",
        "question": "Quy định về ăn uống và giữ gìn vệ sinh trong khu vực sản xuất được quy định như thế nào?",
        "options": [
            "A. Có thể mang đồ ăn nhẹ vào khu vực sản xuất nếu để gọn gàng",
            "B. Được phép uống nước ngọt đóng chai tại bàn điều khiển máy",
            "C. Nhân viên tuyệt đối không được mang thức ăn, nước uống vào khu vực sản xuất; không nấu nướng xả rác bừa bãi",
            "D. Có thể mang trà sữa vào xưởng nếu có nắp đậy chống đổ"
        ],
        "answer": "C. Nhân viên tuyệt đối không được mang thức ăn, nước uống vào khu vực sản xuất; không nấu nướng xả rác bừa bãi",
        "explanation": "Theo Điều 15 (khoản 3) về Vệ sinh lao động: 'Nhân viên có trách nhiệm giữ gìn vệ sinh... không được mang thức ăn, nước uống vào khu vực sản xuất; không nấu nướng, ăn uống, xả rác...'"
    },

    # === PHẦN 3: SOP AOQI AUTO FOLDING (25 câu) ===
    {
        "id": 11,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Mục đích chính của quy trình 3-PO-121-00 SOP AOQI Auto Folding là gì?",
        "options": [
            "A. Hướng dẫn sửa chữa phần cứng hệ thống cơ điện toàn nhà máy",
            "B. Hướng dẫn các bước thực hiện vận hành máy Gấp nhãn Tự động, nhằm bảo đảm sản phẩm đạt chất lượng yêu cầu",
            "C. Quy định tiêu chuẩn thiết kế chế tạo máy gấp nhãn của nhà sản xuất",
            "D. Hướng dẫn tuyển dụng nhân viên vận hành máy gấp nhãn"
        ],
        "answer": "B. Hướng dẫn các bước thực hiện vận hành máy Gấp nhãn Tự động, nhằm bảo đảm sản phẩm đạt chất lượng yêu cầu",
        "explanation": "Theo SOP AOQI mục 1 (Purposes): 'Hướng dẫn các bước thực hiện vận hành máy Gấp nhãn Tự động, nhằm bảo đảm sản phẩm đạt chất lượng yêu cầu.'"
    },
    {
        "id": 12,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Theo mục trách nhiệm (Responsibilities), đối tượng nào có trách nhiệm tuân thủ đúng quy trình này trong sản xuất?",
        "options": [
            "A. Chỉ nhân viên vận hành máy",
            "B. Chỉ nhân viên đảm bảo chất lượng (QA)",
            "C. Nhân viên vận hành, đảm bảo chất lượng, an toàn lao động và giám sát",
            "D. Toàn bộ nhân viên văn phòng khối hành chính"
        ],
        "answer": "C. Nhân viên vận hành, đảm bảo chất lượng, an toàn lao động và giám sát",
        "explanation": "Theo SOP mục 5: 'Nhân viên vận hành, đảm bảo chất lượng, an toàn và có trách nhiệm làm theo đúng quy trình trong sản xuất. Giám sát có trách nhiệm kiểm tra việc thực hiện đúng và hiệu quả.'"
    },
    {
        "id": 13,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Khi kiểm tra đầu ca chuẩn bị đơn hàng (mục 8.3.1), bước kiểm tra Routing yêu cầu gì?",
        "options": [
            "A. Chỉ cần thấy có đơn hàng trên bàn là tiến hành gấp ngay",
            "B. Kiểm tra Routing có chữ ký xác nhận từ công đoạn trước xem đã ký xác nhận chưa và kiểm tra ghi chú đặc biệt; nếu chưa ký thì báo Team Lead và KHÔNG được tiến hành gấp nhãn",
            "C. Tự ký xác nhận thay công đoạn trước để đẩy nhanh tiến độ",
            "D. Bỏ qua bước Routing nếu đơn hàng có số lượng dưới 100 tờ"
        ],
        "answer": "B. Kiểm tra Routing có chữ ký xác nhận từ công đoạn trước xem đã ký xác nhận chưa và kiểm tra ghi chú đặc biệt; nếu chưa ký thì báo Team Lead và KHÔNG được tiến hành gấp nhãn",
        "explanation": "Theo SOP mục 8.3.1: 'Kiểm tra Routing: chữ ký xác nhận từ công đoạn trước... Nếu chưa báo Team Lead và không được tiến hành gấp nhãn.'"
    },
    {
        "id": 14,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Thao tác nào là bắt buộc trước khi nạp giấy lên khu vực cấp giấy (Pile Feeder) để tránh kẹt hoặc lỗi double sheet?",
        "options": [
            "A. Thấm một ít nước lên các mép giấy để giấy bám tốt",
            "B. Vỗ giấy (Fan the sheets) kỹ lưỡng trước khi nạp và loại bỏ giấy bị cong (curled sheets)",
            "C. Đập mạnh sấp giấy xuống bàn máy để các tờ giấy dính chặt vào nhau",
            "D. Không cần thao tác gì, đặt trực tiếp sấp hàng lên"
        ],
        "answer": "B. Vỗ giấy (Fan the sheets) kỹ lưỡng trước khi nạp và loại bỏ giấy bị cong (curled sheets)",
        "explanation": "Theo SOP mục 8.3.2: 'Vỗ giấy (Fan the sheets) kỹ lưỡng trước khi nạp để tránh kẹt hoặc lỗi double. Loại bỏ giấy bị cong (curled sheets).'"
    },
    {
        "id": 15,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Để nâng sấp giấy lên bàn cấp giấy đến vị trí hoạt động tự động dừng, bạn bấm nút nào trên màn hình?",
        "options": [
            "A. Bấm nút màu đỏ 'Stop feed'",
            "B. Bấm nút 'Infeed Single Paper' màu xanh dương",
            "C. Bấm nút 'Paper Feeder UP' (Thăng giấy lên) màu TÍM trên màn hình",
            "D. Xoay vô lăng tay (hand wheel) liên tục cho đến khi giấy chạm đầu hút"
        ],
        "answer": "C. Bấm nút 'Paper Feeder UP' (Thăng giấy lên) màu TÍM trên màn hình",
        "explanation": "Theo SOP mục 8.3.3: 'Bấm nút \"Paper Feeder UP\" (Thăng giấy lên) màu TÍM trên màn hình... Cảm biến chiều cao giấy sẽ tự động dừng bàn cấp giấy ở vị trí thích hợp.'"
    },
    {
        "id": 16,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Khi căn chỉnh khu vực đầu vào (Feeder head), đầu nạp (Feeder head) được di chuyển sang trái và mép nhọn của thép đè giấy (paper pressing steel) phải cách mặt giấy bao nhiêu mm?",
        "options": [
            "A. Cách mặt giấy đúng 1mm",
            "B. Cách mặt giấy đúng 5mm",
            "C. Cách mặt giấy đúng 10mm",
            "D. Áp sát trực tiếp đè chặt lên mặt giấy (0mm)"
        ],
        "answer": "B. Cách mặt giấy đúng 5mm",
        "explanation": "Theo SOP mục 8.3.4: 'Di chuyển Đầu nạp (Feeder head) sang trái, đặt mép nhọn của thép đè giấy cách mặt giấy 5mm.'"
    },
    {
        "id": 17,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Khi căn chỉnh Bàn truyền giấy (Register Table), dụng cụ nào dùng để trượt thanh dẫn bên (side guide) đến vị trí cần thiết theo chiều rộng giấy?",
        "options": [
            "A. Lục giác 5mm",
            "B. Tuốc nơ vít dẹt",
            "C. Núm xoay có rãnh/núm vặn định vị (fluted knob)",
            "D. Búa cao su để gõ"
        ],
        "answer": "C. Núm xoay có rãnh/núm vặn định vị (fluted knob)",
        "explanation": "Theo SOP mục 8.3.5.1: 'Sử dụng núm xoay có rãnh (fluted knob) để trượt thanh dẫn bên (side guide) với giá đỡ viên bi (marble holder) đến vị trí cần thiết...'"
    },
    {
        "id": 18,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Quy tắc bố trí bi thép và bi nhựa trên bàn truyền giấy (Register Table) được quy định như thế nào?",
        "options": [
            "A. Sử dụng toàn bộ bi thép để ép giấy nặng xuống",
            "B. Đặt ít nhất hai viên bi thép ở 4-6 vị trí gần bàn cấp giấy nhất, sau đó xếp xen kẽ bi thép và bi nhựa trên giá đỡ",
            "C. Đặt bi nhựa ở phía đầu vào, bi thép ở phía đầu ra",
            "D. Không sử dụng viên bi nào, chỉ dùng thanh thép đỡ giấy"
        ],
        "answer": "B. Đặt ít nhất hai viên bi thép ở 4-6 vị trí gần bàn cấp giấy nhất, sau đó xếp xen kẽ bi thép và bi nhựa trên giá đỡ",
        "explanation": "Theo SOP mục 8.3.5.1: 'Sử dụng bi: Đặt ít nhất hai viên bi thép ở 4-6 vị trí gần bàn cấp giấy nhất, sau đó xen kẽ bi thép và bi nhựa trên giá đỡ.'"
    },
    {
        "id": 19,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Thiết bị ép/giữ giấy (clip-on sheet hold-downs) dạng kẹp được lắp ngang qua bàn truyền giấy nhằm mục đích gì?",
        "options": [
            "A. Để cắt đứt các mép giấy thừa",
            "B. Để giữ giấy không bị bay lên trong quá trình truyền giấy tốc độ cao",
            "C. Để bôi trơn bề mặt giấy bằng dầu máy",
            "D. Để đếm số lượng tờ giấy đi qua"
        ],
        "answer": "B. Để giữ giấy không bị bay lên trong quá trình truyền giấy tốc độ cao",
        "explanation": "Theo SOP mục 8.3.5.1: 'Lắp các bộ phận đè giấy dạng kẹp (clip-on sheet hold-downs) ngang qua bàn truyền giấy để giữ giấy không bay lên.'"
    },
    {
        "id": 20,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Các túi gấp (buckle plates) số lẻ (1, 3, 5...) và số chẵn (2, 4, 6...) được bố trí lắp đặt ở vị trí nào của máy?",
        "options": [
            "A. Số lẻ bên dưới, số chẵn bên trên",
            "B. Số lẻ bên trên, số chẵn bên dưới",
            "C. Tất cả lắp bên trên, bên dưới để trống",
            "D. Lắp xen kẽ trái và phải dọc theo hướng đi của giấy"
        ],
        "answer": "B. Số lẻ bên trên, số chẵn bên dưới",
        "explanation": "Theo SOP mục 8.3.5.2: 'Các túi gấp số lẻ (1,3,5,...) sẽ được setup Bên trên, và các túi gấp số chẵn (2,4,6,8..) sẽ được setup bên dưới.'"
    },
    {
        "id": 21,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Tại vị trí trục gấp không cần tạo nếp gấp (không setup túi gấp), bạn phải gắn chi tiết nào?",
        "options": [
            "A. Để trống hoàn toàn trục gấp đó",
            "B. Gắn một thanh sắt đè giấy thay thế",
            "C. Phải gắn thoi mù (blind plate) vào vị trí đó",
            "D. Dán băng keo hai mặt bịt kín khe hở"
        ],
        "answer": "C. Phải gắn thoi mù (blind plate) vào vị trí đó",
        "explanation": "Theo SOP mục 8.3.5.2: 'Chú ý: Vị trí nào không setup các túi gấp, phải gắn thoi mù vào vị trí đó.'"
    },
    {
        "id": 22,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Mục đích của việc căn chỉnh Tấm chặn giấy (Paper Stop Slider) trong thùng gấp là gì?",
        "options": [
            "A. Để điều chỉnh tốc độ chạy của băng tải",
            "B. Canh chỉnh chiều rộng giữa các đường gấp cho phù hợp theo yêu cầu kích thước bản vẽ (AW)",
            "C. Để ngăn không cho giấy đi vào trục gấp tiếp theo",
            "D. Để cố định vị trí của camera bắt lỗi"
        ],
        "answer": "B. Canh chỉnh chiều rộng giữa các đường gấp cho phù hợp theo yêu cầu kích thước bản vẽ (AW)",
        "explanation": "Theo SOP mục 8.3.5.3: 'Mục đích: Canh chỉnh chiều rộng giữa các đường gấp cho phù hợp theo yêu cầu. Đo chiều rộng giữa các đường gấp theo AW...'"
    },
    {
        "id": 23,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Khi điều chỉnh Tấm chặn giấy (Paper Stop Slider), sau khi nới lỏng núm khóa cao su và xoay tay cầm điều chỉnh xong, bước tiếp theo là gì?",
        "options": [
            "A. Để lỏng núm khóa cao su để tấm tự động xê dịch khi chạy",
            "B. Tháo hẳn núm cao su ra cất đi",
            "C. Siết chặt lại núm khóa cao su để cố định vị trí chặn giấy",
            "D. Phun keo dán sắt vào ren để giữ chặt"
        ],
        "answer": "C. Siết chặt lại núm khóa cao su để cố định vị trí chặn giấy",
        "explanation": "Theo SOP mục 8.3.5.3: 'Xoay tay cầm cao su điều chỉnh để di chuyển tấm chặn giấy... Siết chặt lại núm khóa cao su sau khi điều chỉnh xong.'"
    },
    {
        "id": 24,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Khi lắp đặt cầu nối (Transfer Unit) sang trạm gấp số 2, tốc độ tối đa của dây đai cầu nối trên Bộ điều khiển tốc độ (Speed Control Unit) là bao nhiêu?",
        "options": [
            "A. Tối đa là mức 5",
            "B. Tối đa là mức 8",
            "C. Tối đa là mức 10",
            "D. Tốc độ tự động không giới hạn"
        ],
        "answer": "B. Tối đa là mức 8",
        "explanation": "Theo SOP mục 8.3.5.4: 'Điều chỉnh tốc độ dây đai cầu nối: Dùng núm xoay 3 trên bộ điều khiển tốc độ... Tốc độ tối đa là 8.'"
    },
    {
        "id": 25,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Nút bấm nào trên bảng điều khiển cơ khí được dùng để khởi động máy chính và bơm khí nén?",
        "options": [
            "A. Nút dừng khẩn cấp màu đỏ (Emergency Stop)",
            "B. Nút nhấn Khởi động máy màu XANH LÁ (Start button)",
            "C. Nút nhấn màu vàng (Inch/Jog button)",
            "D. Công tắc xoay chọn chế độ thủ công"
        ],
        "answer": "B. Nút nhấn Khởi động máy màu XANH LÁ (Start button)",
        "explanation": "Theo SOP mục 8.3.7.1 và 8.3.8.1: 'Nhấn nút Khởi động máy màu XANH LÁ trên bảng điều khiển để khởi động máy chính và bơm khí nén.'"
    },
    {
        "id": 26,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Khi chạy thử nghiệm (mục 8.3.7), để kiểm tra cấp thử từng tờ giấy, bạn chọn chế độ cấp giấy nào trên màn hình cảm ứng?",
        "options": [
            "A. Continuous Feed (Cấp giấy liên tục)",
            "B. Manual paper ejection (Đá giấy thủ công)",
            "C. 'Infeed Single Paper' hoặc 'Infeed Single Paper' (Cấp từng tờ/Từng tờ)",
            "D. Stop feed (Dừng cấp giấy)"
        ],
        "answer": "C. 'Infeed Single Paper' hoặc 'Infeed Single Paper' (Cấp từng tờ/Từng tờ)",
        "explanation": "Theo SOP mục 8.3.7.1: 'Chọn chế độ cấp giấy: Nhấn \"Infeed Single Paper\" (Từng tờ).'"
    },
    {
        "id": 27,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Làm thế nào để xác định quá trình cài đặt cảm biến phát hiện 2 tờ (double sheet sensor) đã thành công?",
        "options": [
            "A. Cho chạy thử 1 tờ giấy, máy phải báo động đỏ và dừng lại",
            "B. Cho chạy thử 2 tờ giấy chồng lên nhau; quá trình cấp giấy phải dừng lại (máy chính vẫn chạy) và máy báo động (alarm)",
            "C. Máy tự động cắt đứt cả hai tờ giấy khi đi qua sensor",
            "D. Sensor nhấp nháy đèn liên tục nhưng máy vẫn cho 2 tờ đi qua bình thường"
        ],
        "answer": "B. Cho chạy thử 2 tờ giấy chồng lên nhau; quá trình cấp giấy phải dừng lại (máy chính vẫn chạy) và máy báo động (alarm)",
        "explanation": "Theo SOP mục 8.3.7.2: 'Thử với hai tờ giấy; quá trình cấp giấy phải dừng lại (máy chính vẫn chạy) và máy báo động (alarm) là cài đặt thành công.'"
    },
    {
        "id": 28,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Nếu trong quá trình kiểm tra ngoại quan tờ đã gấp thấy có hiện tượng Dơ hoặc Mất nội dung do máy bám dầu mỡ, người vận hành cần làm gì đầu tiên?",
        "options": [
            "A. Đổ thêm dầu bôi trơn vào trục gấp",
            "B. Tiến hành lau chùi các bộ phận máy sạch sẽ; nếu không phải nguyên nhân từ máy thì báo Team Leader/Kỹ thuật để có phương án phù hợp",
            "C. Tiếp tục chạy hàng loạt và phân loại nhãn dơ ra sau khi kết thúc ca",
            "D. Giảm tốc độ chạy máy xuống mức thấp nhất"
        ],
        "answer": "B. Tiến hành lau chùi các bộ phận máy sạch sẽ; nếu không phải nguyên nhân từ máy thì báo Team Leader/Kỹ thuật để có phương án phù hợp",
        "explanation": "Theo SOP mục 8.3.8.2: 'Kiểm tra ngoại quan tờ đã gấp: Dơ, Mất nội dung... -> Kiểm tra các cơ quan xem có bám dầu không -> Lau chùi nếu có -> Nếu không phải nguyên nhân từ Máy, báo lại cho TL và kĩ thuật...'"
    },
    {
        "id": 29,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Khi đường gấp nhãn bị nứt/vỡ giấy quá nặng do lực ép lớn, làm cách nào để giảm áp lực lô gấp (Fold Roller Gap Adjustment)?",
        "options": [
            "A. Xoay núm điều chỉnh cơ khí để giảm khe hở (ép chặt hơn) giữa các lô",
            "B. Xoay núm điều chỉnh cơ khí để tăng khe hở (nới lỏng) giữa các lô gấp",
            "C. Đổ thêm nước vào sấp giấy để làm mềm giấy trước khi gấp",
            "D. Tăng tốc độ của máy lên tối đa để giấy đi qua nhanh hơn"
        ],
        "answer": "B. Xoay núm điều chỉnh cơ khí để tăng khe hở (nới lỏng) giữa các lô gấp",
        "explanation": "Theo SOP mục 8.3.8.3: 'Giảm áp lực: Xoay núm điều chỉnh để tăng khe hở (nới lỏng) giữa các lô gấp. Điều này làm giảm lực ép lên giấy khi đi qua, tạo ra nếp gấp nhẹ hơn.'"
    },
    {
        "id": 30,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Tuyệt đối nghiêm cấm hành vi nào sau đây khi máy gấp nhãn đang hoạt động?",
        "options": [
            "A. Đứng quan sát máy vận hành",
            "B. Thực hiện bất kỳ thao tác canh chỉnh, vệ sinh máy khi máy đang chạy (chỉ được phép chỉnh khi máy đã dừng hoàn toàn/bấm dừng khẩn cấp)",
            "C. Nhấn nút dừng cấp giấy (Stop feed)",
            "D. Điều chỉnh tốc độ dây đai cầu nối từ mức 5 lên mức 6"
        ],
        "answer": "B. Thực hiện bất kỳ thao tác canh chỉnh, vệ sinh máy khi máy đang chạy (chỉ được phép chỉnh khi máy đã dừng hoàn toàn/bấm dừng khẩn cấp)",
        "explanation": "Theo SOP mục 8.3.8.3: 'Lưu ý: Chỉ được điều chỉnh máy khi máy không hoạt động. Bấm nút dừng khẩn cấp khi muốn canh chỉnh máy. Bất kỳ các thao tác canh chỉnh máy khi máy đang hoạt động đều bị nghiêm cấm.'"
    },
    {
        "id": 31,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Đối với đơn hàng có số lượng dưới 100 tờ (<100 tờ), tần suất kiểm tra chất lượng trong quá trình vận hành được quy định thế nào?",
        "options": [
            "A. Kiểm tra toàn bộ 100% không bỏ sót tờ nào",
            "B. Cứ 20 tờ kiểm tra chất lượng đường gấp và ngoại quan 1 lần",
            "C. Chỉ kiểm tra 1 tờ duy nhất ở đầu đơn hàng",
            "D. Cứ 50 tờ kiểm tra chất lượng 1 lần"
        ],
        "answer": "B. Cứ 20 tờ kiểm tra chất lượng đường gấp và ngoại quan 1 lần",
        "explanation": "Theo bảng tần suất tại SOP mục 8.3.10: Đối với đơn hàng '<100 tờ', yêu cầu '20 tờ kiểm 1 lần' để kiểm tra tình trạng bể giấy và ngoại quan."
    },
    {
        "id": 32,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Đối với đơn hàng có số lượng trên 1000 tờ (>1000 tờ), tần suất kiểm tra chất lượng trong quá trình vận hành được quy định thế nào?",
        "options": [
            "A. Cứ 500 tờ kiểm tra 1 lần",
            "B. Chỉ kiểm tra lúc bắt đầu và lúc kết thúc đơn hàng",
            "C. Cứ 200 tờ kiểm tra chất lượng đường gấp và ngoại quan 1 lần",
            "D. Không cần kiểm tra vì máy chạy số lượng lớn rất ổn định"
        ],
        "answer": "C. Cứ 200 tờ kiểm tra chất lượng đường gấp và ngoại quan 1 lần",
        "explanation": "Theo bảng tần suất tại SOP mục 8.3.10: Đối với đơn hàng '> 1000 tờ', yêu cầu '200 tờ kiểm 1 lần'."
    },
    {
        "id": 33,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Quy trình đóng gói nhãn sau khi gấp hoàn thành được tiến hành như thế nào?",
        "options": [
            "A. Cho toàn bộ nhãn đã gấp vào thùng lớn mà không cần đếm hay bó lại",
            "B. Tiến hành quấn thun 1 cọc từ 25 - 50 pcs, đóng bịch 250 - 500 pcs tùy độ dày, sau đó dán bịch và dán nhãn sticker ghi đầy đủ thông tin SO#, Số lượng, Người kiểm",
            "C. Dùng băng keo dán chặt từng tờ nhãn lại với nhau",
            "D. Đóng gói ngẫu nhiên mỗi bịch 1000 pcs và không cần dán nhãn thông tin"
        ],
        "answer": "B. Tiến hành quấn thun 1 cọc từ 25 - 50 pcs, đóng bịch 250 - 500 pcs tùy độ dày, sau đó dán bịch và dán nhãn sticker ghi đầy đủ thông tin SO#, Số lượng, Người kiểm",
        "explanation": "Theo SOP mục 8.3.11: 'Tiến hành quấn thun 1 cọc 25 - 50 pcs tùy vào độ dày... Đóng bịch 250 - 500 pcs... Dán bịch và dán sticker bịch hàng có thông tin đầy đủ: SO# - Số lượng - Người kiểm.'"
    },
    {
        "id": 34,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Khi hoàn thành xong một đơn hàng, người vận hành phải thực hiện những thủ tục nào trước khi bàn giao?",
        "options": [
            "A. Kéo hàng ra khu vực bất kỳ và ra về",
            "B. Ký tên xác nhận và ghi số tờ ở Routing trên Lệnh sản xuất (LSX), kéo hàng ra khu vực quy định, vệ sinh sạch sẽ khu vực làm việc",
            "C. Không cần ghi chép gì, chỉ cần báo miệng cho ca sau",
            "D. Để nguyên rác thải và dầu mỡ tại bàn máy cho người bảo trì dọn"
        ],
        "answer": "B. Ký tên xác nhận và ghi số tờ ở Routing trên Lệnh sản xuất (LSX), kéo hàng ra khu vực quy định, vệ sinh sạch sẽ khu vực làm việc",
        "explanation": "Theo SOP mục 8.3.12: 'Hoàn thành đơn hàng: Kí tên xác nhận và ghi số tờ ở routing trên LSX -> Kéo hàng ra khu vực quy định -> Vệ sinh khu vực.'"
    },
    {
        "id": 35,
        "category": "SOP Vận hành Máy Gấp nhãn",
        "question": "Trong bảng tham số cài đặt trên màn hình (Setting Screen), tham số 'Paper Jam Time' (塞纸时间) có ý nghĩa gì?",
        "options": [
            "A. Tốc độ quay của trục dao cắt tạo nếp gấp",
            "B. Khoảng cách (khe hở) giữa hai tờ giấy đang được nạp vào máy",
            "C. Thời gian trễ (tính bằng giây) để máy bắt đầu báo động khi xảy ra lỗi cấp giấy kép (double sheet) hoặc kẹt giấy (paper jam)",
            "D. Tổng thời gian máy chạy một mẻ đơn hàng"
        ],
        "answer": "C. Thời gian trễ (tính bằng giây) để máy bắt đầu báo động khi xảy ra lỗi cấp giấy kép (double sheet) hoặc kẹt giấy (paper jam)",
        "explanation": "Theo bảng tham số cài đặt SOP mục 8.3.6: 'Paper Jam Time (塞纸时间): Thời gian trễ (tính bằng giây) để máy bắt đầu báo động khi xảy ra lỗi cấp giấy kép hoặc kẹt giấy.'"
    },

    # === PHẦN 4: HƯỚNG DẪN KHẮC PHỤC LỖI (OPL) (15 câu) ===
    {
        "id": 36,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Khi gặp sự cố đầu hút cấp giấy hoạt động nhưng 'Hút giấy không lên' do hơi yếu ở van đầu bò, bạn điều chỉnh thế nào?",
        "options": [
            "A. Vặn các núm van hơi về hướng dấu trừ (-) để giảm hơi",
            "B. Kiểm tra căn chỉnh 3 núm van hơi và chỉnh về hướng dấu cộng (+) để tăng lực hơi mạnh hơn",
            "C. Tắt máy và gọi thợ cơ điện bên ngoài vào thay van mới",
            "D. Đổ thêm dầu mỡ vào van đầu bò"
        ],
        "answer": "B. Kiểm tra căn chỉnh 3 núm van hơi và chỉnh về hướng dấu cộng (+) để tăng lực hơi mạnh hơn",
        "explanation": "Theo OPL mục 1.1: 'Hơi yếu ở van đầu bò: Kiểm tra canh chỉnh 3 núm van hơi cho phù hợp với từng loại giấy. Chỉnh về hướng dấu (+) -> lực hơi mạnh hơn.'"
    },
    {
        "id": 37,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Khi điều chỉnh họng ống hơi thổi tách giấy trong trường hợp 'Hút giấy không lên', thao tác vặn cùng chiều kim đồng hồ và ngược chiều kim đồng hồ có tác dụng gì?",
        "options": [
            "A. Cùng chiều kim đồng hồ làm hạ họng hơi; ngược chiều làm nâng họng hơi",
            "B. Cùng chiều kim đồng hồ làm nâng họng hơi lên; ngược chiều kim đồng hồ làm hạ họng hơi xuống",
            "C. Cùng chiều làm tăng áp lực khí thổi; ngược chiều làm giảm áp lực khí thổi",
            "D. Vặn chiều nào cũng giống nhau, chỉ dùng để xoay góc thổi sang trái/phải"
        ],
        "answer": "B. Cùng chiều kim đồng hồ làm nâng họng hơi lên; ngược chiều kim đồng hồ làm hạ họng hơi xuống",
        "explanation": "Theo OPL mục 1.2: 'Vặn núm để điều chỉnh hướng họng ống hơi thổi tách giấy: Cùng chiều kim đồng hồ -> họng nâng lên; Ngược chiều kim đồng hồ -> họng hạ xuống.'"
    },
    {
        "id": 38,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Lỗi 'Double sheet không đá nhãn' xảy ra. Quy trình các bước thực hiện trên màn hình cảm ứng để điều chỉnh thông số này là gì?",
        "options": [
            "A. B1: Chọn Monitor Screen -> B2: Nhập thông số mới trực tiếp -> B3: Nhấn CLEAR",
            "B. B1: Chọn mục Set the screen -> B2: Chọn số ở mục 'Double sheet ejection compensation' -> B3: Nhập thông số mới rồi nhấn ENTER để lưu",
            "C. B1: Bấm dừng khẩn cấp -> B2: Nhập số vào ô Total production -> B3: Khởi động lại máy",
            "D. B1: Chọn mục Hand movement -> B2: Nhấn giữ nút Manual paper ejection -> B3: Nhấn quay lại"
        ],
        "answer": "B. B1: Chọn mục Set the screen -> B2: Chọn số ở mục 'Double sheet ejection compensation' -> B3: Nhập thông số mới rồi nhấn ENTER để lưu",
        "explanation": "Theo OPL mục 2: 'B1: Chọn mục Set the screen. B2: Chọn vô số -300 mục Double sheet ejection compensation để điều chỉnh thông số. B3: Nhập thông số mới rồi nhấn ENTER để lưu.'"
    },
    {
        "id": 39,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Khi điều chỉnh thông số 'Double sheet ejection compensation', quy tắc bù trừ theo tốc độ băng tải được thực hiện thế nào?",
        "options": [
            "A. Tốc độ băng tải càng cao thì thông số càng giảm (ví dụ từ -300 về -200)",
            "B. Tốc độ băng tải càng cao thì trị số âm của thông số càng tăng (ví dụ tốc độ 120-130 dùng thông số -300; khi tăng tốc độ thì điều chỉnh từ -300 sang -400)",
            "C. Giữ nguyên cố định thông số ở mức -300 cho mọi dải tốc độ",
            "D. Trị số âm luôn cài đặt ở mức bằng một nửa tốc độ băng tải"
        ],
        "answer": "B. Bị trị số âm của thông số càng tăng (ví dụ tốc độ 120-130 dùng thông số -300; khi tăng tốc độ thì điều chỉnh từ -300 sang -400)",
        "explanation": "Theo OPL mục 2: 'Tốc độ băng tải càng cao -> Thông số càng cao và ngược lại. Ví dụ: Tốc độ băng tải 120-130 -> thông số -300. Tốc độ càng tăng thì thông số từ -300 -> -400.'"
    },
    {
        "id": 40,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Sự cố 'Camera bắt lỗi nhưng không đá kịp nhãn' (mục 3 OPL). Khi tăng tốc độ băng tải, bạn cần điều chỉnh thông số 'Camera ejection compensation' như thế nào?",
        "options": [
            "A. Giữ nguyên thông số -600 cho mọi tốc độ",
            "B. Giảm trị số âm từ -600 về -500 khi tăng tốc độ",
            "C. Tăng trị số âm từ -600 sang -700 khi tốc độ băng tải tăng lên",
            "D. Cài đặt thông số này về bằng 0 để hệ thống tự bù trừ"
        ],
        "answer": "C. Tăng trị số âm từ -600 sang -700 khi tốc độ băng tải tăng lên",
        "explanation": "Theo OPL mục 3: 'Ví dụ: Tốc độ băng tải 120-130 -> thông số -600. Tốc độ càng tăng thì thông số từ -600 -> -700.'"
    },
    {
        "id": 41,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Để khắc phục lỗi 'Sensor Camera không nhận diện', đối với việc điều chỉnh độ nhận diện sensor cơ vật lý, nếu phát hiện độ nhận diện sensor yếu, bạn dùng tua vít vặn ốc trên sensor về hướng nào?",
        "options": [
            "A. Vặn về hướng dấu cộng (+) để tăng khoảng cách",
            "B. Vặn về hướng dấu trừ (-) để hạ khoảng cách nhận diện",
            "C. Vặn liên tục nhiều vòng không giới hạn",
            "D. Giữ nguyên không vặn ốc, chỉ lau bề mặt kính cảm biến"
        ],
        "answer": "B. Vặn về hướng dấu trừ (-) để hạ khoảng cách nhận diện",
        "explanation": "Theo OPL mục 4.2: 'Dùng tua vít vặn ốc trên sensor. Độ nhận diện sensor yếu -> Vặn (-) hạ khoảng cách.'"
    },
    {
        "id": 42,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Để khắc phục lỗi 'Sensor Camera không nhận diện', nếu độ nhận diện của cảm biến đang quá mạnh dẫn đến báo động giả, bạn vặn ốc trên sensor về hướng nào?",
        "options": [
            "A. Vặn về hướng dấu cộng (+) để tăng khoảng cách",
            "B. Vặn về hướng dấu trừ (-) để giảm khoảng cách",
            "C. Tháo hẳn cảm biến ra lau chùi rồi lắp lại vị trí cũ",
            "D. Vặn ốc theo cả hai chiều trái phải xen kẽ"
        ],
        "answer": "A. Vặn về hướng dấu cộng (+) để tăng khoảng cách",
        "explanation": "Theo OPL mục 4.2: 'Dùng tua vít vặn ốc trên sensor. Độ nhận diện sensor mạnh -> Vặn (+) tăng khoảng cách.'"
    },
    {
        "id": 43,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Khi máy xảy ra lỗi 'Kẹt Giấy' (mục 5 OPL), hai nguyên nhân chính thường gặp được xác định là gì?",
        "options": [
            "A. Do giấy quá mỏng và tốc độ máy quá chậm",
            "B. Do bị lỗi cấp giấy kép (Double sheet) hoặc do áp lực lô gấp quá nặng",
            "C. Do hỏng motor chính và hỏng van khí nén đầu bò",
            "D. Do hết giấy nạp đầu vào và rác bám đầy bàn ra giấy"
        ],
        "answer": "B. Do bị lỗi cấp giấy kép (Double sheet) hoặc do áp lực lô gấp quá nặng",
        "explanation": "Theo OPL mục 5 (Kẹt giấy) chỉ ra hai nguyên nhân chính: '5.1. Double sheet' và '5.2. Áp lực lô nặng'."
    },
    {
        "id": 44,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Cách khắc phục triệt để khi máy gặp lỗi 'Kẹt giấy do Áp lực lô nặng' hoặc lỗi 'Bể giấy, cấn giấy' (mục 5.2 và mục 6 OPL) là gì?",
        "options": [
            "A. Vặn tăng áp lực tất cả các lô gấp về hướng dấu cộng (+)",
            "B. Chỉnh đều toàn bộ các lô gấp về hướng dấu trừ (-) để nới lỏng áp lực, sau đó chạy thử để kiểm tra lại",
            "C. Tháo toàn bộ lô gấp ra và bôi mỡ bò bôi trơn",
            "D. Tăng áp suất khí nén đầu bò lên tối đa để thổi bay giấy bị kẹt"
        ],
        "answer": "B. Chỉnh đều toàn bộ các lô gấp về hướng dấu trừ (-) để nới lỏng áp lực, sau đó chạy thử để kiểm tra lại",
        "explanation": "Theo OPL mục 5.2 và mục 6: 'Khắc phục: Chỉnh đều toàn bộ các lô về (-). Sau khi chỉnh chạy thử để kiểm tra lại.'"
    },
    {
        "id": 45,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Mô tả lỗi của hiện tượng 'Đường gấp bị xéo' (mục 7 OPL) trên tờ nhãn sau khi gấp là gì?",
        "options": [
            "A. Tờ nhãn bị lệch kích thước hoàn toàn ở cả hai đầu",
            "B. Đường gấp một đầu bị xéo lệch đi, còn một đầu thì OK",
            "C. Tờ nhãn bị rách nát hoàn toàn không nhìn rõ đường gấp",
            "D. Nhãn gấp đúng kích thước nhưng bị ngược mặt nội dung"
        ],
        "answer": "B. Đường gấp một đầu bị xéo lệch đi, còn một đầu thì OK",
        "explanation": "Theo OPL mục 7: 'Mô tả lỗi: đường gấp một đầu bị xéo, một đầu OK.'"
    },
    {
        "id": 46,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Để khắc phục lỗi 'Đường gấp bị xéo', sau khi xác định đường gấp bị sai, thao tác chỉnh núm thoi túi giấy được thực hiện như thế nào?",
        "options": [
            "A. Vặn chặt núm màu đen rồi quay trực tiếp núm đỏ bên cạnh",
            "B. Vặn lỏng núm đen, sau đó vặn vòng kim loại có dấu + - (vặn sang (+) để tăng đường gấp, vặn sang (-) để giảm đường gấp)",
            "C. Dùng kìm siết mạnh vòng kim loại mà không cần nới lỏng núm đen",
            "D. Thay toàn bộ tấm túi gấp mới"
        ],
        "answer": "B. Vặn lỏng núm đen, sau đó vặn vòng kim loại có dấu + - (vặn sang (+) để tăng đường gấp, vặn sang (-) để giảm đường gấp)",
        "explanation": "Theo OPL mục 7: 'B2: Chỉnh núm thoi túi giấy của đường gấp đó: 2.1: vặn lỏng núm đen. 2.2: vặn vòng kim loại có dấu + -: Vặn sang (+) -> đường gấp tăng lên, Vặn sang (-) -> đường gấp giảm xuống.'"
    },
    {
        "id": 47,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Mô tả lỗi của hiện tượng 'Đường gấp sai kích thước' (mục 8 OPL) trên tờ nhãn sau khi gấp là gì?",
        "options": [
            "A. Đường gấp bị xéo lệch chỉ một đầu",
            "B. Đường gấp lệch toàn bộ kích thước ở cả hai đầu so với tiêu chuẩn",
            "C. Đường gấp bị nhăn nhúm ở giữa tờ nhãn",
            "D. Nhãn không gấp được đường nào, đi thẳng ra bàn nhận giấy"
        ],
        "answer": "B. Đường gấp lệch toàn bộ kích thước ở cả hai đầu so với tiêu chuẩn",
        "explanation": "Theo OPL mục 8: 'Mô tả lỗi: Đường gấp lệch toàn bộ.'"
    },
    {
        "id": 48,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Các bước chính xác để khắc phục lỗi 'Đường gấp sai kích thước' bằng cách điều chỉnh núm thoi túi giấy là gì?",
        "options": [
            "A. B1: Nới lỏng núm đen -> B2: Vặn núm đỏ -> B3: Siết chặt núm đen",
            "B. B1: Kiểm tra đảm bảo núm đen đã siết chặt -> B2: Mở khóa màu đỏ -> B3: Vặn vòng kim loại có dấu + - (vặn sang (+) để tăng đường gấp, vặn sang (-) để giảm)",
            "C. B1: Tháo khóa màu đỏ cất đi -> B2: Gõ nhẹ túi gấp -> B3: Bấm chạy máy",
            "D. B1: Chỉnh toàn bộ các lô gấp về hướng dấu trừ (-)"
        ],
        "answer": "B. B1: Kiểm tra đảm bảo núm đen đã siết chặt -> B2: Mở khóa màu đỏ -> B3: Vặn vòng kim loại có dấu + - (vặn sang (+) để tăng đường gấp, vặn sang (-) để giảm)",
        "explanation": "Theo OPL mục 8: 'Cách khắc phục: 2.1: Kiểm tra núm đen đã siết chặt. 2.2: Mở khóa màu đỏ. 2.3: vặn vòng kim loại có dấu + -: Vặn sang (+) -> đường gấp tăng lên, Vặn sang (-) -> đường gấp giảm xuống.'"
    },
    {
        "id": 49,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Ba nguyên nhân chính dẫn đến lỗi 'Bắn nhãn sang cụm 2 không đúng vị trí' (mục 9 OPL) là gì?",
        "options": [
            "A. Do giấy quá dày, lỗi double sheet và hết khí nén đầu nạp",
            "B. Tốc độ bắn nhãn yếu, Dây belt phân bổ không đều, Bi cụm 2 phân bố không đều",
            "C. Do hỏng camera bắt lỗi, đai ốc lỏng và rách dây curoa chính",
            "D. Do bụi giấy bám nhiều, nhiệt độ phòng quá nóng và rò rỉ khí"
        ],
        "answer": "B. Tốc độ bắn nhãn yếu, Dây belt phân bổ không đều, Bi cụm 2 phân bố không đều",
        "explanation": "Theo OPL mục 9 chỉ ra 3 nguyên nhân: '9.1. Tốc độ bắn nhãn yếu', '9.2. Dây belt phân bổ không đều' và '9.3. Bi cụm 2 phân bố không đều'."
    },
    {
        "id": 50,
        "category": "Khắc phục Lỗi Máy Gấp nhãn",
        "question": "Khi khắc phục lỗi bắn nhãn không đúng vị trí do 'Bi cụm 2 phân bố không đều', quy định lựa chọn loại bi nào được ƯU TIÊN khi setup lại?",
        "options": [
            "A. Ưu tiên setup toàn bộ bi thép nặng",
            "B. Ưu tiên setup bi nhựa nhẹ",
            "C. Trộn lẫn ngẫu nhiên bi nhựa và bi thép không cần phân biệt",
            "D. Không sử dụng viên bi nào, chỉ dùng thanh thép đè"
        ],
        "answer": "B. Ưu tiên setup bi nhựa nhẹ",
        "explanation": "Theo OPL mục 9.3 bước B2: 'Setup xong chạy thử kiểm tra lại. Chú ý: Ưu tiên setup bi nhựa.'"
    }
]

# --- STREAMLIT UI LAYOUT ---

st.title("🎓 ĐỀ KIỂM TRA TRẮC NGHIỆM")
st.subheader("Quy Trình Vận Hành & Khắc Phục Lỗi Máy Gấp Nhãn Tự Động AOQI")
st.caption("Tài liệu huấn luyện nội bộ bám sát Quy trình SOP và OPL máy AOQI")

# Step 1: Employee Registration Form
if not st.session_state.started:
    st.markdown("""
    Chào mừng bạn đến với hệ thống kiểm tra kiến thức vận hành thiết bị!
    Vui lòng nhập thông tin cá nhân dưới đây để bắt đầu làm đề thi **50 câu hỏi**.
    
    *   **Yêu cầu Đạt (PASS):** Trả lời đúng từ **45/50 câu hỏi** trở lên.
    *   **Thời gian:** Làm bài không giới hạn, kết quả sẽ được hiển thị chi tiết ở cuối bài.
    """)
    
    with st.form("employee_info_form"):
        name_input = st.text_input("✍️ Họ và Tên Nhân Viên:", value=st.session_state.employee_name, placeholder="Ví dụ: Nguyễn Văn A")
        id_input = st.text_input("🆔 Mã Số Nhân Viên (Employee ID):", value=st.session_state.employee_id, placeholder="Ví dụ: ADVN-12345")
        
        submit_btn = st.form_submit_button("🚀 BẮT ĐẦU LÀM BÀI")
        
        if submit_btn:
            if not name_input.strip():
                st.error("Vui lòng nhập Họ và Tên!")
            elif not id_input.strip():
                st.error("Vui lòng nhập Mã số nhân viên!")
            else:
                st.session_state.employee_name = name_input.strip()
                st.session_state.employee_id = id_input.strip()
                st.session_state.started = True
                st.session_state.current_q = 0
                st.session_state.answers = {}
                st.session_state.finished = False
                st.rerun()

# Step 2: Quiz in Progress
elif st.session_state.started and not st.session_state.finished:
    q_idx = st.session_state.current_q
    total_qs = len(QUESTIONS)
    q_data = QUESTIONS[q_idx]
    
    # Progress Bar
    progress = (q_idx) / total_qs
    st.progress(progress)
    st.write(f"**Câu hỏi {q_idx + 1} / {total_qs}** | Chuyên mục: *{q_data['category']}*")
    
    # Display Question
    st.markdown(f"### Q{q_idx + 1}: {q_data['question']}")
    
    # Check if there is any visual help description for visual-related questions
    if "bi thép" in q_data['question'].lower() or "bi nhựa" in q_data['question'].lower():
        st.info("ℹ️ *Câu hỏi này liên quan đến việc căn chỉnh bi trên bàn truyền giấy (Register Table) hoặc bi cụm 2 (OPL).*")
    elif "compensation" in q_data['question'].lower() or "ejection" in q_data['question'].lower():
        st.info("ℹ️ *Câu hỏi liên quan đến cài đặt thông số bù trừ khoảng cách trên màn hình cảm ứng điều khiển.*")
    
    # Set default choice index if already answered before
    prev_ans = st.session_state.answers.get(q_idx, None)
    default_idx = 0
    if prev_ans in q_data['options']:
        default_idx = q_data['options'].index(prev_ans)
        
    user_choice = st.radio("Chọn đáp án chính xác nhất:", q_data['options'], index=default_idx, key=f"q_radio_{q_idx}")
    
    # Navigation Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if q_idx > 0:
            if st.button("⬅️ Câu Trước"):
                st.session_state.answers[q_idx] = user_choice
                st.session_state.current_q -= 1
                st.rerun()
                
    with col3:
        if q_idx < total_qs - 1:
            if st.button("Tiếp Theo ➡️"):
                st.session_state.answers[q_idx] = user_choice
                st.session_state.current_q += 1
                st.rerun()
        else:
            if st.button("🏁 NỘP BÀI THI"):
                st.session_state.answers[q_idx] = user_choice
                st.session_state.finished = True
                st.rerun()

# Step 3: Quiz Finished & Score Report
elif st.session_state.finished:
    total_qs = len(QUESTIONS)
    correct_count = 0
    detailed_report = []
    
    for i, q in enumerate(QUESTIONS):
        user_ans = st.session_state.answers.get(i, "Chưa trả lời")
        is_correct = user_ans == q['answer']
        if is_correct:
            correct_count += 1
        detailed_report.append({
            "STT": i + 1,
            "Chuyên mục": q['category'],
            "Câu hỏi": q['question'],
            "Đáp án của bạn": user_ans,
            "Đáp án đúng": q['answer'],
            "Kết quả": "✅ Đúng" if is_correct else "❌ Sai",
            "Giải thích giải pháp": q['explanation']
        })
        
    score_pct = (correct_count / total_qs) * 100
    is_passed = correct_count >= 45
    
    # Display Result Certificate
    st.markdown("---")
    st.markdown("## 📊 KẾT QUẢ KIỂM TRA TRẮC NGHIỆM")
    
    # Certificate Panel
    st.info(f"""
    👤 **Nhân viên:** {st.session_state.employee_name}  
    🆔 **Mã số:** {st.session_state.employee_id}  
    📅 **Ngày kiểm tra:** {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}
    """)
    
    # Score presentation
    if is_passed:
        st.success(f"""
        ### 🎉 ĐẠT (PASS)
        **Chúc mừng! Bạn đã vượt qua bài kiểm tra xuất sắc!**  
        * **Số câu đúng:** {correct_count} / {total_qs} câu  
        * **Tỉ lệ chính xác:** {score_pct:.1f}%  
        * **Yêu cầu đạt:** Tối thiểu 45/50 (90%)
        """)
    else:
        st.error(f"""
        ### ❌ CHƯA ĐẠT (FAIL)
        **Bạn cần ôn tập lại quy trình và thực hiện kiểm tra lại.**  
        * **Số câu đúng:** {correct_count} / {total_qs} câu  
        * **Tỉ lệ chính xác:** {score_pct:.1f}%  
        * **Yêu cầu đạt:** Tối thiểu 45/50 (90%)
        """)
        
    # Re-take Exam button
    if st.button("🔄 THI LẠI (RESET EXAM)"):
        st.session_state.started = False
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.session_state.finished = False
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🔍 BẢNG CHI TIẾT ĐÁP ÁN VÀ GIẢI THÍCH LỖI")
    
    # Let user filter detailed review
    show_all = st.checkbox("Hiển thị toàn bộ 50 câu hỏi", value=False)
    
    for row in detailed_report:
        if not show_all and row["Kết quả"] == "✅ Đúng":
            continue  # Only show mistakes by default to help them learn
            
        color = "green" if row["Kết quả"] == "✅ Đúng" else "red"
        with st.expander(f"Câu {row['STT']}: {row['Kết quả']} - {row['Chuyên mục']}"):
            st.markdown(f"**Câu hỏi:** {row['Câu hỏi']}")
            st.markdown(f"* **Đáp án của bạn:** {row['Đáp án của bạn']}")
            st.markdown(f"* **Đáp án đúng:** <span style='color:green;font-weight:bold;'>{row['Đáp án đúng']}</span>", unsafe_allow_html=True)
            st.markdown(f"💡 **Giải thích quy trình:** {row['Giải thích giải pháp']}")
