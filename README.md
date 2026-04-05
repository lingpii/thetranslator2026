# thetranslator2026
demo for KTW1 - AIO 2026 (ứng dụng translate,audio,pdf)
Mình kết hợp tạo demo cho D7 đọc pdf cùng pypdf và D10 tìm hiểu về translate, googletranslate và audio (gTTS). 
Ban đầu mình sử dụng translate và gTTS nhưng cả hai đều có nhiều hạn chế (bản dịch của translate không được mượt và giọng đọc của gTTS không được hay lắm). Do đó, mình đổi qua dùng googletrans và edge_tts để lấy bản đọc từ Microsoft. Theo mình tìm hiểu thì có thể gọi API đến GPT4 (nhưng tốn phí)
Hiện tại demo chỉ sử dụng dịch từ En - Vi. Tiếp đến mình sẽ tiếp tục phát triển để có thể dịch nhiều ngôn ngữ hơn, cải thiện giao diện. 
Một tính năng mới mà mình muốn thêm vào đó là dùng opencv để ocr dịch từ ảnh và trả về kết quả. Nhưng phần này khá phức tạp nên mình vẫn phải tìm hiểu thêm. 
