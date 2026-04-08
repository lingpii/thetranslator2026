# thetranslator2026
demo for KTW1 - AIO 2026 (ứng dụng translate,audio,pdf)

Mình kết hợp tạo demo cho D7 đọc pdf cùng pypdf và D10 tìm hiểu về translate, googletranslate và audio (gTTS). 


Ban đầu mình sử dụng translate và gTTS nhưng cả hai đều có nhiều hạn chế (bản dịch của translate không được mượt và giọng đọc của gTTS không được hay lắm). Do đó, mình đổi qua dùng googletrans và edge_tts để lấy bản đọc từ Microsoft. Theo mình tìm hiểu thì có thể gọi API đến GPT4 (nhưng tốn phí)


Hiện tại demo chỉ sử dụng dịch từ En - Vi. Tiếp đến mình sẽ tiếp tục phát triển để có thể dịch nhiều ngôn ngữ hơn, cho phép input là âm thanh để nhận diện và đưa ra bản dịch đồng thời cải thiện giao diện. 


Một tính năng mới mà mình muốn thêm vào đó là dùng opencv để ocr dịch từ ảnh và trả về kết quả. Nhưng phần này khá phức tạp nên mình vẫn phải tìm hiểu thêm. 

8/4/26: 

Mình thực hiện nâng cấp thêm tính năng summarize một đoạn văn bản bằng text/file pdf (en), trích xuất được chủ đề và cảm xúc, đầu ra vẫn có audio(vi, vốn muốn thêm 'en' nữa nhưng bản đó cứ bị bug nên mình không làm kịp)

Nâng cấp lên sử dụng deep_translator để việc dịch được mượt hơn, ứng dụng BoW, newspaper3k và underthesea vào project. Nhưng mình thấy nó còn hơi lộn xộn. Nhiều kỹ thuật mình không thể tự thực hiện mà phải nhờ sự giúp sức của các bài tutorial, AI. 

Hạn chế thì khá nhiều ở phần output summary mình vẫn chưa thật sự hài lòng và đang tìm thêm thông tin để cải thiện phần này, chủ đề và từ khoá luôn. 

Kết luận thì project này đang chỉ dừng lại ở mức vận dụng hẹp, cần cải tiến nhiều để nâng cấp. Mình sẽ tiếp tục cải thiện. Mong là ở những phiên bản sau sẽ khắc phục được nhược điểm của nó. 
